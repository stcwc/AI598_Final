
class p:
    def __init__(self,a):
        self.a=1

    def __str__(self):
        return ("321")
class test:
    def __init__(self,a):
        self.a=a
        self.b = p(2)
    def __str__(self):
        return (str)(self.b)

t=test("asdfsadf")
print(t)
