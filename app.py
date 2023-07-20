from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)



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
def reset_and_start_survey():
    """Clears current list of responses and directs user to first
    survey question
    """

    session['responses'] = []
    return redirect('/questions/0')


@app.get('/questions/<int:id>')
def show_next_question(id):
    """Renders survey question at #id"""

    responses = session['responses']

    if not ( id == len(responses)):
        print(f'\n\n***Redirecting*** Responses: {len(responses)} ID:{id}\n')
        return redirect(f'/questions/{len(responses)}')

    question = survey.questions[id].prompt
    choices = survey.questions[id].choices

    return render_template(
        "question.html",
        question=question,
        choices=choices,
        id=id)


@app.post('/answer/<int:id>')
def save_answer_and_advance(id):
    """Save user answer to responses list. Direct user to the next question
    or completion page if survey is complete"""

    responses = session['responses']
    responses.append(request.form["answer"])
    session['responses'] = responses


    id += 1
    if id >= len(survey.questions):
        return redirect('/completion')

    return redirect(f'/questions/{id}')


@app.get('/completion')
def display_thank_you():
    """Displays thank you page and survey overview"""

    questions = survey.questions
    answers = session['responses']

    return render_template(
        'completion.html',
        questions = questions,
        answers = answers
        )