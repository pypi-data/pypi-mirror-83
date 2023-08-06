# -*- coding:utf-8 -*-
# CREATED BY: bohuai jiang 
# CREATED ON: 2020/8/16 5:34 PM
# LAST MODIFIED ON: 2020/10/27 6:07 PM
# AIM:
import sys
from typing import Union, List

from sentence_spliter.automata.symbols import SYMBOLS


def print_percent(current: int, max: int, header: str = ''):
    percent = float(current) / max * 100
    sys.stdout.write("\r{0}{1:.3g}%".format(header, percent))


class StrSequence:
    def __init__(self, str_block: Union[str, List[str]], verbose=None):
        self.value = str_block
        # -- pointers -- #
        self.v_pointer = -1
        self.sentence_start = 0
        # -- results -- #
        self.sentence_list_idx = []
        self.length = len(self.value)
        self.verbose = verbose
        if verbose is None and len(self.value) > 50000:
            self.verbose = True

        # -- other pointers -- #
        self.bracket_left = 0
        self.bracket_right = 0
        self.quota_left = 0
        self.quota_en = 0
        self.book_left = 0
        self.book_right = 0

    # -- magic method -- #
    def __str__(self):
        return self.value[self.sentence_start:self.v_pointer]

    def __getitem__(self, item: int):
        return self.value[item]

    @property
    def pre_value(self):
        return self[max(0, self.v_pointer - 1)]

    @property
    def next_value(self):
        return self[min(self.length - 1, self.v_pointer + 1)]

    @property
    def candidate_len(self):
        return self.v_pointer - self.sentence_start + 1

    @property
    def current_value(self):
        if self.value:
            try:
                return self.value[self.v_pointer]
            except:
                return self.value[-1]
        else:
            return self.value

    def sentence_list(self):
        out = []
        for v in self.__sentence_list:
            if v[0] < v[1]:
                if isinstance(self.value, str):
                    out.append(self.value[v[0]:v[1]])
                else:
                    out.append(' '.join(self.value[v[0]:v[1]]))
        return out

    def at_end_pos(self):
        return self.v_pointer >= self.length

    def add_to_candidate(self):
        self.v_pointer = min(self.v_pointer + 1, self.length)
        # -- update pointer -- #
        self.update_barcket()
        self.update_quota()
        self.update_bookmark()
        if self.verbose:
            print_percent(self.v_pointer, self.length, 'process cutting ')

    def add_to_sentence_list(self):
        self.__sentence_list.append((self.sentence_start, min(self.length, self.v_pointer + 1)))
        self.sentence_start = self.v_pointer + 1

    def reach_right_end(self):
        if self.v_pointer >= self.length - 1:
            self.v_pointer = self.length - 1
            return True
        else:
            return False

    # --- update pointer --- #
    def update_barcket(self):
        key = self.current_value
        if SYMBOLS['bracket_left'].match(key):
            self.bracket_left += 1
        if SYMBOLS['bracket_right'].match(key):
            self.bracket_right += 1

    def reset_bracket(self):
        self.bracket_left = 0
        self.bracket_right = 0

    def update_quota(self):
        word = self.current_value
        if SYMBOLS['quotation_en'].match(word):
            self.quota_en += 1
        if SYMBOLS['quotation_left'].match(word):
            self.quota_left += 1
        if SYMBOLS['quotation_right'].match(word):
            self.quota_en = 0
            self.quota_left = 0

    def reset_quota(self):
        self.quota_en = 0
        self.quota_left = 0

    def update_bookmark(self):
        word = self.current_value
        if SYMBOLS['book_left'].match(word):
            self.book_left += 1
        if SYMBOLS['book_right'].match(word):
            self.book_right += 1

    def reset_bookmark(self):
        self.book_left = 0
        self.book_right = 0
