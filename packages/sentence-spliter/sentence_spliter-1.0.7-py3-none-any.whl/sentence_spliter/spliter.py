# -*- coding:utf-8 -*-
# CREATED BY: bohuai jiang 
# CREATED ON: 2020/8/14 4:30 PM
# LAST MODIFIED ON:
# AIM:
from typing import List

from sentence_spliter.automata.state_machine import StateMachine
from sentence_spliter.automata.sequence import StrSequence

from sentence_spliter.logic_graph import long_short_cuter, simple_cuter

# --  init default state machine -- #
__long_short_machine = StateMachine(long_short_cuter())
__simple_logic = StateMachine(simple_cuter())


def cut_to_sentences(paragraph: str, long_short: bool = False, verbose: bool = False):
    m_input = StrSequence(paragraph, verbose)
    if long_short:
        __long_short_machine.run(m_input)
        return m_input.sentence_list()
    else:
        __simple_logic.run(m_input)
        return m_input.sentence_list()


def run_cut(str_block: str, logic_graph: dict) -> List[str]:
    machine = StateMachine(logic_graph)
    m_input = StrSequence(str_block)
    machine.run(m_input, verbose=False)
    return m_input.sentence_list()
