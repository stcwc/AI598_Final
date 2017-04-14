#from test import test
from Util import Point, Graph, Obstacle, Environment


p=Point(1,2)
b=Point(4,3)

g=Graph(p)
#g.addVertex(b)
g.addVertex(Point(4,6))
g.addVertex(Point(3,7))
g.addEdge((0,1))
print(str(g))
print(str(g.getVertex(3)))
print(str(g.getIndex(Point(3,9))))

o=Obstacle([Point(1,1),Point(2,1),Point(2,2)])
print(str(o))
print(str(o.getVertex(4)))
print(str(o.getIndex(Point(3,9))))

e=Environment(300,200)
e.addObstacle(o)
print(str(e))