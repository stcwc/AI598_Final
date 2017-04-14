#defin the class of Point, Graph, Obstacle, Environment
#Author: YI

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __str__(self):
        return ("("+str(self.x)+","+str(self.y)+")")
    def __eq__(self,other):
        return other.x==self.x and other.y==self.y
    def __hash__(self):
        return hash(str(self.x)+","+str(self.y))
        
class Graph:
    def __init__(self,p):
        #p is the start point
        self.VertexIndex={p:0}
        self.IndexVertex={0:p}
        self.edges=[]
        self.VertexNumber=1
    def __str__(self):
        output="Vertex:"
        for i in range(self.VertexNumber):
            output=output+str(i)+":"+str(self.IndexVertex[i])
        output=output+"\nEdges:"
        for edge in self.edges:
            output=output+"("+str(edge[0])+","+str(edge[1])+") "
        return output #to be contonue

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
        output="Obstical:"
        for i in range(self.number):
            output=output+str(self.IndexVertex[i+1])+" "
        return output

    def getVertex(self,index):
        return self.IndexVertex[index] if (index in self.IndexVertex) else Point(-1,-1)
    def getIndex(self,point):
        return self.VertexIndex[point] if (point in self.VertexIndex) else -1



class Environment:
    def __init__(self,x,y,obs,start,goal):
        self.obstacles=[]
        self.x_max=x
        self.y_max=y
        self.obstacles=obs
        self.start=start
        self.goal=goal
    def __str__(self):
        output="Environment: rectangle from (0,0) to ("+str(self.x_max)+","+str(self.y_max)+")\n"
        for obs in self.obstacles:
            output=output+str(obs)+"\n"
        return output

