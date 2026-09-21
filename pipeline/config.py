"""Shared Vertex + ALTAVIA build config."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "work"
ASSETS = ROOT / "assets"
VID = ASSETS / "vid"

PROJECT = "railmantri"
LOCATION = "us-central1"
BUCKET = "railmantri-altavia-scroll"
GCS_PREFIX = f"gs://{BUCKET}"

STILL_MODEL = "gemini-2.5-flash-image"
STILL_FALLBACKS = (
    "imagen-4.0-generate-001",
    "gemini-3-pro-image-preview",
)
VIDEO_MODEL = "veo-3.1-generate-001"
DURATION = 6
ASPECT = "16:9"
NEGATIVE = (
    "text, watermark, logos, badges, license plates, people, cuts, jump cut, "
    "real car marque, Lamborghini, Ferrari, brand emblem"
)

STYLE = """Cinematic low-angle photoreal film still, 16:9 anamorphic widescreen, shallow depth of field, hard key light with deep shadow falloff, volumetric haze in industrial interiors, practical lens flare outdoors, film grain, slight halation on highlights. Original unbranded Italian V12 hypercar concept (homage form, not a real marque): low wedge silhouette, sharp hexagonal surfacing, Y-motif lighting signature, scissor doors, quad exhaust, deep Verde Mantis green with a satin finish. Palette: near-black #1A1A1A, Verde Mantis green #7BB026, forge orange #D94F00, bone white #E8E6E1. Absolutely no text, no letters, no numbers, no logos, no badges, no license plates, no people, no watermarks. Focal subject horizontally centred."""

SECTIONS = [
    {
        "id": "ore",
        "label": "Ore",
        "eyebrow": "Ore",
        "title": "It starts as nothing.",
        "body": "Dark foundry air. A crucible tips. Molten metal finds the mould.",
        "tags": ["Foundry", "Crucible", "Billet"],
        "accent": "#D94F00",
        "scroll": 1.5,
        "linger": 0.38,
        "seed": 11001,
        "still": (
            "A dark industrial foundry at night. A massive iron crucible tips, "
            "pouring a blinding stream of molten metal into a sand mould. Sparks "
            "drift through volumetric haze. Wide high establishing view of the pour, "
            "the glowing stream centred in frame. Hard key from the metal itself, "
            "deep shadow falloff, cinematic low-angle photoreal."
        ),
        "dive": (
            "Single continuous cinematic camera move, no cuts. Begin on a wide high "
            "shot of a dark foundry as a crucible tips and molten metal pours into a "
            "mould, sparks drifting through haze. The camera slowly descends into the "
            "glowing stream until the cooling billet's molten surface fills the frame. "
            "Smooth graceful slow motion. In the final second, settle into a slow "
            "steady push toward the glowing metal."
        ),
        "focal": "the glowing surface of the cooling billet",
    },
    {
        "id": "forge",
        "label": "Forge",
        "eyebrow": "Forge",
        "title": "Twelve tonnes of pressure. One line.",
        "body": "A hydraulic press closes. The shoulder line is born in one strike.",
        "tags": ["Press", "Carbon", "Shoulder"],
        "accent": "#D94F00",
        "scroll": 1.45,
        "linger": 0.36,
        "seed": 22002,
        "still": (
            "A vast stamping hall. A hydraulic press forms a sharp hexagonal body "
            "panel in Verde Mantis green — a single panel, not a finished car. "
            "Adjacent bay: carbon fibre weave being laid by robotic arms. Raking hard "
            "light along the panel's shoulder line. Blank unmarked surfaces, no emblem "
            "on the nose. Cinematic photoreal, no people, centred composition."
        ),
        "dive": (
            "Single continuous cinematic camera move, no cuts. Pull off a glowing "
            "cooling billet, track low and level along a hydraulic press line with "
            "foreground parallax, then push into the press as it closes on a sharp "
            "hexagonal body panel. End tight on the stamped panel's shoulder line in "
            "raking light. Smooth graceful slow motion. In the final second, settle "
            "into a slow steady push toward the shoulder line."
        ),
        "focal": "the stamped panel's sharp shoulder line",
    },
    {
        "id": "assembly",
        "label": "Assembly",
        "eyebrow": "Assembly",
        "title": "V12. Naturally aspirated. Unapologetic.",
        "body": "Chassis on a rotating jig. The engine drops. Panels find their home.",
        "tags": ["V12", "Jig", "Bay"],
        "accent": "#7BB026",
        "scroll": 1.55,
        "linger": 0.4,
        "seed": 33003,
        "still": (
            "A bright, immaculate assembly hall. An unbranded Italian V12 hypercar "
            "chassis on a rotating jig, naturally aspirated V12 being lowered in, "
            "Verde Mantis green hexagonal panels floating into position around it. "
            "Y-motif lighting signature unlit. Hard key, deep shadows, no people, "
            "no badges, cinematic photoreal."
        ),
        "dive": (
            "Single continuous cinematic camera move, no cuts. Rise over a bright "
            "assembly hall, then swoop down and through the open engine bay of an "
            "unbranded V12 hypercar on a rotating jig as panels float into place. "
            "End in an extreme close-up of the V12 intake plenum. Smooth graceful "
            "slow motion. In the final second, settle into a slow steady push toward "
            "the intake plenum."
        ),
        "focal": "the V12 intake plenum",
    },
    {
        "id": "reveal",
        "label": "Reveal",
        "eyebrow": "Reveal",
        "title": "ALTAVIA",
        "body": "One hard key. Wet satin green. The Y-motif ignites.",
        "tags": ["Studio", "Y-motif", "Satin"],
        "accent": "#7BB026",
        "scroll": 2.15,
        "linger": 0.52,
        "seed": 44004,
        "still": (
            "A black photography studio. The finished unbranded Verde Mantis green "
            "satin V12 hypercar under a single hard key light, paint wet-looking, "
            "low wedge silhouette, sharp hexagonal surfacing, scissor doors closed, "
            "Y-motif headlights just igniting. Completely blank nose — no emblem, no "
            "badge, no crest. Empty cabin, no driver. Deep shadow falloff, film grain, "
            "slight halation. No badges, no text, centred hero three-quarter view."
        ),
        "dive": (
            "Single continuous cinematic camera move, no cuts. Pull back out of an "
            "engine bay into a black studio, then orbit 180 degrees around the "
            "finished Verde Mantis green hypercar under a single hard key, paint "
            "wet-looking. End with the Y-motif headlight signature filling the frame "
            "as it switches on. Smooth graceful slow motion. In the final second, "
            "settle into a slow steady push into the headlight."
        ),
        "focal": "the Y-motif headlight signature switching on",
    },
    {
        "id": "rollout",
        "label": "Roll-out",
        "eyebrow": "Roll-out",
        "title": "Doors up. Lights on.",
        "body": "A shutter lifts. Daylight cuts the tunnel. The car creeps forward.",
        "tags": ["Tunnel", "Scissor", "Disc"],
        "accent": "#E8E6E1",
        "scroll": 1.45,
        "linger": 0.36,
        "seed": 55005,
        "still": (
            "A concrete tunnel. A shutter door lifting, hard daylight cutting in. "
            "The Verde Mantis green hypercar creeping forward, scissor door closing, "
            "Y-motif lights on. Completely blank nose — no emblem, no badge. Empty "
            "cabin, no driver, no plates. Low-angle photoreal at wheel height, "
            "practical flare from the daylight slit."
        ),
        "dive": (
            "Single continuous cinematic camera move, no cuts. Drop from a glowing "
            "Y-motif headlight down to a low tracking shot at wheel height beside "
            "the moving tyre as the car creeps through a concrete tunnel, shutter "
            "door lifting, scissor door closing. End on the tyre and brake disc as "
            "motion starts. Smooth graceful slow motion. In the final second, settle "
            "into a slow steady push toward the spinning disc."
        ),
        "focal": "the tyre and brake disc",
    },
    {
        "id": "road",
        "label": "Road",
        "eyebrow": "Road",
        "title": "Now go.",
        "body": "Golden hour. Heat shimmer off the exhaust. The coast road opens.",
        "tags": ["Coast", "Golden hour", "Aerial"],
        "accent": "#7BB026",
        "scroll": 1.7,
        "linger": 0.42,
        "seed": 66006,
        "still": (
            "A coastal mountain road at golden hour. The Verde Mantis green hypercar "
            "at speed, heat shimmer off the quad exhaust, anamorphic lens flare. "
            "Completely blank nose — no emblem, no badge. Dark empty cabin, no driver, "
            "no plates. Wide establishing view of the road threading into the distance, "
            "car centred. Cinematic photoreal."
        ),
        "dive": (
            "Single continuous cinematic camera move, no cuts. Pull out from a wheel "
            "and brake disc into a chase cam beside the Verde Mantis green hypercar "
            "on a coastal mountain road at golden hour, heat shimmer off the exhaust, "
            "then climb into a high wide aerial as the car disappears into the corner. "
            "End on the wide aerial, road threading into the distance. Smooth graceful "
            "slow motion. In the final second, settle into a slow steady climb on the "
            "aerial view."
        ),
        "focal": "the wide aerial of the road threading away",
    },
]

CONNECTORS = [
    {
        "id": "1",
        "from": "ore",
        "to": "forge",
        "seed": 12012,
        "prompt": (
            "Single continuous cinematic camera move, no cuts. Pull back from the "
            "glowing surface of a cooling billet, travel through foundry haze into a "
            "stamping hall, and arrive on a wide view of a hydraulic press line. "
            "Seamless flowing industrial transition, photoreal, no people, no text."
        ),
    },
    {
        "id": "2",
        "from": "forge",
        "to": "assembly",
        "seed": 23023,
        "prompt": (
            "Single continuous cinematic camera move, no cuts. Pull back from a "
            "stamped body-panel shoulder line, glide out of the press hall into a "
            "bright assembly hall, and arrive above a chassis on a rotating jig. "
            "Seamless flowing industrial transition, photoreal, no people, no text."
        ),
    },
    {
        "id": "3",
        "from": "assembly",
        "to": "reveal",
        "seed": 34034,
        "prompt": (
            "Single continuous cinematic camera move, no cuts. Pull back from a V12 "
            "intake plenum, leave the assembly hall, and arrive in a black studio on "
            "the finished Verde Mantis green hypercar under a single hard key. "
            "Seamless flowing cinematic transition, photoreal, no people, no text."
        ),
    },
    {
        "id": "4",
        "from": "reveal",
        "to": "rollout",
        "seed": 45045,
        "prompt": (
            "Single continuous cinematic camera move, no cuts. Pull back from a "
            "Y-motif headlight filling the frame, leave the black studio, and arrive "
            "in a concrete tunnel as a shutter door lifts and daylight cuts in. "
            "Seamless flowing cinematic transition, photoreal, no people, no text."
        ),
    },
    {
        "id": "5",
        "from": "rollout",
        "to": "road",
        "seed": 56056,
        "prompt": (
            "Single continuous cinematic camera move, no cuts. Pull back from a tyre "
            "and brake disc in a tunnel, burst into golden-hour daylight, and arrive "
            "on a coastal mountain road with the hypercar at speed. Seamless flowing "
            "cinematic transition, photoreal, no people, no text."
        ),
    },
]


def still_prompt(section):
    return f"{STYLE}\n\nSubject: {section['still']}"


def dive_prompt(section):
    return (
        f"{section['dive']} {STYLE} No text, no captions. Ends on {section['focal']}."
    )


def conn_prompt(conn):
    return f"{conn['prompt']} {STYLE} No text, no captions."
