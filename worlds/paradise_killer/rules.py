from dataclasses import dataclass
from typing import List, Union

from worlds.generic.Rules import CollectionRule

from .enums import TrialStage

RuleInput = Union[CollectionRule, str, List[str]]


@dataclass
class RuleData:
    spot: str
    rule: RuleInput

    def to_collection_rule(self, player: int) -> CollectionRule:
        if callable(self.rule):
            return lambda state, f=self.rule: f(state, player)
        if isinstance(self.rule, str):
            return lambda state: state.has(self.rule, player)
        if isinstance(self.rule, List):
            return lambda state: any(state.has(item, player) for item in self.rule)
        assert False, f"RuleData rule is invalid type {type(self.rule)}"


connection_rules: List[RuleData] = [
    RuleData("Menu -> Main Island", lambda state, player: True),
    RuleData("Main Island -> Floating Islands", lambda state, player: True),
    RuleData("Main Island -> Paradise Island", lambda state, player: True),
    RuleData("Paradise Island -> Courtroom", lambda state, player: True),

    RuleData("Courtroom -> Trial: Menu", lambda state, player: True),
    RuleData("Trial: Menu -> Trial: Henry's Escape", lambda state, player: True),

    RuleData("Trial: Henry's Escape -> Trial: Henry's Possession",
             TrialStage.HENRY_ESCAPE.value),
    RuleData("Trial: Henry's Possession -> Trial: Grace Bloodlines",
             TrialStage.HENRY_POSSESSION.value),
    RuleData("Trial: Grace Bloodlines -> Trial: Crimson Agenda",
             TrialStage.GRACE_BLOODLINES.value),
    RuleData("Trial: Crimson Agenda -> Trial: Doom Jazz Partnership",
             TrialStage.CRIMSON_AGENDA.value),
    RuleData("Trial: Doom Jazz Partnership -> Trial: Yuri Testimony",
             TrialStage.DOOM_JAZZ_PARTNERSHIP.value),
    RuleData("Trial: Yuri Testimony -> Trial: Lydia & Sam Accusation",
             TrialStage.YURI_TESTIMONY.value),
    RuleData("Trial: Lydia & Sam Accusation -> Trial: Carmelina Betrayal",
             TrialStage.LYDIA_SAM_ACCUSATION.value),
    RuleData("Trial: Carmelina Betrayal -> Trial: Witness Corroboration",
             TrialStage.CARMELINA_BETRAYAL.value),
    RuleData("Trial: Witness Corroboration -> Trial: Final Argument",
             TrialStage.WITNESS_CORROBORATION.value),
    RuleData("Trial: Final Argument -> Trial: Conviction",
             TrialStage.FINAL_ARGUMENT.value),
]

location_rules: List[RuleData] = [
    RuleData("Trial: Henry's Escape", TrialStage.HENRY_ESCAPE.value),
    RuleData("Trial: Henry's Possession", TrialStage.HENRY_POSSESSION.value),
    RuleData("Trial: Grace Bloodlines", TrialStage.GRACE_BLOODLINES.value),
    RuleData("Trial: Crimson Agenda", TrialStage.CRIMSON_AGENDA.value),
    RuleData("Trial: Doom Jazz Partnership", TrialStage.DOOM_JAZZ_PARTNERSHIP.value),
    RuleData("Trial: Yuri Testimony", TrialStage.YURI_TESTIMONY.value),
    RuleData("Trial: Lydia & Sam Accusation", TrialStage.LYDIA_SAM_ACCUSATION.value),
    RuleData("Trial: Carmelina Betrayal", TrialStage.CARMELINA_BETRAYAL.value),
    RuleData("Trial: Witness Corroboration", TrialStage.WITNESS_CORROBORATION.value),
    RuleData("Trial: Final Argument", TrialStage.FINAL_ARGUMENT.value),
]
