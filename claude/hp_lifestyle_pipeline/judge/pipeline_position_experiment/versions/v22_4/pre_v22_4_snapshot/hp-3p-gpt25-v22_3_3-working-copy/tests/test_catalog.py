from hp3p.catalog import StyleRef, pick_refs


def _cat():
    refs = []
    for i in range(6):
        refs.append(StyleRef(f"s{i}", f"n{i}", "Warm", "Cafe", "image/webp", b"x"))
    refs.append(StyleRef("s9", "n9", "Warm", "Office", "image/webp", b"x"))
    refs.append(StyleRef("s10", "n10", "Cool", "Cafe", "image/webp", b"x"))
    return refs


def test_pick_is_deterministic_and_bucketed():
    a = pick_refs(_cat(), "Warm", "Cafe", "row-1")
    assert [r.id for r in a] == [r.id for r in pick_refs(_cat(), "Warm", "Cafe", "row-1")]
    assert len(a) == 4 and all(r.tone == "Warm" and r.content == "Cafe" for r in a)


def test_load_catalog_drops_duplicate_images(tmp_path):
    import base64
    import json

    from hp3p.catalog import load_catalog

    def ref(i, data):
        return {"id": f"s{i}", "name": "n", "tone": "T", "content": "C",
                "image": {"mime_type": "image/webp", "base64": base64.b64encode(data).decode()}}

    (tmp_path / "s.json").write_text(json.dumps({"references": [ref(1, b"a"), ref(2, b"b"), ref(3, b"a")]}))
    assert [r.id for r in load_catalog(tmp_path / "s.json")] == ["s1", "s2"]


def test_pick_backfills_same_content_then_same_tone():
    cat = [r for r in _cat() if r.id in {"s0", "s10", "s9"}]
    ids = [r.id for r in pick_refs(cat, "Warm", "Cafe", "row-1", k=3)]
    assert ids[0] == "s0" and ids[1:] == ["s10", "s9"]


def test_catalog_retains_user_tags_and_rejects_conflicting_duplicate_tags(tmp_path):
    import base64
    import json

    import pytest

    from hp3p.catalog import load_catalog

    ref = {"id": "r", "name": "n", "tone": "T", "content": "C", "human_presence": "no_humans",
           "image": {"mime_type": "image/webp", "base64": base64.b64encode(b"same").decode()}}
    path = tmp_path / "styles.json"
    path.write_text(json.dumps({"references": [ref]}))
    assert load_catalog(path)[0].human_presence == "no_humans"
    path.write_text(json.dumps({"references": [ref, {**ref, "id": "other", "human_presence": "human"}]}))
    with pytest.raises(ValueError, match="conflicting human-presence"):
        load_catalog(path)
