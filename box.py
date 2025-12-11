import math

def test(seg,points):
    angle = math.atan2(seg[1][1] - seg[0][1], seg[1][0] - seg[0][0])
    temp_points = [list(p) for p in points]
    left = 100000
    right = -100000
    bot = 100000
    top = -100000

    def rotate(ang,a,b):
        x, y = a, b
        a = x * math.cos(ang) - y * math.sin(ang)
        b = x * math.sin(ang) + y * math.cos(ang)
        return a,b

    for p in temp_points:
        p[0], p[1] = rotate(-angle,p[0],p[1])
        if p[0] < left:
            left = p[0]
        if p[0] > right:
            right = p[0]
        if p[1] > top:
            top = p[1]
        if p[1] < bot:
            bot = p[1]

    lb = (left,bot)
    lt = (left,top)
    rb = (right,bot)
    rt = (right,top)
    lb,lt,rt,rb = [rotate(angle,p[0],p[1]) for p in (lb,lt,rt,rb)]
    box = [lb, rb, rt, lt]
    return box
