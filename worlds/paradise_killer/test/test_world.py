from .bases import ParadiseKillerTestBase


class TestWorldDefaultOptions(ParadiseKillerTestBase):
    options = {}

    def test_all_regions_have_locations(self) -> None:
        regions_with_locations = set()
        for loc in self.multiworld.get_locations(self.player):
            regions_with_locations.add(loc.parent_region.name)
        self.assertIn("Main Island", regions_with_locations)
        self.assertIn("Floating Islands", regions_with_locations)
        self.assertIn("Courtroom", regions_with_locations)

    def test_generate(self) -> None:
        self.assertGreater(len(self.multiworld.get_locations(self.player)), 0)
        self.assertGreater(len(self.multiworld.itempool), 0)

    def test_victory_condition(self) -> None:
        victory = self.multiworld.completion_condition[self.player]
        self.assertIsNotNone(victory)

    def test_filler_items_exist(self) -> None:
        from ..items import item_list
        from BaseClasses import ItemClassification
        fillers = [i for i in item_list if i.classification == ItemClassification.filler]
        self.assertGreater(len(fillers), 0)

    def test_progression_items_exist(self) -> None:
        from ..items import item_list
        from BaseClasses import ItemClassification
        prog = [i for i in item_list if i.classification == ItemClassification.progression]
        self.assertGreater(len(prog), 0)

    def test_pool_size_matches_locations(self) -> None:
        fillable = [loc for loc in self.multiworld.get_locations(self.player) if loc.address is not None]
        self.assertEqual(len(self.multiworld.itempool), len(fillable))


class TestWorldGoldCoinsExcluded(ParadiseKillerTestBase):
    options = {
        "shuffle_gold_coins": False,
    }

    def test_no_gold_coins_in_pool(self) -> None:
        from ..items import item_dictionary
        from ..enums import ItemCategory
        for item in self.multiworld.itempool:
            data = item_dictionary.get(item.name)
            if data:
                self.assertNotEqual(data.category, ItemCategory.GOLD_COIN,
                                    f"Gold coin found in pool: {item.name}")


class TestWorldEmptyIncludeLocations(ParadiseKillerTestBase):
    options = {
        "include_locations": [],
    }

    def test_generates_with_no_include_filter(self) -> None:
        self.assertGreater(len(self.multiworld.get_locations(self.player)), 0)
