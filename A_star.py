# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 21:27:17 2017

Usage:
A* algorithm accomplishment.

@author: Wangchao Sheng
"""

def A_star(graph, start, goal):
    if(graph.getIndex(start)==-1):
        print("[A_star] no start point in graph.")
        return
    if(graph.getIndex(goal)==-1):
        print("[A_star] no goal point in graph.")
        return
    s_index = graph.getIndex(start)
    g_index = graph.getIndex(goal)
    p = s_index
    queue=[TreeNode(s_index, None, 0)]  #
    path = []
    dis = 0  # total distance
    expanded = set()
    while(len(queue)!=0):
        temp = queue[0]
        del(queue[0])
        expanded.add(temp.index)
        neib = []
        for edge in graph.edges:
            if ######################
        choose the one with the min (d+h)
        path.append(graph.getVertex(q1_index))
        p_index=q1_index
      
class TreeNode:
    def __init__(self, index, pre, d):
        self.index = index
        self.pre = pre
        self.d = d

class C:
    __hash__=object.__hash__
    def __init__(self,a):
        self.a = a
    
    def __eq__(self,other):
        return (self.a==other.a)

'''
a = C(1)
b = C(1)
d = {a:2}
print(d.get(b))
'''