#!/usr/bin/python
# -- coding: utf-8 --
import traceback

from os import environ
import math
from flask import request, Flask, render_template
# import time
import re
import json
import io
import random
from game.fly import *
from game.train import *
from game.connect import *
from utils.utils import *

app = Flask(__name__)
app.debug = True


#初始管道数据
@app.route("/h", methods=['POST'])
def h():
    group_id = request.form.get('group_id')
    user_id = request.form.get('user_id', type=int)
    print(user_id, type(user_id), '*'*20)
    divide_userid = user_id//5
    group_list = group_list_Arr[divide_userid]
    return str(group_list.groups[int(group_id)].randomh)

#分组
@app.route("/gp", methods=['POST'])
def gp():
    #获取参数
    user_id = request.form.get('user_id', type=int)
    print(user_id, type(user_id), '*'*20)
    divide_userid = user_id//5
    print('len(Con_Arr)=', len(Con_Arr), 'divide_userid=',divide_userid)
    Con = Con_Arr[divide_userid]

    g,b = Con.getbird_id(user_id%5)
    print('in /gp', g, b, '-'*20)
    return str([g,b])

#匹配
@app.route("/pp", methods=['POST'])
def pp():
    #获取参数
    group_id = request.form.get('group_id')
    print('in /pp group_id=', group_id)

    user_id = request.form.get('user_id', type=int)
    print(user_id, type(user_id), '*'*20)
    divide_userid = user_id//5
    Con = Con_Arr[divide_userid]

    if Con.wait_con(int(group_id)):
        return "true"
    return "false"

#页面
@app.route("/")
def index():
    return render_template('index.html')

#画面数据
@app.route("/img", methods=['POST'])
def img():
    # 获取上传base64图片
    base64_data = request.form.get('base64')
    bird_id = request.form.get('bird_id')
    group_id = request.form.get('group_id')
    die_id = request.form.get('die_id')
    bird_id = int(bird_id)
    group_id = int(group_id)
    die_id = int(die_id)

    user_id = request.form.get('user_id', type=int)
    if user_id is None:
        print('user_id should not be None')
        user_id = 0
    print(user_id, type(user_id), '*'*20)
    divide_userid = user_id//5
    print('divide_userid=', divide_userid, 'group_id=', group_id, 'die_id=', die_id)
    group_list = group_list_Arr[divide_userid]
    try:

        if die_id==6:
            base64_data=base64_data.replace(" ","+").replace("data:image/jpeg;base64,","")
            target = basetoimg(base64_data)
            action = group_list.groups[group_id].model[bird_id].detect(target)
            group_list.groups[group_id].action[bird_id][1] = action[1]
        else:
            group_list.groups[group_id].action[die_id][0] = 1
            group_list.groups[group_id].die_temp +=1
            group_list.groups[group_id].isdie = True 

        group_list.groups[group_id].visit += 1
        if group_list.groups[group_id].visit == group_list.groups[group_id].real-group_list.groups[group_id].die:#控制访问
            group_list.groups[group_id]._refresh()#更新柱子参数
            for i in range(5-group_list.groups[group_id].real):#机器人
                live,ac = group_list.groups[group_id].robmodel[i].detect(group_list.groups[group_id].action[5])
                group_list.groups[group_id].action[-i-2][0] = live
                group_list.groups[group_id].action[-i-2][1] = ac
            group_list.groups[group_id].visit = 0 #重置访问数量
            group_list.groups[group_id].isok = [True,True,True,True,True] #开放统一获取action
        return '1'
    except Exception:
        traceback.print_exc()

#同步获取动作
@app.route("/getact", methods=['POST'])
def getact():
    # 获取上传base64图片
    group_id = request.form.get('group_id')
    bird_id = request.form.get('bird_id')
    group_id = int(group_id)
    bird_id = int(bird_id)

    user_id = request.form.get('user_id', type=int)
    # print(user_id, type(user_id), '*'*20)
    divide_userid = user_id//5


    group_list = group_list_Arr[divide_userid]
    # if group_list.groups == 0:
    #     group_list = group_list()
    #     Con = Connect(group_list)
    #     if divide_userid <= len(group_list_Arr):
    #         group_list_Arr[divide_userid] = group_list
    #         Con_Arr[divide_userid] = Con
    #         Con.wait_con(int(group_id))

    print('divide_userid=', divide_userid, 'group_id=',group_id, 'bird_id=', bird_id,
        'len(group_list.groups)=', len(group_list.groups), ' _ in getact')
    # print('group_list.groups[group_id].isok[bird_id]=', group_list.groups[group_id].isok[bird_id])
    # print(group_id, group_list.groups[group_id].isok, bird_id)
    if len(group_list.groups) > 0:
        if  group_list.groups[group_id].isok[bird_id]:
            group_list.groups[group_id].isok[bird_id] = False
            return str(group_list.groups[group_id].action)
    else:
            
        randomh = [random.randint(12, 20),random.randint(12, 20) ,random.randint(12, 20)]
        myaction =  [[0,0],[0,0],[0,0],[0,0],[0,0], randomh]
        return str(myaction)

    return "false"

@app.route("/abel_refresh", methods=['POST'])
def abel_refresh():
    print('abel_refresh')


    user_id = request.form.get('user_id', type=int)
    print(user_id, type(user_id), '*'*20)
    divide_userid = user_id//5


    # Tmodel.abel_close()

    # #初始化训练模型
    # Tmodel = TrainNetwork()
    #初始化训练模型
    # model = Detect("saved_networks/")
    #初始化对战组
    group_list = Group_list()
    #初始化连接器
    Con = Connect(group_list)
    if divide_userid <= len(group_list_Arr):
        group_list_Arr[divide_userid] = group_list
        Con_Arr[divide_userid] = Con
        Con.wait_con(0)
    return str([])

#训练
# @app.route("/trainhtml")
# def html():
#     return render_template('train.html')

#获取训练数据
# @app.route("/train", methods=['POST'])
# def t():
#     # 获取上传base64图片
#     base64_data = request.form.get('base64')
#     reward =request.form.get('reward')
#     print(reward)
#     base64_data=base64_data.replace(" ","+").replace("data:image/jpeg;base64,","")
#     target = basetoimg(base64_data)
#     action = Tmodel.train(target,float(reward))
#     return str([[0,action[1]],[0,1],[0,0],[0,1],[0,0],[random.randint(12, 20) ,random.randint(12, 20) ,random.randint(12, 20) ]])


# group_list = None
# Con = None


global group_list_Arr, Con_Arr
group_list_Arr = []
Con_Arr = []
max_user_num = environ.get('SupportUserMaxNumber', 10)


def create_related_sessions(max_user_num):
    c = max_user_num / 5
    n = math.ceil(c)
    for i in range(n):
        print(i)
        #初始化训练模型
        # model = Detect("saved_networks/")
        #初始化对战组
        group_list = Group_list()
        #初始化连接器
        Con = Connect(group_list)
        group_list_Arr.append(group_list)
        Con_Arr.append(Con)


if __name__ == "__main__":
    #初始化训练模型
    # Tmodel = TrainNetwork()

    #初始化训练模型
    # model = Detect("saved_networks/")
    #初始化对战组
    # group_list = Group_list()
    # #初始化连接器
    # Con = Connect(group_list)
    create_related_sessions(max_user_num)

    app.run(host="0.0.0.0", port=80)
