# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

# 为具体的HTML文件请求提供路由
from flask import Blueprint, current_app, make_response
from flask_wtf.csrf import generate_csrf

html = Blueprint('html', __name__)

@html.route('/<re(".*"):file_name>')
def get_html_file(file_name):

    if not file_name:
        file_name = 'index.html'

    # 判断是否是图标，如果不是图标，拼接HTML
    if file_name != 'favicon.ico':
        file_name = 'html/' + file_name

    # send_static_file: 通过指定的文件名找到指定的静态文件并封装成响应
    response = make_response(current_app.send_static_file(file_name))
    # 生成 csrf_token 的值
    csrf_token = generate_csrf()
    # 设置 csrf_token
    response.set_cookie('csrf_token', csrf_token)
    return response


