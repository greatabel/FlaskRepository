#coding:utf-8
from __future__ import print_function
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import cv2
import sys
sys.path.append("Game/")
import random
import numpy as np
from collections import deque
from game.Net import *



class TrainNetwork():
    def __init__(self):
        self.Actions = 2 # 有两种动作0和1
        self.Gamma = 0.99 # 对于过去行为动作的损失参数
        self.Observe = 10000. # 前100000次不进行训练，只为获得样本动作
        self.Explore = 200000.
        self.InitoalEpsilon = 0.0001 # 一开始的探索概率
        self.FinalEpsilon = 0.0001 # 最终的探索概率
        self.ReplayMemory = 500000 # 经验池中最多存放500000个数据样本
        self.Batch = 32 # 一次选取32个数据样本用来更新网络
        self.PerAction = 1
        self.epsilon = self.InitoalEpsilon
        self.t = 0
        self.endpoint = False
        self.flag = True
        self.initmodel()

    def initmodel(self):
        self.sess = tf.InteractiveSession()
        self.s, self.readout, self.h_fc1 = createNetwork()

        # 定义Q值函数
        self.a = tf.placeholder("float", [None, self.Actions])
        self.y = tf.placeholder("float", [None])
        readout_action = tf.reduce_sum(tf.multiply(self.readout, self.a), reduction_indices=1)
        cost = tf.reduce_mean(tf.square(self.y - readout_action))
        self.train_step = tf.train.AdamOptimizer(1e-6).minimize(cost)
        # 将一开始得到的数据存入经验池D中
        self.D = deque()

        # 保存于加载网络
        self.saver = tf.train.Saver()
        self.sess.run(tf.initialize_all_variables())
        checkpoint = tf.train.get_checkpoint_state("saved_networks/")
        self.saver.restore(self.sess, checkpoint.model_checkpoint_path)
        tf.reset_default_graph()


    # 开始训练
    def train(self,img,reward):
        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, simg = cv2.threshold(grayimg,1,255,cv2.THRESH_BINARY)
        # cv2.imwrite("3.jpg",simg)
        if self.flag:
            self.s_t = np.stack((simg, simg, simg, simg), axis=2)
            self.flag = False
        else:
            x_t1 = np.reshape( simg, (80, 80, 1))
            s_t1 = np.append( x_t1, self.s_t[:, :, :3], axis=2)
            # 将数据样本保存在D中
            self.D.append((self.s_t,self.actiond,reward, s_t1, self.endpoint))
            if len(self.D) > self.ReplayMemory:
                self.D.popleft()

            # 只有在观察之后才会进行新一次的训练
            if self.t > self.Observe:
                # 从D中选取Batch数量的样本更新miniBatch
                miniBatch = random.sample(self.D, self.Batch)

                # 获得(s,a,r,s)
                s_j_Batch = [d[0] for d in miniBatch]
                a_Batch = [d[1] for d in miniBatch]
                r_Batch = [d[2] for d in miniBatch]
                s_j1_Batch = [d[3] for d in miniBatch]

                y_Batch = []
                readout_j1_Batch = self.readout.eval(session=self.sess,feed_dict={self.s : s_j1_Batch})
                for i in range(0, len(miniBatch)):
                    self.endpoint = miniBatch[i][4]
                    if self.endpoint:
                        y_Batch.append(r_Batch[i])
                    else:
                       
                        y_Batch.append(r_Batch[i] +  self.Gamma * np.max(readout_j1_Batch[i]))

                self.train_step.run(session=self.sess,feed_dict = {
                    self.y : y_Batch,
                    self.a : a_Batch,
                    self.s : s_j_Batch}
                )

            # 更新值
            self.s_t =  s_t1
            self.t += 1

            # 没10000次训练保存一次网络
            if self.t % 10000 == 0:
                print(self.t)
                self.saver.save(self.sess, 'saved_networks/bird-dqn', global_step = self.t)

        readout_t = self.readout.eval(session=self.sess,feed_dict={self.s : [self.s_t]})[0]
        action = np.zeros([self.Actions])
        action_index = 0
        if self.t % self.PerAction == 0:
            if random.random() <= self.epsilon:
                print("----------Random Action----------")
                action_index = random.randrange(self.Actions)
                action[random.randrange(self.Actions)] = 1
            else:
                action_index = np.argmax(readout_t)
                action[action_index] = 1
        else:
            action[0] = 1
        # 缩小探索的概率
        if self.epsilon > self.FinalEpsilon and self.t > self.Observe:
            self.epsilon -= (self.InitoalEpsilon - self.FinalEpsilon) / self.Explore

        self.actiond = action
        return action
  

if __name__ == "__main__":
    main()
