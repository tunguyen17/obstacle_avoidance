from keras.models import Sequential
from keras.layers import Dense
import numpy as np

class Brain():
    def __init__(self, buffer_size, p = 0.8, gamma = 0.9, input_shape = 6):
        
        # Initialize learning model
        self.model = Sequential()

        # Hidden Layer 1
        self.model.add(Dense(30, activation = 'sigmoid', input_shape = (input_shape,), kernel_initializer = 'lecun_uniform')) #, bias_initializer = 'Zeros'))
        # Hidden Layer 2
        self.model.add(Dense(10, activation = 'sigmoid', kernel_initializer = 'lecun_uniform')) #, bias_initializer = 'Zeros'))
        # Output
        self.model.add(Dense(3, activation = 'linear', kernel_initializer = 'lecun_uniform')) #, bias_initializer = 'Zeros'))
        # Compile model
        self.model.compile(optimizer = 'rmsprop', loss = 'mse')

        # Learning parameter
        self.buffer_size = buffer_size
        self.learning_size = int(buffer_size*p)
        self.p = p
        self.gamma = gamma

        # Initialize buffer
        tmp_mem = [ [0.0]*5, 0, 0.0, [0.0]*5]
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
            
    def predict_a(self, s):
        feature = np.array(s)[np.newaxis, :]
        predict = self.model.predict(feature)

        return predict.argmax()
    
    def create_input(data, i = 0):
        return data[0] 

    def train(self):
        idx = np.random.randint(self.buffer_size, size = self.learning_size)

        train = self.buffer[idx]
        
        s0 = np.apply_along_axis(lambda x: x[0], 1, train)
        
        r = train[:,2]

        s1 = np.apply_along_axis(lambda x: x[3], 1, train)
        
        oldQ = self.model.predict(s0)
        newQ = self.model.predict(s1)
        
        target = oldQ.copy()

        for i, v in enumerate(r):
            a0 = int(train[i][1])
            if v <= - 500:
                target[i][a0] = v 
            else:
                target[i][a0] = v + self.gamma*max(newQ[i])

        
        self.model.fit(s0, target, epochs=10, verbose=0)

    def save(self, age):
        filename = 'saved-model-age-'+ str(age) + '.h5'  
        self.model.save_weights("weights/" + filename, overwrite = True)
        print(filename)
