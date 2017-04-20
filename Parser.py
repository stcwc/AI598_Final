# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 20:00:11 2017

Usage:
given an input, parse it into an environment object.

@author: Wangchao Sheng
"""

from Util import Point, Obstacle, Environment
import random

def parse(path):

    file = open(path)
    line = file.readline()
    line1=line.replace("(","").replace(")","").replace("\n","").split(",")
    
    #boundary = Point(300,200)  # boundary is fixed in this question.
    x_max, y_max = int(line1[4]), int(line1[5])  # boundary is fixed in this question.
    temp = []
    while True:
        line = file.readline()
        if line == None or line == "":
            break
        temp.append(line)
    lastline = (temp[-1]).replace("(","").replace(")","").replace("\n","").split(",")
    start, goal = Point(float(lastline[0]),float(lastline[1])),Point(float(lastline[2]),float(lastline[3]))
    temp = temp[:-1]

    obstacles = []
    vx=set() # To deal with vertices with the same x value.
    for i in temp:
        t = i.replace("(","").replace(")","").replace("\n","").split(",")
        p = []
        for j in range(len(t)//2):
            if t[j*2] not in vx:    
                p.append(Point(float(t[j*2]),float(t[j*2+1])))
                vx.add(t[j*2])
            else:
                rand=random.uniform(-0.01,0.01)
                print("[Warning] Two vertices have the same x value: "+str(t[j*2])+". One has been changed to "+str(float(t[j*2])+rand)+".")
                p.append(Point(float(t[j*2])+rand,float(t[j*2+1])))
        obstacles.append(Obstacle(p))
    return Environment(x = x_max, y = y_max, obs = obstacles, start = start, goal = goal)



