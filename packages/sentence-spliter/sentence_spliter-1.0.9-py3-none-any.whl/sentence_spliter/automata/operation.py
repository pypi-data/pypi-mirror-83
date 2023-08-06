# -*- coding:utf-8 -*-
# CREATED BY: bohuai jiang 
# CREATED ON: 2020/8/7 3:54 PM
# LAST MODIFIED ON:
# AIM:
from abc import ABC

from sentence_spliter.automata.abc import Operation
from sentence_spliter.automata.sequence import StrSequence
from sentence_spliter.automata import condition
import copy


class Indolent(Operation):
    def __init__(self, name: str = None):
        super(Indolent, self).__init__('Indolent' if not name else name)

    def operate(self, state: StrSequence) -> StrSequence:
        state.add_to_candidate()
        return state


class Normal(Operation):
    def __init__(self):
        super(Normal, self).__init__('Normal')

    def operate(self, state: StrSequence) -> StrSequence:
        state.add_to_sentence_list()
        return state


class LongHandler(Operation):
    def __init__(self, hard_max: int = 300):
        super(LongHandler, self).__init__('LongHandler')
        self.is_end_symbol = condition.IsEndSymbol()
        self.is_comma = condition.IsComma()
        self.is_book_close = condition.IsBookClose()
        self.is_barcket_close = condition.IsBracketClose()
        self.hard_max = hard_max

    def operate(self, state: StrSequence) -> StrSequence:
        # new_candidate = []
        # - step 1. end_symbol 过滤
        temps_state = copy.copy(state)
        for i in range(temps_state.sentence_start, temps_state.v_pointer - 1)[::-1]:
            temps_state.v_pointer = i
            if all([self.is_end_symbol(temps_state), self.is_book_close(temps_state)]):
                cut_id = i
                break
        else:
            temps_state = copy.copy(state)
            # - step 2. comma 过滤
            for i in range(temps_state.sentence_start, temps_state.v_pointer - 1)[::-1]:  # enumerate(state.candidate):
                temps_state.v_pointer = i
                if self.is_comma(temps_state):
                    cut_id = i
                    break
            else:
                cut_id = state.sentence_start + self.hard_max - 1

        state.v_pointer = cut_id

        return state


class ShortHandler(Operation):

    def __init__(self):
        super(ShortHandler, self).__init__('ShortHandler')

    def operate(self, state: StrSequence) -> StrSequence:
        state.add_to_candidate()
        return state


class EndState(Operation):
    def __init__(self):
        super(EndState, self).__init__('EndState')

    def operate(self, state: StrSequence) -> StrSequence:
        if state.sentence_list and state.sentence_start >= state.length or state.length == 0:
            return state
        else:
            state.add_to_sentence_list()
            return state


# =========================== #
#      Special Condition      #
# =========================== #

class SpecialOperation(Operation, ABC):
    pass
