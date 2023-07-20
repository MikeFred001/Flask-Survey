from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.get('/')
def display_survey_start():
    """Displays survey start page when user reaches root of site"""

    title = survey.title
    instructions = survey.instructions

    return render_template(
        "survey_start.html",
        title=title,
        instructions=instructions)


@app.post('/begin')
def redirect_to_first_question():
     return redirect('/questions/0')



@app.get('/questions/<int:id>')
def show_next_question(id):
    question = survey.questions[id].prompt
    choices = survey.questions[id].choices

    return render_template(
        "question.html",
        question=question,
        choices=choices,
        id=id)


@app.post('/answer/<int:id>')
def redirect_to_next_question(id):
     id += 1
     responses.append(request.args["answer"])
     return redirect(f'/questions/{id}')