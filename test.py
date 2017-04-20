from Util import Point
class p:
    def __init__(self,a):
        self.a=a

    def __str__(self):
        return str(self.a)
class test:
    def __init__(self,a):
        self.a=a
        self.b = p(2)
    def __str__(self):
        return (str)(self.b)


p1=Point(1,2)
p2=Point(3,4)
b=set()
b.add(p1)
print(p2 in b)
a={p1:1,p2:2}
for i in a.keys():
    if i.x==1:
        i.x=3
        i.y=4
print(len(a))
