from game import *
from training_data import generate_training_data

from keras.models import Sequential
from keras.layers import Dense

display_width = 500
display_height = 500
green = (0,255,0)
red = (255,0,0)
black = (0,0,0)
white = (255,255,255)

pygame.init()  # start game
display=pygame.display.set_mode((display_width,display_height)) #set display width and height
clock=pygame.time.Clock() #speed of snake

'''
LEFT -> button_direction = 0
RIGHT -> button_direction = 1
DOWN ->button_direction = 2
UP -> button_direction = 3
'''
training_data_x, training_data_y = generate_training_data(display,clock)


# I have used hit and trial method to find network architecture. After some hit and trials, 
# I have found a workable architecture, which consists of 2 hidden layers one of 9 units and other of 15 units. For the hidden layer, 
# I have used the non-linear function ‘relu’ and for the output layer, I have used ‘softmax’.

#  Here I have used keras

model = Sequential()
model.add(Dense(units=9,input_dim=7))

model.add(Dense(units=15, activation='relu'))
model.add(Dense(units=3,  activation = 'softmax'))

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
model.fit((np.array(training_data_x).reshape(-1,7)),( np.array(training_data_y).reshape(-1,3)), batch_size = 256,epochs= 3)

model.save_weights('model.h5')
model_json = model.to_json()
with open('model.json', 'w') as json_file:
    json_file.write(model_json)