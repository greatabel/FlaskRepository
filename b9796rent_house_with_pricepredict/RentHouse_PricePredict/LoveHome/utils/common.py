# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

'''通用工具'''
from werkzeug.routing import BaseConverter
from LoveHome.utils.response_code import RET
from flask import jsonify, session, g
import functools


# 定义正则路由转换器
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


# 判断用户是否登录
def login_required(func):
    # 防止装饰器去修改函数的名字
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        user_id = session.get('user_id')
        if not user_id:
            return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')
        else:
            # 使用Fl量去存储用户的user_id,在执行具体的视图函数的时候就可以不用再去session中取user_id
            g.user_id = user_id
            return func(*args, **kwargs)

    return wrapper