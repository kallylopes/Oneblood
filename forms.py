#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://stackoverflow.com/questions/21129020/how-to-fix-unicodedecodeerror-ascii-codec-cant-decode-byte
from flask_wtf import Form
from wtforms import validators
from wtforms.fields import RadioField, StringField, IntegerField

import sys

import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class QuizzForm(Form):
    opt = RadioField('Escolha', choices=[(True, 'Sim'), (False, 'Não')])


class SexForm(Form):
    opt = RadioField('Escolha', choices=[(0, 'Feminino'), (1, 'Masculino')])


class RegistrationQuizzForm(Form):
    question = StringField('Question', [validators.Length(min=4, max=800)])
    man_temp = IntegerField('Man Temp')
    woman_temp = IntegerField('Women Temp')
    status = IntegerField('Status')
