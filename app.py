from flask import Flask, request, render_template, redirect, flash, jsonify
# from random import randint, choice, sample
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "12345"
debug = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

responses = []
question_num = 0

@app.route('/')
def home_page():
    return render_template('home.html', satisfaction_survey=satisfaction_survey)


@app.route('/question/<q_num>')
def show_question(q_num):
    q_num = int(q_num)
    question = satisfaction_survey.questions[q_num].question
    choices = satisfaction_survey.questions[q_num].choices
    length = len(choices)
    question_num += 1

    return render_template('question.html', question=question, q_num=q_num, choices=choices, length=length)

@app.route('/question/new', methods=["POST"])
def add_answer():
    answer = request.form['q_0_answer']
    responses[0] = answer
    return redirect('/question/1')

