# -*- coding:utf-8 -*-
# CREATED BY: bohuai jiang 
# CREATED ON: 2020/8/7 3:50 PM
# LAST MODIFIED ON:
# AIM:
from abc import ABC
import re

from sentence_spliter.automata.abc import Criteria
from sentence_spliter.automata.sequence import StrSequence
from sentence_spliter.automata.symbols import SYMBOLS


class IsEndState(Criteria):
    def __init__(self):
        super(IsEndState, self).__init__('IsEndState')

    def accept(self, state: StrSequence) -> bool:
        return state.reach_right_end()


class IsEndSymbol(Criteria):
    def __init__(self):
        super(IsEndSymbol, self).__init__('IsEndSymbolZH')
        self.empty = re.compile('\s')

    def is_zh(self, char: str):
        if '\u4e00' <= char <= '\u9fa5':
            return True

    def accept(self, state: StrSequence) -> bool:
        if SYMBOLS['end_symbols'].match(state.current_value) and \
                not (SYMBOLS['en_dot'].match(state.next_value) or SYMBOLS['end_symbols'].match(state.next_value)):
            return True
        if SYMBOLS['en_dot'].match(state.current_value):
            if self.is_zh(state.next_value) or self.empty.match(state.next_value):
                return True
        return False


class IsComma(Criteria):
    def __init__(self):
        super(IsComma, self).__init__('IsComma')

    def accept(self, state: StrSequence) -> bool:
        if SYMBOLS['comma'].match(state.current_value):
            return True
        return False


class IsBracketClose(Criteria):
    def __init__(self):
        super(IsBracketClose, self).__init__('IsBracketClose')

    def accept(self, state: StrSequence) -> bool:
        # -- avoid endless loop -- #
        if state.reach_right_end():
            return True
        if state.bracket_left <= state.bracket_right:
            state.reset_bracket()
            return True
        else:
            return False


class IsQuoteClose(Criteria):
    def __init__(self):
        super(IsQuoteClose, self).__init__('IsQuoteClose')

    def accept(self, state: StrSequence) -> bool:
        # -- avoid endless loop -- #
        if state.reach_right_end():
            return True

        if state.quota_en > 0:
            if (state.quota_en + state.quota_left) % 2 == 0:
                state.reset_quota()
                return True
            else:
                return False
        elif state.quota_left > 0:
            return False
        else:
            return True


class IsBookClose(Criteria):
    def __init__(self):
        super(IsBookClose, self).__init__('IsBookClose')

    def accept(self, state: StrSequence) -> bool:
        # -- avoid endless loop -- #
        if state.reach_right_end():
            return True
        if state.book_left <= state.book_right:
            # state.reset_bookmark()
            return True
        else:
            return False


class IsLongSentence(Criteria):
    def __init__(self, max_len: int = 128):
        super(IsLongSentence, self).__init__('IsLongSentence')
        self.max_len = max_len

    def accept(self, state: StrSequence) -> bool:
        if state.candidate_len > self.max_len:
            return True
        return False


class IsShortSentence(Criteria):
    def __init__(self, min_len: int = 17):
        super(IsShortSentence, self).__init__('IsShortSentence')
        self.min_len = min_len

    def accept(self, state: StrSequence) -> bool:
        if state.candidate_len < self.min_len:
            return True
        return False


class IsSpace(Criteria):
    def __init__(self):
        super(IsSpace, self).__init__('IsSpace')
        self.pattern = re.compile('\s')

    def accept(self, state: StrSequence) -> bool:
        if self.pattern.match(state.current_value):
            return True
        else:
            return False


# =========================== #
#      Special Condition      #
# =========================== #

class SpecialCondition(Criteria, ABC):
    pass


class IsRightQuota(SpecialCondition):
    def __init__(self, index=0):
        super(IsRightQuota, self).__init__('IsRightQuota')
        self.index = index

    def accept(self, state: StrSequence) -> bool:
        if self.index >= 0:
            index = min(state.v_pointer + self.index, state.length - 1)
        else:
            index = max(0, state.v_pointer + self.index)
        if SYMBOLS["quotation_right"].match(state[index]):
            return True
        return False


class IsLeftQuota(SpecialCondition):
    def __init__(self, index=0):
        super(IsLeftQuota, self).__init__('IsLeftQuota')
        self.index = index

    def accept(self, state: StrSequence) -> bool:
        if self.index >= 0:
            index = min(state.v_pointer + self.index, state.length - 1)
        else:
            index = max(0, state.v_pointer + self.index)
        if SYMBOLS["quotation_left"].match(state[index]):
            return True
        return False


class IsLeftQuotaGreaterThan(SpecialCondition):
    '''
    左引号 重复次数大于一定值
    '''

    def __init__(self, theta: int = 1):
        super(IsLeftQuotaGreaterThan, self).__init__('IsLeftQuotaGreaterThan')
        self.theta = theta

    def accept(self, state: StrSequence) -> bool:
        if state.quota_left > self.theta:
            state.reset_quota()
            state.v_pointer -= 1
            return True


class IsRQuotaStickWithLQuota(SpecialCondition):
    '''
    右引号紧跟着左引号
    '''

    def __init__(self):
        super(IsRQuotaStickWithLQuota, self).__init__('IsRQuotaStickWithLQuota')

    def accept(self, state: StrSequence) -> bool:
        if SYMBOLS['quotation_right'].match(state.current_value) and \
                SYMBOLS['quotation_left'].match(state.next_value):
            return True
        return False


class WithSays(SpecialCondition):
    def __init__(self):
        super(WithSays, self).__init__('WithSays')
        self.pattern = re.compile('([他她](说|说道|笑道|道))+')

    def accept(self, state: StrSequence) -> bool:
        sentence = state[state.v_pointer + 1:15]
        if self.pattern.match(sentence):
            return True
        return False


class SpecialEnds(SpecialCondition):
    def __init__(self):
        super(SpecialEnds, self).__init__('SpecialEnds')
        self.pattern_pre = re.compile('([~～])')
        self.pattern_cur = re.compile('\s')

    def accept(self, state: StrSequence) -> bool:
        if self.pattern_pre.match(state.pre_value) and self.pattern_cur.match(state.current_value):
            return True
        else:
            return False
