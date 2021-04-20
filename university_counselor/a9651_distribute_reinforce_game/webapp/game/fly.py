#coding:utf-8
from __future__ import print_function
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import cv2
import sys
import random
import numpy as np
from game.Net import *


class Detect():
    def __init__(self,path):
        self.Actions = 2 # 有两种动作0和1
        self.epsilon = 0.0001 # 一开始的探索概率
        self.PerAction = 1
        self.t = 0
        self.flag = True 
        self.initmodel(path)

    def initmodel(self,path):
        self.sess = tf.InteractiveSession()
        self.s, self.readout, self.h_fc1 = createNetwork()
        saver = tf.train.Saver()
        self.sess.run(tf.initialize_all_variables())
        checkpoint = tf.train.get_checkpoint_state(path)
        if checkpoint and checkpoint.model_checkpoint_path:
            saver.restore(self.sess, checkpoint.model_checkpoint_path)
        tf.reset_default_graph()
 

    def detect(self,target):
        grayimg = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        ret, simg = cv2.threshold(grayimg,1,255,cv2.THRESH_BINARY)
        # cv2.imwrite("3.jpg",simg)
        if self.flag:
            self.s_t = np.stack((simg, simg, simg, simg), axis=2)
            self.flag = False
        else:
            x_t1 = np.reshape( simg, (80, 80, 1))
            self.s_t  = np.append( x_t1, self.s_t[:, :, :3], axis=2)

        # 根据贪心策略选择所作的动作
        readout_t = self.readout.eval(session=self.sess,feed_dict={self.s : [self.s_t]})[0]
        action = np.zeros([self.Actions])
        action_index = 0
        if self.t % self.PerAction == 0:
            if random.random() <= self.epsilon:
                action_index = random.randrange(self.Actions)
                action[random.randrange(self.Actions)] = 1
            else:
                action_index = np.argmax(readout_t)
                action[action_index] = 1
        else:
            action[0] = 1

        self.t += 1
        return action
        print(action)

if __name__ == "__main__":
    main()
