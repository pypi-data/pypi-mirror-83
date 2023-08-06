# -*- coding:utf-8 -*-
# CREATED BY: bohuai jiang 
# CREATED ON: 2020/8/17 10:01 AM
# LAST MODIFIED ON:
# AIM:

import unittest

from sentence_spliter import spliter

from sentence_spliter.logic_graph import long_short_cuter, simple_cuter
from sentence_spliter.automata.state_machine import StateMachine
from sentence_spliter.automata.sequence import StrSequence


class test_spliter(unittest.TestCase):
    def setUp(self) -> None:
        self.long_short_machine = StateMachine(long_short_cuter())
        self.simple_logic = StateMachine(simple_cuter())

    # @unittest.skip('ignore')
    def test_book(self):
        sentence = '《霸道总裁你在哪？》是一本很好看的书，小明非常喜欢这本书。《霸道总裁你在哪？》是一本很好看的书，小明非常喜欢这本书。'
        out = spliter.cut_to_sentences(sentence)
        expect = ['《霸道总裁你在哪？》是一本很好看的书，小明非常喜欢这本书。', '《霸道总裁你在哪？》是一本很好看的书，小明非常喜欢这本书。']
        self.assertEqual(expect, out)

    # @unittest.skip('ignore')
    def test_simple_quota(self):
        sentence = '"《霸道总裁你在哪？》是一本很好看的书!"，小明自豪的说到。'
        out = spliter.cut_to_sentences(sentence)
        expect = ['"《霸道总裁你在哪？》是一本很好看的书!"，小明自豪的说到。']
        self.assertEqual(expect, out)

    # @unittest.skip('ignore')
    def test_simple_bracket(self):
        sentence = '"《霸道总裁你在哪？》是一本很好看的书!"，小明自豪的说到(其实小明并不知道写的是什么。)。' \
                   '"《霸道总裁你在哪？》是一本很好看的书!"，小明自豪的说到(其实小明并不知道写的是什么。)。'
        out = spliter.cut_to_sentences(sentence)
        expect = ['"《霸道总裁你在哪？》是一本很好看的书!"，小明自豪的说到(其实小明并不知道写的是什么。)。',
                  '"《霸道总裁你在哪？》是一本很好看的书!"，小明自豪的说到(其实小明并不知道写的是什么。)。']
        self.assertEqual(expect, out)

    # @unittest.skip('ignore')
    def test_end_sentence(self):
        sentence = '在很久很久以前......... 有座山。山里有座庙啊!!!庙里竟然有个老和尚！？。。。。'
        out = self.simple_logic.run(StrSequence(sentence))
        out = out.sentence_list()
        expect = ['在很久很久以前.........', ' 有座山。', '山里有座庙啊!!!', '庙里竟然有个老和尚！？。。。。']
        self.assertEqual(expect, out)

        sentence = '在很久很久以前......... 有座山。山里有座庙啊!!!庙里竟然有个老和尚！？。。。。www.baidu.com。1.23.4'
        out = self.simple_logic.run(StrSequence(sentence))
        out = out.sentence_list()
        expect = ['在很久很久以前.........', ' 有座山。', '山里有座庙啊!!!', '庙里竟然有个老和尚！？。。。。', 'www.baidu.com。', '1.23.4']
        self.assertEqual(expect, out)

    # @unittest.skip('ignore')
    def test_quota(self):
        sentence = '张晓风笑着说道，“我们这些年可比过去强多了！“过去吃不起饭，穿不暖衣服。 现在呢？要啥有啥！'
        out = spliter.cut_to_sentences(sentence)
        expect = ['张晓风笑着说道，“我们这些年可比过去强多了！', '“过去吃不起饭，穿不暖衣服。 现在呢？要啥有啥！']
        self.assertEqual(expect, out)

    # @unittest.skip('ignore')
    def test_Lquota(self):
        sentence = '“我和你讨论的不是一个东西，死亡率与死亡比例是不同的”“你知道么？CNN你们总是制造假新闻。。。”'
        out = spliter.cut_to_sentences(sentence)
        expect = ['“我和你讨论的不是一个东西，死亡率与死亡比例是不同的”', '“你知道么？CNN你们总是制造假新闻。。。”']
        self.assertEqual(expect, out)

        sentence = '“我和你讨论的不是一个东西，死亡率与死亡比例是不同的” “你知道么？CNN你们总是制造假新闻。。。”'
        out = spliter.cut_to_sentences(sentence)
        expect = ['“我和你讨论的不是一个东西，死亡率与死亡比例是不同的” ', '“你知道么？CNN你们总是制造假新闻。。。”']
        self.assertEqual(expect, out)

    # @unittest.skip('ignore')
    def test_quota(self):
        sentence = '"师傅，前面有烟火，我去去就来！"，悟空道。"徒儿慢点，记住千万不要伤到人家"。唐生急忙跑过来。'
        out = spliter.cut_to_sentences(sentence)
        expect = ['"师傅，前面有烟火，我去去就来！"，悟空道。', '"徒儿慢点，记住千万不要伤到人家"。', '唐生急忙跑过来。']
        self.assertEqual(expect, out)

    # @unittest.skip('ignore')
    def test_long(self):
        sentence = '1234567890123456789012345678901234567890123456789012345678901234567890' \
                   '1234567890123456789012345678901234567890123456789012345678901234567890' \
                   '1234567890123456789012345678901234567890123456789012345678901234567890'
        long_short_machine = StateMachine(long_short_cuter(hard_max=70, max_len=70))
        out = long_short_machine.run(StrSequence(sentence))
        out = out.sentence_list()
        expect = ['1234567890123456789012345678901234567890123456789012345678901234567890',
                  '1234567890123456789012345678901234567890123456789012345678901234567890',
                  '1234567890123456789012345678901234567890123456789012345678901234567890']
        self.assertEqual(expect, out)

    # @unittest.skip('ignore')
    def test_short(self):
        sentence = '1234567890.1234567890。'
        out = spliter.cut_to_sentences(sentence)
        expect = ['1234567890.1234567890。']
        self.assertEqual(expect, out)

        sentence = '123。12354657789。 12324354364。'
        out = spliter.cut_to_sentences(sentence)
        expect = ['123。','12354657789。', ' 12324354364。']
        self.assertEqual(expect, out)

    def test_says(self):
        sentence = '“没走，在街上找了个客栈，闹出一场自尽的把戏，现在又上门来了。”她说'
        out = spliter.cut_to_sentences(sentence)
        expect = ['“没走，在街上找了个客栈，闹出一场自尽的把戏，现在又上门来了。”她说']
        self.assertEqual(expect, out)

    def test_empty(self):
        sentence = ''
        out = spliter.cut_to_sentences(sentence)
        expect = []
        self.assertEqual(expect, out)
    def test_long(self):
        de

if __name__ == '__main__':
    unittest.main()
