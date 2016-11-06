from json import JSONDecoder

from flask import Flask, render_template, request, session

from forms import QuizzForm, SexForm, RegistrationQuizzForm
from flask_sqlalchemy import SQLAlchemy

import models

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oneblood.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

list_quizz = []
current_quizz = None
final_temp = 0


@app.route('/', methods=['post', 'get'])
def index():
    global list_quizz, current_quizz, final_temp

    if request.method == 'POST':
        if not list_quizz:
            return render_template('index.html', temp=final_temp)

        form = QuizzForm()

        if 'sex' not in session:
            session['sex'] = form.opt.data
            current_quizz = list_quizz.pop()
            label = current_quizz.question
            return render_template('index.html', form=form, label=label)

        if bool(form.opt.data):
            app.logger.info(form.opt.data)
            if session['sex'] == 0:
                t = current_quizz.woman_temp
            else:
                t = current_quizz.man_temp
            if t == -1 or t > final_temp:
                final_temp = t

        while True:
            if not list_quizz:
                return render_template('index.html', temp=final_temp)
            current_quizz = list_quizz.pop()
            label = current_quizz.question
            if current_quizz.status != session['sex'] and current_quizz.status != 2:
                continue
            else:
                break
    else:
        app.logger.info('Index page')

        form = SexForm()
        label = form.opt.label
        list_quizz = models.Quizz.query.all()

        final_temp = 0
        session.pop('sex', None)

    return render_template('index.html', form=form, label=label)


@app.route('/add', methods=['post', 'get'])
def players():
    form = RegistrationQuizzForm(request.form)
    if request.method == "POST":
        q = models.Quizz(form.question.data, form.man_temp.data, form.woman_temp.data, form.status.data)
        db.session.add(q)
        db.session.commit()
    return render_template('quizzes.html', form=form, quizzes=models.Quizz.query.all())


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    form = RegistrationQuizzForm(request.form)

    if request.method == "POST":
        id = int(request.form['id'])
        db.session.delete(models.Quizz.query.get(id))
        db.session.commit()
    return render_template('quizzes.html', form=form, quizzes=models.Quizz.query.all())


if __name__ == '__main__':
    app.run(debug=True)
