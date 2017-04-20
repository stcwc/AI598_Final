import random
from Parser import *
from Util import *
from algorithms import *
from A_star import *

def main():
    random.seed(1)
    E = parse("test4.txt")
    #print(str(E))
    G = Graph(E.start)
    VCD(E,G)
    print("\n\n"+str(G))
    
    path=A_star(G, 0, 1)
    print("\n\n")
    '''
    spath=''
    for i in path:
        spath += str(i)+","
    print(str(G)+"\n"+spath[:-1])
    file = open("output.txt","w")
    file.truncate()
    file.write(str(G)+"\n"+spath[:-1])
    print("[Success] Output has been written into 'output.txt'.")
    '''
main()
