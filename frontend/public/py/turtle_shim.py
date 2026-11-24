"""浏览器版 turtle —— 把海龟指令记录下来，交给前端 Canvas 画出来（带动画）。

支持的命令是真 turtle 的常用子集，够画星星、多边形、魔法阵。
坐标系和真 turtle 一致：画布中心是 (0, 0)，y 轴向上，初始朝向正右方。
"""
import math

_CMDS = []
_BG = None


def _reset_all():
    global _CMDS, _BG
    _CMDS = []
    _BG = None


def _dump():
    return {"bg": _BG, "cmds": _CMDS}


class Turtle:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.heading = 0.0          # 角度，0 = 正右方，逆时针为正
        self._pen = True
        self._color = "#7C3AED"
        self._fillcolor = "#DDCEFF"
        self._width = 3
        self._speed = 5
        self._visible = True
        self._filling = False
        self._fillpath = []

    # ---------------------------------------------------------- 移动
    def forward(self, dist):
        rad = math.radians(self.heading)
        nx = self.x + dist * math.cos(rad)
        ny = self.y + dist * math.sin(rad)
        self._goto(nx, ny)

    def backward(self, dist):
        self.forward(-dist)

    def right(self, angle):
        self.heading -= angle

    def left(self, angle):
        self.heading += angle

    def goto(self, x, y=None):
        if y is None:
            x, y = x
        self._goto(float(x), float(y))

    def setx(self, x):
        self._goto(float(x), self.y)

    def sety(self, y):
        self._goto(self.x, float(y))

    def setheading(self, angle):
        self.heading = float(angle)

    def home(self):
        self._goto(0.0, 0.0)
        self.heading = 0.0

    def _goto(self, nx, ny):
        if self._pen:
            _CMDS.append({
                "op": "line", "x1": self.x, "y1": self.y, "x2": nx, "y2": ny,
                "color": self._color, "w": self._width, "speed": self._speed,
            })
        if self._filling:
            self._fillpath.append([nx, ny])
        self.x, self.y = nx, ny

    def circle(self, radius, extent=360, steps=None):
        radius = float(radius)
        extent = float(extent)
        if steps is None:
            steps = max(6, int(abs(extent) / 8) + 4)
        seg_angle = extent / steps
        seg_len = 2 * radius * math.sin(math.radians(abs(seg_angle) / 2))
        sign = 1 if radius >= 0 else -1
        self.left(sign * seg_angle / 2)
        for _ in range(steps):
            self.forward(seg_len if radius >= 0 else -seg_len)
            self.left(sign * seg_angle)
        self.left(-sign * seg_angle / 2)

    def dot(self, size=None, color=None):
        _CMDS.append({
            "op": "dot", "x": self.x, "y": self.y,
            "r": (size or self._width * 2) / 2,
            "color": color or self._color, "speed": self._speed,
        })

    def stamp(self):
        self.dot(self._width * 3)

    # ---------------------------------------------------------- 画笔
    def penup(self):
        self._pen = False

    def pendown(self):
        self._pen = True

    def pensize(self, w=None):
        if w is None:
            return self._width
        self._width = float(w)

    width = pensize

    def pencolor(self, *c):
        if not c:
            return self._color
        self._color = _norm_color(c)

    def fillcolor(self, *c):
        if not c:
            return self._fillcolor
        self._fillcolor = _norm_color(c)

    def color(self, *c):
        if not c:
            return self._color
        if len(c) == 2 and isinstance(c[0], str) and isinstance(c[1], str):
            self._color, self._fillcolor = c[0], c[1]
        else:
            col = _norm_color(c)
            self._color = col
            self._fillcolor = col

    def begin_fill(self):
        self._filling = True
        self._fillpath = [[self.x, self.y]]

    def end_fill(self):
        if self._filling and len(self._fillpath) > 2:
            _CMDS.append({
                "op": "fill", "points": self._fillpath,
                "color": self._fillcolor, "speed": self._speed,
            })
        self._filling = False
        self._fillpath = []

    def write(self, text, move=False, align="left", font=("", 16, "normal")):
        size = font[1] if isinstance(font, (tuple, list)) and len(font) > 1 else 16
        _CMDS.append({
            "op": "write", "x": self.x, "y": self.y, "text": str(text),
            "color": self._color, "size": size, "align": align, "speed": self._speed,
        })

    # ---------------------------------------------------------- 其它
    def speed(self, s=None):
        if s is None:
            return self._speed
        if isinstance(s, str):
            s = {"fastest": 0, "fast": 10, "normal": 6, "slow": 3, "slowest": 1}.get(s, 5)
        self._speed = int(s)

    def hideturtle(self):
        self._visible = False

    def showturtle(self):
        self._visible = True

    def clear(self):
        _CMDS.clear()

    def reset(self):
        _reset_all()
        self.__init__()

    def position(self):
        return (self.x, self.y)

    pos = position

    def xcor(self):
        return self.x

    def ycor(self):
        return self.y

    def isdown(self):
        return self._pen


def _norm_color(c):
    if len(c) == 1:
        v = c[0]
        if isinstance(v, (tuple, list)):
            return _rgb(*v)
        return str(v)
    if len(c) == 3:
        return _rgb(*c)
    return str(c[0])


def _rgb(r, g, b):
    if max(r, g, b) <= 1:
        r, g, b = r * 255, g * 255, b * 255
    return "#%02X%02X%02X" % (int(r), int(g), int(b))


class Screen:
    def bgcolor(self, *c):
        global _BG
        if not c:
            return _BG
        _BG = _norm_color(c)

    def title(self, t):
        pass

    def setup(self, *a, **k):
        pass

    def tracer(self, *a, **k):
        pass

    def update(self):
        pass

    def exitonclick(self):
        pass

    def clear(self):
        _reset_all()


_screen = Screen()
_t = Turtle()


def Screen_():
    return _screen


# 模块级函数：turtle.forward(100) 这种写法
def forward(d): _t.forward(d)
def fd(d): _t.forward(d)
def backward(d): _t.backward(d)
def bk(d): _t.backward(d)
def back(d): _t.backward(d)
def right(a): _t.right(a)
def rt(a): _t.right(a)
def left(a): _t.left(a)
def lt(a): _t.left(a)
def goto(x, y=None): _t.goto(x, y)
def setpos(x, y=None): _t.goto(x, y)
def setx(x): _t.setx(x)
def sety(y): _t.sety(y)
def setheading(a): _t.setheading(a)
def seth(a): _t.setheading(a)
def home(): _t.home()
def circle(r, extent=360, steps=None): _t.circle(r, extent, steps)
def dot(size=None, color=None): _t.dot(size, color)
def stamp(): _t.stamp()
def penup(): _t.penup()
def pu(): _t.penup()
def up(): _t.penup()
def pendown(): _t.pendown()
def pd(): _t.pendown()
def down(): _t.pendown()
def pensize(w=None): return _t.pensize(w)
def width(w=None): return _t.pensize(w)
def pencolor(*c): return _t.pencolor(*c)
def fillcolor(*c): return _t.fillcolor(*c)
def color(*c): return _t.color(*c)
def begin_fill(): _t.begin_fill()
def end_fill(): _t.end_fill()
def write(text, move=False, align="left", font=("", 16, "normal")): _t.write(text, move, align, font)
def speed(s=None): return _t.speed(s)
def hideturtle(): _t.hideturtle()
def ht(): _t.hideturtle()
def showturtle(): _t.showturtle()
def st(): _t.showturtle()
def clear(): _t.clear()
def reset(): _t.reset()
def position(): return _t.position()
def pos(): return _t.position()
def xcor(): return _t.xcor()
def ycor(): return _t.ycor()
def bgcolor(*c): return _screen.bgcolor(*c)
def done(): pass
def mainloop(): pass
def exitonclick(): pass
def update(): pass
def tracer(*a, **k): pass
def title(t): pass
def setup(*a, **k): pass


Pen = Turtle
