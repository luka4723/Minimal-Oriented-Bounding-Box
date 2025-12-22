import math
from pstats import add_callers


def box(seg, points):
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


def is_convex(points):
    n = len(points)
    sign = None
    for i in range(n):
        p1 = points[i]
        p2 = points[(i + 1) % n]
        p3 = points[(i + 2) % n]

        cross = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

        if abs(cross) < 1e-10:
            continue

        if sign is None:
            sign = cross > 0
        elif (cross > 0) != sign:
            return False
    return True
def is_ccw(points):
    area = 0
    n = len(points)
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    return area > 0
def dot(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

def minus(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]

def box2(seg,points,segments,seg_it):
    k1 = math.atan2(seg[1][1] - seg[0][1], seg[1][0] - seg[0][0])
    vec1 =  [math.cos(k1),math.sin(k1)]
    vec2 =  [-vec1[1],vec1[0]]
    points[seg_it] = points[seg_it][0] + 0.001*vec1[0],points[seg_it][1] + 0.001*vec1[1]

    def extreme_points(vec, pts):
        a = 0
        b = len(pts) - 1
        n = len(pts)

        if dot(vec, pts[a])>=dot(vec, pts[(a-1+n)%n]) and dot(vec, pts[a])>= dot(vec, pts[(a + 1) % n]):
            return pts[a]

        if dot(vec, pts[b]) >= dot(vec, pts[(b - 1 + n) % n]) and dot(vec, pts[b]) >= dot(vec, pts[(b + 1) % n]):
            return pts[b]

        while True:
            if a<b:
                c = (a+b)//2
            else:
                c = ((b+a+n)//2)%n

            iprev = (c - 1 + n) % n
            inxt = (c + 1) % n

            mid = dot(vec,pts[c])
            prev = dot(vec,pts[iprev])
            nxt = dot(vec,pts[inxt])
            a_val = dot(vec,pts[a])
            nxt_a = dot(vec,pts[(a+1)%n])

            if mid >= prev and mid >= nxt:
                return pts[c]

            if nxt_a>a_val and nxt<mid:
                b = c

            elif nxt_a<a_val and nxt>mid:
                a = c

            elif nxt_a>a_val  and nxt>mid:
                if a_val>mid:
                    b = c
                else:
                    a = c
            else:
                if a_val<mid:
                    b = c
                else:
                    a = c

    points[seg_it] = points[seg_it][0] - 0.001 * vec1[0], points[seg_it][1] - 0.001 * vec1[1]
    p1,p2,p3,p4 = extreme_points(vec1, points),extreme_points(vec2, points),extreme_points([-vec1[0], -vec1[1]],points),extreme_points([-vec2[0], -vec2[1]],points)

    maxx = dot(p1, vec1)
    minx = dot(p3, vec1)
    maxy = dot(p2, vec2)
    miny = dot(p4, vec2)

    lb = (minx * vec1[0] + miny * vec2[0], minx * vec1[1] + miny * vec2[1])
    lt = (minx * vec1[0] + maxy * vec2[0], minx * vec1[1] + maxy * vec2[1])
    rb = (maxx * vec1[0] + miny * vec2[0], maxx * vec1[1] + miny * vec2[1])
    rt = (maxx * vec1[0] + maxy * vec2[0], maxx * vec1[1] + maxy * vec2[1])
    return [lb, rb, rt, lt]

