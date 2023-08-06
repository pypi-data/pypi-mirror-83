# -*- coding:utf-8 -*-
# CREATED BY: bohuai jiang
# CREATED ON: 2020/8/4 2:52 PM
# LAST MODIFIED ON:
# AIM: automata abstract class
from abc import ABC, abstractmethod

from sentence_spliter.automata.sequence import StrSequence


class Criteria(ABC):
    def __init__(self, name: str, reverse: bool = False):
        self.name = name
        self.revers = reverse

    @abstractmethod
    def accept(self, state: StrSequence) -> bool:
        assert (0)

    def __call__(self, state: StrSequence):
        if self.revers:
            return not self.accept(state)
        else:
            return self.accept(state)


class Operation(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def operate(self, state: StrSequence) -> StrSequence:
        assert (0)

    def __call__(self, state: StrSequence) -> StrSequence:
        return self.operate(state)
