from keras.models import Sequential
from keras.layers import Dense
import numpy as np

class Brain():
    def __init__(self, buffer_size, p = 0.2, alpha = 0.3):
        
        # Initialize learning model
        self.model = Sequential()

        # Hidden Layer 1
        self.model.add(Dense(10, activation = 'sigmoid', input_shape = (6,), kernel_initializer = 'random_uniform', bias_initializer = 'Zeros'))
        # Hidden Layer 2
        self.model.add(Dense(5, activation = 'sigmoid', kernel_initializer = 'random_uniform', bias_initializer = 'Zeros'))
        # Output
        self.model.add(Dense(3, activation = 'linear', kernel_initializer = 'random_uniform', bias_initializer = 'Zeros'))
        # Compile model
        self.model.compile(optimizer = 'rmsprop', loss = 'mse')

        # Learning parameter
        self.buffer_size = buffer_size
        self.learning_size = int(buffer_size*p)
        self.p = p
        self.alpha = alpha

        # Initialize buffer
        tmp_mem = [ [0.0]*5, 0, 0.0, [0.0]*5, 0  ]
        self.buffer = np.array([tmp_mem]*buffer_size)
        self.buffer_head = 0
        
    
    def add_memory(self, memory):
        if self.buffer_head < self.buffer_size:
            self.buffer[self.buffer_head] = np.array(memory)
            self.buffer_head += 1
        else:
            idx = np.random.randint(self.buffer_size)
            self.buffer[idx] = memory
    
    def print_buffer(self):
        for i,v in enumerate(self.buffer):
            print(i, ". ", v)
            
    def predict_a(self, s0a0):
        feature = np.array(s0a0)[np.newaxis, :]
        predict = self.model.predict(feature)

        return predict.argmax()
    
    def create_input(data):
        return data[0] + [data[1]]

    def train(self):
        idx = np.random.randint(self.buffer_size, size = self.learning_size)

        train = self.buffer[idx]
        
        s0a0 = np.apply_along_axis(Brain.create_input, 1, train[:,:2])
        
        r = train[:,2]

        s1a1 = np.apply_along_axis(Brain.create_input, 1, train[:,3:])
        
        pred1 = self.model.predict(s1a1)
        
        target = pred1.copy()

        for i, v in enumerate(r):
            a0 = int(s0a0[i][-1])
            a1 = int(s1a1[i][-1])
            if v <= - 500:
                target[i][a0] = v 
            else:
                target[i][a0] = v + self.alpha*pred1[i][a1]

        
        self.model.fit(s0a0, target, epochs=5, verbose=0)
