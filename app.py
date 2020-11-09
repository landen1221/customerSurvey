from flask import Flask, request, render_template, redirect, flash, jsonify
# from random import randint, choice, sample
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "12345"
debug = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

responses = {}
survey_quest = satisfaction_survey.questions

@app.route('/')
def home_page():
    global responses 
    responses = {}
    return render_template('home.html', satisfaction_survey=satisfaction_survey)


@app.route('/question/<q_num>')
def show_question(q_num):
    q_num = int(q_num)
    

    if len(responses) == len(survey_quest):
        flash("Survey already completed. You can go now!!!")
        return redirect('/thankyou')

    if q_num != len(responses):
        flash("Invalid URL. You've been redirected to the next question")
        return redirect(f'/question/{len(responses)}')
    
    question = survey_quest[q_num].question
    choices = survey_quest[q_num].choices
    length = len(choices)
    global question_num
    question_num = q_num

    return render_template('question.html', question=question, q_num=q_num, choices=choices, length=length)

@app.route('/question/new', methods=["POST"])
def add_answer():
    global question_num
    answer = int(request.form[f'q_{question_num}_answer'])
    responses[question_num] = survey_quest[question_num].choices[answer]
    question_num += 1
    length = len(survey_quest)
    if question_num < length:
        return redirect(f'/question/{question_num}')
    else:
        return redirect('/thankyou')

@app.route('/thankyou')
def thankyou_page():

    return render_template('thankyou.html', responses=responses, satisfaction_survey=satisfaction_survey)

