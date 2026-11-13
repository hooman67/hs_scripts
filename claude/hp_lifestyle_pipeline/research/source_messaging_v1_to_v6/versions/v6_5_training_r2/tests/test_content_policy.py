import pytest
from research.source_messaging_v1_to_v6.versions.v6_5_training_r2.content_policy import check_content_policy


@pytest.mark.parametrize('text,groups,code', [
    ('A café with a chalkboard menu.', {'chalkboard'}, 'menu_text_treatment'),
    ('A table menu rests on a background table as non-legible café detail.', {'menu'}, 'menu_text_treatment'),
    ('A clearly readable menu above the table.', {'menu'}, 'legible_text_request'),
    ('Framed portraits above the desk.', {'wall_art'}, 'human_face_request'),
    ('A smiling woman works at the table.', set(), 'human_face_request'),
])
def test_unsafe_requests(text, groups, code):
    assert code in {issue[0] for issue in check_content_policy(text, groups)}


@pytest.mark.parametrize('text,groups', [
    ('A café with a chalkboard menu whose text is non-legible background detail.', {'chalkboard'}),
    ('A menu with non-legible text remains in the background.', {'menu'}),
    ('A table menu with indistinct text in the background.', {'menu'}),
    ('Abstract wall art without portraits or human faces.', {'wall_art'}),
    ('A closed book with a plain unmarked cover.', {'book'}),
    ('A blank page supports planning without requiring readable text.', {'paper_documents'}),
    ('A folder and papers are both kept free of readable labels.', {'document_folder', 'paper_documents'}),
])
def test_safe_treatments(text, groups):
    assert check_content_policy(text, groups) == []


@pytest.mark.parametrize('text', [
    'A return-label sheet with indistinct markings rests on the desk.',
    'A plain return label lies beside a folder.',
])
def test_return_labels_are_text_carrier_risks(text):
    assert 'text_carrier_risk' in {issue[0] for issue in check_content_policy(text, {'paper_documents'})}


@pytest.mark.parametrize('text,groups', [
    ('An open notebook rests on the table.', {'notebook'}),
    ('A ring binder sits partly open.', {'ring_binder'}),
    ('A plain desk calendar sits near the edge.', {'calendar'}),
    ('A reference pinboard sits behind the table.', {'pinboard'}),
    ('A mostly empty reference pinboard sits behind the table.', {'pinboard'}),
    ('An unbranded board game rests on the desk.', {'board_game'}),
    ('A closed document storage box rests on the desk.', {'document_box'}),
    ('A measuring tape rests on the table.', {'measuring_tape'}),
    ('Sugar sachets rest beside a cup.', {'sugar_sachets'}),
    ('Color swatches sit on the table.', {'color_swatches'}),
])
def test_text_bearing_props_require_visible_safe_treatment(text, groups):
    assert 'text_bearing_prop_treatment' in {
        issue[0] for issue in check_content_policy(text, groups)
    }


@pytest.mark.parametrize('text', [
    'An open unlabelled ring binder rests on the desk.',
    'An open ring binder with unlabelled pages rests on the desk.',
    'An open ring binder with unlabelled pages sits beside a calendar with non-readable dates.',
])
def test_open_binder_requires_safe_visible_pages(text):
    assert 'open_binder_page_treatment' in {
        issue[0] for issue in check_content_policy(text, {'ring_binder'})
    }


@pytest.mark.parametrize('text,groups,code', [
    ('A ruler rests beside a textbook with a plain unmarked cover.', {'ruler', 'book'}, 'measurement_tool_text_treatment'),
    ('A small unbranded trophy sits beside a game with no readable text.', {'trophy', 'board_game'}, 'trophy_text_treatment'),
])
def test_special_text_carriers_need_their_own_treatment(text, groups, code):
    assert code in {issue[0] for issue in check_content_policy(text, groups)}


def test_each_swatch_type_needs_its_own_treatment():
    text = 'Layered fabric swatches sit beside unlabelled color swatches.'
    assert 'swatch_text_treatment' in {
        issue[0] for issue in check_content_policy(text, {'fabric_swatches', 'color_swatches'})
    }


def test_each_swatch_type_can_be_made_safe():
    text = 'Unlabelled fabric swatches sit beside unmarked color swatches.'
    assert check_content_policy(text, {'fabric_swatches', 'color_swatches'}) == []


def test_document_box_requires_its_own_label_treatment():
    text = 'A closed document storage box sits beside a calendar with non-readable dates.'
    assert 'document_box_label_treatment' in {
        issue[0] for issue in check_content_policy(text, {'document_box', 'calendar'})
    }


def test_sugar_sachets_require_their_own_text_treatment():
    text = 'Sugar sachets sit beside a folder with indistinct markings.'
    assert 'sugar_sachet_text_treatment' in {
        issue[0] for issue in check_content_policy(text, {'sugar_sachets', 'document_folder'})
    }


def test_mostly_empty_pinboard_is_not_a_complete_safe_treatment():
    text = (
        'A mostly empty cork pinboard hangs behind a face-down clipboard with a blank back.'
    )
    codes = {issue[0] for issue in check_content_policy(text, {'pinboard', 'clipboard'})}
    assert 'blank_board_treatment' in codes


@pytest.mark.parametrize('text', [
    'A blank whiteboard hangs behind the table.',
    'A fully empty cork pinboard hangs behind the table.',
    'A whiteboard is left blank against the wall.',
])
def test_v62_rejects_blank_wall_boards(text):
    codes = {
        issue[0]
        for issue in check_content_policy(text, {'wall_writing_board'})
    }
    assert 'blank_board_treatment' in codes


@pytest.mark.parametrize('text,groups', [
    ('An open notebook shows blank pages.', {'notebook'}),
    ('An unlabelled ring binder sits closed.', {'ring_binder'}),
    ('An open ring binder shows blank pages.', {'ring_binder'}),
    ('An open ring binder has pages with indistinct markings.', {'ring_binder'}),
    ('A closed plain unmarked document storage box rests nearby.', {'document_box'}),
    ('A desk calendar has non-readable dates.', {'calendar'}),
    ('A reference pinboard shows sparse non-readable geometric marks.', {'pinboard'}),
    ('An unbranded board game uses simple geometric pieces.', {'board_game'}),
    ('An unbranded board game uses abstract shapes and no readable markings.', {'board_game'}),
    ('A whiteboard with distant non-legible geometric marks sits in the background.', {'whiteboard'}),
    ('A closed textbook has no readable title or markings.', {'book'}),
    ('Unlabelled color swatches sit on the table.', {'color_swatches'}),
    ('A ruler with non-readable measurement markings rests nearby.', {'ruler'}),
    ('A measuring tape with indistinct numbers lies on the worktable.', {'measuring_tape'}),
    ('An unmarked ruler lies on the worktable.', {'ruler'}),
    ('A set square with no readable measurement markings lies nearby.', {'set_square'}),
    ('A plain uninscribed trophy sits on the shelf.', {'trophy'}),
    ('A trophy without an inscription sits on the shelf.', {'trophy'}),
    ('Plain unmarked sugar sachets rest beside a cup.', {'sugar_sachets'}),
    ('A tabletop globe has no readable place names.', {'globe'}),
    ('A tabletop globe has map labels too small to read.', {'globe'}),
])
def test_text_bearing_props_accept_specific_safe_treatments(text, groups):
    assert check_content_policy(text, groups) == []


@pytest.mark.parametrize('text,groups', [
    ('A photo album rests on the table.', {'photo_album'}),
    ('Framed artwork hangs behind the desk.', {'wall_art'}),
])
def test_face_bearing_visuals_require_safe_subjects(text, groups):
    codes = {issue[0] for issue in check_content_policy(text, groups)}
    assert codes.intersection({'face_bearing_prop_treatment', 'artwork_face_treatment'})


@pytest.mark.parametrize('text,groups', [
    ('A partly assembled jigsaw puzzle rests on the table.', {'jigsaw_puzzle'}),
    ('A small wooden model sits on a shelf.', {'wooden_model'}),
    ('A paper origami model sits on the table.', {'origami'}),
])
def test_puzzles_and_models_require_nonhuman_subjects(text, groups):
    assert 'face_bearing_prop_treatment' in {
        issue[0] for issue in check_content_policy(text, groups)
    }


@pytest.mark.parametrize('text,groups', [
    ('A closed photo album with a plain unmarked cover rests on the table.', {'photo_album'}),
    ('Abstract framed artwork hangs behind the desk.', {'wall_art'}),
    ('Reference photographs of material textures sit on the table.', {'reference_photos'}),
    ('A jigsaw puzzle shows an abstract botanical pattern.', {'jigsaw_puzzle'}),
    ('A small architectural wooden model sits on a shelf.', {'wooden_model'}),
    ('A small wooden model of simple architecture sits on a shelf without human figures.', {'wooden_model'}),
    ('A geometric paper origami model sits on the table.', {'origami'}),
])
def test_face_bearing_visuals_accept_nonhuman_treatment(text, groups):
    assert check_content_policy(text, groups) == []


@pytest.mark.parametrize("text", [
    "A stone paperweight holds a sheet.",
    "A clear glass paperweight rests nearby.",
    "A metal paper weight sits at the edge.",
    "Loose decorative stones rest on the table.",
    "A few pebbles sit beside the cup.",
])
def test_paperweights_are_unavailable_even_without_a_declaration(text):
    assert "excluded_paperweight" in {
        issue[0] for issue in check_content_policy(text, set())
    }


def test_stone_materials_and_approved_coasters_are_not_decorative_stones():
    assert check_content_policy(
        "A stone worktop anchors the room. A stone coaster sits to one side.",
        {"coaster"},
    ) == []


@pytest.mark.parametrize("text,groups,code", [
    ("An open unbranded backpack hangs nearby.", {"laptop_bag"}, "bag_content_treatment"),
    ("A closed backpack hangs beside an unbranded notebook.", {"laptop_bag"}, "bag_content_treatment"),
    ("A partly closed unbranded bag hangs nearby.", {"laptop_bag"}, "bag_content_treatment"),
    ("An analog clock hangs on the wall.", {"clock"}, "clock_text_treatment"),
    ("An unnumbered clock sits beside an unbranded bag.", {"clock"}, "clock_text_treatment"),
    ("An unbranded clock hangs above an unnumbered sheet.", {"clock"}, "clock_text_treatment"),
])
def test_new_props_need_their_own_safe_treatment(text, groups, code):
    assert code in {issue[0] for issue in check_content_policy(text, groups)}


@pytest.mark.parametrize("text,groups", [
    ("A closed plain unbranded canvas backpack hangs nearby.", {"laptop_bag"}),
    ("A CLOSED UNBRANDED BACKPACK hangs nearby.", {"laptop_bag"}),
    ("An unbranded bag is kept closed beside the seating.", {"laptop_bag"}),
    ("A backpack is closed and unbranded.", {"laptop_bag"}),
    ("An unnumbered unbranded analog clock hangs on the wall.", {"clock"}),
    ("An unbranded analog clock is unnumbered.", {"clock"}),
    ("An analog clock is unnumbered and unbranded.", {"clock"}),
])
def test_new_props_accept_explicit_safe_descriptions(text, groups):
    assert check_content_policy(text, groups) == []
