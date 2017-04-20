import random
from Parser import *
from Util import *
from algorithms import *
from A_star import *
import sys

def main():
    random.seed(1)
    if len(sys.argv)==3 and sys.argv[2]=="VCD":
        E = parse(sys.argv[1])
        G = Graph(E.start)
        print("......Doing VCD......")
        VCD(E,G)
        path=A_star(G, 0, 1)
    elif len(sys.argv)==4 and sys.argv[2]=="RRT":
        E = parse(sys.argv[1])
        G = Graph(E.start)
        print("......Doing RRT with "+str(int(sys.argv[3]))+" iterations......")
        I=int(sys.argv[3])
        RRT(E,G,I)
        path=A_star(G, 0, G.VertexNumber-1)
    else:    
        print("[ERROR] Input arguments incorrect. Use command like 'python main.py input.txt VCD' or 'python main.py input.txt RRT 1000' and try again.")
        sys.exit()
        
    #print("\n\n")
    spath=''
    for i in path:
        spath += str(i)+","
    #print(str(G)+"\n"+spath[:-1])
    file = open("output.txt","w")
    file.truncate()
    file.write(str(G)+"\n"+spath[:-1])
    print("[Success] Output has been written into 'output.txt'.")
    
main()
