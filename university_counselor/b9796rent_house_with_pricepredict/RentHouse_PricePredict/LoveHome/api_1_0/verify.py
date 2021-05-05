# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

# 图片验证码和短信验证码的处理
from . import api
from LoveHome.utils.captcha.captcha import captcha
from flask import request, jsonify, make_response, abort, current_app, json
from LoveHome import redis_store, constants
from LoveHome.utils.response_code import RET
import re, random
from LoveHome.utils.sms import CCP


'''短信验证码视图函数'''
@api.route('/sms_code', methods=['POST'])
def send_sms_code():
    # 1、接收前端发送到后端的参数：手机号，用户图片验证码的内容，图片验证码的编号
    # JSON字符串
    json_data = request.data
    # 转字典
    json_dict = json.loads(json_data)
    # 取出字典中的值
    mobile = json_dict.get('mobile')
    image_code = json_dict.get('image_code')
    imageCode_id = json_dict.get('imageCode_id')

    # 2、判断参数是否有值并进行校验
    if not all([mobile, image_code, imageCode_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    # 对手机号码进行判断
    if not re.match('^1[34578][0-9]{9}', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号有误，请重新输入')

    # 3、从redis中取出正确的图片验证码（如果没有取到，代表验证码已经过期）
    try:
        real_image_code = redis_store.get('ImageCode:'+imageCode_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询验证码出错')

    # 如果没有取到，代表验证码已经过期了
    if not real_image_code:
        return jsonify(errno=RET.NODATA, errmsg='验证码已过期，请重新发送')

    # 4、用接收前端的图片验证码和后端存储的进行比对
    if image_code.lower() != real_image_code.lower():
        return jsonify(errno=RET.DATAERR, errmsg='验证码输入不正确')

    # 5、如果前后的验证码比对一致，则可以发送短信验证码
    # 生成短信验证码
    sms_code = '%06d' % random.randint(0, 999999)
    current_app.logger.debug('短信验证码为：'+ sms_code)
    # 发送短信验证码测试
    # # 6、发送短信验证码
    # result = CCP().send_templates_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES/60], '1')
    # if result != 1:
    #     # 发送失败
    #     return jsonify(errno=RET.THIRDERR, errmsg='发送短信失败')

    # 7、短信发送成功，保存到redis中
    try:
        redis_store.set('Mobile' + mobile, sms_code, constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存验证码失败')

    # 8、通知前端短信验证码发送成功
    return jsonify(errno=RET.OK, errmsg='短信验证码发送成功')



'''图片验证码的视图函数'''
@api.route('/image_code')
def get_image_code():
    # 1、取到图片验证码编码
    cur_id = request.args.get('cur_id')
    pre_id = request.args.get('pre_id')

    if not cur_id:
        abort(403)

    # 2、生成图片验证码
    name, text, image = captcha.generate_captcha()
    current_app.logger.debug('图片验证码为：'+text)
    # 3、将图片验证码的内容通过图片编码保存到redis中
    try:
        redis_store.set('ImageCode:'+cur_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
        if pre_id:
            redis_store.delete('ImageCode:'+pre_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='存储图片验证码数据失败')
    # 返回图片验证码的图片
    response = make_response(image)
    # 设置响应的内容类型
    response.headers['Content-Type'] = 'image/jpg'
    return response