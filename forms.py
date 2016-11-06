#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://stackoverflow.com/questions/21129020/how-to-fix-unicodedecodeerror-ascii-codec-cant-decode-byte
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import RadioField, StringField, IntegerField

import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class QuizzForm(FlaskForm):
    opt = RadioField('Escolha', choices=[(True, 'Sim'), (False, 'Não')])


class SexForm(FlaskForm):
    opt = RadioField('Qual seu sexo?', choices=[(0, 'Feminino'), (1, 'Masculino')])


class RegistrationQuizzForm(FlaskForm):
    question = StringField('Questão', [validators.Length(min=4, max=800)])
    man_temp = IntegerField('Tempo para o homem')
    woman_temp = IntegerField('Tempo para a mulher')
    status = RadioField('Para quem é a pergunta?', choices=[(0, 'Mulher'), (1, 'Homem'), (2, 'Ambos')])
