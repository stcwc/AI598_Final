#from test import test
from Util import Point, Graph, Obstacle, Environment
import random
from Parser import parse
from algorithms import VCD, RRT

random.seed(1)
E = parse("test3.txt")

print(str(E))
#print(str(i) for i in E.obstacles)
#print(E.obstacles[1])

G = Graph(E.start)
VCD(E,G)
print("\n\n"+str(G))

path=A_star(G, 15, 18)
print("\npath:\n",path)
''''''

#e=Environment(300,200)
#e.addObstacle(o)
#print(str(e))