from json import JSONDecoder

from flask import Flask, render_template, request, session

from forms import QuizzForm, SexForm, RegistrationQuizzForm
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oneblood.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


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

    def __eq__(self, other):
        if not isinstance(other, Quizz):
            return False
        return self.id == other.id

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
        list_quizz = Quizz.query.all()

        final_temp = 0
        session.pop('sex', None)

    return render_template('index.html', form=form, label=label)


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    form = RegistrationQuizzForm(request.form)
    return render_template('quizzes.html', form=form, quizzes=Quizz.query.all())


@app.route('/add', methods=['POST'])
def players():
    form = RegistrationQuizzForm(request.form)
    if request.method == "POST":
        q = Quizz(form.question.data, form.man_temp.data, form.woman_temp.data, form.status.data)
        db.session.add(q)
        db.session.commit()
    return render_template('quizzes.html', form=form, quizzes=Quizz.query.all())


@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    form = RegistrationQuizzForm(request.form)
    q = Quizz.query.filter(Quizz.id == id).first()
    current_db_sessions = db.object_session()
    current_db_sessions.delete(q)
    db.session.commit()
    # db.session.delete(q)
    # db.session.commit()
    return render_template('quizzes.html', form=form, quizzes=Quizz.query.all())


@app.route('/edit', methods=['GET'])
def edit():
    pass


if __name__ == '__main__':
    app.run(debug=True)
