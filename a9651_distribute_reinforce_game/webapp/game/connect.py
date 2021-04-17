#!/usr/bin/python
# -- coding: utf-8 --
import os
import time 
from game.fly import *
from game.robot import *

class Group_list():
    def __init__(self):
        self.groups = []

class Group():
    def __init__(self):
        self.birds = [] #连接的小鸟id列表
        self.model = [] #模型列表
        self.robmodel = []#机器人列表
        self.ready = False #对局加载
        self.randomh = [random.randint(12, 20),random.randint(12, 20) ,random.randint(12, 20)]
        self.action = [[0,0],[0,0],[0,0],[0,0],[0,0],self.randomh]
        self.num = 0 #访问的小鸟数量
        #同步参数
        self.visit = 0
        self.isok = [False,False,False,False,False]
        #死亡数量
        self.die = 0
        self.die_temp = 0
        self.isdie = False
        #超时相关
        self.timec = 0 # 初始时间
        self.timeout=True
        self.real = 0#真实的小鸟数量


    def _refresh(self):
        self.num += 1
        if self.num == 100:
            self.action[5] = [random.randint(12, 20),random.randint(12, 20) ,random.randint(12, 20)]
            self.num = 0
        if self.isdie:
            self.die += self.die_temp
            self.die_temp = 0
            self.isdie = False

    def _init_model(self):
        bo = os.listdir("user/")
        self.real = len(self.birds)
        for i in self.birds:
            bo.remove(str(i))
            self.model.append(Detect("user/"+str(i)))
        for i in range(5-self.real):
            self.robmodel.append(RobotDetect("user/"+bo[random.randint(0,len(bo)-1)]+"/",self.randomh))

        self.ready = True #对局加载

class Connect():
    def __init__(self,group_list):
        self.cnum = 0 # 小鸟id列表
        self.gnum = 0 # 分组id
        self.group = Group() #一个组
        self.group_list = group_list.groups #分组列表

    def getbird_id(self,user_id):#获取小鸟id
        if not user_id in self.group.birds:
            if self.cnum == 0 :
                self.group_list.append(self.group)
                # 等待时间 修改为2
                self.group_list[self.gnum].timec = int(time.time())+0.1
            self.group_list[self.gnum].birds.append(user_id)
            self.cnum +=1

        if self.cnum == 5:
            self.group_list[self.gnum]._init_model()
            self.cnum = 0 # 连接id
            self.group = Group() #一个组
            self.gnum += 1 # 分组id
            return self.gnum-1,4
        return self.gnum,self.cnum-1

    def wait_con(self,group_id):#等待连接
        if self.group_list[group_id].timeout and self.group_list[group_id].timec < int(time.time()):
            self.group_list[group_id].timeout = False
            self.group_list[group_id]._init_model()
        return self.group_list[group_id].ready