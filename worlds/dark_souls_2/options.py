from dataclasses import dataclass

from Options import Choice, ItemSet, LocationSet, OptionGroup, PerGameCommonOptions, Range, Toggle, Visibility, DeathLink


class GameVersion(Choice):
    """Set the game version you will be playing on

    - **sotfs:** You will be playing the Scholar of the First Sin version
    - **vanilla:** You will be playing the Vanilla version"""
    display_name = "Game Version"
    option_sotfs = 0
    option_vanilla = 1
    default = 0

class OldIronKingDLC(Toggle):
    """Enable Crown of the Old Iron King DLC."""
    display_name = "Enable Crown of the Old Iron King DLC"


class IvoryKingDLC(Toggle):
    """Enable Crown of the Ivory King DLC."""
    display_name = "Enable Crown of the Ivory King DLC"


class SunkenKingDLC(Toggle):
    """Enable Crown of the Sunken King DLC."""
    display_name = "Enable Crown of the Sunken King DLC"

class CombatLogic(Choice):
    """
    Determines the distribution of Estus Flask Shards and Sublime Bone Dust.
    Easy - Most shards/dust available fairly early on
    Medium - Moderate amount of shards/dust available early in the game
    Hard - There is minimal logical requirement for shards/dust to be available before the end of the game
    Disabled - There is zero requirements for shards/dust anywhere; Lost Bastille is Sphere 1 in Scholar, and Sinners' Rise is Sphere 1 in vanilla.
    """
    display_name = "Combat Logic"
    option_easy = 0
    option_medium = 1
    option_hard = 2
    option_disabled = 3
    default = option_medium

class KeepInfiniteLifegems(Toggle):
    """Keep Melentia's infinite supply of lifegems unrandomized"""
    display_name = "Keep Infinite Lifegems"


class NoWeaponRequirements(Toggle):
    """Remove the requirements to wield weapons"""
    display_name = "No Weapon Requirements"


class NoSpellRequirements(Toggle):
    """Remove the requirements to cast spells"""
    display_name = "No Spell Requirements"


class NoArmorRequirements(Toggle):
    """Remove the requirements to wear armor"""
    display_name = "No Armor Requirements"


class NoEquipLoad(Toggle):
    """Disable the equip load constraint from the game."""
    display_name = "No Equip Load"


class RandomizeEquipmentLevelPercentageOption(Range):
    """The percentage of weapons and armor in the pool to be reinforced."""
    display_name = "Percentage of Randomized Weapons"
    range_start = 0
    range_end = 100
    default = 33


class MinEquipmentReinforcementIn5Option(Range):
    """The minimum reinforcement level for equipment that can only reach +5."""
    display_name = "Minimum Reinforcement of +5 Equipment"
    range_start = 1
    range_end = 5
    default = 1


class MaxEquipmentReinforcementIn5Option(Range):
    """The maximum reinforcement level for equipment that can only reach +5."""
    display_name = "Maximum Reinforcement of +5 Equipment"
    range_start = 1
    range_end = 5
    default = 5


class MinEquipmentReinforcementIn10Option(Range):
    """The minimum reinforcement level for equipment that can only reach +10."""
    display_name = "Minimum Reinforcement of +10 Equipment"
    range_start = 1
    range_end = 10
    default = 1


class MaxEquipmentReinforcementIn10Option(Range):
    """The maximum reinforcement level for equipment that can only reach +10."""
    display_name = "Maximum Reinforcement of +10 Equipment"
    range_start = 1
    range_end = 10
    default = 10


class EarlyBlacksmith(Choice):
    """Force Lenigrast's key into an early sphere in your world or across all worlds."""
    display_name = "Early Blacksmith"
    option_anywhere = 0
    option_early_global = 1
    option_early_local = 2
    default = option_early_local

class UsefulItems(ItemSet):
    """
    Items that will be marked as useful.
    Useful items cannot be placed in excluded or unreachable locations.
    Both individual item names and item categories can be used here.
    """
    display_name = "Useful Items"
    default = frozenset({"Boss Souls", "Upgrade Materials"})

class IncludeItems(ItemSet):
    """
    Items that will be included in the item pool if there is space.
    This can be helpful if you want to include an item that is not in logic by default.
    Each item will only be added to the item pool once.
    """
    display_name = "Include Items"

class IncludeLocations(LocationSet):
    """
    Only these locations may contain an important item.
    This does the opposite of Excluded Locations.
    If empty, no restriction is applied.
    """
    display_name = "Included Locations"

class ExcludeLocations(LocationSet):
    """Prevent these locations from having an important item."""
    display_name = "Excluded Locations"

class TrapPreset(Choice):
    """Default selection for trap counts. Possible trap counts can be limited by the number of games being played"""
    display_name = "Trap Preset"
    option_none = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_good_luck = 4
    default = option_none

class PoisonTrap(Range):
    """Immediately triggers poison"""
    display_name = "Poison Trap"
    range_start = 0
    range_end = 100
    default = 0
    visibility = Visibility.complex_ui

class BleedingTrap(Range):
    """Immediately deals bleeding damage"""
    display_name = "Bleeding Trap"
    range_start = 0
    range_end = 100
    default = 0
    visibility = Visibility.complex_ui

class CurseTrap(Range):
    """Immediately triggers a curse"""
    display_name = "Curse Trap"
    range_start = 0
    range_end = 100
    default = 0
    visibility = Visibility.complex_ui

class FireAndKnockdownTrap(Range):
    """Immediately triggers the fire & knockdown efffect (covered in oil and encounter fire)"""
    display_name = "Fire & Knockdown Trap"
    range_start = 0
    range_end = 100
    default = 0
    visibility = Visibility.complex_ui

class ToxicTrap(Range):
    """Immediately trigger toxic"""
    display_name = "Toxic Trap"
    range_start = 0
    range_end = 100
    default = 0
    visibility = Visibility.complex_ui
class PetrificationTrap(Range):
    """Immediately trigger petrification (kills player)"""
    display_name = "Petrification Trap"
    range_start = 0
    range_end = 100
    default = 0
    visibility = Visibility.complex_ui

class SlightCorrosionTrap(Range):
    """Only apply a small amount of corrosion to equipment (roughly 10-15%)"""
    display_name = "Slight Corrosion Trap"
    range_start = 0
    range_end = 100
    default = 0
    visibility = Visibility.complex_ui

class MediumCorrosionTrap(Range):
    """Only apply a medium amount of corrosion to equipment (roughly 30-50%)"""
    display_name = "Medium Corrosion Trap"
    range_start = 0
    range_end = 100
    default = 0
    visibility = Visibility.complex_ui

class HeavyCorrosionTrap(Range):
    """Only apply a small amount of corrosion to equipment (roughly 70-100%)"""
    display_name = "Heavy Corrosion Trap"
    range_start = 0
    range_end = 100
    default = 0
    visibility = Visibility.complex_ui

class HelloCarvingTrap(Range):
    """Immediately throws the hello carving"""
    display_name = "Hello Carving Trap"
    range_start = 0
    range_end = 100
    default = 0
    visibility = Visibility.complex_ui

class ThankYouCarvingTrap(Range):
    """Immediately throws the thank you carving"""
    display_name = "Thank You Carving Trap"
    range_start = 0
    range_end = 100
    default = 0
    visibility = Visibility.complex_ui

class SorryCarvingTrap(Range):
    """Immediately throws the sorry carving"""
    display_name = "Sorry Carving Trap"
    range_start = 0
    range_end = 100
    default = 0
    visibility = Visibility.complex_ui

class VeryGoodCarvingTrap(Range):
    """Immediately throws the very good carving"""
    display_name = "Very Good Carving Trap"
    range_start = 0
    range_end = 100
    default = 0
    visibility = Visibility.complex_ui

class ImmolationTrap(Range):
    """Immediately triggers immolation"""
    display_name = "Immolation Trap"
    range_start = 0
    range_end = 100
    default = 0
    visibility = Visibility.complex_ui

class FirebombTrap(Range):
    """Immediately throws a firebomb"""
    display_name = "Firebomb Trap"
    range_start = 0
    range_end = 100
    default = 0
    visibility = Visibility.complex_ui

class BlackFirebombTrap(Range):
    """Immediately throws a black firebomb"""
    display_name = "Black Firebomb Trap"
    range_start = 0
    range_end = 100
    default = 0
    visibility = Visibility.complex_ui

class RandomDeathCarving(Toggle):
    """Throw out a random carving upon death."""
    display_name = "Random Death Carving"

class RandomTrapCarving(Toggle):
    """Throw out a random carving upon getting a trap."""
    display_name = "Random Trap Carving"

class DS2SharedTraps(Toggle):
    """This allows a player sending a trap to someone else to also experience said trap."""
    display_name = "DS2 Shared Traps"

class TrapLink(Toggle):
    """Whether your received traps are linked to other players.
    You will also receive any linked traps from other players with Trap Link enabled,
    if you have a weight above "none" set for that trap.
    """
    display_name = "Trap Link"

option_groups = [
    OptionGroup("Game Options", [
        GameVersion,
        SunkenKingDLC,
        OldIronKingDLC,
        IvoryKingDLC
    ]),

    OptionGroup("Equipment", [
        NoWeaponRequirements,
        NoSpellRequirements,
        NoArmorRequirements,
        NoEquipLoad,

        RandomizeEquipmentLevelPercentageOption,
        MinEquipmentReinforcementIn5Option,
        MaxEquipmentReinforcementIn5Option,
        MinEquipmentReinforcementIn10Option,
        MaxEquipmentReinforcementIn10Option
    ]),


    OptionGroup("Quality of Life", [
        KeepInfiniteLifegems,
        EarlyBlacksmith,
        CombatLogic
    ]),

    OptionGroup("Item & Location Options", [
        ExcludeLocations,
        IncludeLocations,
        UsefulItems,
        IncludeItems
    ]),

    OptionGroup("Traps", [
        TrapPreset,
        RandomTrapCarving,
        DS2SharedTraps,
        TrapLink,
        PoisonTrap,
        BleedingTrap,
        CurseTrap,
        FireAndKnockdownTrap,
        ToxicTrap,
        PetrificationTrap,
        SlightCorrosionTrap,
        MediumCorrosionTrap,
        HeavyCorrosionTrap,
        HelloCarvingTrap,
        ThankYouCarvingTrap,
        SorryCarvingTrap,
        VeryGoodCarvingTrap,
        ImmolationTrap,
        FirebombTrap,
        BlackFirebombTrap,

        DeathLink,
        RandomDeathCarving,
    ]),
]

@dataclass
class DarkSouls2Options(PerGameCommonOptions):
    game_version: GameVersion
    sunken_king_dlc: SunkenKingDLC
    old_iron_king_dlc: OldIronKingDLC
    ivory_king_dlc: IvoryKingDLC

    no_weapon_req: NoWeaponRequirements
    no_spell_req: NoSpellRequirements
    no_armor_req: NoArmorRequirements
    no_equip_load: NoEquipLoad

    randomize_equipment_level_percentage: RandomizeEquipmentLevelPercentageOption
    min_equipment_reinforcement_in_5: MinEquipmentReinforcementIn5Option
    max_equipment_reinforcement_in_5: MaxEquipmentReinforcementIn5Option
    min_equipment_reinforcement_in_10: MinEquipmentReinforcementIn10Option
    max_equipment_reinforcement_in_10: MaxEquipmentReinforcementIn10Option

    combat_logic: CombatLogic
    infinite_lifegems: KeepInfiniteLifegems
    early_blacksmith: EarlyBlacksmith

    exclude_locations: ExcludeLocations
    include_locations: IncludeLocations
    useful_items: UsefulItems
    include_items: IncludeItems

    trap_preset: TrapPreset
    random_trap_carving: RandomTrapCarving
    ds2_shared_traps: DS2SharedTraps
    trap_link: TrapLink
    poison_trap: PoisonTrap
    bleeding_trap: BleedingTrap
    curse_trap: CurseTrap
    fire_and_knockdown_trap: FireAndKnockdownTrap
    toxic_trap: ToxicTrap
    petrification_trap: PetrificationTrap
    slight_corrosion_trap: SlightCorrosionTrap
    medium_corrosion_trap: MediumCorrosionTrap
    heavy_corrosion_trap: HeavyCorrosionTrap
    hello_carving_trap: HelloCarvingTrap
    thank_you_carving_trap: ThankYouCarvingTrap
    sorry_carving_trap: SorryCarvingTrap
    very_good_carving_trap: VeryGoodCarvingTrap
    immolation_trap: ImmolationTrap
    firebomb_trap: FirebombTrap
    black_firebomb_trap: BlackFirebombTrap

    death_link: DeathLink
    random_death_carving: RandomDeathCarving

    def get_trap_range_value(self, trap_name: str):
        if (trap_name == "Poison Trap"):
            return self.poison_trap.value
        if (trap_name == "Bleeding Trap"):
            return self.bleeding_trap.value
        if (trap_name == "Curse Trap"):
            return self.curse_trap.value
        if (trap_name == "Fire & Knockdown Trap"):
            return self.fire_and_knockdown_trap.value
        if (trap_name == "Toxic Trap"):
            return self.toxic_trap.value
        if (trap_name == "Petrification Trap"):
            return self.petrification_trap.value
        if (trap_name == "Slight Corrosion Trap"):
            return self.slight_corrosion_trap.value
        if (trap_name == "Medium Corrosion Trap"):
            return self.medium_corrosion_trap.value
        if (trap_name == "Heavy Corrosion Trap"):
            return self.heavy_corrosion_trap.value
        if (trap_name == "Hello Carving Trap"):
            return self.hello_carving_trap.value
        if (trap_name == "Thank You Carving Trap"):
            return self.thank_you_carving_trap.value
        if (trap_name == "Sorry Carving Trap"):
            return self.sorry_carving_trap.value
        if (trap_name == "Very Good Carving Trap"):
            return self.very_good_carving_trap.value
        if (trap_name == "Immolation Trap"):
            return self.immolation_trap.value
        if (trap_name == "Firebomb Trap"):
            return self.firebomb_trap.value
        if (trap_name == "Black Firebomb Trap"):
            return self.black_firebomb_trap.value
        return None
    
    def set_trap_range_value(self, trap_name: str, value: int):
        if (trap_name == "Poison Trap"):
            self.poison_trap.value = value
            return 1
        if (trap_name == "Bleeding Trap"):
            self.bleeding_trap.value = value
            return 1
        if (trap_name == "Curse Trap"):
            self.curse_trap.value = value
            return 1
        if (trap_name == "Fire & Knockdown Trap"):
            self.fire_and_knockdown_trap.value = value
            return 1
        if (trap_name == "Toxic Trap"):
            self.toxic_trap.value = value
            return 1
        if (trap_name == "Petrification Trap"):
            self.petrification_trap.value = value
            return 1
        if (trap_name == "Slight Corrosion Trap"):
            self.slight_corrosion_trap.value = value
            return 1
        if (trap_name == "Medium Corrosion Trap"):
            self.medium_corrosion_trap.value = value
            return 1
        if (trap_name == "Heavy Corrosion Trap"):
            self.heavy_corrosion_trap.value = value
            return 1
        if (trap_name == "Hello Carving Trap"):
            self.hello_carving_trap.value = value
            return 1
        if (trap_name == "Thank You Carving Trap"):
            self.thank_you_carving_trap.value = value
            return 1
        if (trap_name == "Sorry Carving Trap"):
            self.sorry_carving_trap.value = value
            return 1
        if (trap_name == "Very Good Carving Trap"):
            self.very_good_carving_trap.value = value
            return 1
        if (trap_name == "Immolation Trap"):
            self.immolation_trap.value = value
            return 1
        if (trap_name == "Firebomb Trap"):
            self.firebomb_trap.value = value
            return 1
        if (trap_name == "Black Firebomb Trap"):
            self.black_firebomb_trap.value = value
            return 1
        return 0
