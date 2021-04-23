# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

from . import api
from flask import session, current_app, jsonify, request, g
from LoveHome.models import User, House
from LoveHome.utils.response_code import RET
from LoveHome.utils.image_storage import upload_image
from LoveHome import db, constants
from LoveHome.utils.common import login_required


'''查询当前用户发布的所有房源'''
@api.route('/user/houses')
@login_required
def get_user_houses():
    try:
        houses = House.query.filter(House.user_id == g.user_id).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')
    house_dict_list = []
    for house in houses:
        house_dict_list.append(house.to_basic_dict())

    return jsonify(errno=RET.OK, errmsg='OK', data=house_dict_list)




'''获取用户实名认证信息'''
@api.route('/user/auth', methods=['GET'])
@login_required
def get_user_auth():
    # 1、查询当前用户的模型
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')

    if not user:
        return jsonify(errno=RET.NODATA, errmsg='用户不存在')

    resp = {
        'real_name': user.real_name,
        'id_card': user.id_card
    }
    return jsonify(errno=RET.OK, errmsg='OK', data=resp)



'''用户实名认证功能'''
@api.route('/user/auth', methods=['POST'])
@login_required
def set_user_auth():
    # 1、获取用户的数据，并判断参数是否有值
    data_dict = request.json
    real_name = data_dict.get('real_name')
    id_card = data_dict.get('id_card')

    # 2、判断参数是否有值
    if not all([real_name, id_card]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    # 3、查询当前用户的模型
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')

    if not user:
        return jsonify(errno=RET.NODATA, errmsg='用户不存在')

    # 4、更新模型
    user.real_name = real_name
    user.id_card = id_card

    # 5、保存数据到数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')

    return jsonify(errno=RET.OK, errmsg='保存成功')


'''修改用户名'''
@api.route('/user/name', methods=['POST'])
@login_required
def set_user_name():
    # 1、获取传过来的用户名，并判断是否有值
    user_name = request.json.get('name')
    if not user_name:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 2、查询到当前用户
    # user_id = session.get('user_id')
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据出错')

    if not user:
        return jsonify(errno=RET.NODATA, errmsg='当前用户不存在')

    # 3、更新当前登录用户的模型
    user.name = user_name

    # 4、保存数据到数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')
    # 更新session中保存的用户名
    session['name'] = user.name

    # 5、返回响应
    return jsonify(errno=RET.OK, errmsg='保存成功')


'''上传用户图像'''
@api.route('/user/head_image', methods=['POST'])
@login_required
def upload_userImage():
    # 1、获取到上传的头像
    try:
        avatar_data = request.files.get('avatar').read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg='读取文件失败')

    # 3、上传图片文件到七牛云
    try:
        key = upload_image(avatar_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传图片失败')

    # 4、如果上传成功，将头像保存到用户表中的头像字段
    # user_id = session.get('user_id')
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')

    if not user:
        return jsonify(errno=RET.NODATA, errmsg='用户不存在')

    # 赋值到用户模型
    user.avatar_url = key
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')

    # 5、返回响应，附带头像地址
    avatar_url = constants.QINIU_DOMIN_PREFIX + key
    return jsonify(errno=RET.OK, errmsg='上传成功', data={'avatar_url': avatar_url})


'''获取用户信息'''
@api.route('/user')
@login_required
def get_user_info():

    # 1、获取当前登录的用户ID
    # user_id = session.get('user_id')
    user_id = g.user_id
    # 2、查询出指定的用户信息
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')
    if not user:
        return jsonify(errno=RET.NODATA, errmsg='用户不存在')

    # 3、组织数据，进行返回
    return jsonify(errno=RET.OK, errmsg='OK', data=user.to_dict())


