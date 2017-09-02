class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rect(object):
    def __init__(self, p1, p2):
        self.left   = min(p1.x, p2.x)
        self.right  = max(p1.x, p2.x)
        self.bottom = min(p1.y, p2.y)
        self.top    = max(p1.y, p2.y)

    def __repr__(self):
        return 'Rectangle(%d, %d, %d, %d)' % (
            self.left,
            self.bottom,
            self.right,
            self.top,
        )

def overlap(r1, r2):
    overlap_h = True
    overlap_v = True
    if (r1.left >= r2.right) or (r1.right <= r2.left):
        overlap_h = False
    if (r1.top <= r2.bottom) or (r1.bottom >= r2.top):
        overlap_v = False
    return overlap_h and overlap_v

