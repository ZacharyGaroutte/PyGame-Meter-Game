############################################################################
# Cole Elam
# Joshua Baldwin
# Garrett Chumbley
# Zachary Garoutte
# Camdon Ritterby
# 12/4/2020
# CptS 111, Fall 2020
# Programming Assignment #8
# Creating a Meteor Shower Game
# This is a program that will create a mini-game where meteors spawn from the
# top of the screen and will slowly fall towards the player. If the player dodges
# the meteor they gain a point, and if they collide with it the game ends.
############################################################################
import pygame as pyg
import random as rand
import numpy as np

def meteor_colors():
    '''
    This is a function that generates a random color for the meteors
    '''
    return (rand.randint(1, 255), rand.randint(1, 255), rand.randint(1, 233))
    
def set_speed(score):
    '''
    This fuction will return the speed scores used in other functions
    '''
    speed = 0 
    if score <= 10:             #sets the initial speed to equal 5 while under 10 points
        speed = 5
    elif score >= 11:           #increases the speed if above 10 points
        speed = 5
        for i in range(score):  #loops through score 
            if i%10 == 0:       #checks for only score values that are varibles of ten
                speed += 2      #adds 2 for each iteration
    return speed

def draw_meteors(met_list, met_dim, screen):
    '''
    This function draws the meteors for every position withing the given list
    '''
    for i in met_list:
        pyg.draw.rect(screen, meteor_colors(), (i[0], i[1], met_dim, met_dim), 25)    #draws a meteor for every corrdinate pair in the list
    return

def drop_meteors(met_list, met_size, scr_width):
    '''
    This is a function that will dictate the location and time in which meteors
    spawn at the top of the screen
    '''
    fall_time = rand.random()
    if (fall_time <= 0.25):              #dictates the rate in which the meteors spawn
        x = rand.randrange(0, scr_width, met_size)  #generates a random x value for the meteor corrdinates
        met_list.append([x, 0])
    return 

def update_meteor_positions(met_list, scr_height, score, met_speed):
    '''
    This is a function that will slowly update the meteors positions that are
    in a list so that it gives the apperiance of moving down the screen
    '''
    for met in met_list:
        met[1] = met[1] + met_speed     #This moves the meteors down the screen by the rate of the current speed
        if met[1] >= scr_height:        #Checks to see if meteors have hit the bottem of the screen
            met_list.remove(met)        #if this iterates, it removes the meteor from the list and adds a point
            score += 1
            continue

    return score

def detect_collision(meteors, player_pos, player_size, met_size):
    '''
    This is a function that will detect whether a player has collided with a
    falling meteor. it does this by checking every single meteor pasted to it
    that alines with the players x and y values.
    '''
    ipl = int(player_pos[0])
    if  (meteors[0] + (met_size-1)) in range(ipl, ipl + player_size):
        if (meteors[1] + (met_size-1)) in range(player_pos[1], player_pos[1] + player_size):  #a nested conditional that test both the x and y values of the player and the meteor
            return True     #returns true if the meteor and the player have overlapped (touched)
    if meteors[0] in range(ipl, ipl + player_size):
        if meteors[1] in range(player_pos[1], player_pos[1] + player_size):
            return True
        else:
             return False
    if ipl < 0:           #Checks to see if the player has crossed the left border
        return True
    if ipl == 800:        #Checks to see if the player has crossed the right border
        return True


def collision_check(met_list,player_pos, player_size, met_size):
    '''
    This is a function that will detect whether a player has collided with any
    meteor currently on screen by sending meteor information to the function
    detect_collision.
    '''
    for meteors in met_list:    #pulls out one meteor at a time to check for collision
        if detect_collision(meteors, player_pos, player_size, met_size) is True:
            return True #Returns true if a meteor has collided with the player
        else:
            if detect_collision(meteors, player_pos, player_size, met_size) is False:
                return False    #Returns false if the player has not collided with a meteor

def main():
    '''
    Initialize pygame and pygame parameters.  Note that both player and meteors
    are square.  Thus, player_dim and met_dim are the height and width of the
    player and meteors, respectively.  Each line of code commented.
    '''
    pyg.init()                # initialize pygame

    width = 800               # set width of game screen in pixels
    height = 600              # set height of game screen in pixels

    pl_color = (0,255,170)           # rgb color of player
    background = (100,100,100)    # rgb color of sky (midnight blue)

    player_dim = 50           # player size in pixels
    player_pos = [width/2, height-2*player_dim]  # initial location of player
                                                 # at bottom middle; height
                                                 # never changes

    met_dim = 20              # meteor size in pixels
    met_list = []             # initialize list of two-element lists
                              # giving meteor positions

    screen = pyg.display.set_mode((width, height)) # initialize game screen

    game_over = False         # initialize game_over; game played until
                              # game_over is True

    score = 0                 # initialize score

    clock = pyg.time.Clock()  # initialize clock to track time

    my_font = pyg.font.SysFont("monospace", 35) # initialize system font

    while not game_over:                       # play until game_over True
        for event in pyg.event.get():          # loop through events in queue
            if event.type == pyg.KEYDOWN:      # checks for key press
                x = player_pos[0]              # assign current x position
                y = player_pos[1]              # assign curren y position
                if event.key == pyg.K_LEFT:    # checks if left arrow;
                    x -= player_dim            # if true, moves player left
                elif event.key == pyg.K_RIGHT: # checks if right arrow;
                    x += player_dim            # else moves player right
                player_pos = [x, y]            # reset player position
            
        screen.fill(background)                # refresh screen bg color
        img = pyg.image.load('boring.jpg')
        bckimage = img.get_rect()
        screen.blit(img, bckimage)
        drop_meteors(met_list, met_dim, width) # self-explanatory; read prompt
        speed = set_speed(score)               # self-explanatory; read prompt
        score = update_meteor_positions(met_list, height, score, speed)
                                               # read prompt
        text = "Score: " + str(score)              # create score text
        label = my_font.render(text, 1, pl_color)    # render text into label
        screen.blit(label, (width-250, height-40)) # blit label to screen at
                                                   # given position; for our 
                                                   # purposes, just think of
                                                   # blit to mean draw
        draw_meteors(met_list, met_dim, screen)#, met_color) # self-explanatory;
                                                        # read prompt

        pyg.draw.rect(screen, pl_color, (player_pos[0], player_pos[1], player_dim, player_dim))                                        # draw player

        if collision_check(met_list, player_pos, player_dim, met_dim):
            game_over = True                       # read prompt
    
        clock.tick(30)                             # set frame rate to control
                                                   # frames per second (~30); 
                                                   # slows down game

        pyg.display.update()                       # update screen characters
    if game_over == True:
        print('Final score is', score)                   # final score
        if score == 0:
            print('Pretty Pathetic, Not Going to Lie')   #adds insults based on score
        elif 0<score<=25:
            print('Not that great')
        elif 25<score<= 50:
            print('At least you tried')
        elif 50<score<=75:
            print('Good Enough I guess....')
        elif 75<score<=150:
            print('Not Bad, Bot Bad')
        else:
            print('We can call that the high score')
    pyg.quit()                                     # leave pygame

main()
