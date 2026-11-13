import importlib.util
from pathlib import Path

from test_geometry import scene, spec


def _load_baseline_geometry():
    path = next((parent / "base" / "hp3p" / "geometry.py" for parent in Path(__file__).parents
                 if (parent / "base" / "hp3p" / "geometry.py").is_file()), None)
    if path is None:
        raise FileNotFoundError("Pinned baseline geometry.py is missing from the isolated candidate tree.")
    module_spec = importlib.util.spec_from_file_location("hp3p_geometry_pinned_baseline", path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def test_omitted_shape_matches_pinned_commit_bytes_and_metadata():
    from hp3p.geometry import build_guide

    baseline = _load_baseline_geometry()
    expected_guide, expected_info = baseline.build_guide(*scene(), spec())
    actual_guide, actual_info = build_guide(*scene(), spec())
    assert actual_guide == expected_guide
    assert actual_info == expected_info
