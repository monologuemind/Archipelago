import unittest
from typing import List

from ..items import item_list, item_dictionary
from ..locations import locations_by_region
from ..regions import region_list
from ..rules import connection_rules, location_rules

from BaseClasses import ItemClassification


class TestStatic(unittest.TestCase):

    location_list = [location for locations in locations_by_region.values() for location in locations]

    @staticmethod
    def _get_rule_items(rule_data):
        if callable(rule_data.rule):
            return []
        if isinstance(rule_data.rule, str):
            return [rule_data.rule]
        if isinstance(rule_data.rule, list):
            return rule_data.rule
        return []

    def test_no_duplicate_location_names(self):
        seen = set()
        duplicates = set()
        for location in self.location_list:
            if location.name in seen:
                duplicates.add(location.name)
            else:
                seen.add(location.name)
        if duplicates:
            self.fail(
                "\n" + "\n".join(
                    f"Location name '{name}' appears more than once"
                    for name in duplicates
                )
            )

    def test_all_location_regions_exist(self):
        location_regions = [region for region in locations_by_region]
        region_names = [region.name for region in region_list]
        extra = [region for region in location_regions if region not in region_names]
        if extra:
            self.fail(
                "\n" + "\n".join(
                    f"Region '{name}' from the location list does not exist in the list of regions"
                    for name in extra
                )
            )

    def test_connections_are_real_regions(self):
        region_names = {region.name for region in region_list}
        connection_names = {connection for region in region_list for connection in region.connections}
        wrong = {connection for connection in connection_names if connection not in region_names}
        if wrong:
            self.fail(
                "\n" + "\n".join(
                    f"Connection '{name}' is not in the region list"
                    for name in wrong
                )
            )

    def test_connection_rule_regions_exist(self):
        region_names = {region.name for region in region_list}
        rule_regions = []
        for rule_data in connection_rules:
            self.assertTrue(" -> " in rule_data.spot, f"Connection rule spot \"{rule_data.spot}\" is invalid")
            rule_regions.extend(rule_data.spot.split(" -> "))
        wrong = {region for region in rule_regions if region not in region_names}
        if wrong:
            self.fail(
                "\n" + "\n".join(
                    f"Region '{name}' from a connection rule is not in the region list"
                    for name in wrong
                )
            )

    def test_location_rule_locations_exist(self):
        location_names = {location.name for location in self.location_list}
        rule_locations = []
        for rule_data in location_rules:
            rule_locations.append(rule_data.spot)
        wrong = {location for location in rule_locations if location not in location_names}
        if wrong:
            self.fail(
                "\n" + "\n".join(
                    f"Location '{name}' from a location rule is not in the location list"
                    for name in wrong
                )
            )

    def test_rule_items_exist(self):
        item_names = {item.name for item in item_list}
        event_items = {location.name for locations in locations_by_region.values() for location in locations if location.is_event}
        item_names = item_names | event_items
        rule_items = []
        for rule_data in connection_rules + location_rules:
            rule_items.extend(self._get_rule_items(rule_data))
        wrong = {item for item in rule_items if item not in item_names}
        if wrong:
            self.fail(
                "\n" + "\n".join(
                    f"Item '{name}' from a rule is not in the item list"
                    for name in wrong
                )
            )

    def test_rule_items_are_progression(self):
        prog_items = {item.name for item in item_list if item.classification in (ItemClassification.progression, ItemClassification.progression_skip_balancing)}
        event_items = {location.name for locations in locations_by_region.values() for location in locations if location.is_event}
        item_names = prog_items | event_items
        rule_items = []
        for rule_data in connection_rules + location_rules:
            rule_items.extend(self._get_rule_items(rule_data))
        wrong = {item for item in rule_items if item not in item_names}
        if wrong:
            self.fail(
                "\n" + "\n".join(
                    f"Item '{name}' from a rule is not a progression item"
                    for name in wrong
                )
            )

    def test_item_codes_unique(self):
        codes = [item.code for item in item_list if item.code is not None]
        seen = set()
        dupes = set()
        for code in codes:
            if code in seen:
                dupes.add(code)
            else:
                seen.add(code)
        if dupes:
            self.fail(f"Duplicate item codes found: {dupes}")

    def test_no_knowledge_in_item_pool(self):
        knowledge_names = {
            "DoubleJumpKnowledge", "DashKnowledge", "MeditationKnowledge",
        }
        item_game_names = {item.game_name for item in item_list}
        found = knowledge_names & item_game_names
        if found:
            self.fail(f"Knowledge items found in item pool (Phase 1): {found}")

    def test_item_count(self):
        actual_items = [item for item in item_list if item.code is not None and item.item_type.name == "ITEM"]
        self.assertGreaterEqual(len(actual_items), 578, f"Expected 578+ items, got {len(actual_items)}")
