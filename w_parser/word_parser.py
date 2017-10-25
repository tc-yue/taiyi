import jieba
import jieba.posseg
import os
import pickle


class WordParser:
    path = os.path.abspath(os.path.dirname(__file__)+os.path.sep+os.pardir)
    jieba.load_userdict(path + '/files/dic/jieba_pos.txt')
    # 停用词
    with open(path+'/files/dic/stops.pkl', 'rb')as f:
        stop_list = pickle.load(f)

    @staticmethod
    def parse(sentence):
        """
        分词和词性标注
        :param sentence:句子 字符串
        :return: 包含分词和词性标注tuple 的list
        """
        return [tuple(item) for item in jieba.posseg.lcut(sentence)]

    @staticmethod
    def lcut(sentence):
        pre = jieba.lcut(sentence)
        return [i for i in pre if i not in WordParser.stop_list]


if __name__ == '__main__':
    for j in WordParser.parse('腹泻很严重0，止泻利颗粒不管用，还有什么药'):
        print(j)
    for j in WordParser.lcut('您好，早上起来腹泻很严重0，吃阿司匹林还是什么药'):
        print(j)
