"""CLI preflight and audit checks; all paths fail before any model call."""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]


def call(*args):
    return subprocess.run([sys.executable, str(HERE / 'cli.py'), *map(str, args)], capture_output=True, text=True)


def test_missing_input_records_zero_calls(tmp_path):
    output = tmp_path / 'result.json'
    result = call('run', '--input', tmp_path / 'missing.json', '--catalog', tmp_path / 'absent.json', '--output', output)
    assert result.returncode == 2
    record = json.loads(output.read_text())
    assert record['error']['code'] == 'preflight_read_failed'
    assert record['audit']['semantic_calls'] == 0
    assert list((tmp_path / 'result.json.run').iterdir()) == []
    assert call('run', '--input', tmp_path / 'missing.json', '--catalog', tmp_path / 'absent.json', '--output', output).returncode != 0
    assert json.loads(output.read_text()) == record


def test_empty_pending_catalogue_never_invokes_model(tmp_path):
    source = tmp_path / 'request.json'
    catalogue = tmp_path / 'catalogue.json'
    output = tmp_path / 'result.json'
    source.write_text(json.dumps({'smart_brief': '', 'source_messaging': {}, 'camera_tag': 'laptop_FrontWide'}))
    catalogue.write_text(json.dumps({'version': 'hp-v6.2-approved-props-v1', 'revision': 'no-approvals', 'purpose': 'production', 'source_sha256': '0' * 64, 'entries': []}))
    result = call('run', '--input', source, '--catalog', catalogue, '--output', output)
    assert result.returncode == 2
    record = json.loads(output.read_text())
    assert record['error']['code'] == 'catalog_invalid'
    assert record['audit']['semantic_calls'] == 0
    assert record['audit']['transport_attempts_known'] == 0
