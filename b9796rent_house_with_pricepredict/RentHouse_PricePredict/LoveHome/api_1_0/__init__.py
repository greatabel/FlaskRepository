# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

from flask import Blueprint

api = Blueprint('api_1_0', __name__)

from . import index, verify, passport, profile, house, order, predict_train, predict_realdata