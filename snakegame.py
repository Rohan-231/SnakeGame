import pygame
import sys
import os 
import random
import math

# from pygame.locals import(K_UP,K_DOWN,K_LEFT,K_RIGHT) 

pygame.init()
pygame.display.set_caption("Snake Game")
pygame.font.init()
random.seed()

speed = 0.36
snake_size =9
food_size = snake_size
separation  = 10
screen_height = 600
screen_width = 800
fps = 25
KEY = {"UP":1,"DOWN":2,"LEFT":3,"RIGHT":4}

screen = pygame.display.set_mode((screen_width,screen_height),pygame.HWSURFACE)

score_font = pygame.font.Font(None,38)
score_numb_font = pygame.font.Font(None,28)
game_over_font = pygame.font.Font(None,48)

play_again_font = score_numb_font

score_mssg = score_font.render("Score : ",1,pygame.Color("green"))
score_mssg_size = score_font.size("Score")
background_color = pygame.Color(0,0,0)
black = pygame.Color(0,0,0)

gameClock = pygame.time.Clock()

def checkcollision(posA,As,posB,Bs):
    if(posA.x<posB.x+Bs and posA.x+As>posB.x and posA.y<posB.y+Bs and posA.y + As > posB.y):
        return True
    return False

def checkLimits(snake):
    if(snake.x>screen_width):
        snake.x = snake_size
    if(snake.x<0):
        snake.x = screen_width-snake_size
    if(snake.y>screen_height):
        snake.y = snake_size
    if(snake.y<0):
        snake.y = screen_height - snake_size

class Food :
    def __init__(self,x,y,state):
        self.x = x
        self.y = y
        self.state = state
        self.color = pygame.color.Color("orange")
    
    def draw(self,screen) :
        pygame.draw.rect(screen,self.color,(self.x,self.y,food_size,food_size),0)

class segment :
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.direction = KEY["UP"]
        self.color = "white"

class snake:
    def __init__(self,x,y) :
        self.x = x
        self.y = y
        self.direction = KEY["UP"]
        self.stack = []
        self.stack.append(self)
        blackBox = segment(self.x,self.y+separation)
        blackBox.direction = KEY["UP"]
        blackBox.color = "NULL"
        self.stack.append(blackBox)
        
    

    def move(self) :
        last_element = len(self.stack) - 1
        while(last_element!=0) :
            self.stack[last_element].direction = self.stack[last_element-1].direction
            self.stack[last_element].x = self.stack[last_element - 1].x
            self.stack[last_element].y = self.stack[last_element-1].y
            last_element -= 1

        if(len(self.stack)<2):
            last_segment = self
        else :
            last_segment = self.stack.pop(last_element)
        last_segment.direction = self.stack[0].direction
        if(self.stack[0].direction == KEY["UP"]):
            last_segment.y = self.stack[0].y-(speed*fps)
        elif(self.stack[0].direction == KEY["DOWN"]):
            last_segment.y = self.stack[0].y+(speed*fps)
        elif(self.stack[0].direction == KEY["LEFT"]):
            last_segment.x = self.stack[0].x-(speed*fps)
        elif(self.stack[0].direction == KEY["RIGHT"]):
            last_segment.x = self.stack[0].x+(speed*fps)
        self.stack.insert(0,last_segment)

    def getHead(self):
        return(self.stack[0])

    def grow(self) :
        last_element = len(self.stack) -1
        self.stack[last_element].direction = self.stack[last_element].direction

        if(self.stack[last_element].direction == KEY["UP"]):
            newSegment = segment(self.stack[last_element].x,self.stack[last_element].y - snake_size)
            blackBox = segment(newSegment.x,newSegment.y - separation)
        elif(self.stack[last_element].direction == KEY["DOWN"]):
            newSegment = segment(self.stack[last_element].x,self.stack[last_element].y + snake_size)
            blackBox = segment(newSegment.x,newSegment.y + separation)
        elif(self.stack[last_element].direction == KEY["LEFT"]):
            newSegment = segment(self.stack[last_element].x-snake_size,self.stack[last_element].y)
            blackBox = segment(newSegment.x - separation,newSegment.y)
        elif(self.stack[last_element].direction == KEY["RIGHT"]):
            newSegment = segment(self.stack[last_element].x+snake_size,self.stack[last_element].y)
            blackBox = segment(newSegment.x + separation,newSegment.y)
        blackBox.color = "NULL"
        self.stack.append(newSegment)
        self.stack.append(blackBox)

    def iterateSegments(self,delta):
        pass

    def setdirection(self,direction) :
        if(self.direction==KEY["RIGHT"] and direction==KEY["LEFT"] or self.direction==KEY["LEFT"] and direction==KEY["RIGHT"]):
            pass
        elif(self.direction==KEY["UP"] and direction==KEY["DOWN"] or self.direction==KEY["UP"] and direction==KEY["DOWN"]):
            pass
        else :
            self.direction = direction

    def get_rect(self) :
        rect = (self.x,self.y)
        return rect
    
    def getX(self):
        return self.x
    
    def getY(self) :
        return self.y
    
    def setX(self,x):
        return self.x    

    def setY(self,y):
        return self.y

    def checkcrashing(self):
        counter = 1
        while(counter<len(self.stack)-1):
            if(checkcollision(self.stack[0],snake_size,self.stack[counter],snake_size) and self.stack[counter].color != "NULL") :
                return True
            counter += 1
        return False

    def draw(self,screen):
        pygame.draw.rect(screen,pygame.color.Color("green"),(self.stack[0].x,self.stack[0].y,snake_size,snake_size),0)
        counter = 1
        while(counter<len(self.stack)):
            if(self.stack[counter].color == "NULL"):
                counter += 1
                continue
            pygame.draw.rect(screen,pygame.color.Color("yellow"),(self.stack[counter].x,self.stack[counter].y,snake_size,snake_size),0)
            counter += 1    

def getkey() :
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                 return KEY["UP"]
            elif event.key == pygame.K_DOWN:
                return KEY["DOWN"]
            elif event.key == pygame.K_RIGHT:
                return KEY["RIGHT"]
            elif event.key == pygame.K_LEFT:
                return KEY["LEFT"]
            
            elif event.key == pygame.K_ESCAPE:
                return "exit"
            elif event.key == pygame.K_y:
                return "yes"
            elif event.key == pygame.K_n:
                return "no"
        if event.type == pygame.QUIT:
                sys.exit(0)

def endGame():
    message = game_over_font.render("Game Over",1,pygame.Color("white"))
    message_play_again = play_again_font.render("Play Again(Y/N)?",1,pygame.Color("green"))
    screen.blit(message,(320,240))
    screen.blit(message_play_again,(320+12,240+40))

    pygame.display.flip()
    pygame.display.update()

    mkey = getkey()

    while(mkey!="exit"):
        if(mkey=="yes"):
            main()
        elif(mkey == "no"):
            break
        mkey = getkey()
        gameClock.tick(fps)
    sys.exit(0)

def drawscore(score):
    score_numb = score_numb_font.render(str(score),1,pygame.Color("red"))
    screen.blit(score_mssg,(screen_width-score_mssg_size[0]-60,10))
    screen.blit(score_numb,(screen_width-45,12))

def GameTime(gameTime):
    game_time = score_font.render("Time : ",1,pygame.Color("white"))
    game_time_numb = score_numb_font.render(str(gameTime/1000),1,pygame.Color("white"))
    screen.blit(game_time,(30,10))
    screen.blit(game_time_numb,(105,14))

def respawnfood(food , index , sx , sy):
    radius = math.sqrt((screen_width/2*screen_width/2 + screen_height/2*screen_height/2))/2
    angle = 999
    while(angle > radius):
        angle = random.uniform(0,800)*math.pi*2
        x = screen_height/2 + radius * math.cos(angle)
        y = screen_height/2 + radius * math.sin(angle)
        if(x == sx and y == sy):
            continue
    newFood = Food(x , y ,1)
    food[index] = newFood
    
def respawnfoods(food,quantity,sx,sy):
    counter = 0
    del food[:]
    radius = math.sqrt((screen_width/2*screen_width/2 + screen_height/2*screen_height/2))/2
    angle =999
    while(counter<quantity):
        while(angle>radius):
            angle = random.uniform(0,800)*math.pi*2
            x = screen_width/2 + radius*math.cos(angle)
            y = screen_height/2 + radius*math.sin(angle)

            if((x-food_size==sx or x + food_size ==sx) and (y-food_size == sy or y+food_size == sy) or radius - angle <=10) :
                continue
            food.append(Food(x,y,1))
            angle = 999
            counter +=1


def main():
    score = 0

    mysnake = snake(screen_width/2,screen_height/2)
    mysnake.setdirection(KEY["UP"])
    mysnake.move()
    start_segments = 3

    while(start_segments>0):
        mysnake.grow()
        mysnake.move()
        start_segments -= 1
    
    max_food = 1
    eaten_food = False
    food =[Food(random.randint(60,screen_width),random.randint(60,screen_height),1)]
    respawnfoods(food,max_food,mysnake.x,mysnake.y)

    startTime = pygame.time.get_ticks()
    endgame = 0

    while(endgame!=1):
        gameClock.tick(fps)

        keyPress = getkey()
        if keyPress == "exit":
            endgame = 1
        
        checkLimits(mysnake)
        if(mysnake.checkcrashing()==True):
            endGame()
        
        for myfood in food :
            if(myfood.state==1):
                if(checkcollision(mysnake.getHead(),snake_size,myfood,food_size)==True):
                    mysnake.grow()
                    myfood.state = 0
                    score += 5
                    eaten_food = True
                    
        if(keyPress):
            mysnake.setdirection(keyPress)
        mysnake.move()

        if(eaten_food == True):
            eaten_food = False
            respawnfood(food,0,mysnake.getHead().x,mysnake.getHead().y)

        screen.fill(background_color)

        for myfood in food :
            if(myfood.state==1):
                myfood.draw(screen)

        mysnake.draw(screen)
        drawscore(score)
        gametime = pygame.time.get_ticks()
        GameTime(gametime)
        pygame.display.flip()
        pygame.display.update()


main()
