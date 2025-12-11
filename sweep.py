from sortedcontainers import SortedList

def ort(p, q, r):
    val = (q[1]-p[1])*(r[0]-q[0])- (q[0] - p[0]) * (r[1] - q[1])
    if val == 0: return 0
    return 1 if val > 0 else 2

def on_line(p, q, r):
    return (max(p[0], r[0]) >= q[0] >= min(p[0], r[0]) and
            max(p[1], r[1]) >= q[1] >= min(p[1], r[1]))

def intersect(p1, q1, p2, q2):
    o1 = ort(p1, q1, p2)
    o2 = ort(p1, q1, q2)
    o3 = ort(p2, q2, p1)
    o4 = ort(p2, q2, q1)

    if o1 != o2 and o3 != o4: return True

    if o1 == 0 and on_line(p1, p2, q1): return True
    if o2 == 0 and on_line(p1, q2, q1): return True
    if o3 == 0 and on_line(p2, p1, q2): return True
    if o4 == 0 and on_line(p2, q1, q2): return True

    return False

class segment:
    def __init__(self, p1, p2):
        if p1[0] > p2[0] or (p1[0] == p2[0] and p1[1] > p2[1]):
            self.p1, self.p2 = p2, p1
        else:
            self.p1, self.p2 = p1, p2

    def get_y_on_x(self, x):

        x1, y1 = self.p1
        x2, y2 = self.p2

        if x1 == x2:
            return y1

        return y1 + (y2 - y1) * (x - x1) / (x2 - x1)

    def __lt__(self, other):
        x = globals().get('hypothetical_sweep_x', self.p1[0])

        y_self = self.get_y_on_x(x)
        y_other = other.get_y_on_x(x)

        return y_self < y_other


def check_new(new, olds):

    for seg in olds:
        shared_points = 0
        if new.p1 == seg.p1 or new.p1 == seg.p2:
            shared_points += 1
        if new.p2 == seg.p1 or new.p2 == seg.p2:
            shared_points += 1

        if shared_points == 1 or shared_points == 2:
            continue

        if intersect(new.p1, new.p2, seg.p1, seg.p2):
            return False

    return True