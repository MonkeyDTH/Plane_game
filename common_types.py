# Author : TH
# File   : common_types.py
# IDE    : PyCharm
# Time   : 2019-12-14_14:59:06
""" common types used in game """


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def position(self, point):
        if self.x <= point.x:
            if self.y <= point.y:
                return 3
            else:
                return


class Image(object):
    def __init__(self, x, y, width, height):
        self.leftUp = Point(x, y)
        self.width = width
        self.height = height

    def touch(self, image):
        # x touch
        if (self.leftUp.x + self.width > image.leftUp.x + image.width) and (self.leftUp.x < image.leftUp.x + image.width):
            if (self.leftUp.y + self.height > image.leftUp.y) and (self.leftUp.y < image.leftUp.y + image.height):
                return True
        return False


class Plane(Image):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)


class Bullet(Image):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def move(self, distance):
        self.leftUp = Point(self.leftUp.x, self.leftUp.y - distance)


class Monster(Image):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def move(self, distance):
        self.leftUp = Point(self.leftUp.x, self.leftUp.y + distance)


def main():
    pass


if __name__ == '__main__':
    main()
