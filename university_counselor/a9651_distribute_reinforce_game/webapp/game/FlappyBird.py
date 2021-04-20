#coding:utf-8
import random
import game.PATH as PATH
import cv2

ScreenWidth  = 288
ScreenHeight = 512

Image = PATH.load()
Screen = Image['background']
PipGapSize = 100 # 管道障碍物中间间隔的长度设置为100
Basey = 400 # 基底线所在的位置

index = random.randint(50, 250) #在gapYs中随机选取
PlayerWidth = Image['player'][0].shape[1]
PlayerHeight = Image['player'][0].shape[0]
PipeWidth = Image['pipe'][0].shape[1]
PipeHeight = Image['pipe'][0].shape[0]
BackgroundHeight = Image['background'].shape[0]



class GameState:
    def __init__(self,randomh):
        self.basex = 0
        self.baseUpline = Image['base'].shape[0] - BackgroundHeight
        self.pipeVx = -2 # 管道障碍物在x轴方向上的移动速度是每帧4格，向x轴负方向移动。就是向左
        self.interval_n =0 #间隔加速度
        self.interval =60 #间隔
        self.baseground=None #基础画面
        self.showground=None #显示画面
        self.playerx = int(ScreenWidth * 0.2)
        self.p = 0
        self.playerx = int(ScreenWidth * 0.2)
        self.playery = int((ScreenHeight - PlayerHeight) / 2)
        self.playerVy = 0
        self.playerAccY = 0.2 # 小鸟的下落加速度
        self.playerFlapAcc = -2.5#在小鸟扇动翅膀时的速度
        self.playerFlapped = False # 标识符，小鸟扇动翅膀时为True
        self.score = self.playerIndex = self.loopIter = 0
        self.reward = 0.1
        self.screen = None
        self.los=0
        # 上升时挥动翅膀
        self.up = False
        #挥动翅膀的间隔
        self.t = 0
        self.tend=4
        #小鸟存活
        self.live=0
 

        newPipe1 = GetPipe(randomh[0])
        newPipe2 = GetPipe(randomh[1])
        newPipe3 = GetPipe(randomh[2])
        self.upPipes = [
            {'x': 300 , 'y': newPipe1[0]['y']},
            {'x': int(300 + PipeWidth * 2.8 ) , 'y': newPipe2[0]['y']},
            {'x': int(300 + PipeWidth * 2.8 *2), 'y': newPipe3[0]['y']},
        ]
        self.downPipes = [
            {'x': 300, 'y': newPipe1[1]['y']},
            {'x': int(300 + PipeWidth * 2.8) , 'y': newPipe2[1]['y']},
            {'x': int(300 + PipeWidth * 2.8 * 2), 'y': newPipe3[1]['y']},
        ]
    def pipeline(self,randomh):
        self.screen=Screen.copy()
        # 管道障碍物向左移动时候的速度 
        for uPipe, lPipe in zip(self.upPipes, self.downPipes):
            uPipe['x'] += self.pipeVx
            lPipe['x'] += self.pipeVx

        # 当旧的管道移动到屏幕最左边的时候，将其从upPips与downPips中删除
        if self.upPipes[0]['x'] <0:
            self.upPipes.pop(0)
            self.downPipes.pop(0)
            
            newPipe = GetPipe(randomh[self.p])
            self.p += 1
            if self.p == 3:
                self.p = 0
            self.upPipes.append({'x': int(self.upPipes[1]['x'] + PipeWidth * 2.8) , 'y': newPipe[0]['y']})
            self.downPipes.append({'x':int( self.upPipes[1]['x'] + PipeWidth * 2.8) , 'y': newPipe[1]['y']})

        #显示管子
        for uPipe, lPipe in zip(self.upPipes, self.downPipes):
            if uPipe['x']>=ScreenWidth+PipeWidth:
                continue
            self.screen[0:uPipe['y']+PipeHeight,uPipe['x']-PipeWidth if uPipe['x']-PipeWidth > 0 else 0: ScreenWidth if uPipe['x']>ScreenWidth else uPipe['x']]=Image['pipe'][0][abs(uPipe['y']):320,PipeWidth-uPipe['x'] if PipeWidth-uPipe['x'] > 0 else 0:ScreenWidth+PipeWidth-uPipe['x'] if ScreenWidth+PipeWidth-uPipe['x']>0 else PipeWidth]
            self.screen[lPipe['y']:400,lPipe['x']-PipeWidth if lPipe['x']-PipeWidth > 0 else 0:lPipe['x'] if ScreenWidth >ScreenWidth else lPipe['x']]=Image['pipe'][1][0:400-lPipe['y'],PipeWidth-lPipe['x'] if PipeWidth-lPipe['x'] > 0 else 0:ScreenWidth+PipeWidth-lPipe['x'] if ScreenWidth+PipeWidth-lPipe['x']>0 else PipeWidth]
        

    def frame_step(self, action,randomh):

        self.pipeline(randomh)
      
        # 确定分数，在小鸟的x超过管道右边界的x时，获得的分数+1
        if self.upPipes[0]['x'] <self.playerx  < self.upPipes[0]['x'] + 3:
            self.score += 1
        self.reward = 0.1
        self.endpoint = False
        # 0：小鸟不做任务事    1：小鸟扇动翅膀
        if action == 1:
            self.playerVy = self.playerFlapAcc
            self.up = True
        self.t +=1
        # 绘制下一帧
        if self.t == self.tend:
            self.t=0
            if self.up:
                self.playerIndex +=1
                if self.playerIndex> 2:
                    self.playerIndex = 0
                    self.up = False
            else:
                self.playerIndex = 0
        # 小鸟在y轴上的移动方式
        self.playery += self.playerVy
        self.playerVy += self.playerAccY
        if self.playery < 0:
            self.playery = 0


        #显示小鸟
        py = int(self.playery)
        self.screen[py:PlayerHeight+py,self.playerx:self.playerx+PlayerWidth]  = addpng(self.screen[py:PlayerHeight+py,self.playerx:self.playerx+PlayerWidth],Image['player'][self.playerIndex]) 

        # cv2.imshow("1",self.screen)

        # 碰撞检测。发生碰撞时结束游戏，并马上开始新一局的游戏
        Crash = CrashHappen({'x': self.playerx, 'y': self.playery,
                            'index': self.playerIndex},
                            self.upPipes, self.downPipes)
        if Crash:
            # self.__init__()
            self.live=1
        x_t1 = cv2.cvtColor(cv2.resize(self.screen, (80, 80)), cv2.COLOR_BGR2GRAY)
        return x_t1,self.live

def addpng(img,png):
    img = cv2.split(img)
    png = cv2.split(png)
    for i in range(3):
        img[i] = img[i]*(255.0  - png[3])/255 + png[i]*(png[3]/255)
    return cv2.merge(img)

def showScore(score,sc):
    scorenum = [int(x) for x in list(str(score))]
    Total = 0

    for num in scorenum:
        Total += Image['numbers'][num].shape[1]

    Xoffset = int((ScreenWidth - Total) / 2)

    for num in scorenum:
        # Screen.blit(Image['numbers'][num], (Xoffset, ScreenHeight * 0.1))
        sc[int(ScreenHeight * 0.1):int(ScreenHeight * 0.1)+Image['numbers'][num].shape[0],Xoffset:Xoffset+Image['numbers'][num].shape[1]]=addpng (sc[int(ScreenHeight * 0.1):int(ScreenHeight * 0.1)+Image['numbers'][num].shape[0],Xoffset:Xoffset+Image['numbers'][num].shape[1]],Image['numbers'][num])
        Xoffset += Image['numbers'][num].shape[1]
    return sc
def GetPipe(a):
    x = a*10 #在gapYs中随机选取
    d = 430-x

    # gapY += int(Basey * 0.2)
    # pipeX = ScreenWidth + 10

    return [
        {'x': 1, 'y': -x},  # 上管道的起始坐标值
        {'x': 1, 'y': d},  # 下管道的起始坐标值
    ]

def CrashHappen(player, upPipes, downPipes):
    pi = player['index']
    player['w'] = Image['player'][0].shape[1]
    player['h'] = Image['player'][0].shape[0]

    # 判断小鸟是否与地面相碰撞
    if player['y'] + player['h'] >= Basey - 1:
        return True
    else:

        for uPipe, lPipe in zip(upPipes, downPipes):
            # 上下管道的矩形位置和长宽数据
            if uPipe['x']-PipeWidth < player['x']+PlayerWidth/5*4 and player['x']+PlayerWidth/5<uPipe['x']:
                if player['y']+PlayerHeight/5 <uPipe['y']+PipeHeight or lPipe['y'] <player['y'] +PlayerHeight/5*4:
                    return True

    return False

if __name__ == '__main__':
    game = GameState()
    birds = []
    for i in range(2):
       birds.append(Bird())

    for _ in range(100):
        birds[1].action[1]=1

        birds = game.frame_step(birds)