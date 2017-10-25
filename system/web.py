# -*-coding:utf-8 -*-
from flask import Flask, request, render_template
from system.question_answering_system import QuestionAnsweringSystem

app = Flask(__name__)


@app.route('/chat', methods=['GET'])
def home():
    return render_template('form3.html')


@app.route('/chat', methods=['POST'])
def chat():
    sentence = qa.answer_question(request.form['word'])
    return sentence

if __name__ == '__main__':
    qa = QuestionAnsweringSystem()
    app.run()
