import numpy as np

inf = 10e10

def point_between(p1, p2, p3):

    lst = zip(p1, p2, p3)
    check = [i[0] <= i[1] <= i[2] or i[0] >= i[1] >= i[2] for i in lst]

    res = False if False in check else True
    return res

def get_equation(points):
    point1, point2 = points

    delta = [p2 - p1 for p1, p2 in zip(point1, point2)]

    # ax + by = c
    if delta[0] == 0:
        a = 1
        b = 0
        c = point1[0]
    else:
        m = delta[1] / delta[0]

        a = -m 
        b = 1
        c = -m*point1[0] + point1[1]

    return [a, b, c]

def distance(points):
    point1, point2 = points

    delta = [(p2 - p1)**2 for p1, p2 in zip(point1, point2)]
    
    # print(np.sqrt(sum(delta)))

    return np.sqrt(sum(delta))
