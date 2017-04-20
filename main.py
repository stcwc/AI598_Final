import random
from Parser import *
from Util import *
from algorithms import *

def main():
    random.seed(1)
    E = parse("test3.txt")
    print(str(E))
    G = Graph(E.start)
    VCD(E,G)
    #print("\n\n"+str(G))
    
    path=A_star(G, 0, 27)
    print("\n\n")
    
    spath=''
    for i in path:
        spath += str(i)+","
    print(str(G)+spath[:-1])


main()
