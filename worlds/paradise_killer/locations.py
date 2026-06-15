from dataclasses import dataclass, field
from typing import ClassVar, Dict, List

from .enums import APLocationType
from .helpers import build_location_data, build_trial_item_data


TRIAL_STAGES = build_trial_item_data()


@dataclass
class LocationData:
    location_type: APLocationType
    name: str
    game_name: str
    pickup_bp: str = None
    address: int = field(init=False)

    next_address: ClassVar[int] = 1

    @property
    def is_event(self):
        return self.address is None

    def __post_init__(self):
        if self.location_type == APLocationType.EVENT:
            self.address = None
        else:
            self.address = LocationData.next_address
            LocationData.next_address += 1


_locations_by_region_raw, _regions_by_location = build_location_data()

locations_by_region: Dict[str, List[LocationData]] = {}
regions_by_location: Dict[str, str] = _regions_by_location

for region_name, locs_raw in _locations_by_region_raw.items():
    if region_name not in locations_by_region:
        locations_by_region[region_name] = []
    for loc_raw in locs_raw:
        loc_type = APLocationType.PICKUP if loc_raw["location_type"] == 100_000_000 else APLocationType.EVENT
        loc = LocationData(
            location_type=loc_type,
            name=loc_raw["name"],
            game_name=loc_raw["game_name"],
            pickup_bp=loc_raw.get("pickup_bp"),
        )
        locations_by_region[region_name].append(loc)

location_name_groups: Dict[str, set] = {
    "Pickups": {loc.name for locs in locations_by_region.values() for loc in locs if not loc.is_event},
    "Trial Events": {loc.name for locs in locations_by_region.values() for loc in locs if loc.is_event},
    "All Locations": {loc.name for locs in locations_by_region.values() for loc in locs},
}
