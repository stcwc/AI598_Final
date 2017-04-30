import random
from Parser import *
from Util import *
from algorithms import *
from A_star import *
import sys

def main():
    random.seed(1)
    if len(sys.argv)==4 and sys.argv[3]=="VCD":
        E = parse(sys.argv[1])
        print("......Doing VCD......")
        G=VCD(E)
        path=A_star(G, 0, 1)
    elif len(sys.argv)==5 and sys.argv[3]=="RRT":
        E = parse(sys.argv[1])
        I=int(sys.argv[4])
        print("......Doing RRT with "+str(I)+" iterations......")
        G = RRT(E,I)
        path=A_star(G, 0, G.VertexNumber-1)
    else:    
        print("[ERROR] Input arguments incorrect. Use command like 'python main.py input.txt output.txt VCD' or 'python main.py input.txt output.txt RRT 1000' and try again.")
        sys.exit()
        
    #print("\n\n")
    spath=''
    for i in path:
        spath += str(i)+","
    #print(str(G)+"\n"+spath[:-1])
    file = open(sys.argv[2],"w")
    file.truncate()
    file.write(str(G)+"\n"+spath[:-1])
    print("[Success] Output has been written into 'output.txt'.")
    file.close()
    
main()
