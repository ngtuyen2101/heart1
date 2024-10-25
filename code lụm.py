'''import turtle
import time
def LittleHeart():
    for i in range(200):
        turtle.right(1)
        turtle.forward(2)

# love = input('请输入表白语句，然后回车，默认为"I Love You":\n')
# me = input('请输入要表白的人:\n')
# if love=='':
# # 如果未输入表白语句，则使用默认语句
#     love='I Love you'

love='I Love you'
me = '我喜欢你'

turtle.setup(width=900,height=600)  # 爱心的画布的大小
turtle.color('red','red')          # 爱心的颜色及外边笔的颜色
turtle.pensize(10)                   # 画笔的粗细
turtle.speed(100000000)               # 绘制速度

turtle.up()                         # 画笔向上

turtle.hideturtle()
turtle.goto(0,-180)
turtle.showturtle()
turtle.down()
turtle.speed(5)
turtle.begin_fill()

# 开始填充
turtle.left(140)
turtle.forward(224)
LittleHeart()
turtle.left(120)
LittleHeart()
turtle.forward(224)
turtle.end_fill()
turtle.pensize(5)
turtle.up()
turtle.hideturtle()
turtle.goto(0,0)
turtle.showturtle()
turtle.color('#CD5C5C','pink')
turtle.write(love,font=('gungsuh',30,),align="center")
turtle.up()
turtle.hideturtle()

if me !='':
    turtle.color('black', 'pink')
    time.sleep(2)
    turtle.goto(180,-180)
    turtle.showturtle()
    turtle.write(me, font=(20,), align="center", move=True)
    window=turtle.Screen()
    window.exitonclick()

# 程序员何未来GitHub爱心代码项目github.com/he-weilai/love-code'''






























import random
from math import sin, cos, pi, log
from tkinter import *
import tkinter
CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480
CANVAS_CENTER_X = CANVAS_WIDTH / 2
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2
IMAGE_ENLARGE = 11
HEART_COLOR = "#ff2121"


def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):

    x = 16 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))

    x *= shrink_ratio
    y *= shrink_ratio

    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y
    return int(x), int(y)


def scatter_inside(x, y, beta=0.15):

    ratio_x = - beta * log(random.random())
    ratio_y = - beta * log(random.random())
    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy


def shrink(x, y, ratio):

    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) **
                  0.6)
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy


def curve(p):

    return 2 * (2 * sin(4 * p)) / (2 * pi)


class Heart:

    def __init__(self, generate_frame=20):
        self._points = set()
        self._edge_diffusion_points = set()
        self._center_diffusion_points = set()
        self.all_points = {}
        self.build(2000)
        self.random_halo = 1000
        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)

    def build(self, number):

        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t)
            self._points.add((x, y))

        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))

        point_list = list(self._points)
        for _ in range(4000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.17)
            self._center_diffusion_points.add((x, y))

    @staticmethod
    def calc_position(x, y, ratio):

        force = 1 / (((x - CANVAS_CENTER_X) ** 2 +
                     (y - CANVAS_CENTER_Y) ** 2) ** 0.520)
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)
        return x - dx, y - dy

    def calc(self, generate_frame):
        ratio = 10 * curve(generate_frame / 10 * pi)
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi)))
        halo_number = int(
            3000 + 4000 * abs(curve(generate_frame / 10 * pi) ** 2))
        all_points = []

        heart_halo_point = set()
        for _ in range(halo_number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t, shrink_ratio=11.6)
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:

                heart_halo_point.add((x, y))
                x += random.randint(-14, 14)
                y += random.randint(-14, 14)
                size = random.choice((1, 2, 2))
                all_points.append((x, y, size))

        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))

        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
        self.all_points[generate_frame] = all_points

    def render(self, render_canvas, render_frame):
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(
                x, y, x + size, y + size, width=0, fill=HEART_COLOR)


def draw(main: Tk, render_canvas: Canvas, render_heart: Heart, render_frame=0):
    render_canvas.delete('all')
    render_heart.render(render_canvas, render_frame)
    main.after(160, draw, main, render_canvas, render_heart, render_frame + 1)


if __name__ == '__main__':
    root = Tk()
    canvas = Canvas(root, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack()
    heart = Heart()
    draw(root, canvas, heart)
    root.mainloop()




































