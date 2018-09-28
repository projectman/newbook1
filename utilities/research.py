


class A():
    def __init__(self):
        print ("world")

    def fromA(self):
        print("From A")

class B(A):
    def __init__(self):
        print ("hello")
        super(B, self).__init__()

ff = B()
ff.fromA()
