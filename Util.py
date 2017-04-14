#defin the class of Point, Graph, Obstacle, Environment
#Author: YI

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __str__(self):
        return ("("+str(self.x)+","+str(self.y)+")")
        
class Graph:
    def __init__(self,p):
        #p is the start point
        self.VertexIndex={p:0}
        self.IndexVertex={0:p}
        self.edges=[]
        self.vertexNumber=1

    def __str__(self):
        return ("vertex:")  #to be contonue

    def addVertex(self,p):
        self.vertexIndex[p]=self.VertexNumber
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
        return self.IndexVertex[index]

    def getIndex(self,point):
        return self.VertexIndex[point]


class Obstacle:
    def __init__(self,points):
        self.VertexIndex={}
        self.IndexVertex={}
        for i in range(len(points)):
            self.VertexIndex[points[i]]=i+1
            self.IndexVertex[i+1]=points[i]
        self.vertexNumber=len(points)    

    def getVertex(self,index):
        return self.IndexVertex[index]

    def getIndex(self,point):
        return self.VertexIndex[point]



class Environment:
    def __init__(self,x,y):
        self.obstacles=[]
        self.x_max=x
        self.y_max=y

    def addObstacle(self,obstacle):
        self.obstacles.append(obstacle)
