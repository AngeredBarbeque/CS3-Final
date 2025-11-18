#Importing needed libraries
import pygame
from abc import ABC, abstractmethod
import math
from pygame import sprite
import random
import time

tolerance = 32
projectiles = sprite.Group()
enemies = sprite.Group()

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
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def compare(self,other):
        dist = math.sqrt(((self.x-other.x)**2) + ((self.y - other.y)**2))
        return dist

class Enemy(sprite.Sprite):
    x:float
    y:float
    health:int
    speed:float
    scale:float 
    def __init__(self, pos=Pos(0,0), health=100, speed=1, scale=1, img=pygame.image.load("Resources/Temporary.png")):
        pygame.sprite.Sprite.__init__(self)
        self.next_waypoint_idx = 0
        self.pos = pos
        self.health = health
        self.speed = speed
        self.scale = scale
        self.image = pygame.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
    def update(self,target):
        #Finds the difference between position of self, and position of target
        #This is representative of if self is above,below,left of, or right of the target.
        difference_x = self.pos.x - target.x
        difference_y = self.pos.y - target.y
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
        elif difference_y == 0:
            y_move = 0
        elif difference_y > 0:
            y_move = self.speed * -1
        #move based on what was calculated
        self.pos.x += x_move
        self.pos.y += y_move
        self.rect.x += x_move
        self.rect.y += y_move

    def at_waypoint(self, waypoint,tolerance):
        dist = self.pos.compare(waypoint)
        #If the objects are a given amount of pixels or less apart, snap self to the position of other.
        if dist <= tolerance:
            self.pos.x = waypoint.x
            self.pos.y = waypoint.y
            self.rect.x = waypoint.x
            self.rect.y = waypoint.y
            self.next_waypoint_idx += 1
            print('true')
            return True
        else:
            return False

class Projectile(ABC,sprite.Sprite):
    speed:float
    damage:int
    x:float
    y:float
    scale:float
    def __init__(self,speed=1,damage=15,pos=Pos(x=0,y=0),scale=1,img=pygame.image.load("Resources/Temporary.png"),target=Pos(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.damage = damage
        self.pos = pos
        self.scale = scale
        self.image = pygame.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))
        self.target = target
        self.rect = self.img.get_rect()
        self.rect = self.image.get_rect()
    def move(self, target):
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
    def has_hit(self):
        for i in enemies:
            if sprite.collide_rect(self,i):
                self.on_hit(i)
                return
    @abstractmethod
    def on_hit():
        pass

class Bee(Projectile):
    def __init__(self, speed=1, damage=15, pos=Pos(x=0, y=0), scale=1, img=pygame.image.load("Resources/Temporary.png"), target=Pos(0, 0)):
        super().__init__(speed, damage, pos, scale, img, target)
    def on_hit(self,enemy):
        enemy.hp -= self.damage
        self.kill()
    def find_target(self,waypoints):
        for i in enemies:
            dist = i.pos.compare(waypoints[len(waypoints)-1], tolerance, waypoints)
            if dist < closest:
                closest = i
        if closest:
            return closest.pos
        else:
            return self.pos
        
class Bolt(Projectile):
    def __init__(self, speed=1, damage=15, pos=Pos(x=0, y=0), scale=1, img=pygame.image.load("Resources/Temporary.png"), target=Pos(0, 0)):
        super().__init__(speed, damage, pos, scale, img, target)
    def on_hit(self,enemy):
        enemy.hp -= self.damage
        #Creates 5 to 10 bees tha spawn in a small area around the impact
        bees = random.randint(5,10)
        for i in range(bees):
            while True:
                new_x = self.x + random.randint(-20,20)
                if new_x >= 0 and new_x <= 1600:
                    while True:
                        new_y = self.y + random.randint(-20,20)
                        if new_y >=0 and new_y <= 1200:
                            break
                    break
            Bee(30,15,Pos(new_x,new_y))
        self.kill()
    
class Honey(Projectile):
    def __init__(self, speed=1, damage=0, pos=Pos(x=0, y=0), scale=1, img=pygame.image.load("Resources/Temporary.png"), target=Pos(0, 0),speed_low=10):
        super().__init__(speed, damage, pos, scale, img, target)
        self.speed_low = speed_low
    def on_hit(self,target):
        target.speed -= self.speed_low
        self.kill()
        

class Tower(ABC,sprite.Sprite):
    x:float
    y:float
    scale:float
    fire_rate:float
    range:float
    def __init__(self,pos=Pos(x=0,y=0),scale=1,fire_rate=2,range=500,img=pygame.image.load("Resources/Temporary.png")):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.scale = scale
        self.fire_rate = fire_rate
        self.range = range
        self.image = pygame.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))
        self.rect = self.image.get_rect()
    @abstractmethod
    def fire():
        pass
    def find_target(self):
        for i in enemies:
            if self.pos.compare(i.pos) <= self.range:
                return i
        return None


class Beellista(Tower):
    def __init__(self, pos=Pos(x=0, y=0), scale=1, fire_rate=2, range=500, img=pygame.image.load("Resources/Temporary.png")):
        super().__init__(pos, scale, fire_rate, range, img)
    def fire(self,target):
        shot = Bolt(30,15,self.pos,1,pygame.image.load("Resources/Temporary.png"),target)
        projectiles.add(shot)
        time.sleep(self.fire_rate)
        return
    
class Beehive(Tower):
    def __init__(self, pos=Pos(x=0, y=0), scale=1, fire_rate=2, range=500, img=pygame.image.load("Resources/Temporary.png")):
        super().__init__(pos, scale, fire_rate, range, img)
    def fire(self,target):
        shot = Bee(30,15,self.pos,1,pygame.image.load("Resources/Temporary.png"),target)
        projectiles.add(shot)
        time.sleep(self.fire_rate)
        return
    
class Honeycannon(Tower):
    def __init__(self, pos=Pos(x=0, y=0), scale=1, fire_rate=2, range=500, img=pygame.image.load("Resources/Temporary.png")):
        super().__init__(pos, scale, fire_rate, range, img)
    def fire(self,target):
        shot = Honey(30,15,self.pos,1,pygame.image.load("Resources/Temporary.png"),target)
        projectiles.add(shot)
        time.sleep(self.fire_rate)
        return
        