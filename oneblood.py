from flask import Flask, render_template, request

from forms import QuizzForm, SexForm, RegistrationQuizzForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/gabriela/Documents/developer/kally-quiz/Oneblood/oneblood.db'
db = SQLAlchemy(app)
temp_final = 0
quizz = []

class Quizz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(800))
    man_temp = db.Column(db.Integer)
    woman_temp = db.Column(db.Integer)

    def __init__(self, question, man_temp, woman_temp):
        self.question = question
        self.man_temp = man_temp
        self.woman_temp = woman_temp

    def __repr__(self):
        return '<Quizz %r>' % self.question

    def __eq__(self, other):
        if not isinstance(other, Quizz):
            return False
        return self.id == other.id


@app.route('/', methods=['post', 'get'])
def index():
    global temp_final, quizz
    if request.method == 'POST':
        if not quizz:
            return render_template('index.html', temp=temp_final)
        current_question = quizz.pop()
        sex = ''
        form = QuizzForm()
        if form.validate_on_submit():
            # verificar se foi SIM
            if form.opt.data:
                # t = -1
                # temp_final = 9
                if sex == 'feminino':
                    t = current_question.woman_temp
                else:
                    t = current_question.man_temp
                if t == -1 or t > temp_final:
                    temp_final = t
        else:
            error = form.errors
    else:
        quizz = Quizz.query.all()
        form = SexForm()
    return render_template('index.html', form=form)


@app.route('/add', methods=['post', 'get'])
def players():
    form = RegistrationQuizzForm(request.form)
    if request.method == "POST" and form.validate():
        q = Quizz(form.question.data, form.man_temp.data, form.woman_temp.data)
        db.session.add(q)
        db.session.commit()
    return render_template('add_question.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
