import os
import sqlite3
from collections import Counter
import logging
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, OrGroup
from model.evidence import Evidence
from model.question import Question


class DataSource:

    @staticmethod
    def index2_open(word):
        results_list = []
        ix = open_dir(os.path.abspath(os.path.dirname(__file__)+os.path.sep+os.pardir)+'/evidence_retrieval/indexer2')
        conn = sqlite3.connect(os.path.abspath(os.path.dirname(__file__)+os.path.sep+os.pardir)+'/evidence_retrieval/qapairs.db')
        cursor1 = conn.cursor()
        with ix.searcher() as search:
            # or query 调整共现 与 高单出现 评分
            og = OrGroup.factory(0.9)
            # search 多field
            parser = MultifieldParser(['title', 'content'], schema=ix.schema, group=og).parse(word)
            # w_parser = MultifieldParser(['title', 'content'], schema=ix.schema).parse(word)
            logging.info(parser)
            # 最多5个结果
            results = search.search(parser, limit=5)
            # 每个结果最多300个字符
            # results.fragmenter.charlimit = 200
            for hit in results:
                i = hit['id']
                cursor1.execute("select * from QAPAIRS WHERE ID = ?", (i,))
                values = cursor1.fetchall()[0]
                print(values)
                results_list.append((values[2], values[1]))
        cursor1.close()
        conn.commit()
        conn.close()
        return results_list

    @staticmethod
    def search_evidence(query):
        evidences = []
        elements = DataSource.index2_open(query)
        for item in elements:
            evidence = Evidence()
            evidence.set_title(item[0])
            evidence.set_snippet(item[1])
            evidences.append(evidence)
        return evidences

    @staticmethod
    def get_evidence(question):
        logging.info('获取支持证据开始')
        question_str = question.get_question()
        evidences = DataSource.search_evidence(question_str)
        question.add_evidences(evidences)
        logging.info('获取支持证据结束')
        return question

    @staticmethod
    def select_medicine(question):
        # todo 候选答案 代入检索进行再评分
        logging.info('数据库查询开始')
        conn = sqlite3.connect(os.path.dirname(__file__)+'/medicine.db')
        cursor = conn.cursor()
        medicine_list = []
        disease_list = question.get_disease()
        for i in disease_list:
            cursor.execute("select NAME from MEDICINE where INDICATIONS like ?", ['%'+i+'%'])
            values = cursor.fetchall()
            medicine_list += [item[0] for item in values]
        top_list = Counter(medicine_list).most_common(3)
        question.set_expect_answer(' '.join([i[0] for i in top_list]))
        cursor.close()
        conn.commit()
        conn.close()
        logging.info('数据库查询结束')
        return question


if __name__ == '__main__':
    a = Question()
    a.set_question('刷牙后出血怎么办')
    b = DataSource.get_evidence(a)
