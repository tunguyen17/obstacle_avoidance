import numpy as np

inf = 100

def point_between(p1, p2, p3, tol = 3):

    lst = zip(p1, p2, p3)
    check = [i[0]-tol <= i[1] <= i[2]+tol or i[0]+tol >= i[1] >= i[2]-tol for i in lst]

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

def round_lst(lst):
    return [int(i) for i in lst]

def scale(x, a = 0, b = 1):
    m = 0
    r = inf - m

    if r == 0:
        r = 1
    y = (x-m)/ r * (b - a) + a
    return y

def get_cross(l1, l2):
    a = np.array([l1[:2], l2[:2]])
    b = np.array([l1[2], l2[2]])

    return np.linalg.solve(a, b)

def r(x):
    return -50*(x-1)**2 + 50

def g(x, init = 0.5):
    return (0.9 - init) * (x ** 2 + 1) /  (x ** 2 + 10**7) + init
    

