"""Verify the restored source snapshot and immutable published experiment records."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json

PROJECT = Path('/home/colligo/hs_scripts/claude/mixology')
SOURCE = Path('/mnt/localssd/mixology')
SNAPSHOT = Path('/home/colligo/mixology_data/source_restored_2026-10-19')
RUN = Path('/home/colligo/mixology_data/refraction_research_2026-10-19')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert PROJECT.resolve().is_relative_to(Path('/home/colligo'))
    files = []
    # Inventory the immutable source copy, not later generated data via the SSD symlink.
    for dest in sorted(SNAPSHOT.rglob('*')):
        if not dest.is_file():
            continue
        rel = dest.relative_to(SNAPSHOT)
        original = SOURCE / rel
        assert original.is_file(), str(original)
        digest = sha(dest)
        assert sha(original) == digest, str(rel)
        files.append({'path': str(rel), 'bytes': dest.stat().st_size, 'sha256': digest})
    records = []
    for path in sorted((RUN / 'runs').glob('*/record.json')):
        r = json.loads(path.read_text())
        assert r['status'] == 'complete'
        assert sha(Path(r['output'])) == r['output_sha256'], r['id']
        for im in r['input_images']:
            assert sha(Path(im['path'])) == im['sha256'], im['path']
        records.append({'id': r['id'], 'output_sha256': r['output_sha256']})
    report = {
        'verified_at': datetime.now(timezone.utc).isoformat(),
        'source': str(SOURCE), 'durable_source_snapshot': str(SNAPSHOT),
        'durable_artifacts': str(RUN), 'source_files': len(files),
        'source_bytes': sum(f['bytes'] for f in files), 'files': files,
        'recovered_complete_runs': records,
        's3_source': 's3://foundry-tccc-enterprise-adobe-assets/mixology/refraction_research_2026-10-19/',
        'compatibility_symlink': str(SOURCE / RUN.name),
        'restore_procedure': 'Copy the durable source snapshot non-destructively to a fresh /mnt/localssd/mixology. Recreate its refraction_research_2026-10-19 symlink to durable_artifacts only if absent. Use /home/colligo/.venvs/mixology/bin/python. S3 is a second copy of published experiment artifacts.',
        'losses': 'Pre-restart _review evidence was not published and was lost. New S3 byte-readback and this source/run audit are replacement checks, not recovered original test evidence.',
    }
    dest = PROJECT / 'research/refraction-prompts/data/recovery_manifest_2026-10-19.json'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, indent=2) + '\n')
    (SNAPSHOT.parent / 'source_restored_2026-10-19.manifest.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'source_files_verified': len(files), 'source_bytes': report['source_bytes'],
                      'complete_runs_verified': len(records), 'manifest': str(dest)}))


if __name__ == '__main__':
    main()
