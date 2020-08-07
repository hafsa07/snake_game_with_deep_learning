import pygame
import random
import time
import math
from tqdm import tqdm
import numpy as np


def display_snake(snake_position, display):
    for position in snake_position:
        pygame.draw.rect(display, (255, 0, 0), pygame.Rect(position[0], position[1], 10, 10)) 
        # will draw a rectangle corresponding to given arguments which will represent our snake


def display_apple(apple_position, display):
    pygame.draw.rect(display, (0, 255, 0), pygame.Rect(apple_position[0], apple_position[1], 10, 10)) # will draw an apple


def starting_positions():
    snake_start = [100, 100]  #snake will start from here where x = 100 and y = 100
    snake_position = [[100, 100], [90, 100], [80, 100]]
    apple_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10] #place apple in random x y plane 
    score = 3  #default score is 3

    return snake_start, snake_position, apple_position, score


def apple_distance_from_snake(apple_position, snake_position):
    return np.linalg.norm(np.array(apple_position) - np.array(snake_position[0])) 
#distance of an apple from snake here numpy array will normalize our snake postion  and apple position .. we are passing list to np.array ...


# in this function we will define movemenet of snake .. to move a snake , one unit must be added to head and one unit must be removed from tail so we are defining rules 
# to move snake  

def generate_snake(snake_start, snake_position, apple_position, button_direction, score):
    if button_direction == 1:
        snake_start[0] += 10  # move snake to right
    elif button_direction == 0:
        snake_start[0] -= 10  #move snkae to left
    elif button_direction == 2:
        snake_start[1] += 10  # move snkae to top
    else:
        snake_start[1] -= 10  #move snake to downward direction



    if snake_start == apple_position: # snake eats apple
        apple_position, score = collision_with_apple(apple_position, score) #calling this function will increase score and snake length
        snake_position.insert(0, list(snake_start))  #move snake in new direction we will not remove one from tail because snake eats an apple so size is increased

    else:
        snake_position.insert(0, list(snake_start)) # add unit to to tail 
        snake_position.pop() #remove a unit from tail

    return snake_position, apple_position, score

#when snake eats an apple then generate new apple and increase score by 1

def collision_with_apple(apple_position, score):
    apple_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10] #generate new apple at random x y positon  
    score += 1  #increase score
    return apple_position, score


def collision_with_boundaries(snake_start):
    if snake_start[0] >= 500 or snake_start[0] < 0 or snake_start[1] >= 500 or snake_start[1] < 0:
        # snake_start[0] means x cordinate and snake[1] means y cordiantes of snake  so if they are greaate than 500 it means collisoin
        # also if any cordinate of snkae is less than 0 then game over 
        return 1
    else:
        return 0


def collision_with_self(snake_start, snake_position):
    # snake_start = snake_position[0]
    if snake_start in snake_position[1:]: 
        return 1
    else:
        return 0


def blocked_directions(snake_position):
    current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1]) #current position of snake

    left_direction_vector = np.array([current_direction_vector[1], -current_direction_vector[0]])   #will make snake in left direction 
    right_direction_vector = np.array([-current_direction_vector[1], current_direction_vector[0]]) 

    is_front_blocked = is_direction_blocked(snake_position, current_direction_vector) #return 1 if blocked
    is_left_blocked = is_direction_blocked(snake_position, left_direction_vector)
    is_right_blocked = is_direction_blocked(snake_position, right_direction_vector)

    return current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked


def is_direction_blocked(snake_position, current_direction_vector):
    next_step = snake_position[0] + current_direction_vector   #check variable for block direction ... 
    # for ecample snake position is 500 then it will become 501 we will call collision with boundaries function to see if collides or not if collides 
    # then we will return 1 to avoid game over      
    
    snake_start = snake_position[0]
    if collision_with_boundaries(next_step) == 1 or collision_with_self(next_step.tolist(), snake_position) == 1:
        return 1
    else:
        return 0


#to move snake automatically without user 

def generate_random_direction(snake_position, angle_with_apple): 
    
#     LEFT -> button_direction = 0
#     RIGHT -> button_direction = 1
#     DOWN ->button_direction = 2
#     UP -> button_direction = 3
    
    
    direction = 0
    if angle_with_apple > 0:
        # If angle > 0, this means Apple is on the right side of the snake. So snake should move to the right. 
        direction = 1
    elif angle_with_apple < 0:
        direction = -1
    else:
        direction = 0

    return direction_vector(snake_position, angle_with_apple, direction)


def direction_vector(snake_position, angle_with_apple, direction):
    current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])
    left_direction_vector = np.array([current_direction_vector[1], -current_direction_vector[0]])
    right_direction_vector = np.array([-current_direction_vector[1], current_direction_vector[0]])

    new_direction = current_direction_vector

    if direction == -1:
        new_direction = left_direction_vector
    if direction == 1:
        new_direction = right_direction_vector

    button_direction = generate_button_direction(new_direction)

    return direction, button_direction


def generate_button_direction(new_direction):
    
    
    button_direction = 0
    if new_direction.tolist() == [10, 0]:
        button_direction = 1
    elif new_direction.tolist() == [-10, 0]:
        button_direction = 0
    elif new_direction.tolist() == [0, 10]:
        button_direction = 2
    else:
        button_direction = 3

    return button_direction


def angle_with_apple(snake_position, apple_position):
    # NumPy is used to work with arrays. The array object in NumPy is called ndarray.
    # we pass a list, tuple or any array-like object into the array() method, and it will be converted into an ndarray:
    # Lets  first calculate the snake’s current direction vector and Apple’s direction from the snake’s current position. 
    # Snake direction vector can be calculated by simply subtracting 0th index of the snake’s list from the 1st index.
    #  And to calculate apple direction from the snake, just subtract 0th index of snake’s list from Apple’s position.
    
    apple_direction_vector = np.array(apple_position) - np.array(snake_position[0])
    snake_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])

    norm_of_apple_direction_vector = np.linalg.norm(apple_direction_vector) 
    # normalzing apple direction vector array
    norm_of_snake_direction_vector = np.linalg.norm(snake_direction_vector)
    if norm_of_apple_direction_vector == 0:
        norm_of_apple_direction_vector = 10
    if norm_of_snake_direction_vector == 0:
        norm_of_snake_direction_vector = 10

    apple_direction_vector_normalized = apple_direction_vector / norm_of_apple_direction_vector
    snake_direction_vector_normalized = snake_direction_vector / norm_of_snake_direction_vector
    angle = math.atan2(
        apple_direction_vector_normalized[1] * snake_direction_vector_normalized[0] - apple_direction_vector_normalized[
            0] * snake_direction_vector_normalized[1],
        apple_direction_vector_normalized[1] * snake_direction_vector_normalized[1] + apple_direction_vector_normalized[
            0] * snake_direction_vector_normalized[0]) / math.pi
    return angle, snake_direction_vector, apple_direction_vector_normalized, snake_direction_vector_normalized


def play_game(snake_start, snake_position, apple_position, button_direction, score, display, clock):
    crashed = False
    while crashed is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #user clicked on close button
                crashed = True
        display.fill((255, 255, 255)) #backfround fill

        display_apple(apple_position, display)  
        display_snake(snake_position, display)

        snake_position, apple_position, score = generate_snake(snake_start, snake_position, apple_position,
                                                               button_direction, score)
        pygame.display.set_caption("SCORE: " + str(score))  #display score at the top
        pygame.display.update() #update user interface
        clock.tick(50)  #speed of game 

        return snake_position, apple_position, score