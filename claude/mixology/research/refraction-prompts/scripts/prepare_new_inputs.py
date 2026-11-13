"""Copy exact finished-drink references into durable run assets; no model calls."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import shutil
from PIL import Image

PROJECT = Path('/home/colligo/hs_scripts/claude/mixology/research/refraction-prompts')
RUN = Path('/home/colligo/mixology_data/refraction_research_2026-10-19')
SOURCE = Path('/home/colligo/mixology_data/source_restored_2026-10-19/ref_inputs')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    cases = json.loads((PROJECT / 'cases.json').read_text())
    inputs = []
    for key, case in cases.items():
        if not key.startswith('new_'):
            continue
        original = SOURCE / Path(case['input']).name
        assert original.name not in ['empty_cup.png', 'white_cap.png']
        destination = RUN / 'assets' / case['input']
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists():
            shutil.copy2(original, destination)
        assert sha(original) == sha(destination)
        with Image.open(destination) as image:
            image.load()
            dimensions = list(image.size)
        inputs.append({'case_id': key, 'source': str(original), 'input': str(destination),
                       'sha256': sha(destination), 'dimensions': dimensions,
                       'planned_run_id': 'v3new_' + key, 'generation_status': 'not_started'})
    assert len(inputs) == 5
    report = {'prepared_at': datetime.now(timezone.utc).isoformat(), 'inputs': inputs,
              'excluded': ['white_cap.png', 'empty_cup.png'], 'model_calls': 0,
              'user_prompt': 'Add refractions.', 'system_version': 'v3',
              'style_reference': str(RUN / 'assets/image_003_p03_xref116.jpg'),
              'status': 'prepared; model access blocked by Foundry HTTP 403'}
    review = RUN / '_review/new_refractions_review.json'
    review.parent.mkdir(exist_ok=True)
    review.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'prepared_inputs': len(inputs), 'model_calls': 0, 'manifest': str(review)}))


if __name__ == '__main__':
    main()
