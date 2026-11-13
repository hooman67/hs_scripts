import json
from html.parser import HTMLParser

import pytest

from hp3p import report
from hp3p.evalset import Row
from hp3p.report import render


def test_render_has_all_columns_and_escapes(tmp_path):
    row = Row("b-1", "<cafe>", "s3://x", 1024, 768, [("Input", "u0"), ("HP12 PROD: seed 1/2", "u1")])
    d = tmp_path / "rows/b-1"
    d.mkdir(parents=True)
    (d / "result.json").write_text(json.dumps({
        "id": "b-1", "status": "ok", "tone": "Warm", "content": "Cafe", "rationale": "r", "ref_ids": ["s1"],
        "prompt": "p", "error": None, "size": "1184x880", "elapsed_s": 1}))
    (d / "ref_2.webp").write_bytes(b"w")
    html = render([row], tmp_path, "T").read_text()
    for s in ["Input", "HP12 PROD: seed 1/2", "GPT 2.5 (ours)", "rows/b-1/ours.png", "rows/b-1/ref_2.webp",
              "&lt;cafe&gt;"]:
        assert s in html


def test_render_surfaces_alignment_warning(tmp_path):
    row = Row("b-1", "cafe", "s3://x", 1024, 768, [])
    d = tmp_path / "rows/b-1"
    d.mkdir(parents=True)
    warning = "Alignment would leave 12% uncovered; kept the direct crop <without repairs>."
    (d / "result.json").write_text(json.dumps({
        "status": "ok", "warning": warning, "locate": {"confident": True},
    }))
    html = render([row], tmp_path, "T").read_text()
    assert "12% uncovered" in html and "&lt;without repairs&gt;" in html
    assert "product location not confident" not in html


def test_render_identifies_direct_generation_without_alignment_failure(tmp_path):
    row = Row("b-1", "cafe", "s3://x", 1024, 768, [])
    d = tmp_path / "rows/b-1"
    d.mkdir(parents=True)
    (d / "result.json").write_text(json.dumps({
        "status": "ok", "generation_mode": "direct", "image_calls": 1,
        "aligned": False, "graded": False, "locate": None,
    }))
    html = render([row], tmp_path, "T").read_text()
    assert "Direct generation" in html and "1 image call" in html
    assert "geometry not validated" in html and "no post-processing" in html
    assert "rows/b-1/gpt_1.png" in html
    assert "not aligned" not in html


def test_render_links_geometry_guide_without_listing_it_as_style_ref(tmp_path):
    row = Row("b-1", "cafe", "s3://x", 1024, 768, [])
    d = tmp_path / "rows/b-1"
    d.mkdir(parents=True)
    (d / "result.json").write_text(json.dumps({"status": "ok", "generation_mode": "direct"}))
    (d / "geometry_guide.png").write_bytes(b"guide")
    html = render([row], tmp_path, "T").read_text()
    assert 'href="rows/b-1/geometry_guide.png"' in html
    assert 'class=r loading=lazy src="rows/b-1/geometry_guide.png"' not in html


def test_render_direct_raw_and_global_grade_with_product_color_warning(tmp_path):
    row = Row("b-1", "cafe", "s3://x", 1024, 768, [])
    d = tmp_path / "rows/b-1"
    d.mkdir(parents=True)
    (d / "result.json").write_text(json.dumps({
        "status": "ok", "generation_mode": "direct", "graded": True,
        "grading": {"scope": "whole_image", "product_colors_preserved": False},
    }))
    (d / "ours_graded.png").write_bytes(b"graded")
    html = render([row], tmp_path, "T").read_text()
    assert 'href="rows/b-1/ours_graded.png"' in html
    assert "changes product colors" in html and "no post-processing" not in html


def test_render_surfaces_grade_error_without_hiding_raw_success(tmp_path):
    row = Row("b-1", "cafe", "s3://x", 1024, 768, [])
    d = tmp_path / "rows/b-1"
    d.mkdir(parents=True)
    (d / "result.json").write_text(json.dumps({
        "status": "ok", "generation_mode": "direct", "graded": False,
        "grade_error": "Reference has insufficient tonal variation <flat>.",
    }))
    html = render([row], tmp_path, "T").read_text()
    assert "insufficient tonal variation &lt;flat&gt;" in html
    assert 'href="rows/b-1/ours.png"' in html


def test_render_distinguishes_nearest_grading_reference_and_reused_generation(tmp_path):
    row = Row("b-1", "cafe", "s3://x", 1024, 768, [])
    d = tmp_path / "rows/b-1"
    d.mkdir(parents=True)
    (d / "result.json").write_text(json.dumps({
        "status": "ok", "generation_mode": "direct", "image_calls": 1, "graded": True,
        "source_generation_run": "original-run", "postprocess_only": True,
        "grading": {"scope": "whole_image", "reference_file": "grade_reference.webp",
                    "selection": {"reference_id": "nearest<ref>", "distance": 0.42, "candidate_count": 341}},
    }))
    for name in ("ours_graded.png", "grade_reference.webp", "ref_2.webp"):
        (d / name).write_bytes(b"image")
    html = render([row], tmp_path, "T").read_text()
    assert 'href="rows/b-1/grade_reference.webp"' in html
    assert "nearest&lt;ref&gt;" in html and "341" in html
    assert 'src="rows/b-1/ref_2.webp"' in html
    assert "original-run" in html and "0 new image calls" in html
    assert "Direct generation · 1 image call" not in html


def test_clean_comparison_shares_original_product_prompt_and_method_images(tmp_path):
    row = Row("b-1", "A desk <without people> & plants", "s3://x", 1024, 768, [
        ("Input", "https://assets.example/input.png"),
        ("HP12 PROD", "https://assets.example/prod.jpg"),
        ("HP12 NEW + blue v2", "https://assets.example/blue.jpg?x=1&y=2")],
        baseline_prompt="<instruction>Blue chair & daylight</instruction>")
    d = tmp_path / "rows/b-1"
    d.mkdir(parents=True)
    (d / "result.json").write_text(json.dumps({
        "status": "ok", "graded": True, "prompt": "Camera: preserve <screen> & geometry.\nNo people.",
        "grade_error": None,
        "guide_info": {"lens_35mm_equivalent_mm": 35},
    }))
    (d / "ours_graded.png").write_bytes(b"graded")
    (d / "hero.png").write_bytes(b"original product")
    (d / "ref_2.webp").write_bytes(b"generation style reference")
    (d / "ref_3.jpg").write_bytes(b"second generation style reference")
    (d / "grade_reference.webp").write_bytes(b"separate grading reference")
    (tmp_path / "viewer.html").write_text("EXISTING VIEWER")
    html = report.render_comparison([row], tmp_path, "https://assets.example/run").read_text()

    class Images(HTMLParser):
        def __init__(self):
            super().__init__()
            self.sources, self.links, self.prompts = [], [], []
            self.model_prompts = []
            self.in_prompt = False
            self.in_pre = False

        def handle_starttag(self, tag, attrs):
            attributes = dict(attrs)
            if tag == "img":
                self.sources.append(attributes["src"])
            elif tag == "a":
                self.links.append(attributes["href"])
            elif tag == "td" and attributes.get("class") == "prompt":
                self.in_prompt = True
            elif tag == "pre":
                self.in_pre = True

        def handle_endtag(self, tag):
            if tag == "td":
                self.in_prompt = False
            elif tag == "pre":
                self.in_pre = False

        def handle_data(self, data):
            if self.in_prompt:
                self.prompts.append(data)
            if self.in_pre:
                self.model_prompts.append(data)

    parsed = Images()
    parsed.feed(html)
    assert parsed.sources == parsed.links == [
        "https://assets.example/run/rows/b-1/hero.png",
        "https://assets.example/prod.jpg",
        "https://assets.example/blue.jpg?x=1&y=2",
        "https://assets.example/run/rows/b-1/ref_2.webp",
        "https://assets.example/run/rows/b-1/ref_3.jpg",
        "https://assets.example/run/rows/b-1/ours_graded.png",
    ]
    assert parsed.prompts == ["A desk <without people> & plants"]
    assert parsed.model_prompts == [
        "<instruction>Blue chair & daylight</instruction>",
        "Camera: preserve <screen> & geometry.\nNo people.",
    ]
    assert "HP12 rewritten input" in html and "GPT2.5 final input" in html
    assert "&lt;instruction&gt;" in html and "&lt;screen&gt;" in html
    assert "<instruction>" not in html and "<screen>" not in html
    assert "b-1" in html and "HP12 NEW + blue v2" in html and "Style reference" in html
    for excluded in ("input.png", "ours.png", "grade_reference", "Lens estimate"):
        assert excluded not in html
    assert (tmp_path / "viewer.html").read_text() == "EXISTING VIEWER"


def test_clean_comparison_replaces_only_the_selected_output_without_overwriting_assets(tmp_path):
    rows = [Row(id, "prompt", "s3://x", 1024, 768, [("HP12", "https://assets.example/base.jpg")],
                baseline_prompt="HP12 rewritten scene")
            for id in ("b-1", "b-2")]
    for row in rows:
        d = tmp_path / "rows" / row.id
        d.mkdir(parents=True)
        (d / "result.json").write_text(json.dumps({
            "status": "ok", "graded": True, "prompt": f"ORIGINAL GPT PROMPT {row.id}",
        }))
        for name in ("hero.png", "ref_2.webp", "ours_graded.png"):
            (d / name).write_bytes(b"original bytes")
    new_output = "https://assets.example/camera-pilot/rows/b-1/ours_graded.png"
    original = {p: p.read_bytes() for p in (tmp_path / "rows").rglob("*") if p.is_file()}
    html = report.render_comparison(
        rows, tmp_path, "https://assets.example/run", graded_output_urls={"b-1": new_output},
        prompt_overrides={"b-1": "NEW CAMERA PILOT GPT PROMPT"},
    ).read_text()
    assert new_output in html
    assert "https://assets.example/run/rows/b-1/ours_graded.png" not in html
    assert "https://assets.example/run/rows/b-2/ours_graded.png" in html
    assert "https://assets.example/run/rows/b-1/hero.png" in html
    assert "https://assets.example/run/rows/b-1/ref_2.webp" in html
    assert "NEW CAMERA PILOT GPT PROMPT" in html
    assert "ORIGINAL GPT PROMPT b-1" not in html
    assert "ORIGINAL GPT PROMPT b-2" in html
    for path, data in original.items():
        assert path.read_bytes() == data
    for overrides in ({"b-1": "http://assets.example/unsafe.png"}, {"unknown-row": new_output}):
        with pytest.raises(ValueError):
            report.render_comparison(rows, tmp_path, "https://assets.example/run",
                                     graded_output_urls=overrides)
    with pytest.raises(ValueError):
        report.render_comparison(rows, tmp_path, "https://assets.example/run",
                                 graded_output_urls={"b-1": new_output})
    with pytest.raises(ValueError):
        report.render_comparison(rows, tmp_path, "https://assets.example/run",
                                 prompt_overrides={"unknown-row": "UNKNOWN GPT PROMPT"})


@pytest.mark.parametrize("failure", [
    "missing_grade", "failed_grade", "missing_baseline", "missing_original", "missing_style",
    "missing_hp12_prompt", "missing_gpt_prompt",
])
def test_clean_comparison_refuses_incomplete_results(tmp_path, failure):
    baselines = [("HP12", "https://assets.example/base.jpg")]
    row = Row("b-1", "prompt", "s3://x", 1024, 768, baselines,
              baseline_prompt="" if failure == "missing_hp12_prompt" else "HP12 rewritten scene")
    d = tmp_path / "rows/b-1"
    d.mkdir(parents=True)
    (d / "result.json").write_text(json.dumps({
        "status": "ok", "graded": failure != "failed_grade", "grade_error": None,
        "prompt": "" if failure == "missing_gpt_prompt" else "FINAL GPT PROMPT",
    }))
    if failure != "missing_grade":
        (d / "ours_graded.png").write_bytes(b"graded")
    if failure != "missing_original":
        (d / "hero.png").write_bytes(b"original product")
    if failure != "missing_style":
        (d / "ref_2.webp").write_bytes(b"style reference")
    rows = [row]
    if failure == "missing_baseline":
        rows.append(Row("b-2", "prompt", "s3://x", 1024, 768, [("HP12 OTHER", "https://assets.example/other.jpg")]))
    with pytest.raises(ValueError):
        report.render_comparison(rows, tmp_path, "https://assets.example/run")
    assert not (tmp_path / "team_comparison.html").exists()
