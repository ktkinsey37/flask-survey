from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a'

responses = []
index = 0

survey = surveys["satisfaction"]
# surveys should not be hard coded in

@app.route('/')
def homepage():
    return render_template('start.html', survey=survey)

@app.route('/questions/<index>')
def question_page(index):
    index = int(index)
    response_index = len(responses)
    if index != response_index:
        flash("UH OH! THERE WAS AN ERROR, RETURNING YOU TO THE QUESTION YOU WERE ON")
        return redirect(f'/questions/{response_index}')
    return render_template('questions.html', index=index, survey=survey, responses=responses)

@app.route('/answers', methods=["POST"]) #how to pass index along with the post that sends the answer?
def handle_answer_question():
    answer = request.form["answer"]
    responses.append(answer)
    index = len(responses)
    if index >= len(survey.questions):
        return redirect('/thank-you')
    return redirect(f'/questions/{index}')

@app.route('/error')
def handle_error():
    index = len(responses)
    return render_template('questions.html', index=index, survey=survey, responses=responses)

@app.route('/thank-you')
def thank_you():
    responses.clear()
    print(responses)
    return render_template('thank-you.html')