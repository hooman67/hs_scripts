import json

from hp3p.evalset import load_rows


def test_load_rows_joins_baselines(tmp_path):
    ev = [{"eval_set_item_id": "b-1", "user_prompt": "cafe", "media": ["s3://b/k.png"],
           "width": 1024, "height": 768,
           "prompt": "<composition> table receding right <camera> wide_angle, high angle",
           "raw_prompt": "on a blue ottoman"}]
    bl = {"rows": [{"meta_data": {"evalset_item_id": "b-1"}, "images": [
        {"meta_text": {"label": "Input"}, "image_src": "u0"},
        {"meta_text": {"label": "HP12 PROD: seed 1/2"}, "image_src": "u1"}]}]}
    (tmp_path / "e.json").write_text(json.dumps(ev))
    (tmp_path / "b.json").write_text(json.dumps(bl))
    [row] = load_rows(tmp_path / "e.json", tmp_path / "b.json")
    assert row.user_prompt == "cafe" and row.hero_s3 == "s3://b/k.png" and row.raw_prompt == "on a blue ottoman"
    assert row.baselines == [("Input", "u0"), ("HP12 PROD: seed 1/2", "u1")]
    assert row.baseline_prompt == "<composition> table receding right <camera> wide_angle, high angle"
