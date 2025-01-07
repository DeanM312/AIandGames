
from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform
from path import Path


class Bullet(object):


    def __init__(self, world=None, velocity=0, pos = None):

        self.world = world
        self.pos = pos



        self.vel = velocity

        

    def update(self, delta):

        self.pos += self.vel * delta

        if self.world.enemy:
            agent = self.world.enemy.pos
            
            

            if self.pos.x < agent.x+10 and self.pos.x > agent.x-10:
                if self.pos.y < agent.y+10 and self.pos.y > agent.y-10:
                    self.world.enemy.hp -= 1
                    self.world.bullets.remove(self)


    def render(self):


 
        egi.white_pen()
        egi.circle(self.pos, 3)
