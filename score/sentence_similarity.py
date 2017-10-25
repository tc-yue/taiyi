"""
合工大 问句相似度研究算法实现
"""
from model.questiontype import QuestionType
from score.word_similarity import WordSimilarity
import logging
from gensim.models import Word2Vec
import os
logging.info('加载词向量')
model = Word2Vec.load(os.path.abspath(os.path.dirname(__file__)+os.path.sep+os.pardir)+'/score/medicine.model')
logging.info('加载完毕')


class SentenceSimilarity:
    def __init__(self):
        # 初始化评分权重
        self.__scores = 0.0
        self.__syntax_scores = 0.0
        self.__order_weight = 0.3
        self.__word_weight = 0.7
        # 本实验暂不考虑问题类别特征
        self.__class_weight = 0.0
        self.__key_weight = 0.4
        self.__syntax_weight = 0.1
        self.__semantic_weight = 0.5
        self.word_similar = WordSimilarity()

    def set_score_weight(self, weight_list):
        self.__syntax_scores = weight_list[0]

    def get_score(self):
        return self.__scores

    def class_sim(self, question_type1, question_type2):
        """
        问句类型相似度
        """
        if question_type1 == question_type2:
            score = 1
        elif question_type1 is QuestionType.Solution or question_type2 is QuestionType.Solution:
            score = 0.5
        else:
            score = 0
        self.__scores += self.__class_weight * score

    def word_sim(self, question1, question2):
        """
        词形相似度，用两个问句中含有共同词的个数来衡量，
        如果出现次数不同以出现少的数目为准
        :param question1: 问题的分词list
        """
        intersection_words = [w for w in question1 if w in question2]
        same_count = 0
        for i in intersection_words:
            a = question1.count(i)
            b = question2.count(i)
            if a >= b:
                same_count += b
            else:
                same_count += a
        score = 2*same_count/(len(question1)+len(question2))
        self.__syntax_scores += self.__word_weight * score
        logging.info('词形相似度结束')

    def order_sim(self, question1, question2):
        """
        词序相似度，用两个问句中词语的位置关系的相似程度
        :param question1: 问题的分词list
        """
        intersection_words = [w for w in question1 if w in question2
                              and question1.count(w) == 1 and question2.count(w) == 1]
        if len(intersection_words) <= 1:
            score = 0
        else:
            pfirst = sorted([question1.index(i) for i in intersection_words])
            psecond = [question2.index(question1[i]) for i in pfirst]
            count = 0
            for i in range(len(psecond)-1):
                if psecond[i] < psecond[i+1]:
                    count += 1
            score = 1 - count/(len(intersection_words)-1)
        self.__syntax_scores += self.__order_weight * score
        logging.info('词序相似度结束')

    def wmd_sim(self, question1, question2):
        """
        :param model:w2v 词向量
        :param question1: 句子
        :return: 分数
        """
        logging.info('wmd start')
        self.__scores += self.__semantic_weight * model.wmdistance(question1, question2)
        logging.info('wmd ok')

    def semantic_sim(self, question1, question2):
        """
        语义方法
        question1中每个词与2中每个词最相似
        :param question1: 问题list
        """
        n = len(question1)
        score1 = 0.0
        for i in question1:
            word_sim_list = []
            # 平均时间3s
            for j in question2:
                word_sim_list.append(self.word_similar.get_similarity(i, j))
            score1 += max(word_sim_list)
        # score2 = 0.0
        # for j in range(m):
        #     score2 += max(self.word_similar.get_similarity(question1[i], question2[j]) for i in range(n))
        # score2 /= (2*n)
        self.word_similar.close_db()
        self.__scores += self.__semantic_weight * score1/n
        logging.info('语义相似度结束')

    def key_sim(self, question_a, question_b):
        """
        关键词相似度
        :param question_a: 问题类
        """
        keya = question_a.get_disease()
        keyb = question_b.get_disease()
        score = 0
        for i in keya:
            if i in keyb:
                score += 1
        if len(keya) > 0:
            self.__scores += self.__key_weight * score * 2/ (len(keya)+len(keyb))
        logging.info('关键词相似度结束')

    def combination_sim(self, question_a, question_b):
        """
        :param question_a: 问题类
        """
        logging.info('句子相似度开始')
        question1 = question_a.get_words()
        question2 = question_b.get_words()
        # self.class_sim(question_type1,question_type2)
        self.key_sim(question_a, question_b)
        self.wmd_sim(' '.join(question1),' '.join(question2))
        # self.semantic_sim(question1, question2)
        self.word_sim(question1, question2)
        self.order_sim(question1, question2)
        self.__scores += self.__syntax_scores * self.__syntax_weight
        logging.info('句子相似度结束,得分为' + question_b.get_question()+ str(self.__scores))


if __name__ == '__main__':
    ss = SentenceSimilarity()
    # ss.combination_sim()

