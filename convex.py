from functools import cmp_to_key

import sweep


def dist(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def findConvexHull(points):
    p0 = min(points, key=lambda p: (p[1], p[0]))

    def compare(p1, p2):
        o = sweep.ort(p0, p1, p2)
        if o == 0:
            return dist(p0, p1) - dist(p0, p2)
        return -1 if o == 1 else 1

    other_points = [p for p in points if p != p0]
    a_sorted = [p0] + sorted(other_points, key=cmp_to_key(compare))

    m = 1
    for i in range(1, len(a_sorted)):
        while i < len(a_sorted) - 1 and sweep.ort(p0, a_sorted[i], a_sorted[i + 1]) == 0:
            i += 1
        if i < len(a_sorted):
            a_sorted[m] = a_sorted[i]
            m += 1

    stek = [a_sorted[0], a_sorted[1], a_sorted[2]]

    for i in range(3, m):
        while len(stek) > 1 and sweep.ort(stek[-2], stek[-1], a_sorted[i]) != 1:
            stek.pop()
        stek.append(a_sorted[i])

    return [[int(p[0]), int(p[1])] for p in stek]