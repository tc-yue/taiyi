from whoosh.analysis import StopFilter
from whoosh.analysis import Tokenizer, Token
import jieba
import re
import pickle
import os

patha = os.path.abspath(os.path.dirname(__file__)+os.path.sep+os.pardir)
with open(patha+'/files/dic/stops.pkl', 'rb')as f:
    stop_list = pickle.load(f)
STOP_WORDS = set(stop_list)

accepted_chars = re.compile(r"[\u4E00-\u9FD5]+")


class ChineseTokenizer(Tokenizer):

    def __call__(self, text, **kargs):
        # mode = search ?
        words = jieba.tokenize(text)
        token = Token()
        for (w, start_pos, stop_pos) in words:
            if not accepted_chars.match(w) and len(w) <= 1:
                continue
            token.original = token.text = w
            token.pos = start_pos
            token.startchar = start_pos
            token.endchar = stop_pos
            yield token


def ChineseAnalyzer(stoplist=STOP_WORDS, minsize=1):
    return ChineseTokenizer() | StopFilter(stoplist=stoplist, minsize=minsize)
