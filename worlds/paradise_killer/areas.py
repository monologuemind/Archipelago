ISLAND_MAIN = "Main Island"
ISLAND_FLOATING = "Floating Islands"
ISLAND_PARADISE = "Paradise Island"

# Canonical area hierarchy from the wiki (Island Sequence 24 page)
# Each area is a tuple: (name, parent_island)
CANONICAL_AREAS = [
    # Main Island sub-areas (21 from wiki)
    ("Agri Fields", ISLAND_MAIN),
    ("Beach", ISLAND_MAIN),
    ("Citizen Apartments", ISLAND_MAIN),
    ("Citizen Housing", ISLAND_MAIN),
    ("Council Building", ISLAND_MAIN),
    ("Court House", ISLAND_MAIN),
    ("Danchi", ISLAND_MAIN),
    ("Dead Zone", ISLAND_MAIN),
    ("Desolation Cell", ISLAND_MAIN),
    ("Gardens", ISLAND_MAIN),
    ("Idle Lands", ISLAND_MAIN),
    ("K.HX's Workshop", ISLAND_MAIN),
    ("Marshal Barracks", ISLAND_MAIN),
    ("Mountain Gorge", ISLAND_MAIN),
    ("Opulent Ziggurat", ISLAND_MAIN),
    ("Paradise Gates", ISLAND_MAIN),
    ("Pyramid", ISLAND_MAIN),
    ("Reality Folding Drive", ISLAND_MAIN),
    ("Syndicate Apartments", ISLAND_MAIN),
    ("Syndicate Graveyard", ISLAND_MAIN),
    ("Syndicate HQ", ISLAND_MAIN),
    # Floating Islands sub-areas
    ("Island Mementos", ISLAND_FLOATING),
    ("Whisky Bar", ISLAND_FLOATING),
]

# Heuristic mapping: substring patterns -> area name
# Checked in order; first match wins
AREA_PATTERNS = [
    ("agri", "Agri Fields"),
    ("farmvalve", "Agri Fields"),
    ("farm", "Agri Fields"),
    ("beach", "Beach"),
    ("apartment", "Citizen Apartments"),
    ("suburb", "Citizen Housing"),
    ("council", "Council Building"),
    ("court", "Court House"),
    ("witnessriver", "Court House"),
    ("danchi", "Danchi"),
    ("deadzone", "Dead Zone"),
    ("dead_zone", "Dead Zone"),
    ("desolation", "Desolation Cell"),
    ("garden", "Gardens"),
    ("idleland", "Idle Lands"),
    ("idle_lands", "Idle Lands"),
    ("khx", "K.HX's Workshop"),
    ("workshop", "K.HX's Workshop"),
    ("barrack", "Marshal Barracks"),
    ("mountain", "Mountain Gorge"),
    ("gorge", "Mountain Gorge"),
    ("ziggurat", "Opulent Ziggurat"),
    ("temple", "Opulent Ziggurat"),
    ("paradisegate", "Paradise Gates"),
    ("pyramid", "Pyramid"),
    ("river", "Reality Folding Drive"),
    ("powerstation", "Reality Folding Drive"),
    ("power_schedule", "Reality Folding Drive"),
    ("syndicate", "Syndicate HQ"),
    ("hq", "Syndicate HQ"),
    ("graveyard", "Syndicate Graveyard"),
    ("grave", "Syndicate Graveyard"),
    ("mural", "Syndicate HQ"),
    ("crimsonacid", "Syndicate HQ"),
    ("crimson_acid", "Syndicate HQ"),
    ("lovedies", "Syndicate HQ"),
    ("love_dies", "Syndicate HQ"),
    ("monserrat", "Council Building"),
    # Floating Islands
    ("collectable_island", "Island Mementos"),
    ("island00", "Island Mementos"),
    ("whisky_", "Whisky Bar"),
    ("whisky-", "Whisky Bar"),
]

# Parent lookup
AREA_PARENT = {name: parent for name, parent in CANONICAL_AREAS}
# Set of all area names
AREA_NAMES = {name for name, _ in CANONICAL_AREAS}


def resolve_area(game_name: str) -> str:
    name_lower = game_name.lower()
    for pattern, area in AREA_PATTERNS:
        if pattern in name_lower:
            return area
    return None


def resolve_region(game_name: str) -> str:
    area = resolve_area(game_name)
    if area is None:
        return ISLAND_MAIN
    parent = AREA_PARENT.get(area)
    if parent is None:
        return ISLAND_MAIN
    return parent
