import math

def distance(point1, point2):
    '''Calculates the Euclidean distance between two points.'''
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5

def tanhtween(t, sharpness):
    return (math.tanh(sharpness * t - sharpness / 2) - math.tanh(-sharpness / 2)) / (math.tanh(sharpness / 2) - math.tanh(-sharpness / 2))

def area(point1, point2, point3):
    return abs(point1.x * (point2.y - point3.y) + point2.x * (point3.y - point1.y) + point3.x * (point1.y - point2.y) ) / 2

def circle_intersect(O, radius, P1, P2):
    t = ((O - P1).x * (P2 - P1).x + (O - P1).y * (P2 - P1).y) / (abs(P2 - P1)**2)
    t_clamped = max(0, min(1, t))
    closest = P1 + (P2 - P1) * t_clamped
    return distance(O, closest) < radius

def orient(a, b, c):
    return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)

def on_segment(A, B, C):
    return orient(A, C, B) == 0 and min(A.x, C.x) <= B.x <= max(A.x, C.x) and min(A.y, C.y) <= B.y <= max(A.y, C.y)


def segments_intersect(P1, P2, Q1, Q2):
    o1 = orient(P1, P2, Q1)
    o2 = orient(P1, P2, Q2)
    o3 = orient(Q1, Q2, P1)
    o4 = orient(Q1, Q2, P2)

    # General case
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True

    # Special collinear cases
    if o1 == 0 and on_segment(P1, Q1, P2): return True
    if o2 == 0 and on_segment(P1, Q2, P2): return True
    if o3 == 0 and on_segment(Q1, P1, Q2): return True
    if o4 == 0 and on_segment(Q1, P2, Q2): return True

    return False



loop = 10 ** 8