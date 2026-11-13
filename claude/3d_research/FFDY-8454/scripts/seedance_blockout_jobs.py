"""Seedance job definitions for the FFDY-8454 Blender-blockout experiment."""

from pathlib import Path


ROOT = Path("/home/colligo/hs_scripts/claude/3d_research/FFDY-8454")
BLOCK = ROOT / "renders" / "seedance_blockouts"
PREP = Path("/home/colligo/THD_laundry_sink_storyboard/prep")
GALLERY = Path("/home/colligo/THD_laundry_sink_storyboard/gallery/assets")

COUPLE = (
    "The two people are the SAME throughout: a woman in her early 30s with shoulder-length "
    "dark-brown hair in a plain cream knit sweater and blue jeans, and a man in his early 50s "
    "with short salt-and-pepper grey hair in a plain light-blue polo and blue jeans. Bright "
    "modern laundry room, grey wainscoting, light tile floor, open wood shelves, dark front-load "
    "washer/dryer. Plain clothing, no text or logos."
)


def prompt(goal, video_role, image_role, relationship, event, consistency):
    return f"""【Generation Goal】
{goal}

【Reference Asset Roles】
@Video1 is a coarse-blockout reference. Use it only for {video_role}; do not adopt its proxy geometry, simplified materials, empty scene, or lack of people.
@Image1 defines {image_role}; do not change the motion defined by @Video1.

【Subjects and Relationships】
{relationship}
{COUPLE}

【Event Script】
{event}

【Maintain Consistency】
{consistency}
"""


JOBS = [
    {
        "id": "shot02_1A_blockout_v1",
        "duration": 4,
        "videos": [BLOCK / "shot02_1A.mp4"],
        "images": [PREP / "S2a_image7_plate.png"],
        "prompt": prompt(
            "Generate a photoreal shot of the same couple beginning the tool-free cabinet assembly on the floor.",
            "the first broad side panel's exact pickup path, edge-pivot rotation from flat to upright, component blocking, action timing, and static camera",
            "the white cabinet parts, orange CLICKREADY connectors, dark work mat, and bright laundry-room appearance",
            "The woman and man kneel on opposite sides of the mat and both hold the moving side panel. The other five cabinet components remain flat and stationary.",
            "At the start, all six cabinet components lie separately on the mat. Following @Video1, the couple keep their hands in contact with one broad side panel, lift its outer edge, rotate the rigid panel around its floor-contact edge, and seat it upright. At the end, that panel remains upright while all other components remain where they started.",
            "Keep the same two people, six cabinet components, panel dimensions, orange connectors, room layout, camera axis, and physical hand-to-panel contact throughout. Do not bend, duplicate, merge, or prematurely assemble the remaining pieces.",
        ),
    },
    {
        "id": "shot04_blockout_v1",
        "duration": 4,
        "videos": [BLOCK / "shot04.mp4"],
        "images": [PREP / "S4a_image8_plate.png"],
        "prompt": prompt(
            "Generate a photoreal shot of the same couple installing the opposite broad side panel.",
            "the second side panel's pickup path, edge-pivot rotation from flat to upright, component blocking, action timing, and static camera",
            "the white cabinet, orange CLICKREADY connectors, dark work mat, and laundry-room materials",
            "One broad side wall is already upright and fixed. The couple hold only the opposite broad side panel, with their hands remaining attached to it throughout the lift.",
            "At the start, the first side wall is already installed and the opposite broad side panel lies flat. Following @Video1, the couple lift the opposite panel, rotate it around its floor-contact edge, and press it into its installed upright position. At the end, both broad side walls stand upright and stationary.",
            "Keep the installed wall, base, front frame, loose narrow boards, room, and camera fixed. Preserve rigid panel geometry and do not move any component except the opposite broad side panel.",
        ),
    },
    {
        "id": "shot05_blockout_v1",
        "duration": 4,
        "videos": [BLOCK / "shot05.mp4"],
        "images": [PREP / "S5_image11_plate.png"],
        "prompt": prompt(
            "Generate a photoreal shot of the same couple installing the shorter perpendicular end wall while clearing the two loose narrow boards from the work area.",
            "the end wall's pickup, rotation, and seating path, the paired relocation of the two loose narrow boards, component blocking, action timing, and static camera",
            "the partially assembled white cabinet, orange CLICKREADY connectors, light tile floor, dark work mat, and laundry-room appearance",
            "The woman controls the shorter end wall. The man moves the two loose narrow boards together to the left edge of the mat. The two installed broad walls and the front-frame base remain fixed.",
            "At the start, two broad side walls stand upright and the shorter perpendicular end wall is loose. Following @Video1, the man slides the two narrow loose boards together out of the work area while the woman lifts the shorter end wall, rotates it to the correct orientation, and lowers it between the fixed broad walls. At the end, the end wall is seated and all other components are stationary.",
            "Keep the same two people, component count, rigid dimensions, white materials, orange connectors, room layout, and camera axis. Do not collapse or broadly swing the already installed walls.",
        ),
    },
    {
        "id": "shot06_blockout_v1",
        "duration": 4,
        "videos": [BLOCK / "shot06.mp4"],
        "images": [PREP / "S6a_box_plate.png"],
        "prompt": prompt(
            "Generate a photoreal continuation of the cabinet assembly in which the side walls close by a very small amount to lock the box squarely.",
            "the precise small inward motion of the two long side walls, fixed base, component blocking, action timing, and static camera",
            "the white cabinet materials, orange CLICKREADY connectors, dark work mat, light tile floor, and bright laundry-room appearance",
            "The woman kneels at the near edge with her left hand on the left long side wall and her right hand on the right long side wall. The man kneels opposite and keeps the cabinet stable. The base, front frame, installed end wall, and loose pieces remain stationary.",
            "At the start, the cabinet rests flat on the mat with the two long side walls almost aligned. Following @Video1, the woman presses both side walls inward by only a small amount while the cabinet base and other parts stay fixed. Her hands remain in physical contact with the moving walls. At the end, both walls are square and stationary and the cabinet remains in the same place on the mat.",
            "Keep the same two people, cabinet component count, white panels, orange connectors, room layout, camera axis, and physical hand-to-panel contact. Preserve rigid panel dimensions; do not bend, duplicate, collapse, or broadly swing the walls.",
        ),
    },
    {
        "id": "shot07A_blockout_v1",
        "duration": 4,
        "videos": [BLOCK / "shot07A.mp4"],
        "images": [PREP / "S6a_box_plate.png"],
        "prompt": prompt(
            "Generate a photoreal shot of the same couple installing the wider of the two remaining narrow cabinet boards.",
            "the wider narrow board's pickup path, rotation, downward seating motion, component blocking, action timing, and static camera",
            "the white cabinet materials, orange CLICKREADY connectors, dark work mat, and bright laundry-room appearance",
            "The cabinet box is fixed on the mat. The woman guides the wider narrow board from the left while the man steadies the two upright side walls. The smaller loose board remains flat and stationary.",
            "At the start, the wider narrow board lies to the left of the cabinet. Following @Video1, the woman lifts it, rotates it into the horizontal installed orientation, carries it over the box, and lowers it into its connector position. At the end, the wider board is seated and released while the cabinet and smaller loose board remain fixed.",
            "Keep the same two people, component count, rigid dimensions, hand contact, room layout, camera axis, and installed cabinet state. Do not bend the board or move the whole cabinet.",
        ),
    },
    {
        "id": "shot07B_blockout_v1",
        "duration": 4,
        "videos": [BLOCK / "shot07B.mp4"],
        "images": [PREP / "S6a_box_plate.png"],
        "prompt": prompt(
            "Generate a photoreal shot of the same couple installing the final smaller narrow cabinet board.",
            "the smaller narrow board's pickup path, translation, downward seating motion, component blocking, action timing, and static camera",
            "the white cabinet materials, orange CLICKREADY connectors, dark work mat, and bright laundry-room appearance",
            "The cabinet and previously installed wider board are fixed. The man guides the final smaller narrow board from the left while the woman stabilizes the cabinet.",
            "At the start, the final smaller narrow board lies alone to the left of the cabinet. Following @Video1, the man lifts it, carries it over the open box, aligns it with its connector position, and lowers it into place. At the end, all six cabinet components are installed and stationary.",
            "Keep the same two people, six continuous components, rigid dimensions, hand contact, room layout, camera axis, and existing installed state. Do not duplicate the narrow board or move the whole cabinet.",
        ),
    },
    {
        "id": "shot08_blockout_v1",
        "duration": 4,
        "videos": [BLOCK / "shot08.mp4"],
        "images": [PREP / "4A_plate.png"],
        "prompt": prompt(
            "Generate a photoreal shot of the same couple standing the fully assembled cabinet upright.",
            "the complete cabinet's rigid rotation around its floor-contact edge, group trajectory, action timing, and widening static camera",
            "the finished white cabinet, bright laundry room, light tile floor, grey wall treatment, and nearby washer and dryer",
            "The woman and man stand on opposite sides of the fully assembled cabinet and grip its structural side walls. Every cabinet component remains locked together as one rigid unit.",
            "At the start, the fully assembled cabinet lies on its back. Following @Video1, the couple lift together, rotating the entire cabinet around the edge that remains on the floor until it stands upright. Their hands maintain firm physical contact and their body motion supports the cabinet's weight. At the end, the cabinet rests upright and stable on its feet.",
            "Keep the same two people, cabinet identity, component count, rigid assembled structure, room layout, and camera axis. Do not detach, deform, duplicate, or independently move any cabinet panel during the lift.",
        ),
    },
]


COMBINED_PROMPT = f"""【Generation Goal】
Generate one photoreal assembly montage of the same couple building the white CLICKREADY laundry-sink cabinet and standing it upright. Infer natural shot boundaries after each visible assembly state is completed, while preserving the supplied action order.

【Reference Asset Roles】
@Video1 through @Video8 are ordered motion references. Use each video only for its component trajectories, action timing, subject blocking, camera position, and completion state; do not adopt blockout materials, empty environments, or missing people. @Video2 is the photoreal connector macro and may retain its macro appearance.
@Image1 defines the initial flat component layout and room. @Image2 defines the CLICKREADY connector macro appearance. @Image3 defines the opposite-side installation appearance. @Image4 defines the perpendicular-wall installation appearance. @Image5 defines the later box-completion appearance. @Image6 defines the upright cabinet and laundry-room appearance.

【Subjects and Relationships】
The same woman and man assemble one continuous six-component cabinet. Their hands remain in physical contact with every component they move. Completed components retain their installed positions in all later shots.
{COUPLE}

【Event Script】
Stage 1 follows @Video1: the couple lift the first broad side panel from flat and seat it upright. At the end, the first wall is installed.
Stage 2 follows @Video2: cut to an extreme close-up of one orange CLICKREADY connector seating firmly. At the end, the connector is locked.
Stage 3 follows @Video3: return to the wider assembly view as the couple lift and install the opposite broad side panel. At the end, both broad walls are upright.
Stage 4 follows @Video4: the two loose narrow boards are cleared together while the shorter perpendicular end wall is lifted, rotated, and seated. At the end, the cabinet has three fixed walls.
Stage 5 follows @Video5: the two long walls press inward only slightly to square and lock the box. At the end, both walls are stationary.
Stage 6 follows @Video6: the wider remaining narrow board is lifted from the left, rotated, and lowered into place. At the end, it is installed.
Stage 7 follows @Video7: the final smaller narrow board is lifted from the left and lowered into place. At the end, all six cabinet components are installed.
Stage 8 follows @Video8: the couple rotate the complete rigid cabinet around its floor-contact edge until it stands upright and stable on its feet.

【Maintain Consistency】
Choose clean cuts at completed action states. Keep the same two people, one continuous cabinet, six rigid components, white materials, orange connectors, room layout, assembly causality, and hand-to-component contact throughout. Do not bend, duplicate, detach, or reset installed parts between shots. No on-screen text, captions, watermarks, or added logos.
"""

COMBINED = {
    "id": "all_references_auto_edit_v1",
    "duration": 22,
    "videos": [
        BLOCK / "shot02_1A.mp4",
        GALLERY / "3A_v1.mp4",
        BLOCK / "shot04.mp4",
        BLOCK / "shot05.mp4",
        BLOCK / "shot06.mp4",
        BLOCK / "shot07A.mp4",
        BLOCK / "shot07B.mp4",
        BLOCK / "shot08.mp4",
    ],
    "images": [
        PREP / "S2a_image7_plate.png",
        GALLERY / "3A_v1_input.jpg",
        PREP / "S4a_image8_plate.png",
        PREP / "S5_image11_plate.png",
        PREP / "S6a_box_plate.png",
        PREP / "4A_plate.png",
    ],
    "prompt": COMBINED_PROMPT,
}

FOLLOWUPS = [
    {
        "id": "shot02_1A_event_script_v2",
        "duration": 4,
        "videos": [BLOCK / "shot02_1A.mp4"],
        "images": [PREP / "S2a_image7_plate.png"],
        "prompt": (ROOT / "prompts/shot02_1A_event_script_v2.txt").read_text(),
    },
    {
        "id": "shot04_event_script_v2",
        "duration": 4,
        "videos": [BLOCK / "shot04.mp4"],
        "images": [PREP / "S4a_image8_plate.png"],
        "prompt": (ROOT / "prompts/shot04_event_script_v2.txt").read_text(),
    },
    {
        "id": "shot05_event_script_v2",
        "duration": 4,
        "videos": [BLOCK / "shot05.mp4"],
        "images": [PREP / "S5_image11_plate.png"],
        "prompt": (ROOT / "prompts/shot05_event_script_v2.txt").read_text(),
    },
    {
        "id": "shot06_event_script_v2",
        "duration": 4,
        "videos": [BLOCK / "shot06.mp4"],
        "images": [PREP / "S6a_box_plate.png"],
        "prompt": (ROOT / "prompts/shot06_event_script_v2.txt").read_text(),
    },
    {
        "id": "shot07A_event_script_v2",
        "duration": 4,
        "videos": [BLOCK / "shot07A.mp4"],
        "images": [PREP / "S6a_box_plate.png"],
        "prompt": (ROOT / "prompts/shot07A_event_script_v2.txt").read_text(),
    },
    {
        "id": "shot07B_event_script_v2",
        "duration": 4,
        "videos": [BLOCK / "shot07B.mp4"],
        "images": [PREP / "S6a_box_plate.png"],
        "prompt": (ROOT / "prompts/shot07B_event_script_v2.txt").read_text(),
    },
    {
        "id": "shot07B_minimal_v3",
        "duration": 4,
        "videos": [BLOCK / "shot07B.mp4"],
        "images": [PREP / "S6a_box_plate.png"],
        "prompt": (ROOT / "prompts/shot07B_minimal_v3.txt").read_text(),
    },
    {
        "id": "shot07B_identity_v4a",
        "duration": 4,
        "videos": [BLOCK / "shot07B.mp4"],
        "images": [PREP / "S6a_box_plate.png"],
        "prompt": (ROOT / "prompts/shot07B_identity_v4a.txt").read_text(),
    },
    {
        "id": "shot07B_identity_v4b",
        "duration": 4,
        "videos": [BLOCK / "shot07B.mp4"],
        "images": [PREP / "S6a_box_plate.png"],
        "prompt": (ROOT / "prompts/shot07B_identity_v4b.txt").read_text(),
    },
    {
        "id": "shot07B_identity_v4c",
        "duration": 4,
        "videos": [BLOCK / "shot07B.mp4"],
        "images": [PREP / "S6a_box_plate.png"],
        "prompt": (ROOT / "prompts/shot07B_identity_v4c.txt").read_text(),
    },
    {
        "id": "shot07B_broad_face_v5",
        "duration": 4,
        "videos": [BLOCK / "shot07B.mp4"],
        "images": [PREP / "S6a_box_plate.png"],
        "prompt": (ROOT / "prompts/shot07B_broad_face_v5.txt").read_text(),
    },
    {
        "id": "shot07B_identity_v4c_narrow_v2",
        "duration": 4,
        "videos": [BLOCK / "shot07B.mp4"],
        "images": [PREP / "S6a_box_plate.png"],
        "prompt": (ROOT / "prompts/shot07B_identity_v4c_narrow_v2.txt").read_text(),
    },
]

ALL_JOBS = JOBS + [COMBINED] + FOLLOWUPS
