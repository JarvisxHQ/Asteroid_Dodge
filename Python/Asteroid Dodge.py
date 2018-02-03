import pygame
import time
import random
import ctypes
import pygame.sprite as sprite
import sys

pygame.init()               #Intializes the pygame module
pygame.mixer.pre_init()     #Intializes the pygame's mixer module

display_width = 800         #Sets the variable display_width to 800
display_height = 500        #Sets the variable display_height to 500

black = (0,0,0)             #RGB colour code for black
white = (255,255,255)       #RGB colour code for white
red = (200,0,0)             #RGB colour code for red
blue = (0,0,200)            #RGB colour code for blue
green = (0,200,0)           #RGB colour code for green
orange = (255,170,0)        #RGB colour code for orange
bright_red = (255,0,0)      #RGB colour code for brighter green
bright_blue = (0,0,255)     #RGB colour code for brighter blue
bright_green = (0,255,0)    #RGB colour code for brighter green

car_width = 100             #Sets the variable car_width to 100
car_height = 50             #Sets the variable car_width to 100

gameDisplay = pygame.display.set_mode((display_width,display_height))#Set the display width and height of the main window
pygame.display.set_caption('Asteriod Dodge')                         #Displays Asteriod ddodge on the top left corner of the window
clock = pygame.time.Clock()                                          #Defines the variable clock as the function time.Clock() to set a speed for the game

SmallImg = pygame.image.load('small.png')   #loads the small.png file into SmallImg
carImg = pygame.image.load('rocket.png')    #loads the rocket.png file into carImg
bgImg = pygame.image.load('space1.png')     #loads the space1.png file into bgImg
bg_rect = bgImg.get_rect()                  #Gets the background image rectangle
bg_size = bgImg.get_size()                  #Gets the background image size in pixels
pause = False                               #Set the booolean variable pause to FALSE
def Out(addr, byte):                                            #defines Out as function with 2 parameters (addr, byte)
    ctypes.windll.inpout32.Out32(addr, byte)                    #######################################################Outputs to the parellel cord

def In(addr):                                                   #defines In as function with 1 parameter (addr)
    return ctypes.windll.inpout32.Inp32(addr)                   #######################################################Gets input from parellel cord

def smallImg(thingx, thingy):                                   #defines smallImg as function with 2 parameters (thingx, thingy)
    gameDisplay.blit(SmallImg,(thingx,thingy))                  #Copies or blits the SmallImg which is the asteriod to the coordinates thingx and thingy

def things_dodged(count):                                       #defines things_dodged as function with one parameter (count)
    font = pygame.font.SysFont(None,25)                         #defines font as a default system font with size 25
    text = font.render("Dodged: " + str(count), True, green)    #render text to display the score 'count' variable(the score) in green with anti-aliasing on(smoother edges)
    gameDisplay.blit(text,(0,0))                                #copies or blits the object text to the coordinates (0,0)
    
def car(x,y):                                                   #defines car as function with 2 parameters (x,y)
    gameDisplay.blit(carImg,(x,y))                              #copies or blits the spaceship to the coordinates defined by the variable x and y
    
def text_objects(text, font):                                   #defines text_objects as function with 2 parameters (text, font)
    textSurface = font.render(text, True, bright_blue)          #defines textSurface as a object which has text, bright_blue color and anti-aliasing on for smoother letters
    return textSurface, textSurface.get_rect()                  #returns the 2 objects

def message_display(text,t):                                    #defines message_display as function with 1 parameter (text)
    largeText = pygame.font.Font('freesansbold.ttf', 115)       #defines largeText as an object with the freesansbold font and 115 size
    TextSurf, TextRect = text_objects(text, largeText)          #defines TextSurf as text and TextRect as largeText
    TextRect.center = ((display_width/2),(display_height/2))    #Sets the location of the text in the middle of the screen
    gameDisplay.blit(TextSurf, TextRect)                        #Copies the text to the screen
    pygame.display.update()                                     #Refreshs the screen so the text is now updated on the screen
    time.sleep(t)                                               #Displays the text for t seconds

def crash():                                                    #defines crash as a function with empty parameters
    message_display('You Crashed',2)                            #runs the message_display() function and inputs "You Crashed"
    game_loop()                                                 #Runs the game_loop() function

def noFuel():
    message_display('Out of fuel',2)
    game_loop()                                                 #Runs the game_loop() function

def fullTank():
    message_display('Fuel Filled',1)
    
def button(msg,x,y,w,h,ic,ac,action=None):                      #defines a function called button with 8 parameters (msg,x,y,w,h,ic,ac,action=None)
    mouse = pygame.mouse.get_pos()                              #gets the coordinates of where the mouse is
    click = pygame.mouse.get_pressed()                          #returns whether any of the mouse buttons are pressed or not the button is pressed or not
    
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y:               #do the following if the mouse's x and y coordinates are with the button
        pygame.draw.rect(gameDisplay, ac, (x,y,w,h))            #draws a rectangle on the gameDisplay with the active colour(ac) on the coordinates x and y with a width of w and a height of h
        if click[0]==1 and action != None:                      #does the following if the mouse is clicked and action has a value
            if action == "play":                                #does the following if action is equal to play
                game_loop()                                     #Runs the game_loop() function
            elif action == "quit":                              #does the following if action is equal to quit
                pygame.quit()                                   #ends the pygame module
                quit()                                          #quits the program
            elif action == "resume":                            #does the following if action is equal to resume
                global pause                                    #calls the variable pause as global
                pause = False                                   #defines the pause variable as False
    else:                                                       #if the if condition at its indent level above is False then does the following
        pygame.draw.rect(gameDisplay, ic, (x,y,w,h))            #draws a rectangle on the gameDisplay with the inactive colour(ic) on the coordinates x and y with a width of w and a height of h

    smallText = pygame.font.Font('freesansbold.ttf', 20)        #defines smallText as an object with the freesansbold font and 115 size
    textSurf, textRect = text_objects(msg, smallText)           #defines textSurf as msg and TextRect as smallText
    textRect.center = (x+(w/2), y+(h/2))                        #defines the coordinates of the object textRect
    gameDisplay.blit(textSurf, textRect)                        #Copies the text to the screen

def paused():                                                       #defines paused as a function with empty parameters
        
    while pause:                                                    #loops the following if pause variable is True
        for event in  pygame.event.get():                           #runs a for loop to read all the events occuring
            if event.type == pygame.QUIT:                           #if the event type is QUIT then the following happens
                pygame.quit()                                       #ends the pygame module
                quit()                                              #quits the program
        gameDisplay.blit(bgImg,(0,0))                               #copies the background image to the coordinates (0,0)
        largeText = pygame.font.Font('freesansbold.ttf', 115)       #defines largeText as an object with the freesansbold font and 115 size
        TextSurf, TextRect = text_objects("Paused", largeText)      #defines TextSurf as "Paused" and TextRect as largeText
        TextRect.center = ((display_width/2),(display_height/2))    #Sets the location of the text in the middle of the screen
        gameDisplay.blit(TextSurf, TextRect)                        #Copies the image to the screen

        button("RESUME",150,400,100,50,green, bright_green,"resume")#calls the button function to display RESUME, width of 100 pixels, height of 50 pixels, green colour and at (150,400)
        button("EXIT",600,400,100,50,red, bright_red,"quit")        #calls the button function to display QUIT, width of 100 pixels, height of 50 pixels, red colour and at (600,400)
        
        pygame.display.update()                                     #Refreshs the screen so the text is now updated on the screen
        clock.tick(15)                                              #sets the clock object to 15 ticks
    
def game_intro():                                                               #defines game_intro as a function with empty parameters
    intro = True                                                                #sets the intro varibale as True
    while intro:                                                                #loops the following as long as intro is True
        for event in  pygame.event.get():                                       #runs a for loop to read all the events occuring
            if event.type == pygame.QUIT:                                       #if the event type is QUIT then the following happens
                pygame.quit()                                                   #ends the pygame module
                quit()                                                          #quits the program
        gameDisplay.blit(bgImg,(0,0))                                           #copies the background image to the coordinates (0,0)
        largeText = pygame.font.Font('freesansbold.ttf', 100)                   #defines largeText as an object with the freesansbold font and 115 size
        TextSurf, TextRect = text_objects("Asteriod Dodge", largeText)          #defines TextSurf as "Asteriod Dodge" and TextRect as largeText
        TextRect.center = ((display_width/2),(display_height/2))                #Sets the location of the text in the middle of the screen
        gameDisplay.blit(TextSurf, TextRect)                                    #Copies the text to the screen

        button("START",150,400,100,50,green, bright_green,"play")               #calls the button function to display START, width of 100 pixels, height of 50 pixels, green colour and at (150,400)
        button("EXIT",600,400,100,50,red, bright_red,"quit")                    #calls the button function to display EXIT, width of 100 pixels, height of 50 pixels, green colour and at (150,400)
                
        pygame.display.update()                                                 #Refreshs the screen so the text is now updated on the screen
        clock.tick(15)                                                          #sets the clock object to 15 ticks

def fuel_bar(colour,width):                                           #defines fuel_bar as a function with two parameters(colour,width)
    pygame.draw.rect(gameDisplay, colour, (290, 10, width, 20))       #draws a rectangle on the gameDisplay with the colour on the coordinates x and y with a width of w and a height of h
    pygame.display.update()                                           #Refreshs the screen so the text is now updated on the screen
    
def game_loop():                                                        #defines game_loop as a function with empty parameters
    global pause                                                        #calls the variable pause as global

    fuelLeft = 100                                                      #sets the fuelLeft variable to 100
    sIncrease = 5                                                       #sets the sIncrease variable to 5 which determines the speed of the asteriods
    w,h = bg_size                                                       #defines the variables w and h as teh width and height of the background image
    x1 = 0                                                              #sets x1 to 0
    y1 = 0                                                              #sets y1 to 0
    x2 = 0                                                              #sets x2 to 0
    y2 = -h                                                             #sets y2 to -h
        
    x = 10                                                              #sets x to 10
    y = (display_height * 0.45)                                         #sets x1 to almost half of the display height

  
    y_change = 0                                                        #sets x_change to 0
    x_change = 0                                                        #sets y_change to 0
    
    thing_starty = random.randrange(-1, display_width + 1 - car_height) #makes the asteroid appear at a random height within the screen range
    thing_startx = 800                                                  #sets thing_startx to 800
    thing_speed = 4                                                     #sets thing_speed to 4

    dodged = 0                                                          #sets dodged to 0
    
    gameExit = False                                                    #defines gameExit as False
    sInput = 0
    while not gameExit:         #loops as long as gameExit is not True
        sInput = In(0x379)      #defines sInput as the output of the In function; bascially a number
        if sInput == 56:        #if sInput is 56 then:
            y_change = 5        #y_change is now 5 so the spacehsip moves down
            fuelLeft -= 1       #fuelLeft is dedcuted by 1 each time the loop executes
        elif sInput == 88:      #if sInput is 88 then:
            y_change = -5       #y_change is now -5 so the spacehsip moves up
            fuelLeft -= 1       #fuelLeft is dedcuted by 1 each time the loop executes
        elif  sInput == 104:    #if sInput is 104 then:
            x_change = -5       #x_change is now -5 so the spacehsip moves to the left
            fuelLeft -= 1       #fuelLeft is dedcuted by 1 each time the loop executes
        elif sInput == 248:     #if sInput is 248 then:
            x_change = 5        #x_change is now 5 so the spacehsip moves to the right
            fuelLeft -= 1       #fuelLeft is dedcuted by 1 each time the loop executes
        if sInput == 112 or sInput == 48 or sInput == 240 or sInput == 80 or sInput == 96: #if sInput is either 48,240,112,80 or 96 then do the following
            fuelLeft += 2       #inceases the fuelLeft by 2s so the fuel bar fills up
        if sInput == 120:       #if sInput is 120 which is when nothing is connected then do:
            y_change = 0        #y_change is 0
            x_change = 0        #x_change is 0
        if fuelLeft <= 0:       #if the fuelLeft is less than or equal to zero then
            noFuel()            #run the noFuel function which basically restarts the game
        elif fuelLeft >= 500:   #if the condition above is false and fuelLeft is more than oor equal to 200 then
            fullTank()          #run the fullTank function which slows the game until the fuel button is released
        elif fuelLeft < 20:     #does the following if fuelLeft is less than 20 then
            message_display('Low Fuel',0.1)
            Out(0x378,1)        #output 1 through the parallel cord
            time.sleep(1)       #sleeps for one second
            Out(0x378,0)        #output 0 through the parallel cord

        gameDisplay.blit(bgImg,bg_rect)                     #copies the background image and bg_rect to the Surface object gameDisplay
        y2 -= 7                                             #decrease y2 by 7 to move the background 
        y1 -= 7                                             #decrease y1 by 7 to give the continuous scrolling background effect
        gameDisplay.blit(bgImg,(y1,x1))                     #copy the background image to its new spot
        gameDisplay.blit(bgImg,(y2,1))                      #move the background to another spot for animation of sliding
        if y1<-h:                                           #if y1 is less than negative h then
            y1 = h                                          #make y1 equal to h
        if y2<-h:                                           #if y2 is less than negative h then
            y2 = h                                          #make y2 equal to h       
        for event in  pygame.event.get():                   #runs a for loop to read all the events occuring
            if event.type == pygame.QUIT:                   #if the event type is QUIT then the following happens
                pygame.quit()                               #ends the pygame module
                quit()                                      #quits the program
            
            if event.type == pygame.KEYDOWN:                #if any key is pressed then
                if event.key == pygame.K_p:                 #is the key is 'p' then
                    pause = True                            #make pause equal to Truw
                    paused()                                #run the paused function to show the pause screen




                #*****the following is commented because this uses keyboard instead of controller*****#
                    
##                elif event.key == pygame.K_SPACE:
##                    sInput = 112
##                else:
##                    if event.key == pygame.K_DOWN:              #
##                        y_change = 5                            #
##                        sInput = 56
##                    elif event.key == pygame.K_UP:              #
##                        y_change = -5                           #
##                        sInput = 88
##                    elif event.key == pygame.K_LEFT:            #
##                        x_change = -5                           #
##                        sInput = 104
##                    elif event.key == pygame.K_RIGHT:           #
##                        x_change = 5                            #
##                        sInput = 248
##            if event.type == pygame.KEYUP:                  #
##                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or pygame.K_DOWN or event.key == pygame.K_UP:#
##                    y_change = 0                            #
##                    x_change = 0                            #
##                    sInput = 120
                    

                    
                    
        fuel_bar(orange,fuelLeft)                           #displays the fuel bar in orange by running the fuel_bar function
        y += y_change                                       #increases y by y_change to move the spaceship up or down
        x += x_change                                       #increases x by x_change to move the spaceship left or right


        smallImg(thing_startx,thing_starty)                 #runs the smallImg function to copy the asteriod to (thing_startx,thing_starty)
        thing_width = 100                                   #defines thing_width to 100
        thing_height = 100                                  #defines thing_height to 100
        thing_startx -= thing_speed                         #makes the asteriod move to the left
        car(x,y)                                            #copies the spaceship to the screen
        things_dodged(dodged)                               #shows thw score
        if y > display_height + car_height:                 #if the spaceship goes too much down then it is teleported to the top
            y = -car_height                                 #
        elif y < -car_height:                               #if the spaceship goes too much up then it is teleported to the bottom
            y = display_height + car_height                 #
        elif x < 0:                                         #won't let the spaceship go off the left side of the screen
            x = 0                                           #
        elif x + car_width > display_width:                 #won't let the spaceship go off the left side of the screen
            x = display_width - car_width                   #

        if thing_startx < 0:                                #when the asteriod goes off the left side of the sceen then put it on the right so comes again
            thing_startx = display_width + thing_width      #
            thing_starty = random.randrange(0,display_height)#
            dodged += 1                                     #add one to dodge so the score increases by one
        if dodged == sIncrease:     #if a certain amount is dodged then increase the speed of the asteroid by 1
            thing_speed += 1        #
            sIncrease += 5          #
            if dodged >= 50:        #when the score is 50, increase the asteriod's speed rapidly to make it very hard.
                sIncrease = dodged  #
        
        if (x + car_width < thing_startx + thing_width and x + car_width > thing_startx) and ((y > thing_starty and y < thing_starty + thing_height) or (y + car_height > thing_starty and y + car_height < thing_starty + thing_height)): #
                crash()                                     #then line above says that if the spaceship is within the area of the asteriod then run crash function
        if (car_height + y < thing_starty)or(y > thing_starty + thing_height):# if the spaceship is not in the way of the asteriod then output 2
            Out(0x378, 2)
        else:                           #if the spaceship is in the way of the asteriod then output 5
            Out(0x378, 5)
        
        pygame.display.update()                             #Refreshs the screen so the text is now updated on the screen
        clock.tick(60)                                      #clock object increases the fps to 60
game_intro()                                                #runs the game_intro function
game_loop()                                                 #runs the game_loop function
pygame.quit()                                               #quits the pygame module
quit()                                                      #ends the program