# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 20:00:11 2017

Usage:
given an input, parse it into an environment object.

@author: Wangchao Sheng
"""

from Util import Point, Obstacle, Environment


def parse(path):

    file = open(path)
    line = file.readline()
    #boundary = Point(300,200)  # boundary is fixed in this question.
    x_max, y_max = 300, 200  # boundary is fixed in this question.

    temp = []
    while True:
        line = file.readline()
        if line == None or line == "":
            break
        temp.append(line)
    lastline = (temp[-1]).replace("(","").replace(")","").replace("\n","").split(",")
    start, goal = Point(lastline[0],lastline[1]),Point(lastline[2],lastline[3])
    temp = temp[:-1]

    obstacles = []
    for i in temp:
        t = i.replace("(","").replace(")","").replace("\n","").split(",")
        p = []
        for j in range(len(t)//2):
            p.append(Point(t[j*2],t[j*2+1]))
        obstacles.append(Obstacle(p))
    return Environment(x = x_max, y = y_max, obs = obstacles, start = start, goal = goal)



