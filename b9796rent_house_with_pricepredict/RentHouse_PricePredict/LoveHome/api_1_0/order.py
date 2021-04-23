# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'


from LoveHome.api_1_0 import api
from flask import request, jsonify, current_app, g
from LoveHome.utils.response_code import RET
import datetime
from LoveHome.models import Order, House
from LoveHome.utils.common import login_required
from LoveHome import db



'''订单评论功能'''
@api.route('/orders/<order_id>/comment', methods=['POST'])
@login_required
def set_orders_comment(order_id):
    # 获取参数
    comment = request.json.get('comment')

    if not comment:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    # 通过order_id查询出指定的订单
    try:
        order = Order.query.filter(Order.id == order_id, Order.status == 'WAIT_COMMENT', Order.user_id == g.user_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')

    if not order:
        return jsonify(errno=RET.NODATA, errmsg='未查询出对应的订单')
    # 设置订单状态
    order.status = 'COMPLETE'
    order.comment = comment

    # 保存订单
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='修改订单状态失败')

    return jsonify(errno=RET.OK, errmsg='OK')



'''设置订单的状态'''
@api.route('/orders/<order_id>', methods=['PUT'])
@login_required
def set_order_status(order_id):

    # 获取对应的响应事件
    action = request.args.get('action')
    if action not in ('accept', 'reject'):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 1、通过order_id找到对应的订单
    try:
        order = Order.query.filter(Order.id == order_id, Order.status == 'WAIT_ACCEPT').first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据错误')
    if not order:
        return jsonify(errno=RET.DBERR, errmsg='订单不存在')

    # 2、判断当前登录用户是否是该订单对应房屋的房东
    user_id = g.user_id
    # 去当前订单对应的房东ID
    landlord_id = order.house.user_id
    if user_id != landlord_id:
        return jsonify(errno=RET.ROLEERR, errmsg='不允许修改订单状态')

    # 3、修改订单状态
    if action == 'accept':
        order.status = 'WAIT_COMMENT'
    else:
        order.status = 'REJECTED'
        reason = request.json.get('reason')
        if not reason:
            return jsonify(errno=RET.PARAMERR, errmsg='请输入拒单的原因')
        # 设置拒单原因
        order.comment = reason

    # 4、更新数据库
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='修改订单状态失败')

    return jsonify(errno=RET.OK, errmsg='OK')


'''获取当前登录用户的所有订单'''
@api.route('/orders')
@login_required
def orders_list():
    user_id = g.user_id
    role = request.args.get('role')     # 如果 role=landlord 代表房东，否则是房客订单
    if not role:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    if role not in('landlord', 'custom'):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    try:
        if role == 'landlord':
            # 查询房东的所有订单
            pass
            houses = House.query.filter(House.user_id == user_id).all()
            # 获取房屋的id
            houses_id = [house.id for house in houses]
            orders = Order.query.filter(Order.house_id.in_(houses_id)).all()
        elif role == 'custom':
            # 查询房客的所有订单
            orders = Order.query.filter(Order.user_id == user_id).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')

    # 订单的字典列表
    order_dict_list = []
    for order in orders:
        order_dict_list.append(order.to_dict())

    return jsonify(errno=RET.OK, errmsg='OK', data=order_dict_list)
    pass


'''添加新订单功能'''
@api.route('/orders', methods=['POST'])
@login_required
def create_order():

    # 1、获取房屋的ID、入住开始时间和结束时间
    data_dict = request.json
    house_id = data_dict.get('house_id')
    start_date_str = data_dict.get('start_date')
    end_date_str = data_dict.get('end_date')

    # 2、对接收的参数进行校验
    if not all([house_id, start_date_str, end_date_str]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    # 判断参数
    try:
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
        if start_date and end_date:
            assert start_date < end_date, Exception('结束日期必须大于开始日期')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    # 判断房屋是否存在
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')

    if not house:
        return jsonify(errno=RET.NODATA, errmsg='未查询到房屋数据')

    # 3、判断当前房屋在当前时间段内是否被预定
    try:
        conflict_orders_list = Order.query.filter(end_date > Order.begin_date, start_date < Order.end_date, Order.house_id == house_id).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据错误')
    if conflict_orders_list:
        return jsonify(errno=RET.HOUSEBOOKED, errmsg='当前房屋已被预定')

    # 4、创建订单模型并设置数据
    order = Order()
    days = (end_date - start_date).days
    order.user_id = g.user_id
    order.house_id = house_id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = days
    order.house_price = house.price
    order.amount = days * order.house_price
    # 设置订单的房屋数量 + 1
    house.order_count += 1

    # 5、将数据添加到数据库中
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存订单失败')

    return jsonify(errno=RET.OK, errmsg='OK')
