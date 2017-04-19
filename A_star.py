# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 21:27:17 2017

Usage:
A* algorithm accomplishment.

@author: Wangchao Sheng
"""
import heapq

def A_star(graph, s_index, g_index):
    
    if(s_index not in graph.IndexVertex):
        print("[A_star] no start point in graph.")
        return
    if(g_index not in graph.IndexVertex):
        print("[A_star] no goal point in graph.")
        return
    queue=[TreeNode(s_index, None, 0)]  #
    path = []
    dis = 0  # total distance, dis+span+hueristic
    expanded = set()  # Nodes that have been expanded
    while(len(queue)!=0):
        #print("Queue:\n",[str(queue[i]) for i in range(len(queue))])
        temp = heapq.heappop(queue)  # TreeNode type in queue
        if temp.index == g_index:  # Goal is at the front of queue, namely find the goal.
            q = temp
            path.append(q.index)
            while(q.pre!=None):
                q=q.pre
                path.append(q.index)
            path.reverse()
            break
        expanded.add(temp.index)  # only index in it
        for edge in graph.edges:
            if edge[0] == temp.index and edge[1] not in expanded:
                dis=dis+graph.getVertex(edge[0]).distance(graph.getVertex(edge[1]))+graph.getVertex(edge[0]).distance(graph.getVertex(g_index))
                heapq.heappush(queue,TreeNode(edge[1],temp,dis))
            elif edge[1] == temp.index and edge[0] not in expanded:
                dis=dis+graph.getVertex(edge[0]).distance(graph.getVertex(edge[1]))+graph.getVertex(edge[1]).distance(graph.getVertex(g_index))
                heapq.heappush(queue,TreeNode(edge[0],temp,dis))
    return path 
      
class TreeNode:
    def __init__(self, index, pre, d):
        self.index = index
        self.pre = pre
        self.d = d
        
    def __cmp__(self, t):
        return self.d>t.d and self.index==t.index and self.d==t.d
    
    def __lt__(self, t):
        return self.d<t.d
    def __le__(self, t):
        return self.d<=t.d
    def __ge__(self, t):
        return self.d>=t.d
    def __gt__(self, t):
        return self.d>t.d
    
    def __str__(self):
        if(self.pre==None): 
            return "index:"+str(self.index)+", pre:None, d:"+str(self.d)+"\n"
        else: 
            return "index:"+str(self.index)+", pre:"+str(self.pre.index)+", d:"+str(self.d)+"\n"


