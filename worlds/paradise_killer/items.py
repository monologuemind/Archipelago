from dataclasses import dataclass
from typing import Dict

from BaseClasses import ItemClassification

from .enums import APItemType, ItemCategory
from .helpers import ITEM_BASE_OFFSET, build_item_data, build_trial_item_data


@dataclass
class ItemData:
    code: int
    name: str
    game_name: str
    category: ItemCategory
    classification: ItemClassification = ItemClassification.filler
    item_type: APItemType = APItemType.ITEM
    skip: bool = False


item_list: list[ItemData] = []

for idata in build_item_data():
    item_list.append(ItemData(
        code=idata["code"],
        name=idata["name"],
        game_name=idata["game_name"],
        category=idata["category"],
        classification=idata["classification"],
        skip=idata["skip"],
    ))

# Trial event items
for tdata in build_trial_item_data():
    item_list.append(ItemData(
        code=tdata["code"],
        name=tdata["name"],
        game_name=tdata["game_name"],
        category=tdata["category"],
        classification=tdata["classification"],
        item_type=APItemType.EVENT,
    ))

item_dictionary: Dict[str, ItemData] = {
    item_data.name: item_data
    for item_data in item_list
}

item_name_groups: Dict[str, set] = {
    "Gold Coins": {item.name for item in item_list if item.category == ItemCategory.GOLD_COIN},
    "Collectables": {item.name for item in item_list if item.category == ItemCategory.COLLECTABLE},
    "Symbol Puzzles": {item.name for item in item_list if item.category == ItemCategory.SYMBOL_PUZZLE},
    "Starlight Skins": {item.name for item in item_list if item.category == ItemCategory.STARLIGHT_SKIN},
    "Soundtracks": {item.name for item in item_list if item.category == ItemCategory.SOUNDTRACK},
    "Crests": {item.name for item in item_list if item.category == ItemCategory.CREST},
    "Whisky": {item.name for item in item_list if item.category == ItemCategory.WHISKY},
    "Drinks": {item.name for item in item_list if item.category == ItemCategory.DRINK},
    "Keys": {item.name for item in item_list if item.category == ItemCategory.KEY},
    "Misc": {item.name for item in item_list if item.category == ItemCategory.MISC},
    "All Items": {item.name for item in item_list},
}
