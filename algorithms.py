# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 20:00:11 2017

Usage:
Achieve Vertical Cell Decomposition and RRT

@author: YI
"""

from Util import Point, Graph, Obstacle, Environment, SweepLine
from Geometry import GetIntersection, NearestPoint
import random
import sys

def RRT(E, G, I):
    # add first vertex to graph
    '''
    not test yet
    not test yet
    not test yet
    not test yet
    not test yet
    '''
    for i in range(I):
        if i == I-1:
            new_vertex = E.goal
        else:
            new_vertex = Point(random.uniform(0, E.x_max),
                               random.uniform(0, E.y_max))
        print("new_vertex:"+str(new_vertex))
        nearest_point = E.start
        edgeLocation = (0, 0)  # on which edge does the nearest_point locate
        for edge in G.edges:
            nearest_temp = NearestPoint(
                G.IndexVertex[edge[0]], G.IndexVertex[edge[1]], new_vertex)
            if new_vertex.distance(nearest_temp) < new_vertex.distance(nearest_point):
                nearest_point = nearest_temp  # update nearest point and the edge location
                edgeLocation = edge
                print("update nearest_temp on the edge:", edge)
    #	print("\nfinish searching nearest_point, result:\n")
    #	print("nearest_temp:"+str(nearest_point))
    #	print("edge location:",edgeLocation)
        if min(G.IndexVertex[edgeLocation[0]].x, G.IndexVertex[edgeLocation[1]].x) < nearest_point.x < max(G.IndexVertex[edgeLocation[0]].x, G.IndexVertex[edgeLocation[1]].x):
            # if nearest_point is on the middle of line, should remove original
            # edge and add new vertex and edges
            G.removeEdge(edgeLocation)
            print("remove edge:"+str(edgeLocation))
            G.addVertex(nearest_point)
            print("add middle nearest_point:"+str(nearest_point))
            G.addEdge((edgeLocation[0], G.VertexIndex[nearest_point]))
            print("add edge:"+str(edgeLocation[0])+str(G.VertexIndex[nearest_point]))
            G.addEdge((edgeLocation[1], G.VertexIndex[nearest_point]))
            print("add edge:"+str(edgeLocation[1])+str(G.VertexIndex[nearest_point]))
        print("nearest_point:"+str(nearest_point))
        intersection = Point(new_vertex.x, new_vertex.y)
        # calculate the intersection of line new_vertex-nearest_point and
        # obstacles
        for obs in E.obstacles:
            for index in range(obs.number-1):
                inter_temp = GetIntersection(nearest_point, new_vertex, obs.IndexVertex[
                                             index+1], obs.IndexVertex[index+2])
                print("check:"+str(nearest_point)+str(new_vertex)+str(obs.IndexVertex[obs.number])+str(obs.IndexVertex[1]))
                print("inter_temp:"+str(inter_temp))
                if inter_temp != Point(-1, -1):  # there IS intersection
                    if ((intersection.x-nearest_point.x)**2+(intersection.y-nearest_point.y)**2) > ((inter_temp.x-nearest_point.x)**2+(inter_temp.y-nearest_point.y)**2):
                        intersection = inter_temp  # inter_temp is closer to nearest_point
            # need sepatate operation for last edge because of CIRCLE
            #print(nearest_point.y==62.6197860825)
            inter_temp = GetIntersection(nearest_point, new_vertex, obs.IndexVertex[obs.number], obs.IndexVertex[1])
            print("check:"+str(nearest_point)+str(new_vertex)+str(obs.IndexVertex[obs.number])+str(obs.IndexVertex[1]))
            print("inter_temp:"+str(inter_temp))
            if inter_temp != Point(-1, -1): 
                if ((intersection.x-nearest_point.x)**2+(intersection.y-nearest_point.y)**2) > ((inter_temp.x-nearest_point.x)**2+(inter_temp.y-nearest_point.y)**2):
                    intersection = inter_temp
        if intersection.distance(nearest_point)>0.001:
            G.addVertex(intersection)
            print("add new_vertex:"+str(intersection))
            G.addEdge((G.VertexIndex[nearest_point], G.VertexIndex[intersection]))
        print(G)
        print("\n")
    if E.goal in G.VertexIndex:
        print("goal cannot be added into the Graph!")
    else:
        print("goal is not in the Graph!")
        print("the graph is:\n"+str(G))
        sys.exit()



def VCD(E, G):
    '''
    transform object!!!
    transform object!!!
    transform object!!!
    add start and goal to graph!!
    add start and goal to graph!!
    add start and goal to graph!!
    add start and goal to graph!!
    '''
    G.addVertex(E.goal)
    SweepLines = []
    all_obs = []
    for obs in E.obstacles:
        for vertex in obs.VertexIndex:
            all_obs.append(vertex)
    all_obs.sort()
    print("obs list:")
    for o in all_obs:
        print(str(o))
    for i in range(len(all_obs)):
        next_vertex = all_obs[i]
        print("\n\nGraph:"+str(G))
        print("SweepLines:")
        for sl in SweepLines:
            print(str(sl))
        print("Now examine obs vertex:"+str(next_vertex))
        type_vertex = 0
        inter_up = E.y_max
        inter_below = 0
        # determine the type of vertex
        for obs in E.obstacles:
            for vertex in obs.VertexIndex:
                if next_vertex == vertex:
                    print("vertex:"+str(vertex))
                    print("obs now:"+str(obs))
                    index = obs.VertexIndex[vertex]
                    pre = Point(-1, -1)
                    pos = Point(-1, -1)
                    # list pre and post vertex
                    if 1 < index < obs.vertexNumber:
                        pre = obs.IndexVertex[index-1]
                        pos = obs.IndexVertex[index+1]
                    elif index == 1:
                        pre = obs.IndexVertex[obs.vertexNumber]
                        pos = obs.IndexVertex[2]
                    else:
                        pre = obs.IndexVertex[obs.vertexNumber-1]
                        pos = obs.IndexVertex[1]
                    # determine the vertex type
                    if (pre.x > vertex.x and pos.x > vertex.x and pre.y > pos.y) or (pre.x < vertex.x and pos.x < vertex.x and pre.y < pos.y):
                        print("type 1")
                        type_vertex = 1
                        inter_up = E.y_max
                        inter_below = 0
                    elif (pre.x > vertex.x and pos.x > vertex.x and pre.y < pos.y):
                        print("type 4")
                        type_vertex = 4
                        inter_up = vertex.y
                        inter_below = vertex.y
                    elif (pre.x < vertex.x and pos.x < vertex.x and pre.y > pos.y):
                        print("type 5")
                        type_vertex = 5
                        inter_up = vertex.y
                        inter_below = vertex.y
                    elif pre.x < vertex.x < pos.x:
                        print("type 3")
                        type_vertex = 3
                        inter_up = vertex.y
                        inter_below = 0
                    elif pos.x < vertex.x < pre.x:
                        print("type 2")
                        type_vertex = 2
                        inter_up = E.y_max
                        inter_below = vertex.y
                    else:
                        print("wrong type!")
                        exit()
        # find the inter_up and inter_below
        for obs in E.obstacles:
            for index in range(obs.number-1):
                inter_temp = GetIntersection(Point(next_vertex.x, 0), Point(
                    next_vertex.x, E.y_max), obs.IndexVertex[index+1], obs.IndexVertex[index+2])
                print("int:"+str(inter_temp))
                print("line:"+str(Point(next_vertex.x, 0))+"-"+str(Point(next_vertex.x, E.y_max))+" and "+str(obs.IndexVertex[index+1])+"-"+str(obs.IndexVertex[index+2]))
                if next_vertex.y < inter_temp.y < inter_up:
                    print("new up:"+str(inter_up))
                    inter_up = inter_temp.y
                elif inter_below < inter_temp.y < next_vertex.y:
                    print("new below:"+str(inter_below))
                    inter_below = inter_temp.y
            # need sepatate operation for last edge because of CIRCLE
            inter_temp = GetIntersection(Point(next_vertex.x, 0), Point(
                next_vertex.x, E.y_max), obs.IndexVertex[obs.number], obs.IndexVertex[1])
            print("int:"+str(inter_temp))
            print("line:"+str(Point(next_vertex.x, 0))+"-"+str(Point(next_vertex.x, E.y_max))+" and "+str(obs.IndexVertex[index+1])+"-"+str(obs.IndexVertex[index+2]))
            if next_vertex.y < inter_temp.y < inter_up:
                inter_up = inter_temp.y
            elif inter_below < inter_temp.y < next_vertex.y:
                inter_below = inter_temp.y
        # second part
        # add vertex and edge to Graph
        if type_vertex == 1 or type_vertex == 2 or type_vertex == 3:
            # denote the middles and vertices of the next sweep line
            if type_vertex == 1:
                middles_y = [(inter_up+next_vertex.y)/2,
                             (inter_below+next_vertex.y)/2]
                middles_yy = [(inter_up+next_vertex.y)/2,
                              (inter_below+next_vertex.y)/2]
                verteices_y = [inter_up, next_vertex.y, inter_below]
            else:
                middles_y = [(inter_up+inter_below)/2]
                middles_yy = [(inter_up+inter_below)/2]
                verteices_y = [inter_up, inter_below]
            # first line
            if len(SweepLines) == 0:
                center = Point(next_vertex.x/2, (E.y_max/2 +
                                                 (middles_y[0]+middles_y[1])/2)/2)
                G.addVertex(center)
                p1 = Point(next_vertex.x, middles_y[0])
                p2 = Point(next_vertex.x, middles_y[1])
                G.addVertex(p1)
                G.addVertex(p2)
                G.addEdge((G.VertexIndex[center], G.VertexIndex[p1]))
                G.addEdge((G.VertexIndex[center], G.VertexIndex[p2]))
                #if possible, add start and goal to graph
                if 0<=E.start.x<next_vertex.x:
                    G.addEdge((0,G.VertexIndex[center]))
                if 0<=E.goal.x<next_vertex.x:
                    G.addEdge((1,G.VertexIndex[center]))
            # not the first line
            else:
                # check every previous sweep line
                while (len(middles_y) != 0):
                    print("middles_y:"+str(middles_y))
                    for i in range(len(SweepLines)-1, -1, -1):
                        pre_l = SweepLines[i]
                        print(len(SweepLines))
                        print(i)
                        print("examine sweep line:"+str(pre_l))
                        # figure out the type of previous sweep line
                        if pre_l.type == 5:
                            continue
                        if pre_l.type == 4:
                            connect_right = []
                            for y in middles_y:
                                inter = Point(-1, -1)
                                for obs in E.obstacles:
                                    for index in range(obs.number-1):
                                        inter_temp = GetIntersection(Point(pre_l.x, pre_l.vertex[0]), Point(
                                            next_vertex.x, y), obs.IndexVertex[index+1], obs.IndexVertex[index+2])
                                        if inter_temp != Point(-1, -1) and inter_temp.distance(Point(pre_l.x, pre_l.vertex[0]))>0.1:
                                            print("obs line: "+str(obs.IndexVertex[index+1])+"-"+str(obs.IndexVertex[index+2]))
                                            inter = inter_temp
                                            print("interection:"+str(inter_temp))
                                            print("distance:"+str(inter_temp.distance(Point(pre_l.x, pre_l.vertex[0]))))
                                    # need seperate operation for last edge
                                    inter_temp = GetIntersection(Point(pre_l.x, pre_l.vertex[0]), Point(
                                        next_vertex.x, y), obs.IndexVertex[obs.number], obs.IndexVertex[1])
                                    if inter_temp != Point(-1, -1) and inter_temp.distance(Point(pre_l.x, pre_l.vertex[0]))>0.1:
                                        print("obs line: "+str(obs.IndexVertex[obs.number])+"-"+str(obs.IndexVertex[1]))
                                        inter = inter_temp
                                        print("interection:"+str(inter_temp))
                                        print("distance:"+str(inter_temp.distance(Point(pre_l.x, pre_l.vertex[0]))))
                                # determine if there is interection
                                if inter == Point(-1, -1):
                                    connect_right.append(y)
                            if len(connect_right) != 0:
                                center = Point(
                                    (pre_l.x+next_vertex.x)/2, sum(connect_right)/len(connect_right))
                                G.addVertex(center)
                                #print("Add new vertex now:"+str(center))
                                for right in connect_right:
                                    G.addVertex(Point(next_vertex.x, right))
                                    #print("Add new vertex now:" +str(Point(next_vertex.x, right)))
                                    G.addEdge((G.VertexIndex[center], G.VertexIndex[
                                              Point(next_vertex.x, right)]))
                                #if possible, add start and goal to graph
                                if pre_l.x<=E.start.x<next_vertex.x:  #start 
                                    inter = Point(-1, -1)
                                    for obs in E.obstacles:
                                        for index in range(obs.number-1):
                                            inter_temp = GetIntersection(E.start, center, obs.IndexVertex[index+1], obs.IndexVertex[index+2])
                                            if inter_temp != Point(-1, -1) and inter_temp.distance(Point(pre_l.x, pre_l.vertex[0]))>0.1:
                                                inter = inter_temp
                                        # need seperate operation for last edge
                                        inter_temp = GetIntersection(E.start, center, obs.IndexVertex[obs.number], obs.IndexVertex[1])
                                        if inter_temp != Point(-1, -1) and inter_temp.distance(Point(pre_l.x, pre_l.vertex[0]))>0.1:
                                            inter = inter_temp
                                    # if there is no interection, add start to graph
                                    if inter == Point(-1, -1):
                                        G.addEdge((0,G.VertexIndex[center]))
                                if pre_l.x<=E.goal.x<next_vertex.x:
                                    inter = Point(-1, -1)
                                    for obs in E.obstacles:
                                        for index in range(obs.number-1):
                                            inter_temp = GetIntersection(E.goal, center, obs.IndexVertex[index+1], obs.IndexVertex[index+2])
                                            if inter_temp != Point(-1, -1) and inter_temp.distance(Point(pre_l.x, pre_l.vertex[0]))>0.1:
                                                inter = inter_temp
                                        # need seperate operation for last edge
                                        inter_temp = GetIntersection(E.goal, center, obs.IndexVertex[obs.number], obs.IndexVertex[1])
                                        if inter_temp != Point(-1, -1) and inter_temp.distance(Point(pre_l.x, pre_l.vertex[0]))>0.1:
                                            inter = inter_temp
                                    # if there is no interection, add goal to graph
                                    if inter == Point(-1, -1):
                                        G.addEdge((1,G.VertexIndex[center]))
                                for r in connect_right:
                                    middles_y.remove(r)
                            if len(middles_y)==0:
                                break
                        if pre_l.type == 1 or pre_l.type == 2 or pre_l.type == 3:
                            print("pre line type:",pre_l.type)
                            connect_left = []
                            connect_right = []                           
                            for y in middles_y:
                                for mid in pre_l.middle:
                                    inter = Point(-1, -1)
                                    inter_temp=Point(-1,-1)
                                    print("now checking mid:"+str(mid)+"and y:"+str(y))
                                    for obs in E.obstacles:
                                        for index in range(obs.number-1):
                                            inter_temp = GetIntersection(Point(pre_l.x, mid), Point(
                                                next_vertex.x, y), obs.IndexVertex[index+1], obs.IndexVertex[index+2])
                                            if inter_temp != Point(-1, -1):
                                                inter = inter_temp
                                                print("obs line: "+str(obs.IndexVertex[index+1])+"-"+str(obs.IndexVertex[index+2]))
                                        # need seperate operation for last edge
                                        inter_temp = GetIntersection(Point(pre_l.x, mid), Point(
                                            next_vertex.x, y), obs.IndexVertex[obs.number], obs.IndexVertex[1])
                                        if inter_temp != Point(-1, -1):
                                            inter = inter_temp
                                            print("obs line: "+str(obs.IndexVertex[obs.number])+"-"+str(obs.IndexVertex[1]))
                                    # determine if there is interection
                                    if inter == Point(-1, -1):
                                        if mid not in connect_left:
                                            connect_left.append(mid)
                                        if y not in connect_right:
                                            connect_right.append(y)
                                    else:
                                        print("intersection:"+str(inter))
                            print("connect_right:"+str(connect_right))
                            if len(connect_right) != 0:
                                center = Point((pre_l.x+next_vertex.x)/2, (sum(connect_left)+sum(
                                    connect_right))/(len(connect_right)+len(connect_left)))
                                print("Add new vertex now:"+str(center))
                                G.addVertex(center)
                                for left in connect_left:
                                    # G.addVertex(Point(pre_l.x,left))
                                    G.addEdge(
                                        (G.VertexIndex[center], G.VertexIndex[Point(pre_l.x, left)]))
                                for right in connect_right:
                                    G.addVertex(Point(next_vertex.x, right))
                                    G.addEdge((G.VertexIndex[center], G.VertexIndex[
                                              Point(next_vertex.x, right)]))
                                for r in connect_right:
                                    if r in middles_y:
                                        middles_y.remove(r)
                            if len(middles_y)==0:
                                break
                    if i == 0 and len(connect_right) == 0:
                        print("ERROR: cannot find pre SweepLine!")
                        exit()
            l = SweepLine(next_vertex.x, middles_yy, verteices_y, type_vertex)
            SweepLines.append(l)
        elif type_vertex == 4:
            l = SweepLine(next_vertex.x, [], [inter_up], type_vertex)
            SweepLines.append(l)
        elif type_vertex == 5:
            middles_y = []
            verteices_y = [inter_up]
            # check every previous sweep line
            for i in range(len(SweepLines)-1, -1, -1):
                pre_l = SweepLines[i]
                # figure out the type of previous sweep line
                if pre_l.type == 5 or pre_l.type == 4:
                    break
                else:
                    connect_left = []
                    for mid in pre_l.middle:
                        inter = Point(-1, -1)
                        inter_temp = Point(-1, -1)
                        for obs in E.obstacles:
                            for index in range(obs.number-1):
                                inter_temp = GetIntersection(Point(pre_l.x, mid), Point(
                                    next_vertex.x, inter_up), obs.IndexVertex[index+1], obs.IndexVertex[index+2])
                                if inter_temp != Point(-1, -1) and inter_temp.distance(Point(next_vertex.x, inter_up))>0.01:
                                    inter = inter_temp
                            # need seperate operation for last edge
                            inter_temp = GetIntersection(Point(pre_l.x, mid), Point(
                                next_vertex.x, inter_up), obs.IndexVertex[obs.number], obs.IndexVertex[1])
                            if inter_temp != Point(-1, -1)and inter_temp.distance(Point(next_vertex.x, inter_up))>0.01:
                                inter = inter_temp
                        # determine if there is interection
                        if inter == Point(-1, -1):
                            connect_left.append(mid)
                    if len(connect_left) != 0:
                        center = Point((pre_l.x+next_vertex.x)/2, (sum(connect_left)/len(connect_left) +
                                                                   inter_up)/2)
                        G.addVertex(center)
                        for left in connect_left:
                            # G.addVertex(Point(pre_l.x,left))
                            G.addEdge(
                                (G.VertexIndex[center], G.VertexIndex[Point(pre_l.x, left)]))
                        
                         #if possible, add start and goal to graph
                        if pre_l.x<=E.start.x<next_vertex.x:  #start 
                            inter = Point(-1, -1)
                            for obs in E.obstacles:
                                for index in range(obs.number-1):
                                    inter_temp = GetIntersection(E.start, center, obs.IndexVertex[index+1], obs.IndexVertex[index+2])
                                    if inter_temp != Point(-1, -1) and inter_temp.distance(Point(pre_l.x, pre_l.vertex[0]))>0.1:
                                        inter = inter_temp
                                # need seperate operation for last edge
                                inter_temp = GetIntersection(E.start, center, obs.IndexVertex[obs.number], obs.IndexVertex[1])
                                if inter_temp != Point(-1, -1) and inter_temp.distance(Point(pre_l.x, pre_l.vertex[0]))>0.1:
                                    inter = inter_temp
                            # if there is no interection, add start to graph
                            if inter == Point(-1, -1):
                                G.addEdge((0,G.VertexIndex[center]))
                        if pre_l.x<=E.goal.x<next_vertex.x:  #goal 
                            inter = Point(-1, -1)
                            for obs in E.obstacles:
                                for index in range(obs.number-1):
                                    inter_temp = GetIntersection(E.goal, center, obs.IndexVertex[index+1], obs.IndexVertex[index+2])
                                    if inter_temp != Point(-1, -1) and inter_temp.distance(Point(pre_l.x, pre_l.vertex[0]))>0.1:
                                        inter = inter_temp
                                # need seperate operation for last edge
                                inter_temp = GetIntersection(E.goal, center, obs.IndexVertex[obs.number], obs.IndexVertex[1])
                                if inter_temp != Point(-1, -1) and inter_temp.distance(Point(pre_l.x, pre_l.vertex[0]))>0.1:
                                    inter = inter_temp
                            # if there is no interection, add goal to graph
                            if inter == Point(-1, -1):
                                G.addEdge((1,G.VertexIndex[center]))

                        break
                    if i == 0 and len(connect_right) == 0:
                        print("ERROR: cannot find pre SweepLine!")
                        sys.exit()
            l = SweepLine(next_vertex.x, [], [], type_vertex)
            SweepLines.append(l)
        else:
            print("wrond type!")
            sys.exit()
    # add last vertex into graph
    print("SweepLines:")
    for sl in SweepLines:
        print("\n"+str(sl))
    pre_l = SweepLines[-1]
    print("pre_l.middle"+str(pre_l.middle))
    last_x = (pre_l.x+E.x_max)/2
    last_y = ((pre_l.middle[0]+pre_l.middle[1])/2+E.y_max/2)/2
    center = Point(last_x, last_y)
    G.addVertex(center)
    if pre_l.x<=E.start.x<=E.x_max:
        G.addEdge((0,G.VertexIndex[center]))
    if pre_l.x<=E.goal.x<=E.x_max:
        G.addEdge((1,G.VertexIndex[center]))
    if pre_l.type != 1:
        print("wrong type for last two line")
        exit()
    G.addEdge((G.VertexIndex[center], G.VertexIndex[
              Point(pre_l.x, pre_l.middle[0])]))
    G.addEdge((G.VertexIndex[center], G.VertexIndex[
              Point(pre_l.x, pre_l.middle[1])]))

<<<<<<< HEAD
=======
<<<<<<< HEAD

random.seed(1)
E = parse("test3.txt")
print(str(E))
G = Graph(E.start)
#RRT(E,G,10)
VCD(E,G)
print("\n\n"+str(G))

path=A_star(G, 1, 27)
print("\n\n",path)

p=Point(290,290)
print(str(p.distance(Point(60.0,183.092129464))))
print(str(p.distance(Point(60.0,183.092129464))))
=======
>>>>>>> origin/master
>>>>>>> refs/remotes/origin/master
