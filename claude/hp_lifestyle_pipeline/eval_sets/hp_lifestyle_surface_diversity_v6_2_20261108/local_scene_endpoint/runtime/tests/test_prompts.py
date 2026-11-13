import pytest

from hp3p.openai_client import load_prompt


@pytest.mark.parametrize("refs,product,guide", [("Image 2", "Image 1", "Image 3"), ("Images 2-5", "Image 6", "Image 1")])
def test_unified_prompt_keeps_brand_blue_and_geometry_without_upstream_brief(refs, product, guide):
    p = load_prompt("system_3p").format(style_images=refs, product_image=product, guide_image=guide)
    flat = " ".join(p.split())
    for needle in ["one broad physical blue carrier", "several clearly visible blue furnishings",
                   "Token props, thin frames, screen graphics, sky and light casts do not count",
                   "Desk props stay neutral", "Explicit requests win: minimal blue",
                   "including no blue, is followed exactly", "everyday color name",
                   f"Do not cite hex codes, claim a measured match to {refs}",
                   "Never change the product or camera to make room for blue",
                   "No orange or global blue color cast", "Return only the fields the current response schema"]:
        assert needle in flat
    for gone in ("World of Blue", "Spatial examples", "scale_plan", "Reference captions"):
        assert gone not in p
    for needle in ["There is no upstream scene rewrite", "stays an ottoman", "natural contact shadow", "For EACH named object",
                   "no-person restriction", product, refs, guide, "parallel on-screen",
                   "vanishing points", "user side", "unlit", "no people"]:
        assert needle in p
    assert "#103FB2" not in p and "35-45%" not in p and "full baseline prompt" not in p
    assert "{style_images}" not in p and "{guide_image}" not in p and "{product_image}" not in p
    assert "{tones}" in load_prompt("select") and "{contents}" in load_prompt("select")


def test_scale_reasoning_distinguishes_estimates_and_retains_projection_uncertainty():
    prompt = " ".join(load_prompt("system_3p").split())
    for requirement in ["never replace them with an estimate", "assume plausible category-level dimensions",
                        "say they are assumed", "Never equate bbox width with physical width or resize the product",
                        "estimates do not guarantee product fidelity"]:
        assert requirement in prompt
