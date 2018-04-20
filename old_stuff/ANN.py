import numpy as np

# Identity Function

def id(x):
    return x

def id_deriv(x):
    return float(1)

# relu function

def relu(x):
    x[x<0] = 0
    return x

def relu_deriv(x):
    return (x>0).astype(float)


# tanh
def tanh(x):
    return np.tanh(x)

def tanh_deriv(x):
    return 1 - tanh(x)**2

# arctan
def arctan(x):
    return np.arctan(x)

def arctan_deriv(x):
    return 1 / (1+x**2)

def sigmoid(x):
    y = np.zeros_like(x)
    idx = x > -700
    y[idx] = 1 / (1 + np.exp(-1*x[idx]))
    return y

def sigmoid_deriv(x):
    y = sigmoid(x)
    return y*(1-y)

def loss(e):
    return (e**2).sum() / 2

def loss_deriv(e)
    return e


