from functools import cmp_to_key

import sweep


def distSq(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def findConvexHull(points):
    n = len(points)

    if n < 3:
        return [[-1]]

    a = [(p[0], p[1]) for p in points]

    p0 = min(a, key=lambda p: (p[1], p[0]))

    def compare(p1, p2):
        o = sweep.ort(p0, p1, p2)
        if o == 0:
            d1 = distSq(p0, p1)
            d2 = distSq(p0, p2)
            if d1 < d2:
                return -1
            elif d1 > d2:
                return 1
            else:
                return 0
        return -1 if o == 1 else 1

    other_points = [p for p in a if p != p0]
    a_sorted = [p0] + sorted(other_points, key=cmp_to_key(compare))

    m = 1
    for i in range(1, len(a_sorted)):
        while i < len(a_sorted) - 1 and \
                sweep.ort(p0, a_sorted[i], a_sorted[i + 1]) == 0:
            i += 1
        if i < len(a_sorted):
            a_sorted[m] = a_sorted[i]
            m += 1

    if m < 3:
        return [[-1]]

    st = [a_sorted[0], a_sorted[1], a_sorted[2]]

    for i in range(3, m):
        while len(st) > 1 and \
                sweep.ort(st[-2], st[-1], a_sorted[i]) != 1:
            st.pop()
        st.append(a_sorted[i])

    if len(st) < 3:
        return [[-1]]

    return [[int(p[0]), int(p[1])] for p in st]