import math

def distance(point1, point2):
    '''Calculates the Euclidean distance between two points.'''
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5

def tanhtween(t, sharpness):
    return (math.tanh(sharpness * t - sharpness / 2) - math.tanh(-sharpness / 2)) / (math.tanh(sharpness / 2) - math.tanh(-sharpness / 2))