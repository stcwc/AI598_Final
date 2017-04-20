#from test import test
from Util import Point, Graph, Obstacle, Environment
import random
from Parser import parse
from algorithms import VCD, RRT

random.seed(1)
E = parse("test3.txt")

<<<<<<< HEAD
a=Point(1,2)
b=Point(3,4)
aa=Point(11,2)
aaa=Point(1,2)

dis={a:'a',b:'b'}
print(dis)
for i in dis:
    print(str(i))

    
for i in dis:
    i.x=i.x+10

for i in dis:
    print(str(i))
    if i in dis:
        print("equal")
=======
print(str(E))
#print(str(i) for i in E.obstacles)
#print(E.obstacles[1])

G = Graph(E.start)
VCD(E,G)
print("\n\n"+str(G))

path=A_star(G, 15, 18)
print("\npath:\n",path)
''''''
>>>>>>> origin/master

print(a in dis.keys())
print(aa in dis.keys())
print(aaa in dis.keys())

print(str(a))
#e=Environment(300,200)
#e.addObstacle(o)
#print(str(e))
