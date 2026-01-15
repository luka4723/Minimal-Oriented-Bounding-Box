
def ort(p, q, r):
    val = (q[1]-p[1])*(r[0]-q[0])- (q[0] - p[0]) * (r[1] - q[1])
    if val == 0: return 0
    return 1 if val > 0 else 2

class segment:
    def __init__(self, p1, p2):
        if p1[0] > p2[0] or (p1[0] == p2[0] and p1[1] > p2[1]):
            self.p1, self.p2 = p2, p1
        else:
            self.p1, self.p2 = p1, p2
    def __str__(self):
        return f"({self.p1[0]},{self.p1[1]},{self.p2[0]},{self.p2[1]})"
    def __repr__(self):
        return self.__str__()

def make_ccw(pts,segments):
    n = len(pts)
    area = 0
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        area += (x0 * y1 - x1 * y0)
    if area < 0:
        pts = pts[::-1]
        segments = segments[::-1]
    return pts, segments

def intersect(A, B, C, D):
    det = (B[0] - A[0]) * (C[1] - D[1]) - (B[1] - A[1]) * (C[0] - D[0])
    detT = (C[0] - A[0]) * (C[1] - D[1]) - (C[1] - A[1]) * (C[0] - D[0])
    detS = (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])

    if det == 0:
        return True

    if 0 < detT / det < 1 and 0 < detS / det < 1:
        return True
    return None

def check_new(new, olds):

    for seg in olds:
        if new.p1 == seg.p1 or new.p1 == seg.p2 or new.p2 == seg.p1 or new.p2 == seg.p2:
            continue

        if intersect(new.p1, new.p2, seg.p1, seg.p2):
            return False
    return True