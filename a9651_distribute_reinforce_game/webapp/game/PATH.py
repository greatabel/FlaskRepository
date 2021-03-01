#coding:utf-8
import cv2
import numpy as np
def load():
    # 小鸟图片的载入路径
    PlayerPath = (
            './game/assets/sprites/redbird-upflap.png',
            './game/assets/sprites/redbird-midflap.png',
            './game/assets/sprites/redbird-downflap.png'
    )

    # 背景图片
    BackgroundPath = './game/assets/sprites/sky.png'

    # 管道障碍物图片
    PipePath = './game/assets/sprites/pipe-green1.png'

    Images = {}

    # 数字
    Images['numbers'] = (
        cv2.imread('./game/assets/sprites/0.png',-1),
        cv2.imread('./game/assets/sprites/1.png',-1),
        cv2.imread('./game/assets/sprites/2.png',-1),
        cv2.imread('./game/assets/sprites/3.png',-1),
        cv2.imread('./game/assets/sprites/4.png',-1),
        cv2.imread('./game/assets/sprites/5.png',-1),
        cv2.imread('./game/assets/sprites/6.png',-1),
        cv2.imread('./game/assets/sprites/7.png',-1),
        cv2.imread('./game/assets/sprites/8.png',-1),
        cv2.imread('./game/assets/sprites/9.png',-1)
    )

    # 地面
    Images['base'] = cv2.imread('./game/assets/sprites/base.jpg')

    Sounds = {}


    Images['background'] = np.zeros((512,288,3),dtype=np.uint8)
    Images['background'][400:512,0:288] = Images['base']
    #随机选取小鸟的样子
    Images['player'] = (
        cv2.imread(PlayerPath[0],-1),
        cv2.imread(PlayerPath[1],-1),
        cv2.imread(PlayerPath[2],-1),
    )

    # 选取管道障碍物
    Images['pipe'] = (
        cv2.flip(cv2.imread(PipePath),-1),
        cv2.imread(PipePath),
    )


    return Images


if __name__ == '__main__':
    load()