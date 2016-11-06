from json import JSONDecoder

from flask import Flask, render_template, request, session

from forms import QuizzForm, SexForm, RegistrationQuizzForm
from flask_sqlalchemy import SQLAlchemy

import logging
import json


app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oneblood.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

list_quizz = []
current_quizz = None


class Quizz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(800))
    man_temp = db.Column(db.Integer)
    woman_temp = db.Column(db.Integer)
    status = db.Column(db.Integer)

    def __init__(self, question, man_temp, woman_temp, status):
        self.question = question.encode('utf8')
        self.man_temp = man_temp
        self.woman_temp = woman_temp
        self.status = status

    def __repr__(self):
        obj_json = '{"question": %r }' % self.question
        return json.dumps(obj_json)

    def __eq__(self, other):
        if not isinstance(other, Quizz):
            return False
        return self.id == other.id


@app.route('/', methods=['post', 'get'])
def index():
    global list_quizz, current_quizz
    if request.method == 'POST':
        if len(list_quizz) == 0:
            return render_template('index.html', temp=session['final_temp'])

        form = QuizzForm()

        if 'sex' not in session:
            session['sex'] = form.opt.data
            app.logger.info('Sex {}'.format(session['sex']))

            # session['current_quizz'] = list_quizz.pop()
            current_quizz = list_quizz.pop()
            # app.logger.info(session['current_quizz'])

            label = current_quizz.question # session['current_quizz'].question
            app.logger.info(label)

        elif form.opt.data:
            if session['sex'] == 0:
                # t = session['current_quizz'].woman_temp
                t = current_quizz.woman_temp
            else:
                # t = session['current_quizz'].man_temp
                t = current_quizz
            if t == -1 or t > session['final_temp']:
                session['final_temp'] = t

            while True:
                if len(list_quizz) == 0:
                    return render_template('index.html', temp=session['final_temp'])
                current_quizz = list_quizz.pop()
                label = current_quizz.question
                if current_quizz.status != session['sex']:
                    continue
    else:
        app.logger.info('Index page')

        form = SexForm()
        label = form.opt.label
        list_quizz = Quizz.query.all()

        session['final_temp'] = 0
        session.pop('final_temp', None)
        # session.pop('current_quizz', None)
        session.pop('sex', None)

    return render_template('index.html', form=form, label=label)


@app.route('/add', methods=['post', 'get'])
def players():
    form = RegistrationQuizzForm(request.form)
    if request.method == "POST":
        q = Quizz(form.question.data, form.man_temp.data, form.woman_temp.data, form.status.data)
        db.session.add(q)
        db.session.commit()
    return render_template('quizzes.html', form=form, quizzes=Quizz.query.all())


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    form = RegistrationQuizzForm(request.form)

    if request.method == "POST":
        id = int(request.form['id'])
        db.session.delete(Quizz.query.get(id))
        db.session.commit()
    return render_template('quizzes.html', form=form, quizzes=Quizz.query.all())


if __name__ == '__main__':
    app.run(debug=True)
