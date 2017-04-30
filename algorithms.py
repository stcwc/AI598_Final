# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 20:00:11 2017

Usage:
Achieve Vertical Cell Decomposition and RRT

@author: YI HOU and Wangchao Sheng
"""

from Util import Point, Graph, Obstacle, Environment, SweepLine
from Geometry import GetIntersection, NearestPoint
import random
import sys
from Parser import parse
from A_star import A_star

def RRT(E, I):
    # add first vertex to graph
    '''
    implement RRT
    E: working environment, including obstacles, start point, goal point
    I: number of iteration 
    '''
    # initiate the graph with start point in it
    G = Graph(E.start)
    #start iteration
    for i in range(I):
        if i == I-1: # last iteration, should try to add goal point into graph
            new_vertex = E.goal
        else: # not last iteration, randomly pick a point 
            new_vertex = Point(random.uniform(0, E.x_max),
                               random.uniform(0, E.y_max))
        nearest_point = E.start  # initially, set nearest_point as start point
        edgeLocation = (0, 0)  # on which edge does the nearest_point locate
        # update the nearest_point
        for edge in G.edges:
            nearest_temp = NearestPoint(
                G.IndexVertex[edge[0]], G.IndexVertex[edge[1]], new_vertex)
            if new_vertex.distance(nearest_temp) < new_vertex.distance(nearest_point):
                nearest_point = nearest_temp  # update nearest point and the edge location
                edgeLocation = edge
        # if nearest_point is in the middle of edge, should remove original edge and add new vertex and edges
        if min(G.IndexVertex[edgeLocation[0]].x, G.IndexVertex[edgeLocation[1]].x) < nearest_point.x < max(G.IndexVertex[edgeLocation[0]].x, G.IndexVertex[edgeLocation[1]].x):
            G.removeEdge(edgeLocation)
            G.addVertex(nearest_point)
            G.addEdge((edgeLocation[0], G.VertexIndex[nearest_point]))
            G.addEdge((edgeLocation[1], G.VertexIndex[nearest_point]))
        # calculate the intersection between line segment from new_vertex to nearest_point and obstacles
        intersection = Point(new_vertex.x, new_vertex.y)
        for obs in E.obstacles:
            for index in range(obs.number-1):
                inter_temp = GetIntersection(nearest_point, new_vertex, obs.IndexVertex[
                                             index+1], obs.IndexVertex[index+2])
                if inter_temp != Point(-1, -1):  # there IS intersection
                    if intersection.distance(nearest_point) > inter_temp.distance(nearest_point):
                        intersection = inter_temp  # inter_temp is closer to nearest_point
            # need sepatate operation for last edge because of CIRCLE
            inter_temp = GetIntersection(nearest_point, new_vertex, obs.IndexVertex[obs.number], obs.IndexVertex[1])
            if inter_temp != Point(-1, -1): 
                if intersection.distance(nearest_point) > inter_temp.distance(nearest_point):
                    intersection = inter_temp
        if intersection.distance(nearest_point)>0.001:
            G.addVertex(intersection)
            G.addEdge((G.VertexIndex[nearest_point], G.VertexIndex[intersection]))
    if E.goal not in G.VertexIndex:
        print("[ERROR] Goal cannot be added into the Graph. Please increase the interation number!")
        #print("The graph is:\n"+str(G))
        sys.exit()
    return G


def VCD(E):
    '''
    impliment VCD
    E: working environment, including obstacles, start point, goal point
    '''
    # initiate graph with start point in it
    G = Graph(E.start)
    G.addVertex(E.goal)
    SweepLines = []
    #sort all obstacle vertices in  from left to rignt
    all_obs = []
    for obs in E.obstacles:
        for vertex in obs.VertexIndex:
            all_obs.append(vertex)
    all_obs.sort()
    # check each obstacle vertex from left to right
    for i in range(len(all_obs)):
        next_vertex = all_obs[i]
        type_vertex = 0
        inter_up = E.y_max
        inter_below = 0
        # determine the type of vertex
        for obs in E.obstacles:
            for vertex in obs.VertexIndex:
                if next_vertex == vertex:
                    index = obs.VertexIndex[vertex]
                    pre = Point(-1, -1)
                    pos = Point(-1, -1)
                    # find pre and post vertex
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
                        type_vertex = 1  # type 1
                        inter_up = E.y_max
                        inter_below = 0
                    elif (pre.x > vertex.x and pos.x > vertex.x and pre.y < pos.y):
                        type_vertex = 4  # type 4
                        inter_up = vertex.y
                        inter_below = vertex.y
                    elif (pre.x < vertex.x and pos.x < vertex.x and pre.y > pos.y):
                        type_vertex = 5  # type 5
                        inter_up = vertex.y
                        inter_below = vertex.y
                    elif pre.x < vertex.x < pos.x:
                        type_vertex = 3  # type 3
                        inter_up = vertex.y
                        inter_below = 0
                    elif pos.x < vertex.x < pre.x:
                        type_vertex = 2  # type 4
                        inter_up = E.y_max
                        inter_below = vertex.y
                    else:
                        print("cannot determine type!")
                        exit()
        # find the highest point and lowest point in the sweep line
        for obs in E.obstacles:
            for index in range(obs.number-1):
                inter_temp = GetIntersection(Point(next_vertex.x, 0), Point(
                    next_vertex.x, E.y_max), obs.IndexVertex[index+1], obs.IndexVertex[index+2])
                if next_vertex.y < inter_temp.y < inter_up:
                    inter_up = inter_temp.y
                elif inter_below < inter_temp.y < next_vertex.y:
                    inter_below = inter_temp.y
            # need sepatate operation for last edge because of CIRCLE
            inter_temp = GetIntersection(Point(next_vertex.x, 0), Point(
                next_vertex.x, E.y_max), obs.IndexVertex[obs.number], obs.IndexVertex[1])
            if next_vertex.y < inter_temp.y < inter_up:
                inter_up = inter_temp.y
            elif inter_below < inter_temp.y < next_vertex.y:
                inter_below = inter_temp.y
        # find the previous sweep line
        # if the current sweep line is type 1 or 2 or 3
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
            # if the current sweep line is the first one
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
                #if possible, add start and goal point to graph
                if 0<=E.start.x<next_vertex.x:
                    G.addEdge((0,G.VertexIndex[center]))
                if 0<=E.goal.x<next_vertex.x:
                    G.addEdge((1,G.VertexIndex[center]))
            # current sweep line is not the first line
            else:
                # check every previous sweep line
                while (len(middles_y) != 0):
                    for i in range(len(SweepLines)-1, -1, -1):
                        pre_l = SweepLines[i]
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
                                            inter = inter_temp
                                    # need seperate operation for last edge
                                    inter_temp = GetIntersection(Point(pre_l.x, pre_l.vertex[0]), Point(
                                        next_vertex.x, y), obs.IndexVertex[obs.number], obs.IndexVertex[1])
                                    if inter_temp != Point(-1, -1) and inter_temp.distance(Point(pre_l.x, pre_l.vertex[0]))>0.1:
                                        inter = inter_temp
                                # determine if there is interection
                                if inter == Point(-1, -1):
                                    connect_right.append(y)
                            # if this previous sweep line is qualified, we should add the center point and corresponding edges
                            if len(connect_right) != 0:
                                center = Point(
                                    (pre_l.x+next_vertex.x)/2, sum(connect_right)/len(connect_right))
                                G.addVertex(center)
                                for right in connect_right:
                                    G.addVertex(Point(next_vertex.x, right))
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
                            if len(middles_y)==0: # if no need to check previous sweep line any more
                                break
                        if pre_l.type == 1 or pre_l.type == 2 or pre_l.type == 3:
                            connect_left = []
                            connect_right = []                           
                            for y in middles_y:
                                for mid in pre_l.middle:
                                    inter = Point(-1, -1)
                                    inter_temp=Point(-1,-1)
                                    for obs in E.obstacles:
                                        for index in range(obs.number-1):
                                            inter_temp = GetIntersection(Point(pre_l.x, mid), Point(
                                                next_vertex.x, y), obs.IndexVertex[index+1], obs.IndexVertex[index+2])
                                            if inter_temp != Point(-1, -1):
                                                inter = inter_temp
                                        # need seperate operation for last edge
                                        inter_temp = GetIntersection(Point(pre_l.x, mid), Point(
                                            next_vertex.x, y), obs.IndexVertex[obs.number], obs.IndexVertex[1])
                                        if inter_temp != Point(-1, -1):
                                            inter = inter_temp
                                    # determine if there is interection
                                    if inter == Point(-1, -1):
                                        if mid not in connect_left:
                                            connect_left.append(mid)
                                        if y not in connect_right:
                                            connect_right.append(y)                                  
                            if len(connect_right) != 0:
                                center = Point((pre_l.x+next_vertex.x)/2, (sum(connect_left)+sum(
                                    connect_right))/(len(connect_right)+len(connect_left)))
                                G.addVertex(center)
                                for left in connect_left:
                                    # G.addVertex(Point(pre_l.x,left))
                                    G.addEdge(
                                        (G.VertexIndex[center], G.VertexIndex[Point(pre_l.x, left)]))
                                for right in connect_right:
                                    G.addVertex(Point(next_vertex.x, right))
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
                                    if r in middles_y:
                                        middles_y.remove(r)
                            if len(middles_y)==0:
                                break
                    if i == 0 and len(connect_right) == 0:
                        print("ERROR: cannot find pre SweepLine!")
                        exit()
            l = SweepLine(next_vertex.x, middles_yy, verteices_y, type_vertex)
            SweepLines.append(l)
        # if the current sweep line is type 4, no need to find previous sweep line
        elif type_vertex == 4:
            l = SweepLine(next_vertex.x, [], [inter_up], type_vertex)
            SweepLines.append(l)
        # if the current sweep line is type 5, similar procedure as if type =1 or 2 or 3
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
            print("ERROR: wrong type for SweepLine!")
            sys.exit()
    # add last vertex into graph
    pre_l = SweepLines[-1]
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
    return G


