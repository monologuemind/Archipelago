import re
from typing import Dict, List, Optional, Tuple

from BaseClasses import ItemClassification

from .areas import AREA_NAMES, ISLAND_FLOATING, ISLAND_MAIN, resolve_area, resolve_region
from .enums import ItemCategory
from .registry_data import REGISTRY
from .bp_zone_data import BP_ZONE_RAW
from .guide_data import GUIDE_ITEM_LOCATION_MAP


_BP_ZONE_MAP = BP_ZONE_RAW.get("bp_zone", {})


def human_readable_name(game_name: str) -> str:
    s = game_name
    s = s.replace("_", " ")
    s = re.sub(r'^(\w+) (\d+)$', lambda m: f"{m.group(1)} {int(m.group(2)):03d}", s)
    words = s.split()
    result = []
    for w in words:
        if w.upper() == w and len(w) > 1:
            result.append(w.title() if w.lower() != w else w)
        elif w.startswith("0") and w[1:].isdigit():
            result.append(w)
        elif w.isdigit():
            result.append(w)
        else:
            result.append(w)
    return " ".join(result)


def classify_item(game_name: str, category: ItemCategory) -> ItemClassification:
    name_upper = game_name.upper()

    is_upgrade = "UNLOCKED" in name_upper or "UPGRADE" in name_upper
    is_key = category in (ItemCategory.KEY,)
    is_gold = category == ItemCategory.GOLD_COIN
    is_ghost = "GHOST" in name_upper
    is_placeholder = "PLACEHOLDER" in name_upper

    if is_key:
        return ItemClassification.progression
    if is_upgrade:
        return ItemClassification.progression
    if is_gold:
        return ItemClassification.filler
    if is_ghost:
        return ItemClassification.filler
    if is_placeholder:
        return ItemClassification.trap

    return ItemClassification.filler


def item_category_from_name(game_name: str) -> ItemCategory:
    prefix = game_name.split("_")[0].upper()

    if prefix == "GOLDCOIN":
        return ItemCategory.GOLD_COIN
    if prefix == "COLLECTABLE":
        name = game_name.upper()
        if "DRINK" in name:
            return ItemCategory.DRINK
        return ItemCategory.COLLECTABLE
    if prefix == "SYMBOLPUZZLE":
        return ItemCategory.SYMBOL_PUZZLE
    if prefix == "STARLIGHTSKIN":
        return ItemCategory.STARLIGHT_SKIN
    if prefix == "SWITCH":
        return ItemCategory.SWITCH
    if prefix == "SOUNDTRACK":
        return ItemCategory.SOUNDTRACK
    if prefix == "CREST":
        return ItemCategory.CREST
    if prefix == "WHISKY":
        return ItemCategory.WHISKY
    if prefix in ("KEYS", "SMALLKEY"):
        return ItemCategory.KEY
    if prefix == "GHOST":
        return ItemCategory.GHOST_ITEM
    if prefix in ("GROUP", "SUBURBCREST", "SYMBOLSDCARD", "PHONECHARM", "FARMVALVE"):
        return ItemCategory.MISC
    if prefix in ("LD", "GRACEBLOODLINES", "FACTORY", "CORRIDOR", "DOG", "GUN", "STARLIGHT", "CURRENCY", "TEMPLEWALKWAYPUZZLE", "UPDATE"):
        return ItemCategory.MISC
    if prefix == "PLACEHOLDER":
        return ItemCategory.MISC
    return ItemCategory.MISC


ITEM_BASE_OFFSET = 10000
EVENT_ITEM_BASE_OFFSET = 30000


def build_item_data() -> List[dict]:
    registry = REGISTRY
    items = []
    code = ITEM_BASE_OFFSET

    for game_name in sorted(registry["items"].keys()):
        cat = item_category_from_name(game_name)
        classification = classify_item(game_name, cat)

        skip = "PLACEHOLDER" in game_name.upper()

        items.append({
            "code": code,
            "name": human_readable_name(game_name),
            "game_name": game_name,
            "category": cat,
            "classification": classification,
            "skip": skip,
        })
        code += 1

    return items


TRIAL_STAGES = [
    ("Trial: Menu", "Trial: Menu"),
    ("Trial: Henry's Escape", "Henry's Escape Conviction"),
    ("Trial: Henry's Possession", "Henry's Possession Conviction"),
    ("Trial: Grace Bloodlines", "Grace Bloodlines Conviction"),
    ("Trial: Crimson Agenda", "Crimson Agenda Conviction"),
    ("Trial: Doom Jazz Partnership", "Doom Jazz Partnership Conviction"),
    ("Trial: Yuri Testimony", "Yuri Testimony Conviction"),
    ("Trial: Lydia & Sam Accusation", "Lydia & Sam Accusation Conviction"),
    ("Trial: Carmelina Betrayal", "Carmelina Betrayal Conviction"),
    ("Trial: Witness Corroboration", "Witness Corroboration Conviction"),
    ("Trial: Final Argument", "Final Argument Conviction"),
    ("Trial: Conviction", "Final Conviction"),
    ("Victory", "Victory"),
]


def build_trial_item_data() -> List[dict]:
    items = []
    for i, (ap_name, _) in enumerate(TRIAL_STAGES):
        items.append({
            "code": EVENT_ITEM_BASE_OFFSET + i if ap_name != "Victory" else None,
            "name": ap_name,
            "game_name": ap_name,
            "category": ItemCategory.MISC,
            "classification": ItemClassification.progression if ap_name != "Victory" else ItemClassification.progression_skip_balancing,
            "skip": False,
        })
    return items


_RESOLVED_AREA_CACHE: Dict[str, Optional[str]] = {}
_RESOLVED_REGION_CACHE: Dict[str, str] = {}


def _resolve_region_from_bp(game_name: str, pickup_bp: str) -> Optional[str]:
    zone = _BP_ZONE_MAP.get(pickup_bp)
    if zone == ISLAND_FLOATING:
        return ISLAND_FLOATING
    return None


def resolve_area_cached(game_name: str) -> Optional[str]:
    if game_name not in _RESOLVED_AREA_CACHE:
        area = GUIDE_ITEM_LOCATION_MAP.get(game_name)
        if area is None:
            area = resolve_area(game_name)
        _RESOLVED_AREA_CACHE[game_name] = area
    return _RESOLVED_AREA_CACHE[game_name]


def resolve_region_cached(game_name: str, pickup_bp: str = None) -> str:
    key = f"{game_name}:{pickup_bp}"
    if key not in _RESOLVED_REGION_CACHE:
        region = None
        if pickup_bp:
            region = _resolve_region_from_bp(game_name, pickup_bp)
        if region is None:
            region = resolve_region(game_name)
        _RESOLVED_REGION_CACHE[key] = region
    return _RESOLVED_REGION_CACHE[key]


def build_location_data() -> Tuple[Dict[str, List[dict]], Dict[str, str]]:
    registry = REGISTRY
    locations_by_region: Dict[str, list] = {}
    regions_by_location: Dict[str, str] = {}

    TRIAL_REGION = "Courtroom"

    for game_name in sorted(registry["items"].keys()):
        item_data = registry["items"][game_name]
        pickup_bps = item_data.get("pickup_bps", [])
        if not pickup_bps:
            continue

        if isinstance(pickup_bps, list):
            bp_name = pickup_bps[0]
        else:
            bp_name = pickup_bps

        region = resolve_region_cached(game_name, bp_name)
        area = resolve_area_cached(game_name)

        if area:
            loc_name = f"{area} - {human_readable_name(game_name)}"
        else:
            loc_name = f"Pickup: {human_readable_name(game_name)}"

        if region not in locations_by_region:
            locations_by_region[region] = []

        loc_data = {
            "location_type": 100_000_000,
            "name": loc_name,
            "game_name": game_name,
            "pickup_bp": bp_name,
        }
        locations_by_region[region].append(loc_data)
        regions_by_location[loc_name] = region

    locations_by_region[TRIAL_REGION] = []

    for ap_name, _ in TRIAL_STAGES:
        if ap_name == "Victory":
            continue
        loc_data = {
            "location_type": 400_000_000,
            "name": ap_name,
            "game_name": ap_name,
            "pickup_bp": None,
        }
        locations_by_region[TRIAL_REGION].append(loc_data)
        regions_by_location[ap_name] = TRIAL_REGION

    return locations_by_region, regions_by_location
