# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 20:00:11 2017

Usage:
define the classes of Point, Graph, Obstacle, Environment.

@author: YI HOU
"""

import sys
import random

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __str__(self):
        return ("("+str(self.x)+","+str(self.y)+")")
    def __eq__(self,other):
        return other.x-0.00001<=self.x<=other.x+0.00001 and other.y-0.00001<=self.y<=other.y+0.00001
    def __cmp__(self,other):
        if other.x-0.00001<=self.x<=other.x+0.00001 and other.y-0.00001<=self.y<=other.y+0.00001:  
            return 0
        elif self.x<other.x or (self.x==other.x and self.y<other.y):  
            return -1
        elif self.x>other.x or (self.x==other.x and self.y>other.y):  
            return 1 
    def __lt__(self,other):
        if self.x<other.x or (self.x==other.x and self.y<other.y): 
            return 1
        else:
            return 0
    def __gt__(self,other):
        if self.x>other.x or (self.x==other.x and self.y>other.y):
            return 1
        else:
            return 0
    def __hash__(self):
        return hash(str(self.x*1.0)+","+str(self.y*1.0))
    def distance(self,p): # square of distance 
        return ((p.x-self.x)**2+(p.y-self.y)**2)
        
class Graph:
    def __init__(self,p):
        #p is the initial point
        self.VertexIndex={p:0}
        self.IndexVertex={0:p}
        self.edges=[]
        self.VertexNumber=1
    def __str__(self):
        output=""
        for i in range(self.VertexNumber):
            output=output+str(i)+":"+str(self.IndexVertex[i])+","
        output=output[:-1]+"\n"
        for edge in self.edges:
            output=output+"("+str(edge[0])+","+str(edge[1])+"),"
        return output[:-1] #to be contonue

    def addVertex(self,p):
        self.VertexIndex[p]=self.VertexNumber
        self.IndexVertex[self.VertexNumber]=p
        self.VertexNumber=self.VertexNumber+1

    def addEdge(self,edge):
        if ( (edge[0] in self.IndexVertex) and (edge[1] in self.IndexVertex) ):
            self.edges.append(edge)
        else:
            print("The vertices are not in the graph!")
            sys.exit(1)

    def removeEdge(self,edge):
        if edge in self.edges:
            self.edges.remove(edge)

    def getVertex(self,index):
        return self.IndexVertex[index] if (index in self.IndexVertex) else Point(-1,-1)
    def getIndex(self,point):
        return self.VertexIndex[point] if (point in self.VertexIndex) else -1


class Obstacle:
    def __init__(self,points):
        self.VertexIndex={}
        self.IndexVertex={}
        for i in range(len(points)):
            self.VertexIndex[points[i]]=i+1
            self.IndexVertex[i+1]=points[i]
        self.vertexNumber=len(points)
        self.number=len(points)
    def __str__(self):
        output="Obstacle:\n"
        for i in range(self.vertexNumber):
            output=output+str(i+1)+":"+str(self.IndexVertex[i+1])+"|"
        return output

    def getVertex(self,index):
        return self.IndexVertex[index] if (index in self.IndexVertex) else Point(-1,-1)
    def getIndex(self,point):
        return self.VertexIndex[point] if (point in self.VertexIndex) else -1



class Environment:
    def __init__(self,x,y,obs,start,goal):
        self.x_max=x
        self.y_max=y
        self.obstacles=obs
        #self.checkObstacleConflict()  # Deal with conflict, in which there are more than two vertices on a vertical line, namely, share the same x.
        self.start=start
        self.goal=goal
    def __str__(self):
        output="Environment: rectangle from (0,0) to ("+str(self.x_max)+","+str(self.y_max)+")\n"
        for obs in self.obstacles:
            output=output+str(obs)+"\n"
        output=output+"start point:"+str(self.start)+" end point:"+str(self.goal)+"\n"
        return output
        
    def checkObstacleConflict(self):
        # Check if there are more than two vertices on a vertical line, namely, share the same x.
        vx = set()
        for obs in self.obstacles:
            for v in obs.VertexIndex:
                if v.x in vx:
                    print("***v.x",v.x)
                    print("###set:",vx)
                    rand=random.uniform(-0.01,0.01)
                    newpoint=Point(v.x+rand,v.y)
                    index = obs.getIndex(v)
                    obs.IndexVertex[index]=newpoint
                    del(obs.VertexIndex[v])
                    obs.VertexIndex[newpoint]=index
                    vx.add(newpoint.x)
                    print("[__init__ in Environment] One vertex conflict solved by adding a random epislon "+str(rand))
                else:
                    vx.add(v.x)

class SweepLine:
    def __init__(self,x,middle,vertex,type):
        self.x=x
        self.middle=middle
        self.vertex=vertex
        self.type=type
    def __str__(self):
        output="Sweep Line type="+str(self.type)+" x="+str(self.x)+"\nvertex="+str(self.vertex)+"\nmiddle="+str(self.middle)
        return output
    def __eq__(self,other):
        return self.x==other.x and self.middle==other.middle and self.vertex==other.vertex and self.type==other.type