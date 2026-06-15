from collections import defaultdict
from typing import Any, Iterable, List, Mapping, TextIO

from BaseClasses import Item, ItemClassification, Location, LocationProgressType, Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_item_rule, add_rule, set_rule

from .enums import APItemType, ItemCategory
from .options import ParadiseKillerOptions, option_groups
from .locations import LocationData, locations_by_region, regions_by_location, location_name_groups
from .items import ItemData, item_dictionary, item_list, item_name_groups
from .regions import region_dictionary, region_list
from .rules import connection_rules, location_rules


class PKLocation(Location):
    game: str = "Paradise Killer"
    data: LocationData

    def __init__(self, player, name, address, parent, data):
        self.data = data
        super(PKLocation, self).__init__(player, name, address, parent)


class PKItem(Item):
    game: str = "Paradise Killer"
    data: ItemData

    def __init__(self, name, classification, code, player, data):
        self.data = data
        super(PKItem, self).__init__(name, classification, code, player)


class ParadiseKillerWeb(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Paradise Killer randomizer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Anomaly"],
    )

    options_page = True
    game_info_languages = ["en"]
    tutorials = [setup_en]
    theme = "ice"
    bug_report_page = "https://github.com/anomalyco/paradise-killer-archipelago/issues"
    options_presets = {}
    option_groups = option_groups
    rich_text_options_doc = True
    location_descriptions = {}
    item_descriptions = {}


class ParadiseKillerWorld(World):
    game = "Paradise Killer"

    web = ParadiseKillerWeb()

    options_dataclass = ParadiseKillerOptions
    options: ParadiseKillerOptions

    item_name_to_id = {
        item_data.name: item_data.code
        for item_data in item_list
        if not item_data.skip and item_data.code is not None
    }

    location_name_to_id = {
        location_data.name: location_data.address
        for locations in locations_by_region.values()
        for location_data in locations
        if location_data.address is not None
    }

    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    def generate_early(self) -> None:
        if len(self.options.include_locations.value) > 0:
            for location in self.location_name_to_id.keys():
                if location not in self.options.include_locations:
                    self.options.exclude_locations.value.add(location)

    def create_regions(self) -> None:
        region_lookup: dict[str, Region] = {}

        for region_data in region_list:
            region = Region(region_data.name, self.player, self.multiworld)

            for location_data in locations_by_region.get(region_data.name, []):
                if location_data.is_event:
                    region.add_event(location_data.name)
                    continue

                location = PKLocation(
                    self.player,
                    location_data.name,
                    location_data.address,
                    region,
                    location_data,
                )
                region.locations.append(location)

            self.multiworld.regions.append(region)
            region_lookup[region_data.name] = region

        for region_data in region_list:
            if region_data.name not in region_lookup:
                continue
            region = region_lookup[region_data.name]
            for connection in region_data.connections:
                if connection not in region_lookup:
                    continue
                region.connect(region_lookup[connection])

        victory_region = region_lookup.get("Trial: Conviction")
        if victory_region:
            victory_loc = Location(
                self.player, "Victory", None, victory_region)
            victory_region.locations.append(victory_loc)
            victory_loc.place_locked_item(Item("Victory", ItemClassification.progression, None, self.player))
            set_rule(victory_loc, lambda state: state.can_reach_location("Trial: Conviction", self.player))
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def create_items(self) -> None:
        item_pool: List[PKItem] = []
        items_added: List[str] = []

        locations_to_fill: List[PKLocation] = self.multiworld.get_unfilled_locations(self.player)
        max_pool_size = len([loc for loc in locations_to_fill if loc.address is not None])

        items_with_pickups = {
            loc.game_name
            for locs in locations_by_region.values()
            for loc in locs
            if not loc.is_event
        }

        excluded_categories = set()
        if not self.options.shuffle_gold_coins:
            excluded_categories.add(ItemCategory.GOLD_COIN)

        filler_candidates = [
            item_data.name for item_data in item_list
            if not item_data.skip
            and item_data.code is not None
            and item_data.item_type == APItemType.ITEM
            and item_data.classification == ItemClassification.filler
            and item_data.category not in excluded_categories
        ]

        for item_data in item_list:
            if item_data.skip or item_data.code is None:
                continue
            if item_data.category in excluded_categories:
                continue
            if item_data.game_name not in items_with_pickups:
                continue

            items_added.append(item_data.name)
            item_pool.append(self.create_item(item_data.name))

        missing_progression = [
            item.name for item in item_list
            if item.name not in items_added
            and item.classification == ItemClassification.progression
            and not item.skip
            and item.code is not None
        ]

        missing_progression_with_pickups = [
            name for name in missing_progression
            if item_dictionary[name].game_name in items_with_pickups
        ]

        assert len(item_pool) + len(missing_progression_with_pickups) <= max_pool_size, (
            f"Item pool ({len(item_pool)} + {len(missing_progression_with_pickups)} progression) "
            f"cannot fit in {max_pool_size} locations"
        )

        for prog_item in missing_progression_with_pickups:
            item_pool.append(self.create_item(prog_item))

        for item_name in self.options.include_items.value:
            if len(item_pool) >= max_pool_size:
                break
            if item_name in items_added:
                continue
            if item_dictionary[item_name].game_name not in items_with_pickups:
                continue
            item_pool.append(self.create_item(item_name))
            items_added.append(item_name)

        while len(item_pool) < max_pool_size:
            if filler_candidates:
                filler_name = self.random.choice(filler_candidates)
                if filler_name in items_added:
                    filler_candidates.remove(filler_name)
                    continue
            else:
                filler_name = self.get_filler_item_name()
                if filler_name in items_added:
                    continue
            item_pool.append(self.create_item(filler_name))
            items_added.append(filler_name)

        assert len(item_pool) == max_pool_size, f"Pool size {len(item_pool)} != {max_pool_size}"

        self.multiworld.itempool.extend(item_pool)

    def set_rules(self) -> None:
        for connection_rule_data in connection_rules:
            _from, _to = connection_rule_data.spot.split(" -> ")
            if _from not in region_dictionary or _to not in region_dictionary:
                continue

            add_rule(
                self.multiworld.get_entrance(connection_rule_data.spot, self.player),
                connection_rule_data.to_collection_rule(self.player)
            )

        for location_rule_data in location_rules:
            loc_name = location_rule_data.spot
            if loc_name not in regions_by_location:
                continue

            add_rule(
                self.multiworld.get_location(location_rule_data.spot, self.player),
                location_rule_data.to_collection_rule(self.player)
            )

    def create_item(self, name: str) -> PKItem:
        item_data: ItemData = item_dictionary[name]
        return PKItem(name, item_data.classification, item_data.code, self.player, item_data)

    def get_filler_item_name(self) -> str:
        filler_items = {
            item.name for item in item_list
            if item.classification == ItemClassification.filler
            and not item.skip
            and item.code is not None
        }
        if not filler_items:
            return "Gold Coin 001"
        return self.random.choice(tuple(filler_items))

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if len(self.options.include_locations.value) > 0:
            spoiler_handle.write(f"\nLocations that can have Progression and Useful items:\n")
            for location in self.multiworld.get_locations(self.player):
                if location.progress_type == LocationProgressType.EXCLUDED:
                    continue
                if location.address is None:
                    continue
                spoiler_handle.write(f"\n- {location.name}")

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = self.options.as_dict(
            "include_floating_islands",
            "include_paradise_island",
            "include_trial",
            "shuffle_gold_coins",
            "include_items",
        )

        slot_data["item_mappings"] = [
            {
                "ap_id": item.code,
                "game_name": item.game_name,
                "category": item.category.value,
            }
            for item in item_list
            if item.code is not None and item.item_type == APItemType.ITEM and not item.skip
        ]

        slot_data["location_mappings"] = [
            {
                "ap_id": loc.address,
                "type": "pickup" if not loc.is_event else "event",
                "game_name": loc.game_name,
                "pickup_bp": loc.pickup_bp,
            }
            for locs in locations_by_region.values()
            for loc in locs
            if not loc.is_event
        ]

        return slot_data
