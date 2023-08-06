

class Vector:
    __data = None

    def __init__(self, x=0,y=0,z=0):
        self.__data = [x,y,z]

    def __index__(self, i):
        return self.__data[i]

    @property
    def x(self):
        return self.__data[0]
    @x.setter
    def x(self, x):
        self.__data[0] = x

    @property
    def y(self):
        return self.__data[1]
    @y.setter
    def y(self, y):
        self.__data[1] = y

    @property
    def z(self):
        return self.__data[2]
    @z.setter
    def z(self, z):
        self.__data[2] = z

class Foot:
    position = None
    orientation = 0 # yaw only
    cycle = 0

    def __init__(self, x=0, y=0, z=0, theta=0, cycle=0):
        self.position = Vector(x,y,z)
        self.orientation = theta
        self.cycle = cycle

class Twist:
    linear = Vector()
    angular = Vector()

class Pose2D:
    x = 0
    y = 0
    theta = 0
