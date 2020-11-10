from flask import Flask, request, render_template, redirect, flash, jsonify, session
# from random import randint, choice, sample
from flask_debugtoolbar import DebugToolbarExtension
from surveys import personality_quiz as satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "12345"
debug = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

survey_quest = satisfaction_survey.questions
length = len(survey_quest)


@app.route('/')
def home_page():
   
    session.clear()
    session['answered'] = 0

    return render_template('home.html', satisfaction_survey=satisfaction_survey)


@app.route('/question/<q_num>')
def show_question(q_num):   
    q_num = int(q_num)
    print(session)
    sesh_num = session['answered']

    if sesh_num == len(survey_quest):
        flash("Survey already completed. You can go now!!!")
        return redirect('/thankyou')

    if q_num != sesh_num:
        flash("Invalid URL. You've been redirected to the next question")
        return redirect(f'/question/{sesh_num}')
    
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
    session['answered'] = session['answered'] + 1
    session[str(question_num)] = survey_quest[question_num].choices[answer]
    
    question_num += 1
    
    if question_num < length:
        return redirect(f'/question/{question_num}')
    else:
        return redirect('/thankyou')

@app.route('/thankyou')
def thankyou_page():
    #Need size, but as a 'str' to pull answer from 'would you use us again' question (changes html functionality)
    size = len(survey_quest)
    size = str(size-1)
    
    #Zip key/value pairs, with one as int and one as str to handle session data
    dict_keys = {}
    for i,j in zip(range(length), range(length)):
        dict_keys[str(i)] = j
    print(session)

    return render_template('thankyou.html', satisfaction_survey=satisfaction_survey, length=length, dict_keys=dict_keys, size=size)

