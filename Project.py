# -*- coding: utf-8 -*-
from visual import *
from visual.graph import *

#PARAMETER#################################################################
G = 6.67408 * (10**-11)  #萬有引力常數 (m^3 * kg^-1 * s ^ -2)
g = 9.8             #重力加速度 9.8 m/s^2   後面有函式改這個值
bottomRadius = 3700   #火箭底面半徑(m)
RocketHeight = 70000       #火箭長度(m)

RocketMass = 200.0    #火箭淨重 (kg)

Fuel1Mass = 800.0      #燃料1重量 (kg)
Stage1SepHeight = 3000000  #火箭1脫節高度(m)
Fuel2Mass = 700.0      #燃料2重量 (kg)

Stage = 1 #階段

CurrentMass = RocketMass + Fuel1Mass + Fuel2Mass #後面有函式改這個值
FuelEmitPS = 0.25  #燃料每秒排放質量 (kg)
FuelEmitSpd = 4200.0   #燃料噴射速度(m/s)

InitV = vector(0, 1, 0) #火箭初始速度
#k = 0.1487630009487594878787878787000000800092000 #空阻係數
Graph_Tmax = 3000 #-t圖的x軸極限
scene_Range = 8700000 #攝影機拍攝範圍
EarthRadius = 6371000.0 ; #地球半徑 (m)
EarthMass = 5.97237 * (10**24) #地球質量(kg)

dt = 0.04     #時間間隔
t = 0.0
#INIT_SCENE#####################################################################
scene = display(title='View',width=600, height=600, background=(0,0,0),
                center=(0,1000,0),range=scene_Range)#設定畫面

y_t = gdisplay(x=600,y=0,width=300,height=300,     #畫y-t圖
              title='x-t', xtitle='t', ytitle='Altitude (m)',
              foreground=color.black,background=color.white,
              xmax=Graph_Tmax, xmin=0, ymax=10000, ymin=0)
f1 = gcurve(color=color.red)

v_t = gdisplay(x=900,y=0,width=300,height=300,   #畫v-t圖
              title='vy-t', xtitle='t', ytitle='Speed (m/s)',
              foreground=color.black,background=color.white,
              xmax=Graph_Tmax, xmin=0, ymax=10000, ymin=0)
f2 = gcurve(color=color.red)

M_t = gdisplay(x=600,y=300,width=300,height=300,   #畫M-t圖
              title='M-t', xtitle='t', ytitle='RocketMass (kg)',
              foreground=color.black,background=color.white,
              xmax=Graph_Tmax, xmin=0, ymax=3000, ymin=0)
f3 = gcurve(color=color.red)

a_t = gdisplay(x=900,y=300,width=300,height=300,   #畫a-t圖
              title='a-t', xtitle='t', ytitle='ay (m/s^2)',
              foreground=color.black,background=color.white,
              xmax=Graph_Tmax, xmin=0, ymax=1000, ymin=-0.1)
f4 = gcurve(color=color.red)

#INIT####################################################################
floor = box(length = 28, height = 0.01, width = 28, color = color.green)  #畫地板
earth = sphere(radius = EarthRadius, pos = (0,-EarthRadius, 0), material = materials.earth )
rocket = cone(radius = bottomRadius, color=color.yellow,
              make_trail= True, trail_type="points", interval=1000, retain = 5000) #畫

botLabel = label(pos=(0,0,0), text='Text')

Yee = text(text='Yee', align='center', height= 7, depth=-0.93, color=color.green, pos = vector(0,4,0)) #Yee.

rocket.pos = vector(0, 0, 0)        #初始位置
rocket.axis = vector(0, RocketHeight, 0)
rocket.v = InitV      #初速


def calc_g():
    #print G * CurrentMass * EarthMass / ( (rocket.pos.y+EarthRadius) ** 2)
    return G * CurrentMass * EarthMass / ( (rocket.pos.y+EarthRadius) ** 2)

def calc_CurrentMass():
    return RocketMass + Fuel1Mass + Fuel2Mass

#LOOP 1######################################################################
while Stage == 1: #phase 1
    rate(6666)   #每一秒跑  次
    t = t + dt    #timer

    #燃料1噴射########################################################
    # M*Pre_ball.v.y = (M-dm)*ball.v.y+dm*(ball.v.y-u)  動量守恆
    if Fuel1Mass > 0: #燃料噴射
        delta_v = FuelEmitPS * FuelEmitSpd / CurrentMass #速度增加量, according to the above formula(F=ma not working)
        Fuel1Mass -= FuelEmitPS
    else:
        FuelMass = 0
        delta_v = 0
    a = delta_v/dt
    if rocket.pos.y > 0:
        a -= g
    #if a < 0 : a = 0

    #如果墜地##########################################################
    if rocket.pos.y <= 0: #墜地
        rocket.pos.y = 0; rocket.v.y = 0; #a = 0;
    print a
    #如果高度達第二次噴射#####################################################
    if rocket.pos.y > Stage1SepHeight:
        Stage = 2

    #基本運算#############################################################
    rocket.v.y += a*dt
    CurrentMass = calc_CurrentMass()
    rocket.pos += rocket.v*dt
    g = calc_g()

    #畫圖#############################################################
    f1.plot( pos=(t, rocket.pos.y))
    f2.plot( pos=(t, rocket.v.y))
    f3.plot( pos=(t, CurrentMass))
    f4.plot( pos=(t, a))
    scene.center = rocket.pos

    #ui設計################################################################
    botLabel.pos = (scene.center.x - 70, scene.center.y - 70, 0);
    botLabel.text = "Stage " + str(Stage)


#LOOP 2######################################################################
while Stage == 2: #phase 1
    rate(6666)   #每一秒跑  次
    t = t + dt    #timer

    #燃料2噴射########################################################
    # M*Pre_ball.v.y = (M-dm)*ball.v.y+dm*(ball.v.y-u)  動量守恆
    if Fuel2Mass > 0: #燃料噴射
        delta_v = FuelEmitPS * FuelEmitSpd / CurrentMass #速度增加量, according to the above formula(F=ma not working)
        Fuel2Mass -= FuelEmitPS
    else:
        FuelMass = 0
        delta_v = 0
    a = delta_v/dt - g
    #if a < 0 : a = 0

    #如果墜地##########################################################
    if rocket.pos.y < 0 and a < 0: #墜地
        rocket.pos.y = 0; rocket.v.y = 0; a = 0;

    #基本運算#############################################################
    rocket.v.x += a*dt
    CurrentMass = calc_CurrentMass()
    rocket.pos += rocket.v*dt
    g = calc_g()

    #畫圖############################################################
    f1.plot( pos=(t, rocket.pos.y))
    f2.plot( pos=(t, rocket.v.y))
    f3.plot( pos=(t, CurrentMass))
    f4.plot( pos=(t, a))
    scene.center = rocket.pos

    #ui設計################################################################
    botLabel.pos = (scene.center.x - 70, scene.center.y - 70, 0);
    botLabel.text = "Stage " + str(Stage)
