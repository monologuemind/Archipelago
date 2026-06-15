from enum import Enum


class ItemCategory(Enum):
    GOLD_COIN = "Gold Coins"
    COLLECTABLE = "Collectables"
    SYMBOL_PUZZLE = "Symbol Puzzles"
    STARLIGHT_SKIN = "Starlight Skins"
    SWITCH = "Switches"
    SOUNDTRACK = "Soundtracks"
    CREST = "Crests"
    WHISKY = "Whisky"
    KEY = "Keys"
    GHOST_ITEM = "Ghost Items"
    DRINK = "Drinks"
    MISC = "Misc"


class APItemType(Enum):
    ITEM = 1
    EVENT = 2


class APLocationType(Enum):
    PICKUP = 100_000_000
    EVENT = 400_000_000


class TrialStage(Enum):
    MENU = "Trial: Menu"
    HENRY_ESCAPE = "Trial: Henry's Escape"
    HENRY_POSSESSION = "Trial: Henry's Possession"
    GRACE_BLOODLINES = "Trial: Grace Bloodlines"
    CRIMSON_AGENDA = "Trial: Crimson Agenda"
    DOOM_JAZZ_PARTNERSHIP = "Trial: Doom Jazz Partnership"
    YURI_TESTIMONY = "Trial: Yuri Testimony"
    LYDIA_SAM_ACCUSATION = "Trial: Lydia & Sam Accusation"
    CARMELINA_BETRAYAL = "Trial: Carmelina Betrayal"
    WITNESS_CORROBORATION = "Trial: Witness Corroboration"
    FINAL_ARGUMENT = "Trial: Final Argument"
    CONVICTION = "Trial: Conviction"
    VICTORY = "Victory"
