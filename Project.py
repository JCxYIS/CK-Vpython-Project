# -*- coding: UTF-8 -*-
from visual import *
from visual.graph import *

#PARAMETER#################################################################
G = 6.67408 * (10**-11)  #萬有引力常數 (m^3 * kg^-1 * s ^ -2)
g = vector(0, -9.8, 0)      #重力加速度 9.8 m/s^2   後面有函式改這個值
bottomRadius = 12   #火箭底面半徑(m)
RocketHeight = 70       #火箭長度(m)

RocketMass = 50.0    #火箭淨重 (kg)
Fuel1Mass = 1100.0      #燃料1重量 (kg)
EarthOrbit = 3000 * 1000 #軌道高度(m)
Stage1SepHeight = 3000 * 1000  #火箭1脫節高度(m)
Fuel2Mass = 100.0      #燃料2重量 (kg)


Stage = 0 #階段 後面有函式改這個值

CurrentMass = RocketMass + Fuel1Mass + Fuel2Mass #後面有函式改這個值
Fuel1EmitPS = 0.0053  #燃料1每秒排放質量 (kg)
Fuel1EmitSpd = 4500.0   #燃料1噴射速度(m/s)
Fuel2EmitPS = 0.0009  #燃料2每秒排放質量 (kg)
Fuel2EmitSpd = 9000.0   #燃料2噴射速度(m/s)

InitV = vector(0, 0, 0) #火箭初始速度

Graph_Tmax = 1500 #-t圖的x軸極限
scene_Range = 870000 #攝影機拍攝範圍
RocketTrailStyle = "points" #"points" or "trail" or "PoiCurve"
SetPointFreq = 10000 #cmd紀錄/軌跡 時間間隔

EarthRadius = 6371 * 1000.0 ; #地球半徑 (m)
EarthMass = 5.97237 * (10**24) #地球質量(kg)

dt = 0.002     #時間間隔
t = 0.0
RATE = 20000 #迴圈執行速度

dist = 0.0
radiavector = vector(0.0,0.0,0.0)
RV = 0
graphClosed = False
Stat = "null"

#INIT_SCENE & GRAPH##################################################################
scene = display(width=600, height=600, background=(0,0,0),
                center=(0,1000,0),range=scene_Range)#設定畫面
scene.title = "Launch! With our Hopes and Dreams!"

y_t = gdisplay(x=600,y=0,width=300,height=300,     #畫y-t圖
              title='x-t', xtitle='t', ytitle='Altitude (m)',
              foreground=color.black,background=color.white,
              xmax=Graph_Tmax, xmin=0, ymax=Stage1SepHeight, ymin=0)
f1 = gcurve(color=color.red)

v_t = gdisplay(x=900,y=0,width=300,height=300,   #畫v-t圖
              title='vy-t', xtitle='t', ytitle='Speed (m/s)',
              foreground=color.black,background=color.white,
              xmax=Graph_Tmax, xmin=0, ymax=10000, ymin=0)
f2 = gcurve(color=color.red)

M_t = gdisplay(x=600,y=300,width=300,height=300,   #畫M-t圖
              title='M-t', xtitle='t', ytitle='RocketMass (kg)',
              foreground=color.black,background=color.white,
              xmax=Graph_Tmax, xmin=0, ymax=CurrentMass * 1.2, ymin=0)
f3 = gcurve(color=color.red)

a_t = gdisplay(x=900,y=300,width=300,height=300,   #畫a-t圖
              title='a-t', xtitle='t', ytitle='ay (m/s^2)',
              foreground=color.black,background=color.white,
              xmax=Graph_Tmax, xmin=0, ymax=100, ymin=0)
f4 = gcurve(color=color.red)

#INIT####################################################################
floor = box(length = 28, height = 0.01, width = 28, color = color.green)  #畫地板
earth = sphere(radius = EarthRadius, pos = (0,-EarthRadius, 0), material = materials.earth )
rocket = cone(radius = bottomRadius, color=color.yellow,
          make_trail= True, trail_type="points", interval=SetPointFreq*10, retain = 666) #畫

OrbitCircle = curve( color = (40.0/255, 40.0/255,40.0/255) )
for N in range(0, 360, 1):
    r = EarthOrbit + EarthRadius
    OrbitCircle.append( pos =(r*cos(N*pi/180), r*sin(N*pi/180) - EarthRadius, 0) )

if RocketTrailStyle == "curve":
    rocket = cone(radius = bottomRadius, color=color.yellow,
              make_trail= True, trail_type="curve", interval=1, retain = 666666) #畫
elif RocketTrailStyle == "PoiCurve":
    rocket = cone(radius = bottomRadius, color=color.yellow,
              make_trail= True, trail_type="points", interval=3, retain = 666666) #畫
else:
    rocket = cone(radius = bottomRadius, color=color.yellow,
              make_trail= True, trail_type="points", interval=SetPointFreq*10, retain = 444) #畫



Yee = text(text='Yee', align='center', height= 99999, depth=48763, color=color.green, pos = vector(0,0,-201700)) #Yee.

rocket.pos = vector(0, 0, 0)        #初始位置
rocket.axis = vector(0, RocketHeight, 0)
rocket.v = InitV      #初速
rocket.a = vector(0,0,0)

UIprintCD = SetPointFreq

#DEFINE#########################################################################
def calc_g(dist): #PARA: distance(vec3)
    #print G , CurrentMass , EarthMass , rocket.pos.y, EarthRadius
    #print G  * EarthMass / ( (rocket.pos.y+EarthRadius) ** 2)
    return -G * EarthMass / ( dist ** 2)

def calc_CurrentMass():
    return RocketMass + Fuel1Mass + Fuel2Mass

def Let_Rocket_Fly():
    global rocket, CurrentMass, dist, radiavector, g, RV
    rocket.v += rocket.a*dt
    CurrentMass = calc_CurrentMass()
    rocket.pos += rocket.v*dt

    #calc g#
    dist = ((rocket.x-earth.x)**2+(rocket.y-earth.y)**2+(rocket.z-earth.z)**2)**0.5 #距離純量
    radiavector = (rocket.pos-earth.pos)/dist #距離(向量)
    g = calc_g(dist) * radiavector
    #print g

    #SPIN#
    RV = ((rocket.v.x)**2+(rocket.v.y)**2+(rocket.v.z)**2)**0.5
    AntiRV = 1 / RV
    rocket.axis = rocket.v * AntiRV * RocketHeight

def Draw_pic(): #繪畫圖表 & set scene focus
    global graphClosed;
    if t < Graph_Tmax:
        Altitude = ((rocket.x-earth.x)**2+(rocket.y-earth.y)**2+(rocket.z-earth.z)**2)**0.5 - EarthRadius
        Speed = ((rocket.v.x)**2+(rocket.v.y)**2+(rocket.v.z)**2)**0.5
        Acc = ((rocket.a.x)**2+(rocket.a.y)**2+(rocket.a.z)**2)**0.5
        f1.plot( pos=(t, Altitude))
        f2.plot( pos=(t, Speed))
        f3.plot( pos=(t, CurrentMass))
        f4.plot( pos=(t, Acc))
    elif graphClosed == False: #刪除圖表(因為爆表了)
        y_t.display.delete();
        v_t.display.delete();
        a_t.display.delete();
        M_t.display.delete();
        print ("Deleting Gdisplay...")
        graphClosed = True


    scene.center = rocket.pos

def print_UI():
    global UIprintCD
    UIprintCD -= 1
    if UIprintCD <= 0:
        UIprintCD = SetPointFreq
        Altitude = ((rocket.x-earth.x)**2+(rocket.y-earth.y)**2+(rocket.z-earth.z)**2)**0.5 - EarthRadius
        Speed = ((rocket.v.x)**2+(rocket.v.y)**2+(rocket.v.z)**2)**0.5
        Acc = ((rocket.a.x)**2+(rocket.a.y)**2+(rocket.a.z)**2)**0.5
        Dialogue  = "Stage "+ str(Stage) + " | "
        Dialogue += "Time " + str("%.0f" % t) + "s | "
        Dialogue += "Mass " + str("%.3f" % CurrentMass) + "kg | "
        Dialogue += "Alt. " + str("%.3f" % (Altitude/1000)) + "km | "
        Dialogue += "Spd. " + str("%.3f" % Speed) + "m/s | "
        Dialogue += "Acc. " + str("%.3f" % Acc) + "m/(s**2) | "
        Dialogue += "Stat: " + Stat
        print Dialogue #cmd紀錄

def KeyInput(Event):  # keyboard interrupt callback function,
    global RATE, dt , Stage    # define the global variables that you want to change by this function
    RATEmod = {'-': -66, '=': 66}
    dtmod = {'[': 1.0/1.1, ']': 1.1}
    Stagemod = {' ': 1}

    s = Event.key
    if s in RATEmod :
        RATE += RATEmod[s]
        print "Modified RATE to ", RATE
    if s in dtmod:
        dt *= dtmod[s]
        print "Modified dt to ", dt
    if s in Stagemod:
        Stage += Stagemod[s]
scene.bind('keydown', KeyInput) # the binding method

#LOOP 0######################################################################
print "### Stage 0: Init ###"
while  Stage == 0:
    rate(RATE)
    #畫圖#############################################################
    Draw_pic()
    #ui設計################################################################
    print_UI()

#LOOP 1######################################################################
print "### Stage 1: S1 I"
while Stage == 1: #phase 1
    rate(RATE)   #每一秒跑  次
    t = t + dt    #timer

    #燃料1噴射########################################################
    # M*Pre_ball.v.y = (M-dm)*ball.v.y+dm*(ball.v.y-u)  動量守恆
    if Fuel1Mass > 0: #燃料噴射
        delta_v = Fuel1EmitPS * Fuel1EmitSpd / CurrentMass #速度增加量, according to the above formula(F=ma not working)
        Fuel1Mass -= Fuel1EmitPS
    else:
        Fuel1Mass = 0
        delta_v = 0
    rocket.a = vector(0, delta_v/dt, 0)

    if rocket.pos.y > 0:
        rocket.a += g
    #if a < 0 : a = 0


    #如果高度達第二次噴射#####################################################
    if rocket.pos.y > Stage1SepHeight:
        Stage = 2

    #基本運算#############################################################
    Let_Rocket_Fly()

    #如果墜地##########################################################
    if(dist < EarthRadius and RV >= 1):
        print "Ahhhhh!!! Rocket Crushed!!"
        Stage = 66666
    elif dist < EarthRadius:
        rocket.y = 0

    #畫圖#############################################################
    Draw_pic()

    #ui設計################################################################
    print_UI()

while Stage == 2:
    Fuel1Mass = 0;
    if Fuel2Mass > 0: #燃料噴射
        delta_v = Fuel2EmitPS * Fuel2EmitSpd / CurrentMass #速度增加量, according to the above formula(F=ma not working)
        Fuel2Mass -= Fuel2EmitPS
    else:
        Stage = 3;
    rocket.a = vector(delta_v/dt , 0, 0)
    rocket.a += g

#LOOP 2######################################################################
while Stage == 3:
    rate(RATE)   #每一秒跑  次
    t = t + dt    #timer

    #燃料2噴射########################################################
    #目標速度 (G*M/H)**0.5
    Altitude = ((rocket.x-earth.x)**2+(rocket.y-earth.y)**2+(rocket.z-earth.z)**2)**0.5 - EarthRadius
    DistanceToCircle = Altitude - EarthOrbit; #比軌道"高"幾m

    delta_v = 0;
    # M*Pre_ball.v.y = (M-dm)*ball.v.y+dm*(ball.v.y-u)  動量守恆
    Speed = ((rocket.v.x)**2+(rocket.v.y)**2+(rocket.v.z)**2)**0.5
    VectorToEarth =  earth.pos - rocket.pos;
    #print (G*EarthMass/EarthOrbit)**0.5
    if DistanceToCircle > 0: #比軌道高
        if Speed < (G*EarthMass/EarthOrbit)**0.5:
            Stat = "Too High, Too Slow"
            delta_v = Fuel2EmitPS * Fuel2EmitSpd * norm(-VectorToEarth) / CurrentMass;
            #Fuel2Mass -= Fuel2EmitPS
        elif Speed > (G*EarthMass/EarthOrbit)**0.5:
            Stat = "Too High, Too Fast"
            delta_v = Fuel2EmitPS * Fuel2EmitSpd * norm(VectorToEarth) / CurrentMass;
            #Fuel2Mass -= Fuel2EmitPS
        elif Speed == (G*EarthMass/EarthOrbit)**0.5:
            Stat = "Too High, Good Spd"
    elif DistanceToCircle < 0:
        if Speed < (G*EarthMass/EarthOrbit)**0.5:
            Stat = "Too Low, Too Slow"
            delta_v = Fuel2EmitPS * Fuel2EmitSpd * norm(-VectorToEarth) / CurrentMass;
            GoUpSpd = vector(-rocket.v.y, rocket.v.x, 0); #與火箭速度垂直的速度向量
            delta_v += Fuel2EmitPS * Fuel2EmitSpd * norm(GoUpSpd) / CurrentMass;
            #Fuel2Mass -= 2*Fuel2EmitPS
        elif Speed > (G*EarthMass/EarthOrbit)**0.5:
            Stat = "Too Low, Too Fast"
            GoUpSpd = vector(-rocket.v.y, rocket.v.x, 0); #與火箭速度垂直的速度向量
            delta_v = Fuel2EmitPS * Fuel2EmitSpd * norm(VectorToEarth) / CurrentMass;
            delta_v += Fuel2EmitPS * Fuel2EmitSpd * norm(GoUpSpd) / CurrentMass;
            #Fuel2Mass -= 2*Fuel2EmitPS
        elif Speed == (G*EarthMass/EarthOrbit)**0.5:
            GoUpSpd = vector(-rocket.v.y, rocket.v.x, 0); #與火箭速度垂直的速度向量
            delta_v += Fuel2EmitPS * Fuel2EmitSpd * norm(GoUpSpd) / CurrentMass;
            #Fuel2Mass -= Fuel2EmitPS
            Stat = "Too Low, Good Spd"
    elif DistanceToCircle == 0:
        if Speed < (G*EarthMass/EarthOrbit)**0.5:
            Stat = "Good Alt, Too Slow"
            delta_v = Fuel2EmitPS * Fuel2EmitSpd * norm(-VectorToEarth) / CurrentMass;
            #Fuel2Mass -= Fuel2EmitPS
        elif Speed > (G*EarthMass/EarthOrbit)**0.5:
            Stat = "Good Alt, Too Fast"
            delta_v = Fuel2EmitPS * Fuel2EmitSpd * norm(VectorToEarth) / CurrentMass;
            #Fuel2Mass -= Fuel2EmitPS
        elif Speed == (G*EarthMass/EarthOrbit)**0.5:
            Stat = "Perfect!!!"

    '''
    if Fuel2Mass > 0: #燃料噴射
        delta_v = Fuel2EmitPS * Fuel2EmitSpd / CurrentMass #速度增加量, according to the above formula(F=ma not working)
        Fuel2Mass -= Fuel2EmitPS
    else:
        Fuel2Mass = 0
        delta_v = 0
    '''
    rocket.a = delta_v/dt
    rocket.a += g

    #基本運算#############################################################
    Let_Rocket_Fly()

    #如果墜地##########################################################
    if(dist < EarthRadius):
        print "Ahhhhh!!! Rocket Crushed!!"
        Stage = 66666

    #畫圖############################################################
    Draw_pic()

    #ui設計################################################################
    print_UI()




while Stage >= 66666: #希望破滅後的世界
    rate(1)
