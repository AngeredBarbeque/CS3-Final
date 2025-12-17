#Importing needed libraries
import pygame
from abc import ABC, abstractmethod
import math
from pygame import sprite
import random
import time

tolerance = 32
towers = sprite.Group()
projectiles = sprite.Group()
enemies = sprite.Group()

class Button:
    x: int
    y: int
    scale: float
    def __init__(self,pos,img,scale):
        self.x = pos[0]
        self.y = pos[1]
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (int(self.img.get_width()*scale),int(self.img.get_height()*scale)))
        self.rect = self.img.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.clicked = False
        #Allows for a delay
        self.start_time = 0
    def draw(self):
        pos = pygame.mouse.get_pos()
        action = False
        #Checks if the mouse is over the button
        if self.rect.collidepoint(pos):
            #if the mouse is clicked and the button hasn't already been clicked, return action as true
            if pygame.mouse.get_pressed()[0]==1 and self.clicked == False:
                self.clicked = False
                action = True
                #Starts a timer since the last press
                self.start_time = time.time()
            else:
                action = False
        return action

class Enemy(sprite.Sprite):
    x:float
    y:float
    health:int
    speed:float
    scale:float 
    def __init__(self, pos=(0,0), health=100, speed=1, scale=1, img=pygame.image.load("Resources/Temporary.png"),type="None"):
        pygame.sprite.Sprite.__init__(self)
        self.next_waypoint_idx = 0
        self.health = health
        self.speed = speed
        self.scale = scale
        self.image = pygame.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.x_move = 0
        self.y_move = 0
        self.type = type
        
    def update(self,target):
        #Finds the difference between position of self, and position of target
        #This is representative of if self is above,below,left of, or right of the target.
        difference_x = self.rect.x - target[0]
        difference_y = self.rect.y - target[1]

        #Tried to add trig, forgot pygame can't handle floats in rects :(

        #If the difference is negative, target is right of self, meaning self needs positive movement
        if difference_x < 0:
            self.x_move = self.speed
        #if the difference is 0, they are at the same x
        elif difference_x == 0:
            self.x_move = 0
        #if the difference is positive, target is left of self, meaning self needs negative movement
        elif difference_x > 0:
            self.x_move = self.speed* -1
        #Y logic is identical to x logic
        if difference_y < 0:
            self.y_move = self.speed
        elif difference_y == 0:
            self.y_move = 0
        elif difference_y > 0:
            self.y_move = self.speed * -1
        #move based on what was calculated
        self.rect.x += self.x_move
        self.rect.y += self.y_move

    #Checks if the enemy is at the waypoint.
    def at_waypoint(self, waypoint,tolerance):
        dist = math.sqrt(((waypoint[0]-self.rect.x)**2) + ((waypoint[1] - self.rect.y)**2))
        if dist <= tolerance:
            self.rect.x = waypoint[0]
            self.rect.y = waypoint[1]
            self.next_waypoint_idx += 1
            return True
        else:
            return False

class Projectile(ABC,sprite.Sprite):
    speed:float
    damage:int
    x:float
    y:float
    scale:float
    def __init__(self,speed=1,damage=15,pos=(0,0),scale=1,img=pygame.image.load("Resources/Temporary.png"),target=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.damage = damage
        self.pos = pos
        self.scale = scale
        self.image = pygame.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))
        self.target = target
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.flipped = False
        self.rot_down = False
        self.rot_up = False
    def move(self, target):
        #Finds the difference between position of self, and position of target
        #This is representative of if self is above,below,left of, or right of the target.
        difference_x = self.rect.x - target[0]
        difference_y = self.rect.y - target[1]
        #If the difference is negative, target is right of self, meaning self needs positive movement
        if difference_x < 0:
            x_move = self.speed
            if not self.flipped:
                self.image = pygame.transform.flip(self.image,True,False)
                self.flipped = True
        #if the difference is 0, they are at the same x
        elif difference_x == 0:
            x_move = 0
        #if the difference is positive, target is left of self, meaning self needs negative movement
        elif difference_x > 0:
            x_move = self.speed * -1
            if self.flipped:
                self.image = pygame.transform.flip(self.image,True,False)
                self.flipped = False
        if difference_y < 0:
            y_move = self.speed
        elif difference_y == 0:
            y_move = 0
        elif difference_y > 0:
            y_move = self.speed * -1
        #move based on what was calculated

        self.rect.x += x_move
        self.rect.y += y_move
    #Checks if the projectile has hit an enemy
    def has_hit(self):
        for i in enemies:
            if sprite.collide_rect(self,i):
                self.on_hit(i)
                return
        x_diff = abs(self.rect.x - self.target[0])
        y_diff = abs(self.rect.y - self.target[1])
        if x_diff <= self.speed and y_diff <= self.speed:
            self.kill()
            return
    @abstractmethod
    def on_hit():
        pass

class Bee(Projectile):
    def __init__(self, speed=1, damage=5, pos=(0, 0), scale=1, img=pygame.image.load("Resources//Bee.png"), target=(0, 0),type="Bee"):
        super().__init__(speed, damage, pos, scale, img, target)
        self.type = type
    #Defines behavior when aprojectile hits an enemy
    def on_hit(self,enemy):
        enemy.health -= self.damage
        self.kill()
    #Checks all enemies to see if there are an viable targets
    def find_target(self,waypoints):
        closest_dist = 10000000
        for i in enemies:
            #Checks for which enemy is the closest to the final waypoint
            dist = math.sqrt(((i.rect.x-waypoints[len(waypoints)-1][0])**2) + ((i.rect.y - waypoints[len(waypoints)-1][1])**2))
            if dist < closest_dist:
                closest = i
                closest_dist = dist
        if closest_dist != 10000000:
            return (closest.rect.x,closest.rect.y)
        else:
            return (self.rect.x,self.rect.y)
        
class Bolt(Projectile):
    def __init__(self, speed=1, damage=10, pos=(0,0), scale=1, img=pygame.image.load("Resources//Temporary.png"), target=(0, 0),type="Bolt"):
        super().__init__(speed, damage, pos, scale, img, target)
        self.type = type
    #The bolts can spawn bees upon hitting an enemy
    def on_hit(self,enemy):
        enemy.health -= self.damage
        #Creates 3 to 7 bees that spawn in a small area around the impact
        bees = random.randint(3,7)
        for i in range(bees):
            while True:
                new_x = self.rect.x + random.randint(-50,50)
                if new_x >= 0 and new_x <= 1600:
                    while True:
                        new_y = self.rect.y + random.randint(-50,50)
                        if new_y >=0 and new_y <= 1200:
                            break
                    break
            projectiles.add(Bee(3,3,(new_x,new_y)))
        self.kill()
    
class Honey(Projectile):
    def __init__(self, speed=1, damage=0, pos=(0, 0), scale=1.5, img=pygame.image.load("Resources//glob.png"), target=Enemy(),speed_low=0.2,type="Honey"):
        super().__init__(speed, damage, pos, scale, img, target)
        self.type = type
        self.speed_low = speed_low
        #Slows an enemy's speed, when they reach a limit 
    def on_hit(self,target):
        #Doesn't work on the boss
        if target.type != "Intezarr":
            target.speed -= self.speed_low
            if target.speed <= 0:
                target.speed = 0
        self.kill()
        

class Tower(ABC,sprite.Sprite):
    x:float
    y:float
    scale:float
    fire_rate:float
    range:float
    def __init__(self,pos=(0,0),scale=1,fire_rate=2,range=500,img=pygame.image.load("Resources//Temporary.png")):
        pygame.sprite.Sprite.__init__(self)
        self.scale = scale
        self.fire_rate = fire_rate
        self.range = range
        self.image = pygame.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
    @abstractmethod
    def fire():
        pass
    #Looks for a target within range
    def _find_target(self):
        for i in enemies:
            if math.sqrt(((i.rect.x-self.rect.x)**2) + ((i.rect.y - self.rect.y)**2)) <= self.range:
                return i
        return None


class Beellista(Tower):
    def __init__(self, pos=(0, 0), scale=2, fire_rate=2, range=500, img=pygame.image.load("Resources//Beellista.png")):
        super().__init__(pos, scale, fire_rate, range, img)
        self.last_shot = 0
        self.flipped = False
    #Shoots a bolt at the enemy
    def fire(self):
        target = super()._find_target()
        if target:
            if target.rect.x < self.rect.x and not self.flipped:
                self.image = pygame.transform.flip(self.image,True,False)
                self.flipped = True
            elif target.rect.x > self.rect.x and self.flipped:
                self.image = pygame.transform.flip(self.image,True,False)
                self.flipped = False
            #Use enemies self.x_move and self.y_move to add/subtract from the target location.
            shot = Bolt(3,10,self.pos,1,pygame.image.load("Resources//Bolt.png"),(target.rect.x + (target.x_move * (100*target.speed)), target.rect.y + (target.y_move * (100*target.speed))))
            projectiles.add(shot)
            self.last_shot = time.time()
            return
    
class Beehive(Tower):
    def __init__(self, pos=(0, 0), scale=1, fire_rate=2, range=5, img=pygame.image.load("Resources//Hive.png")):
        super().__init__(pos, scale, fire_rate, range, img)
        self.last_shot = 0
    #Spawns a bee
    def fire(self):
        target = super()._find_target()
        if target:
            shot = Bee(3,5,(self.rect.x +32,self.rect.y +32),1,pygame.image.load("Resources//Bee.png"),target)
            projectiles.add(shot)
            self.last_shot = time.time()
            return
    
class Honeycannon(Tower):
    def __init__(self, pos=(0,0), scale=1.5, fire_rate=2, range=500, img=pygame.image.load("Resources//Honeycannon.png")):
        super().__init__(pos, scale, fire_rate, range, img)
        self.last_shot = 0
    #Shoots a honey glob
    def fire(self):
        target = super()._find_target()
        if target:
            if target.type != "Intezarr":
                shot = Honey(3,0,(self.pos[0],self.pos[1]-32),1.5,pygame.image.load("Resources//glob.png"),(target.rect.x + (target.x_move * (100*target.speed)), target.rect.y + (target.y_move * (100*target.speed))))
                projectiles.add(shot)
                self.last_shot = time.time()
                return
        