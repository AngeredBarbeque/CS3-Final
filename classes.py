#Importing needed libraries
import pygame
from abc import ABC, abstractmethod
import math


class Button:
    x: int
    y: int
    scale: float
    def __init__(self,x,y,img,scale):
        self.x = x
        self.y = y
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (int(self.img.get_width()*scale),int(self.img.get_height()*scale)))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
    def draw(self,screen):
        pos = pygame.mouse.get_pos()
        action = False
        #Checks if the mouse is over the button
        if self.rect.collidepoint(pos):
            #if the mouse is clicked and the button hasn't already been clicked, return action as true
            if pygame.mouse.get_pressed()[0]==1 and self.clicked == False:
                self.clicked = False
                action = False
            else:
                action = False
        screen.blit(self.img, (self.x, self.y))
        return action

class Pos:
    x: int
    y: int
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def compare(self,other,tolerance):
        dist = math.sqrt(((self.x-other.x)**2) + ((self.y - other.y)**2))
        #If the objects are a given amount of pixels or less apart, snap self to the position of other.
        #This is largely helpful for waypoints and enemies.
        if dist <= tolerance:
            self.x = other.x
            self.y = other.y

class Enemy:
    x:int
    y:int
    health:int
    speed:int
    scale:float 
    def __init__(self, pos=Pos(x,y), health=100, speed=10, scale=1, img=pygame.image.load("Resources\Temporary.png")):
        self.pos = pos
        self.health = health
        self.speed = speed
        self.scale = scale
        self.img = pygame.transform.scale(img,self.scale)
    def move(self,target):
        #Finds the difference between position of self, and position of target
        #This is representative of if self is above,below,left of, or right of the target.
        difference_x = self.pos.x - target.pos.x
        difference_y = self.pos.y - target.pos.y
        #If the difference is negative, target is right of self, meaning self needs positive movement
        if difference_x < 0:
            x_move = self.speed
        #if the difference is 0, they are at the same x
        elif difference_x == 0:
            x_move = 0
        #if the difference is positive, target is left of self, meaning self needs negative movement
        elif difference_x > 0:
            x_move = self.speed * -1
        #Y logic is identical to x logic
        if difference_y < 0:
            y_move = self.speed
        elif difference_x == 0:
            y_move = 0
        elif difference_y > 0:
            y_move = self.speed * -1
        #move based on what was calculated
        self.pos.x += x_move
        self.pos.y += y_move
    def dist_calc_waypoint(self,waypoint):
        dist = math.sqrt(((self.x-waypoint.x)**2) + ((self.y - waypoint.y)**2))

class Projectile(ABC):
    speed:int
    damage:int
    x:int
    y:int
    scale:float
    def __init__(self,speed=30,damage=15,pos=Pos(x,y),scale=1,img=pygame.image.load("Resources\Temporary.png"),target=Pos(0,0)):
        self.speed = speed
        self.damage = damage
        self.pos = pos
        self.scale = scale
        self.img = pygame.transform.scale(img,self.scale)
        self.target = target
    @abstractmethod
    def move():
        pass
    @abstractmethod
    def on_hit():
        pass

class Tower(ABC):
    x:int
    y:int
    scale:float
    fire_rate:float
    range:float
    def __init__(self,pos=Pos(x,y),scale=1,fire_rate=2,range=500,img=pygame.image.load("Resources\Temporary.png")):
        self.pos = pos
        self.scale = scale
        self.fire_rate = fire_rate
        self.range = range
        self.img = pygame.transform.scale(img,self.scale)
    @abstractmethod
    def fire():
        pass
    def find_target():
        pass