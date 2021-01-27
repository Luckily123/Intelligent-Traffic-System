import sys
import math
import pygame
import time
import os
import numpy as np
from pygame.locals import *

# 固定窗口出现位置
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d"%(550,80)

# 速度改变系数
mul = 0.1

#在pygame中打印文本的函数
def print_text(font1, x1, y1, text, color1=(0, 0, 0)):
    imgText = font1.render(text, True, color1)
    screen.blit(imgText,(x1, y1))

# 每个玩家可选择的9种行动，1代表加速，0代表保持当前速度，-1代表减速
# 玩家1：（2,4） 玩家2：（1,3）
ACTION_CHOICE = [np.array([1, 1]), np.array([1, 0]), np.array([0, 1]),
                 np.array([0, 0]), np.array([1, -1]), np.array([-1, 1]),
                 np.array([0, -1]), np.array([-1, 0]), np.array([-1, -1])]
# 每个玩家可选择车的9种行动，1代表右转，0代表直行，-1代表左转
# 玩家1：（2,4） 玩家2：（1,3）
DIRECTION_CHOICE = [np.array([1, 1]), np.array([1, 0]), np.array([0, 1]),
                    np.array([0, 0]), np.array([1, -1]), np.array([-1, 1]),
                    np.array([0, -1]), np.array([-1, 0]), np.array([-1, -1])]


# wrap_angle function
def wrap_angle(angle):
    return angle % 90


def wrap_angle1(angle):
    return angle % -90


class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
    # X property
    def getx(self): return self.__x
    def setx(self, x): self.__x = x
    x = property(getx, setx)
    # Y property
    def gety(self): return self.__y
    def sety(self, y): self.__y = y
    y = property(gety, sety)


def crash(car1, car2):
    """
    car1=(d1,v1),d1为car1距离碰撞点的距离，v1为car1更新后的速度
    car2=(d2,v2),d2为car2距离碰撞点的距离，v2为car2更新后的速度
    碰撞则返回True,未碰撞则返回False
    左直行+右直行
    """
    t1b = (car1[0] + 60)/car1[1]
    t1f = (car1[0] + 90 + 60)/car1[1]
    if car2[1] * t1b >= (car2[0] + 90+30) or car2[1] * t1f <= (car2[0]+10):
        return False
    else:
        return True


def crashrs(car1, car2):
    """
    右转+直行
    """
    t1b = (car1[0] + 10)/car1[1]
    t1f = (car1[0] + 50*3.1416/4 + 50)/car1[1]
    if (car2[1] * t1b >= (car2[0] + 90+60+60) and car2[1] >=car1[1]) or (car2[1] * t1f <= (car2[0]+30) and car2[1] <=car1[1]):
        return False
    else:
        return True


def crashrl1(car1, car2):
    """
    右转+左侧左转
    """
    t1b = (car1[0] + 10)/car1[1]
    t1f = (car1[0] + 50*3.1416/4 + 40)/car1[1]
    if car2[1] * t1b >= (car2[0] + 150/4*3.1416 + 20) or car2[1] * t1f <= (car2[0]+60):
        return False
    else:
        return True


def crashrl2(car1, car2):
    """
    右转+对面左转
    """
    t1b = (car1[0] + 10)/car1[1]
    t1f = (car1[0] + 50*3.1416/4+80)/car1[1]
    if (car2[1] * t1b >= (car2[0] + 150*3.1416/4+80) and car2[1] > car1[1]) or (car2[1] * t1f <= (car2[0]) and car2[1]<car1[1]):
        return False
    else:
        return True


def crash1s1(car1, car2):
    """
    左转+右侧直行
    """
    t1b = (car1[0] + 150/8*3.1416)/car1[1]
    t1f = (car1[0] + 150/4*3.1416+30)/car1[1]
    if (car2[1] * t1b >= (car2[0] + 90 + 60) and car2[1] >= car1[1]) or (car2[1] * t1f <= (car2[0]) and car2[1] <= car1[1]):
        return False
    else:
        return True


def crashls2(car1, car2):
    """
    左转+左侧直行
    """
    t1b = (car1[0] + 10)/car1[1]
    t1f = (car1[0] + 150*3.1416/4)/car1[1]
    if car2[1] * t1b >= (car2[0] + 90+60) or car2[1] * t1f <= (car2[0] + 60):
        return False
    else:
        return True


def crashls3(car1, car2):
    """
    左转+对面直行
    """
    t1b = (car1[0] + 150/10*3.1416)/car1[1]
    t1f = (car1[0] + 150/4*3.1416+70)/car1[1]
    if car2[1] * t1b >= (car2[0] + 110) or car2[1] * t1f <= car2[0]:
        return False
    else:
        return True


def crashll1(car1, car2):
    """
    左转+左侧左转
    """
    t1b = (car1[0] + 10)/car1[1]
    t1f = (car1[0] + 150/4*3.1416+60)/car1[1]
    if car2[1] * t1b >= (car2[0] + 150/4*3.1415+60) or car2[1] * t1f <= (car2[0]+ 60):
        return False
    else:
        return True


def crashll2(car1, car2):
    """
    左转+对面左转
    """
    t1b = (car1[0])/car1[1]
    t1f = (car1[0] + 150/4*3.1416+80)/car1[1]
    if car2[1] * t1b >= (car2[0] + 150/4*3.1416+80) or car2[1] * t1f <= car2[0]:
        return False
    else:
        return True


def pass_time(d, v, action, direction):
    """
    输入：
        d: 4维向量，代表4辆车距离stop_line的距离，索引与图2中小汽车编号相同
        v: 4维向量，代表4辆车在位置d处的速度(取值范围100-200,也就是10m/s-20m/s（36km/h-72km/h）)，索引与图2中小汽车编号相同
        action：4维向量，代表4辆车的采取的行动，1代表加速，0代表保持当前速度，-1代表减速,索引与图2中小汽车编号相同
    返回：
        如发生碰撞，则返回-1
        如未发生碰撞，则返回4辆车通过该路口（200m）的平均时间
    """
    v_new = v * (1 + action * mul)  # 根据所选行动更新速度
    v_new[v_new > 200.] = 200.  # 速度上限
    if direction[2] == 0 and direction[3]==0:
        #全部直行
        car1 = d[2], v_new[2]
        car2 = d[3], v_new[3]
        if crash(car1, car2):
            return -1
    if direction[3]==0 and direction[0]==0:
        car1 = d[3], v_new[3]
        car2 = d[0], v_new[0]
        if crash(car1, car2):
            return -1
    if direction[0]==0 and direction[1]==0:
        car1 = d[0], v_new[0]
        car2 = d[1], v_new[1]
        if crash(car1, car2):
            return -1
    if direction[1]==0 and direction[2]==0:
        car1 = d[1], v_new[1]
        car2 = d[2], v_new[2]
        if crash(car1, car2):
            return -1



    if direction[0]==1 and direction[3]==0:
        #右转+直行
        car1 = d[0], v_new[0]
        car2 = d[3], v_new[3]
        if crashrs(car1, car2):
            return -1
    if direction[1]==1 and direction[0]==0:
        #右转+直行
        car1 = d[1], v_new[1]
        car2 = d[0], v_new[0]
        if crashrs(car1, car2):
            return -1
    if direction[2]==1 and direction[1]==0:
        #右转+直行
        car1 = d[2], v_new[2]
        car2 = d[1], v_new[1]
        if crashrs(car1, car2):
            return -1
    if direction[3]==1 and direction[2]==0:
        #右转+直行
        car1 = d[3], v_new[3]
        car2 = d[2], v_new[2]
        if crashrs(car1, car2):
            return -1



    if direction[0]==-1 and direction[1]==0:
        #左转+右侧直行
        car1 = d[0], v_new[0]
        car2 = d[1], v_new[1]
        if crash1s1(car1, car2):
            return -1
    if direction[1]==-1 and direction[2]==0:
        #左转+右侧直行
        car1 = d[1], v_new[1]
        car2 = d[2], v_new[2]
        if crash1s1(car1, car2):
            return -1
    if direction[2]==-1 and direction[3]==0:
        #左转+右侧直行
        car1 = d[2], v_new[2]
        car2 = d[3], v_new[3]
        if crash1s1(car1, car2):
            return -1
    if direction[3]==-1 and direction[0]==0:
        #左转+右侧直行
        car1 = d[3], v_new[3]
        car2 = d[0], v_new[0]
        if crash1s1(car1, car2):
            return -1

    if direction[0]==-1 and direction[3]==0:
        # 左转+左侧直行
        car1 = d[0], v_new[0]
        car2 = d[3], v_new[3]
        if crashls2(car1, car2):
            return -1
    if direction[1]==-1 and direction[0]==0:
        # 左转+左侧直行
        car1 = d[1], v_new[1]
        car2 = d[0], v_new[0]
        if crashls2(car1, car2):
            return -1
    if direction[2]==-1 and direction[1]==0:
        # 左转+左侧直行
        car1 = d[2], v_new[2]
        car2 = d[1], v_new[1]
        if crashls2(car1, car2):
            return -1
    if direction[3]==-1 and direction[2]==0:
        # 左转+左侧直行
        car1 = d[3], v_new[3]
        car2 = d[2], v_new[2]
        if crashls2(car1, car2):
            return -1

    if direction[0]==-1 and direction[2]==0:
        # 左转+对面直行
        car1 = d[0], v_new[0]
        car2 = d[2], v_new[2]
        if crashls3(car1, car2):
            return -1
    if direction[1]==-1 and direction[3]==0:
        # 左转+对面直行
        car1 = d[1], v_new[1]
        car2 = d[3], v_new[3]
        if crashls3(car1, car2):
            return -1
    if direction[2]==-1 and direction[0]==0:
        # 左转+对面直行
        car1 = d[2], v_new[2]
        car2 = d[0], v_new[0]
        if crashls3(car1, car2):
            return -1
    if direction[3]==-1 and direction[1]==0:
        # 左转+对面直行
        car1 = d[3], v_new[3]
        car2 = d[1], v_new[1]
        if crashls3(car1, car2):
            return -1

    if direction[0] == 1 and direction[3] == -1:
        # 右转+左侧左转
        car1 = d[0], v_new[0]
        car2 = d[3], v_new[3]
        if crashrl1(car1, car2):
            return -1
    if direction[1] == 1 and direction[0] == -1:
        # 右转+左侧左转
        car1 = d[1], v_new[1]
        car2 = d[0], v_new[0]
        if crashrl1(car1, car2):
            return -1
    if direction[2] == 1 and direction[1] == -1:
        # 右转+左侧左转
        car1 = d[2], v_new[2]
        car2 = d[1], v_new[1]
        if crashrl1(car1, car2):
            return -1
    if direction[3] == -1 and direction[2] == -1:
        # 右转+左侧左转
        car1 = d[3], v_new[3]
        car2 = d[2], v_new[2]
        if crashrl1(car1, car2):
            return -1

    if direction[0] == 1 and direction[2] == -1:
        # 右转+对面左转
        car1 = d[0], v_new[0]
        car2 = d[2], v_new[2]
        if crashrl2(car1, car2):
            return -1

    if direction[1] == 1 and direction[3]==-1:
        # 右转+对面左转
        car1 = d[1], v_new[1]
        car2 = d[3], v_new[3]
        if crashrl2(car1, car2):
            return -1
    if direction[2] == 1 and direction[0] == -1:
        # 右转+对面左转
        car1 = d[2], v_new[2]
        car2 = d[0], v_new[0]
        if crashrl2(car1, car2):
            return -1
    if direction[3]==1 and direction[1]==-1:
        # 右转+对面左转
        car1 = d[3], v_new[3]
        car2 = d[1], v_new[1]
        if crashrl2(car1, car2):
            return -1

    if direction[0] == -1 and direction[3] == -1:
        # 左转+左侧左转
        car1 = d[0], v_new[0]
        car2 = d[3], v_new[3]
        if crashll1(car1, car2):
            return -1
    if direction[1] == -1 and direction[0] == -1:
        # 左转+左侧左转
        car1 = d[1], v_new[1]
        car2 = d[0], v_new[0]
        if crashll1(car1, car2):
            return -1
    if direction[2] ==-1 and direction[1] == -1:
        # 左转+左侧左转
        car1 = d[2], v_new[2]
        car2 = d[1], v_new[1]
        if crashll1(car1, car2):
            return -1
    if direction[3] == -1 and direction[2]==-1:
        # 左转+左侧左转
        car1 = d[3], v_new[3]
        car2 = d[2], v_new[2]
        if crashll1(car1, car2):
            return -1

    if direction[0] == -1 and direction[2] == -1:
        # 左转+对面左转
        car1 = d[0], v_new[0]
        car2 = d[2], v_new[2]
        if crashll2(car1, car2):
            return -1
    if direction[1] == -1 and direction[3] == -1:
        # 左转+对面左转
        car1 = d[1], v_new[1]
        car2 = d[3], v_new[3]
        if crashll2(car1, car2):
            return -1

    time_all = (450. - d - 60) / v + (160. + d + 60) / v_new + 290 / 200   # 未发生碰撞则返回4辆车通过该路口的平均时间
    return time_all.max()


pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("针对双向单行道十字路口的基于博弈论的多车协作算法演示动画")
font = pygame.font.SysFont("simhei", 25)

dirch1 = -1
dirch2 = -1
radius1 = 75
radius2 = 25
angle1 = 0.0
pos1 = Point(0, 0)
old_pos1 = Point(0, 0)

angle2 = 0.0
pos2 = Point(0, 0)
old_pos2 = Point(0, 0)

angle3 = 0.0
pos3 = Point(0, 0)
old_pos3 = Point(0, 0)

angle4 = 0.0
pos4 = Point(0, 0)
old_pos4 = Point(0, 0)


#加载图片
back = pygame.image.load("lukou8.png").convert_alpha()
car10L = pygame.image.load("car10L.png").convert_alpha()
car10R = pygame.image.load("car10R.png").convert_alpha()
car20L = pygame.image.load("car20L.png").convert_alpha()
car20R = pygame.image.load("car20R.png").convert_alpha()
car10 = pygame.image.load("car10.png").convert_alpha()
car20 = pygame.image.load("car20.png").convert_alpha()
car30 = pygame.image.load("car30.png").convert_alpha()
car40 = pygame.image.load("car40.png").convert_alpha()
car30L = pygame.image.load("car30L.png").convert_alpha()
car30R = pygame.image.load("car30R.png").convert_alpha()
car40L = pygame.image.load("car40L.png").convert_alpha()
car40R = pygame.image.load("car40R.png").convert_alpha()
car10LB = pygame.transform.rotate(car10L, -90)
car10RB = pygame.transform.rotate(car10R, 90)
car10BL = pygame.transform.rotate(car10, 90)
car10BR = pygame.transform.rotate(car10, -90)
car20LB = pygame.transform.rotate(car20L, -90)
car20RB = pygame.transform.rotate(car20R, 90)
car20BL = pygame.transform.rotate(car20, 90)
car20BR = pygame.transform.rotate(car20, -90)
car30LB = pygame.transform.rotate(car30L, -90)
car30RB = pygame.transform.rotate(car30R, 90)
car30BL = pygame.transform.rotate(car30, 90)
car30BR = pygame.transform.rotate(car30, -90)
car40LB = pygame.transform.rotate(car40L, -90)
car40RB = pygame.transform.rotate(car40R, 90)
car40BL = pygame.transform.rotate(car40, 90)
car40BR = pygame.transform.rotate(car40, -90)

width, height = car10.get_size()

while True:

    clock = pygame.time.Clock()
    v20 = 200/60
    t = time.perf_counter()
    # 速度初始化（100-200），d是在四车距离stop_line 390m之后再各自行进1s后距离stop_line的距离
    vv = np.random.rand(4) * 100 + 100

    # v = np.array([149.92177139, 164.36460619, 111.08582486, 130.0684954 ])
    dd = 390 - vv * 1
    c = np.random.randint(-1, 2, 4)
    # c = np.array([1, 1, 1, 1])
    print("vv:",vv)
    print("dd:",dd)
    flag = 1
    fdir1 = 1
    fdir2 = 1
    fdir3 = 1
    fdir4 = 1
    # 定义存储最短通过时间的矩阵
    game_matrix = np.zeros((9, 9, 9, 9))

    # 遍历所有玩家选择并在game_matrix中写入通过时间

    for m, playerdir_1 in enumerate(DIRECTION_CHOICE):
        for n, playerdir_2 in enumerate(DIRECTION_CHOICE):
            direction1 = np.array([playerdir_2[0], playerdir_1[0], playerdir_2[1], playerdir_1[1]])
            for i, player_1 in enumerate(ACTION_CHOICE):
                for j, player_2 in enumerate(ACTION_CHOICE):
                    action1 = np.array([player_2[0], player_1[0], player_2[1], player_1[1]])
                    # action = np.array([0,0,0,0])
                    game_matrix[m, n, i, j] = pass_time(dd, vv, action1, direction1)
    print(c)
    # print(game_matrix[0, 5, :, :])
    for i in range(9):
        if (DIRECTION_CHOICE[i][0] == c[0] )and (DIRECTION_CHOICE[i][1] )== c[2]:
            dirch2 = i
            break
    for j in range(9):
        if (DIRECTION_CHOICE[j][0] == c[1] )and (DIRECTION_CHOICE[j][1] )== c[3]:
            dirch1 = j
            break
    zong = 0
    for he in range(9):
        for zo in range(9):
            if game_matrix[dirch1, dirch2, he, zo] == -1:
                zong = zong + 1
    if zong == 81 or (dirch1 == -1 and dirch2 == -1):
        vv[0] = 0
        vv[1] = 0
        vv[2] = 0
        vv[3] = 0
        continue
    # 如果碰撞，时间设置为inf
    game_matrix[game_matrix < 0] = np.inf
    # 找到game_matrix中最小值位置
    re = np.where(game_matrix[dirch1, dirch2, :, :] == np.min(game_matrix[dirch1, dirch2, :, :]))
    #print(game_matrix[dirch1, dirch2, :, :])
    print("action",ACTION_CHOICE[re[1][0]][0],ACTION_CHOICE[re[0][0]][0],ACTION_CHOICE[re[1][0]][1],ACTION_CHOICE[re[0][0]][1])
    # 初始化car1到car4初始位置
    xw = [0, 510, 940, 460]
    yw = [510, 940, 460, 0]
    v1 = vv[0] / 60
    v2 = vv[1] / 60
    v3 = vv[2] / 60
    v4 = vv[3] / 60
    # 游戏开始
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            sys.exit()
        clock.tick(60)

        # 小车变速
        if flag == 1:
            if 450 - xw[0] - 60 <= dd[0]:
                v1 = vv[0] * (1 + mul * ACTION_CHOICE[re[1][0]][0]) / 60
                if v1 > 200 / 60:
                    v1 = 200 / 60
            if yw[1] - 550 <= dd[1]:
                v2 = vv[1] * (1 + mul * ACTION_CHOICE[re[0][0]][0]) / 60
                if v2 > 200 / 60:
                    v2 = 200 / 60
            if xw[2] - 550 <= dd[2]:
                v3 = vv[2] * (1 + mul * ACTION_CHOICE[re[1][0]][1]) / 60
                if v3 > 200 / 60:
                    v3 = 200 / 60
            if 450 - yw[3] - 60 <= dd[3]:
                v4 = vv[3] * (1 + mul * ACTION_CHOICE[re[0][0]][1]) / 60
                if v4 > 200 / 60:
                    v4 = 200 / 60
            if 450 - xw[0] + 60 <= dd[0] and yw[1] - 550 <= dd[1] and xw[2] - 550 <= dd[2] and 450 - yw[3] - 60 <= dd[3]:
                flag = 0

        screen.blit(back, (0, 0))

        # 1
        if c[0] == -1:
            if fdir1 == 1:
                xw[0] = xw[0] + v1
                if xw[0] >= 420:
                    fdir1= 0
                    angle1 = 0.0
                    pos1 = Point(0, 0)
                    old_pos1 = Point(0, 0)
                if 450 - 60 - xw[0] >= dd[0]:
                    screen.blit(car10, (xw[0], yw[0]))
                else:
                    screen.blit(car10LB, (xw[0], yw[0]))
            if fdir1 == 2:
                if yw[0] >= 390:
                    yw[0] = yw[0] - v1
                else:
                    v1 = v20
                    yw[0] = yw[0] - v1
                if yw[0] >= 100:
                    screen.blit(car10L, (510, yw[0]))
                else:
                    screen.blit(car10BL, (510, yw[0]))
            if fdir1 == 0:
                # move the ship
                angle1 = wrap_angle(angle1 + v1*1.8/3.1416)
                pos1.x = math.sin(math.radians(angle1)) * radius1
                pos1.y = math.cos(math.radians(angle1)) * radius1
                # rotate the ship
                delta_x = (pos1.x - old_pos1.x)
                delta_y = (pos1.y - old_pos1.y)
                rangle = math.atan2(delta_y, delta_x)
                rangled = wrap_angle(-math.degrees(rangle))
                scratch_car = pygame.transform.rotate(car10LB, rangled)
                # draw the ship
                width1, height1 = scratch_car.get_size()
                x = 450 + pos1.x - width1 // 2
                y = 450 + pos1.y - height1 // 2
                screen.blit(scratch_car, (x, y))
                if angle1 >= 88.5:
                    fdir1 = 2
                    yw[0] = 420
        if c[0] == 0:
            if xw[0] <= 551:
                xw[0] = xw[0] + v1
            else:
                v1 = v20
                xw[0] = xw[0] + v1
            screen.blit(car10, (xw[0], yw[0]))
        if c[0] == 1:
            if fdir1 == 1:
                xw[0] = xw[0] + v1
                if xw[0] >= 419.5:
                    fdir1 = 0
                    angle1 = 0.0
                    pos1 = Point(0, 0)
                    old_pos1 = Point(0, 0)
                if 450 - 60 - xw[0] >= dd[0]:
                    screen.blit(car10, (xw[0], yw[0]))
                else:
                    screen.blit(car10RB, (xw[0], yw[0]))
            if fdir1 == 2:
                if yw[0] <= 551:
                    yw[0] = yw[0] + v1
                else:
                    v1 = v20
                    yw[0] = yw[0] + v1
                if yw[0] <= 840:
                    screen.blit(car10R, (460, yw[0]))
                else:
                    screen.blit(car10BR, (460, yw[0]))
            if fdir1 == 0:
                # move the ship
                angle1 = wrap_angle1(angle1 - v1*3.6/3.1416)
                pos1.x = math.sin(math.radians(angle1)) * radius2
                pos1.y = math.cos(math.radians(angle1)) * radius2
                # rotate the ship
                delta_x = (pos1.x - old_pos1.x)
                delta_y = (pos1.y - old_pos1.y)
                rangle = math.atan2(delta_y, delta_x)
                rangled = wrap_angle1(-math.degrees(rangle))
                scratch_car = pygame.transform.rotate(car10RB, rangled)
                # draw the ship
                width1, height1 = scratch_car.get_size()
                x = 450 - pos1.x - width1 // 2
                y = 550 - pos1.y - height1 // 2
                screen.blit(scratch_car, (x, y))
                if angle1 <= -86.5:
                    fdir1 = 2
                    yw[0] = 520
        # 2
        if c[1] == -1:
            if fdir2 == 1:
                yw[1] = yw[1] - v2
                if yw[1] <= 520:
                    fdir2 = 0
                    angle2 = 0.0
                    pos2 = Point(0, 0)
                    old_pos2 = Point(0, 0)
                if yw[1] - 550 >= dd[1]:
                    screen.blit(car20, (xw[1], yw[1]))
                else:
                    screen.blit(car20LB, (xw[1], yw[1]))
            if fdir2 == 2:
                if xw[1] >= 390:
                    xw[1] = xw[1] - v2
                else:
                    v2 = v20
                    xw[1] = xw[1] - v2
                if xw[1] >= 100:
                    screen.blit(car20L, (xw[1], yw[1]))
                else:
                    screen.blit(car20BL, (xw[1], yw[1]))
            if fdir2 == 0:
                # move the ship
                angle2 = wrap_angle(angle2 + v2*1.8/3.1416)
                pos2.x = math.sin(math.radians(angle2)) * radius1
                pos2.y = math.cos(math.radians(angle2)) * radius1
                # rotate the ship
                delta_x = (pos2.x - old_pos2.x)
                delta_y = (pos2.y - old_pos2.y)
                rangle = math.atan2(delta_y, delta_x)
                rangled = wrap_angle(-math.degrees(rangle))
                scratch_car = pygame.transform.rotate(car20LB, rangled)
                # draw the ship
                width2, height2 = scratch_car.get_size()
                x = 450 + pos2.y - width2 // 2
                y = 550 - pos2.x - height2 // 2
                screen.blit(scratch_car, (x, y))
                if angle2 >= 87.5:
                    fdir2 = 2
                    yw[1] = 460
                    xw[1] = 420
        if c[1] == 0:
            if yw[1] >= 390:
                yw[1] = yw[1] - v2
            else:
                v2 = v20
                yw[1] = yw[1] - v2
            screen.blit(car20, (xw[1], yw[1]))
        if c[1] == 1:
            if fdir2 == 1:
                yw[1] = yw[1] - v2
                if yw[1] <= 520:
                    fdir2 = 0
                    angle2 = 0.0
                    pos2 = Point(0, 0)
                    old_pos2 = Point(0, 0)
                if yw[1] - 550 >= dd[1]:
                    screen.blit(car20, (xw[1], yw[1]))
                else:
                    screen.blit(car20RB, (xw[1], yw[1]))
            if fdir2 == 2:
                if xw[1] <= 551:
                    xw[1] = xw[1] + v2
                else:
                    v2 = v20
                    xw[1] = xw[1] + v2
                if xw[1] <= 840:
                    screen.blit(car20R, (xw[1], 510))
                else:
                    screen.blit(car20BR, (xw[1], 510))
            if fdir2 == 0:
                # move the ship
                angle2 = wrap_angle1(angle2 - v2*3.6/3.1416)
                pos2.x = math.sin(math.radians(angle2)) * radius2
                pos2.y = math.cos(math.radians(angle2)) * radius2
                # rotate the ship
                delta_x = (pos2.x - old_pos2.x)
                delta_y = (pos2.y - old_pos2.y)
                rangle = math.atan2(delta_y, delta_x)
                rangled = wrap_angle1(-math.degrees(rangle))
                scratch_car = pygame.transform.rotate(car20RB, rangled)
                # draw the ship
                width2, height2 = scratch_car.get_size()
                x = 550 - pos2.y - width2 // 2
                y = 550 + pos2.x - height2 // 2
                screen.blit(scratch_car, (x, y))
                if angle2 <= -86.5:
                    fdir2 = 2
                    xw[1] = 520
                    yw[1] = 510

        # 3
        if c[2] == -1:
            if fdir3 == 1:
                xw[2] = xw[2] - v3
                if xw[2] <= 520:
                    fdir3 = 0
                    angle3 = 0.0
                    pos3 = Point(0, 0)
                    old_pos3 = Point(0, 0)
                if xw[2] - 550 >= dd[2]:
                    screen.blit(car30, (xw[2], yw[2]))
                else:
                    screen.blit(car30LB, (xw[2], yw[2]))
            if fdir3 == 2:
                if yw[2] <= 551:
                    yw[2] = yw[2] + v3
                else:
                    v3 = v20
                    yw[2] = yw[2] + v3
                if yw[2] <= 840:
                    screen.blit(car30L, (460, yw[2]))
                else:
                    screen.blit(car30BL, (460, yw[2]))
            if fdir3 == 0:
                # move the ship
                angle3 = wrap_angle(angle3 + v3*1.8/3.1416)
                pos3.x = math.sin(math.radians(angle3)) * radius1
                pos3.y = math.cos(math.radians(angle3)) * radius1
                # rotate the ship
                delta_x = (pos3.x - old_pos3.x)
                delta_y = (pos3.y - old_pos3.y)
                rangle = math.atan2(delta_y, delta_x)
                rangled = wrap_angle(-math.degrees(rangle))
                scratch_car = pygame.transform.rotate(car30LB, rangled)
                # draw the ship
                width3, height3 = scratch_car.get_size()
                x = 550 - pos3.x - width3 // 2
                y = 550 - pos3.y - height3 // 2
                screen.blit(scratch_car, (x, y))
                if angle3 >= 88.5:
                    fdir3 = 2
                    xw[2] = 460
                    yw[2] = 520
        if c[2] == 0:
            if xw[2] >= 390:
                xw[2] = xw[2] - v3
            else:
                v3 = v20
                xw[2] = xw[2] - v3
            screen.blit(car30, (xw[2], yw[2]))
        if c[2] == 1:
            if fdir3 == 1:
                xw[2] = xw[2] - v3
                if xw[2] <= 520:
                    fdir3 = 0
                    angle3 = 0.0
                    pos3 = Point(0, 0)
                    old_pos3 = Point(0, 0)
                if xw[2] - 550 >= dd[2]:
                    screen.blit(car30, (xw[2], yw[2]))
                else:
                    screen.blit(car30RB, (xw[2], yw[2]))
            if fdir3 == 2:
                if yw[2] >= 390:
                    yw[2] = yw[2] - v3
                else:
                    v3 = v20
                    yw[2] = yw[2] - v3
                if yw[2] >= 100:
                    screen.blit(car30R, (510, yw[2]))
                else:
                    screen.blit(car30BR, (510, yw[2]))
            if fdir3 == 0:
                # move the ship
                angle3 = wrap_angle1(angle3 - v3*3.6/3.1416)
                pos3.x = math.sin(math.radians(angle3)) * radius2
                pos3.y = math.cos(math.radians(angle3)) * radius2
                # rotate the ship
                delta_x = (pos3.x - old_pos3.x)
                delta_y = (pos3.y - old_pos3.y)
                rangle = math.atan2(delta_y, delta_x)
                rangled = wrap_angle1(-math.degrees(rangle))
                scratch_car = pygame.transform.rotate(car30RB, rangled)
                # draw the ship
                width3, height3 = scratch_car.get_size()
                x = 550 + pos3.x - width3 // 2
                y = 450 + pos3.y - height3 // 2
                screen.blit(scratch_car, (x, y))
                if angle3 <= -86.5:
                    fdir3 = 2
                    xw[2] = 510
                    yw[2] = 420

        # 4
        if c[3] == -1:
            if fdir4 == 1:
                yw[3] = yw[3] + v4
                if yw[3] >= 420:
                    fdir4 = 0
                    angle4 = 0.0
                    pos4 = Point(0, 0)
                    old_pos4 = Point(0, 0)
                if 450 - 60 - yw[3] >= dd[3]:
                    screen.blit(car40, (xw[3], yw[3]))
                else:
                    screen.blit(car40LB, (xw[3], yw[3]))
            if fdir4 == 2:
                if xw[3] <= 551:
                    xw[3] = xw[3] + v4
                else:
                    v4 = v20
                    xw[3] = xw[3] + v4
                if xw[3] <= 840:
                    screen.blit(car40L, (xw[3], 510))
                else:
                    screen.blit(car40BL, (xw[3], 510))
            if fdir4 == 0:
                # move the ship
                angle4 = wrap_angle(angle4 + v4*1.8/3.1416)
                pos4.x = math.sin(math.radians(angle4)) * radius1
                pos4.y = math.cos(math.radians(angle4)) * radius1
                # rotate the ship
                delta_x = (pos4.x - old_pos4.x)
                delta_y = (pos4.y - old_pos4.y)
                rangle = math.atan2(delta_y, delta_x)
                rangled = wrap_angle(-math.degrees(rangle))
                scratch_car = pygame.transform.rotate(car40LB, rangled)
                # draw the ship
                width4, height4 = scratch_car.get_size()
                x = 550 - pos4.y - width4 // 2
                y = 450 + pos4.x - height4 // 2
                screen.blit(scratch_car, (x, y))
                if angle4 >= 88.5:
                    fdir4 = 2
                    yw[3] = 510
                    xw[3] = 520
        if c[3] == 0:
            if yw[3] <= 551:
                yw[3] = yw[3] + v4
            else:
                v4 = v20
                yw[3] = yw[3] + v4
            screen.blit(car40, (xw[3], yw[3]))
        if c[3] == 1:
            if fdir4 == 1:
                yw[3] = yw[3] + v4
                if yw[3] >= 415:
                    fdir4 = 0
                    angle4 = 0.0
                    pos4 = Point(0, 0)
                    old_pos4 = Point(0, 0)
                if 450 - 60 - yw[3] >= dd[3]:
                    screen.blit(car40, (xw[3], yw[3]))
                else:
                    screen.blit(car40RB, (xw[3], yw[3]))
            if fdir4 == 2:
                if xw[3] >= 390:
                    xw[3] = xw[3] - v4
                else:
                    v4 = v20
                    xw[3] = xw[3] - v4
                if xw[3] >= 100:
                    screen.blit(car40R, (xw[3], 460))
                else:
                    screen.blit(car40BR, (xw[3], 460))
            if fdir4 == 0:
                # move the ship
                angle4 = wrap_angle1(angle4 - v4*3.6/3.1416)
                pos4.x = math.sin(math.radians(angle4)) * radius2
                pos4.y = math.cos(math.radians(angle4)) * radius2
                # rotate the ship
                delta_x = (pos4.x - old_pos4.x)
                delta_y = (pos4.y - old_pos4.y)
                rangle = math.atan2(delta_y, delta_x)
                rangled = wrap_angle1(-math.degrees(rangle))
                scratch_car = pygame.transform.rotate(car40RB, rangled)
                # draw the ship
                width4, height4 = scratch_car.get_size()
                x = 450 + pos4.y - width4 // 2
                y = 450 - pos4.x - height4 // 2
                screen.blit(scratch_car, (x, y))
                if angle4 <= -86:
                    fdir4 = 2
                    xw[3] = 420
                    yw[3] = 460

        DT = ["左转","直走","右转"]
        if 450 - xw[0] - 60 <= dd[0]:
            print_text(font, 0, 25, "一号车"+DT[c[0]+1]+"v1: " + "{:.2f}".format(v1 * 6*3.6) + "km/h")
        elif 450 - xw[0] - 60 > dd[0]:
            print_text(font, 0, 25, "         v1: " + "{:.2f}".format(vv[0] / 10*3.6) + "km/h")
        if yw[1] - 550 <= dd[1]:
            print_text(font, 0, 50, "二号车"+DT[c[1]+1]+"v2: " + "{:.2f}".format(v2 * 6*3.6) + "km/h")
        elif yw[1] - 550 > dd[1]:
            print_text(font, 0, 50, "         v2: " + "{:.2f}".format(vv[1] / 10*3.6) + "km/h")
        if xw[2] - 550 <= dd[2]:
            print_text(font, 0, 75, "三号车"+DT[c[2]+1]+"v3: " + "{:.2f}".format(v3 * 6*3.6) + "km/h")
        elif xw[2] - 550 > dd[2]:
            print_text(font, 0, 75, "         v3: " + "{:.2f}".format(vv[2] / 10*3.6) + "km/h")
        if 450 - yw[3] - 60 <= dd[3]:
            print_text(font, 0, 100, "四号车"+DT[c[3]+1]+"v4: " + "{:.2f}".format(v4 * 6*3.6) + "km/h")
        elif 450 - yw[3] - 60 > dd[3]:
            print_text(font, 0, 100, "         v4: " + "{:.2f}".format(vv[3] / 10*3.6) + "km/h")

        t2 = time.perf_counter() - t
        if t2 >= 10:
            break
        pygame.display.update()
        # remember position
        old_pos1.x = pos1.x
        old_pos1.y = pos1.y
        old_pos2.x = pos2.x
        old_pos2.y = pos2.y
        old_pos3.x = pos3.x
        old_pos3.y = pos3.y
        old_pos4.x = pos4.x
        old_pos4.y = pos4.y