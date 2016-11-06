from oneblood import db


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