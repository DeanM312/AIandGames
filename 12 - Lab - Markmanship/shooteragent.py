
from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform
from path import Path
from bullet import Bullet


class ShooterAgent(object):


    def __init__(self, world=None):

        self.world = world
        self.pos = Vector2D(500, 50)
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]
        self.heading = Vector2D(sin(100), cos(100))
        self.side = self.heading.perp()
        self.color = 'ORANGE'
        self.scale = Vector2D(10, 10)

        self.reload = 0
        self.bulletspeed = 500

        self.weapon = 'rifle'


    def update(self, delta):

        tar = self.world.agents[0]

        if self.weapon == 'rifle':
            bulletspeed = self.bulletspeed
            inaccuracy = 3
            



        elif self.weapon == 'pistol':
            bulletspeed = self.bulletspeed
            inaccuracy = 50
          

        elif self.weapon == 'rocket':
            bulletspeed = self.bulletspeed * 0.7
            inaccuracy = 1
            

        predictedpos = Vector2D(randrange(-inaccuracy, inaccuracy) + tar.pos.x + tar.pos.distance(self.pos)/bulletspeed * tar.vel.x, randrange(-inaccuracy, inaccuracy) + tar.pos.y + tar.pos.distance(self.pos)/bulletspeed * tar.vel.y)

        vel = (predictedpos - self.pos).normalise()


        if self.reload > 0:
            self.reload -= 1 * delta

        else:
            self.reload = 1
            
            self.heading = vel
            self.side = self.heading.perp()


            vel = vel * bulletspeed

            pos = Vector2D(self.pos.x,self.pos.y)

            self.world.bullets.append(Bullet(self.world,vel,pos))
        


    def render(self, color=None):


 
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
 
        egi.closed_shape(pts)
