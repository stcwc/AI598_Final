# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 20:00:11 2017

Vertical Cell Decomposition Algorithm

@author: Wangchao Sheng
"""

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def parse(path):
    file = open(path)
    file.readline()
    boundary = Point(300,200)  # boundary is fixed in this question.
    temp = []
    while True:
        line = file.readline()
        if line == None or line == "":
            break
        temp.append(line)
    start, goal = Point(helper(temp[-1])[0],helper(temp[-1])[1]),Point(helper(temp[-1])[2],helper(temp[-1])[3])
    temp = temp[:-1] 
    obstacles = []
    for i in temp:
        t = helper(i)
        p = []
        for j in range(len(t)//2):
            p.append(Point(t[j*2],t[j*2+1]))
        obstacles.append(p)
    return boundary, obstacles, start, goal


def helper(string):
    return string.replace("(","").replace(")","").replace("\n","").split(",")
    
boundary, obstacles, start, goal = parse("test.txt")

