from math import sqrt


class Point:

    def __init__(self, x, y, tag=None):
        self.x = x
        self.y = y
        if tag is not None: self.tag = tag

    @property
    def distance(self): return sqrt(self.x ** 2 + self.y ** 2)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        return self

    @staticmethod
    def build(x, y): return Point(x, y)
