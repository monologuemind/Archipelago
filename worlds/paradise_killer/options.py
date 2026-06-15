from dataclasses import dataclass

from Options import ExcludeLocations, ItemSet, LocationSet, OptionGroup, PerGameCommonOptions, Toggle


class IncludeFloatingIslands(Toggle):
    """Include Floating Islands locations in the item pool."""
    display_name = "Include Floating Islands"


class IncludeParadiseIsland(Toggle):
    """Include Paradise Island locations in the item pool."""
    display_name = "Include Paradise Island"


class IncludeTrial(Toggle):
    """Include trial conviction locations in the pool."""
    display_name = "Include Trial"


class ShuffleGoldCoins(Toggle):
    """Whether to shuffle gold coins (may dilute pool)."""
    display_name = "Shuffle Gold Coins"


class ExcludeLocations(ExcludeLocations):
    """Prevent these locations from having an important item."""
    display_name = "Excluded Locations"


class IncludeLocations(LocationSet):
    """Only these locations may contain an important item."""
    display_name = "Included Locations"


class IncludeItems(ItemSet):
    """Always include these items in the pool (if they have pickup locations)."""
    display_name = "Included Items"


option_groups = [
    OptionGroup("Game Options", [
        IncludeFloatingIslands,
        IncludeParadiseIsland,
        IncludeTrial,
        ShuffleGoldCoins,
    ]),
    OptionGroup("Location Options", [
        ExcludeLocations,
        IncludeLocations,
    ]),
    OptionGroup("Item Options", [
        IncludeItems,
    ]),
]


@dataclass
class ParadiseKillerOptions(PerGameCommonOptions):
    include_floating_islands: IncludeFloatingIslands
    include_paradise_island: IncludeParadiseIsland
    include_trial: IncludeTrial
    shuffle_gold_coins: ShuffleGoldCoins
    exclude_locations: ExcludeLocations
    include_locations: IncludeLocations
    include_items: IncludeItems
