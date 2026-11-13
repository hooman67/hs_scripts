"""Recipe-system research orchestration; image inference uses unchanged bundled CLI."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone
from PIL import Image
from foundry_aws_gateway import llm

TOPIC = Path(__file__).resolve().parents[1]
RUN = Path('/home/colligo/mixology_data/refraction_research_2026-10-19')
ROOT = RUN/'recipe-to-image'
CLI = Path('/home/colligo/.codex/skills/.system/imagegen/scripts/image_gen.py')
MODEL = 'gpt-image-2.5-sunburst'
LIMIT = 12


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def save(p, value):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


def describe(p, role):
    im = Image.open(p)
    return {'path':str(p), 'role':role, 'sha256':sha(p), 'bytes':Path(p).stat().st_size,
            'dimensions':list(im.size), 'mode':im.mode}


def prepare_master():
    source = RUN/'assets/ref_input_originals/TCCC – Crafted Sept 2026-5.png'
    target = ROOT/'sources/master_source_canvas.png'
    if not target.exists():
        image = Image.open(source).convert('RGBA')
        canvas = Image.new('RGBA', (1024,1536), 'white')
        canvas.alpha_composite(image, (76,130))
        canvas.convert('RGB').save(target)
    save(ROOT/'sources/master_source_canvas.json', {
        'source':describe(source,'Cup-family reference, not recipe input'),
        'transform':'No scaling. Composite source RGBA on white 1024x1536 at x76,y130.',
        'output':describe(target,'One fixed cup family and view; temporary amber contents will be neutralized')})
    prompt = ('Use case: precise-object-edit. Prepare a fixed studio master for a recipe-driven drink series. '
        'Image 1 is the edit target. Keep this exact clear PET cup, its rolled rim, wall taper, molded base, '
        'size, position, camera view, and the same white vanilla soft-serve silhouette. '
        'Change only the amber tea inside into clear colorless iced soda: transparent ice cubes and tiny bubbles, '
        'no amber, red or other colored syrup. Keep realistic transparent PET highlights. '
        'The cup stands upright on a white horizontal studio surface, with a tiny neutral contact shadow directly '
        'under the lowest base; no floating, tilt or broad cast shadow. Pure white seamless background. '
        'Keep the full 1024x1536 canvas and all existing margins. No text, branding, straw, lid or garnish.')
    generate('master_neutral_v1', prompt, '', prompt, [describe(target,'edit target: fixed cup-family master preparation')],
             {'purpose':'one-time neutral fixed master, derived from amber original; not a recipe output'})


def generate(run_id, system, user, prompt, refs, extra):
    folder = ROOT/'runs'/run_id
    folder.mkdir(parents=True, exist_ok=True)
    if (folder/'record.json').exists():
        raise RuntimeError(f'Run already exists, inspect rather than retry: {run_id}')
    (folder/'system_prompt.txt').write_text(system)
    (folder/'user_prompt.txt').write_text(user)
    (folder/'image_prompt.txt').write_text(prompt)
    record = {'id':run_id, 'created_at':now(), 'status':'prepared', 'provider':'Foundry-vended OpenAI direct',
              'model':MODEL, 'quality':'high', 'size':'1024x1536', 'output_format':'png',
              'api_operation':'edit' if refs else 'generate', 'references':refs, 'system_prompt':system,
              'user_prompt':user, 'image_prompt':prompt, 'prompt_transport':'System contract compiled into Image API single prompt; no separate system-message parameter.',
              'cli_path':str(CLI), 'cli_sha256':sha(CLI),
              'metadata_limitations':'Unchanged CLI does not expose image request ID, response model snapshot, usage or cost.', **extra}
    journal_path = ROOT/'generation_journal.json'
    credentials = llm.get_openai()
    env = os.environ.copy()
    env['OPENAI_API_KEY'] = credentials.api_key
    env['OPENAI_BASE_URL'] = str(credentials.base_url)
    if credentials.project:
        env['OPENAI_PROJECT_ID'] = credentials.project
    # Secret values exist only in process memory/environment, never in prompt or record.
    command = [sys.executable, str(CLI), record['api_operation'], '--model', MODEL,
               '--prompt-file', str(folder/'image_prompt.txt'), '--quality','high','--size','1024x1536',
               '--output-format','png','--out',str(folder/'output.png'),'--no-augment']
    for ref in refs:
        command.extend(['--image',ref['path']])
    with (ROOT/'generation.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        journal = json.loads(journal_path.read_text()) if journal_path.exists() else {'limit':LIMIT, 'entries':[]}
        if len(journal['entries']) >= LIMIT:
            raise RuntimeError('Bounded image-job ceiling reached')
        if any(e['id']==run_id for e in journal['entries']):
            raise RuntimeError('Run already submitted')
        record.update(status='post_starting',started_at=now(),generation_number=len(journal['entries'])+1,command=command,
                      retry_policy='No orchestration retry. Bundled CLI constructs the SDK with default internal retry policy; wire-level attempts are not exposed.')
        save(folder/'record.json',record)
        journal['entries'].append({'id':run_id,'status':'post_starting','at':now()})
        save(journal_path,journal)
    start=time.monotonic()
    try:
        process=subprocess.run(command, env=env, capture_output=True, text=True, timeout=600)
        log=(process.stdout+'\n'+process.stderr).replace(credentials.api_key,'[REDACTED]')
        (folder/'image_cli.log').write_text(log)
        record.update(elapsed_seconds=round(time.monotonic()-start,2),cli_returncode=process.returncode)
        if process.returncode:
            raise RuntimeError('Image CLI failed; inspect sanitized log, never automatically retry')
        record.update(status='complete',completed_at=now(),output=describe(folder/'output.png','unmodified generated output'))
    except Exception as exc:
        record.update(status='failed_or_uncertain',error_type=type(exc).__name__)
        raise
    finally:
        save(folder/'record.json',record)
        with (ROOT/'generation.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            journal=json.loads(journal_path.read_text())
            next(e for e in journal['entries'] if e['id']==run_id)['status']=record['status']
            save(journal_path,journal)
    print(json.dumps({'id':run_id,'status':record['status'],'seconds':record['elapsed_seconds'],'sha256':record['output']['sha256']}),flush=True)


def run_test(mode, recipe_id, repeat):
    recipe = next(r for r in json.loads((TOPIC/'data/recipes.json').read_text()) if r['id']==recipe_id)
    system=(TOPIC/'data/system_v1.txt').read_text()
    user=f"Make {recipe['name']}: {recipe['recipe']}"
    policy='House appearance convention (derived from the supplied recipe-book photograph, not additional ingredients): '+recipe['appearance_policy']
    refs=[]
    conditioning='No input images. Reconstruct the standard cup and camera from the system specification.'
    if mode=='anchored':
        refs=[describe(ROOT/'runs/master_neutral_v1/output.png','Fixed neutral cup/camera/soft-serve master shared by EVERY recipe; not a target drink photo')]
        conditioning=('Image 1 is the fixed edit target for the whole series. Replace only the beverage inside the cup '
                      'according to the recipe; preserve its exact cup shell, rim, base, soft-serve silhouette, placement, '
                      'camera view, white background and contact shadow. Do not redraw or resize the vessel. '
                      'Clear master liquid is not a recipe ingredient.')
    prompt=system+'\n\n'+conditioning+'\n\n'+policy+'\n\nRecipe request:\n'+user
    generate(f'v1_{mode}_{recipe_id}_{repeat}',system,user,prompt,refs,
             {'mode':mode,'recipe':recipe,'repeat':repeat,'appearance_policy':policy,
              'comparison_original':describe(RUN/'assets/ref_input_originals'/recipe['original'],'Human/judge comparison only; NOT sent to image model')})


if __name__=='__main__':
    os.environ['FOUNDRY_AWS_GATEWAY_HOST']='https://foundry-aws-pluto.adobe.io'
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['master','text','anchored'])
    parser.add_argument('--recipe')
    parser.add_argument('--repeat',type=int,default=1)
    args=parser.parse_args()
    if args.mode=='master':
        prepare_master()
    else:
        run_test(args.mode,args.recipe,args.repeat)
