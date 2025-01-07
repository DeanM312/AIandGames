
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

        agent = self.world.agents[0].pos
        
        self.pos += self.vel * delta

        if self.pos.x < agent.x+10 and self.pos.x > agent.x-10:
            if self.pos.y < agent.y+10 and self.pos.y > agent.y-10:
                self.world.agents[0].hit = 0.5
                self.world.bullets.remove(self)


    def render(self):


 
        egi.white_pen()
        egi.circle(self.pos, 3)
