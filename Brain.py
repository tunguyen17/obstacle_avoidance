from keras.models import Sequential
from keras.layers import Dense
import numpy as np

class Brain():
    def __init__(self, buffer_size, p = 0.2, alpha = 0.3):
        
        # Initialize learning model
        self.model = Sequential()

        # Hidden Layer 1
        self.model.add(Dense(70, activation = 'sigmoid', input_shape = (6,), kernel_initializer = 'random_uniform', bias_initializer = 'Zeros'))
        # Hidden Layer 2
        self.model.add(Dense(50, activation = 'sigmoid', kernel_initializer = 'random_uniform', bias_initializer = 'Zeros'))
        # Output
        self.model.add(Dense(3, activation = 'linear', kernel_initializer = 'random_uniform', bias_initializer = 'Zeros'))
        # Compile model
        self.model.compile(optimizer = 'rmsprop', loss = 'mse')

       # Learning parameter
        self.buffer_size = buffer_size
        self.learning_size = int(buffer_size*p)
        self.p = p
        self.alpha = alpha

    def predict_a(self, s0a0):
        feature = np.array(s0a0)[np.newaxis, :]
        predict = self.model.predict(s0a0)

        return predict.argmax()
