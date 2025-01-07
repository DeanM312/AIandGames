'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform
from path import Path
from bullet import Bullet

AGENT_MODES = {
    KEY._1: 'seek',
    KEY._2: 'arrive_slow',
    KEY._3: 'arrive_normal',
    KEY._4: 'arrive_fast',
    KEY._5: 'flee',
    KEY._6: 'pursuit',
    KEY._7: 'follow_path',
    KEY._8: 'wander',
}

class Agent(object):

    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.9,
        'normal': 0.6,
        'fast': 0.3,
    }

    def __init__(self, world=None, scale=10.0, mass=1.0, mode='none'):
        # keep a reference to the world object
        self.world = world
        self.mode = mode
        # where am i and where am i going? random start pos
        dir = radians(random()*360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.force = Vector2D()  # current steering force
        self.accel = Vector2D() # current acceleration due to force
        self.mass = mass

        # data for drawing this agent
        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]
        ### path to follow?
 
        self.waypoint_threshold = 30.0


        self.path = self.world.patrolpath
        

        ### wander details
        self.wander_target = Vector2D(1, 0)
        self.wander_dist = 1.0 * scale
        self.wander_radius = 1.0 * scale 
        self.wander_jitter = 10.0 * scale
        self.bRadius = scale
        # Force and speed limiting code
        self.max_speed = 10.0 * scale
        self.max_force = 500.0

        self.state =  'patrol'
        self.secondstate = 'followpath'
        self.reload = 0
        self.bulletspeed = 500
        self.weapon = 'rifle'
        

        # debug draw info?
        self.show_info = False

    def calculate(self, delta):
        # calculate the current steering force
        mode = self.mode

        if self.world.enemy:
            tarpos = self.world.enemy.pos
        else:
            tarpos = Vector2D(0,0)
            
        if mode == 'seek':
            force = self.seek(tarpos)
        elif mode == 'arrive_slow':
            force = self.arrive(tarpos, 'slow')
        elif mode == 'arrive_normal':
            force = self.arrive(tarpos, 'normal')
        elif mode == 'arrive_fast':
            force = self.arrive(tarpos, 'fast')
        elif mode == 'flee':
            force = self.flee(tarpos)
        elif mode == 'pursuit':
            force = self.pursuit(tarpos)
        elif mode == 'wander':
            force = self.wander(delta)
        elif mode == 'follow_path':
            force = self.follow_path()
        else:
            force = Vector2D()
        self.force = force
        return force

    def update(self, delta):
        ''' update vehicle position and orientation '''


        self.fsm(delta)

        force = self.calculate(delta)
        force.truncate(self.max_force) 
        self.accel = force / self.mass  
        self.vel += self.accel * delta
        self.vel.truncate(self.max_speed)
        self.pos += self.vel * delta
        if self.vel.lengthSq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()
        self.world.wrap_around(self.pos)

    def fsm(self, delta):
        state = self.state
        secondstate = self.secondstate

        if self.world.enemy:
            enemydist = (self.world.enemy.pos - self.pos).length()
        else:
            enemydist = 9999
            
   
        if state == 'patrol':
            self.color = 'ORANGE'
            if secondstate == 'followpath':
                self.mode = 'follow_path'

                if self.path.is_finished():
                    
                    self.secondstate = 'resetpath'

                if enemydist < 400:
                    self.secondstate = 'search'

            elif secondstate == 'resetpath':
                
                self.path._reset()

                self.secondstate = 'followpath'


            elif secondstate == 'search':
                self.mode = 'wander'
                
                if enemydist > 450:
                    self.secondstate = 'followpath'

                if enemydist < 300:
                    self.state = 'attack'
                    self.secondstate = 'shoot'




        elif state == 'attack':
            self.color = 'BLUE'
            if secondstate == 'shoot':
                self.mode = 'arrive_slow'


                if self.world.enemy:
                    tar = self.world.enemy

                    if self.weapon == 'rifle':
                        bulletspeed = self.bulletspeed
                        inaccuracy = 25
                        
      
                    predictedpos = Vector2D(randrange(-inaccuracy, inaccuracy) + tar.pos.x + tar.pos.distance(self.pos)/bulletspeed * tar.vel.x, randrange(-inaccuracy, inaccuracy) + tar.pos.y + tar.pos.distance(self.pos)/bulletspeed * tar.vel.y)

                    vel = (predictedpos - self.pos).normalise()


                    if self.reload > 0:
                        self.secondstate = 'reload'
                    else:
                        self.reload = 0.5
                        
                        


                        vel = vel * bulletspeed

                        pos = Vector2D(self.pos.x,self.pos.y)

                        self.world.bullets.append(Bullet(self.world,vel,pos))


                if enemydist < 150:
                    self.secondstate = 'flee'

                if enemydist > 300:
                    self.state = 'patrol'
                    self.secondstate = 'search'
                    
        

            elif secondstate == 'reload':

                self.reload -= 1 * delta

                if self.reload <= 0:
                    self.secondstate = 'shoot'


                

            elif secondstate == 'flee':
                self.mode = 'flee'

                if enemydist > 150:
                    self.secondstate = 'shoot'
              
            

    def render(self, color=None):
        ''' Draw the triangle agent with color'''


        # draw the ship
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)

        # add some handy debug drawing info lines - force and velocity
        if self.show_info:
            s = 0.5 # <-- scaling factor
            # force
            egi.red_pen()
            egi.line_with_arrow(self.pos, self.pos + self.force * s, 5)
            # velocity
            egi.grey_pen()
            egi.line_with_arrow(self.pos, self.pos + self.vel * s, 5)
            # net (desired) change
            egi.white_pen()
            egi.line_with_arrow(self.pos+self.vel * s, self.pos+ (self.force+self.vel) * s, 5)
            egi.line_with_arrow(self.pos, self.pos+ (self.force+self.vel) * s, 5)

            if self.mode == 'wander':
                # calculate the center of the wander circle in front of the agent
                wnd_pos = Vector2D(self.wander_dist, 0)
                wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
                # draw the wander circle
                egi.green_pen()
                egi.circle(wld_pos, self.wander_radius) 
                # draw the wander target (little circle on the big circle)
                egi.red_pen()
                wnd_pos = (self.wander_target + Vector2D(self.wander_dist, 0))
                wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
                egi.circle(wld_pos, 3)

            if self.mode == 'follow_path':
                self.path.render()

    def speed(self):
        return self.vel.length()


    def randomise_path(self):
        cx = self.world.cx 
        cy = self.world.cy 
        margin = min(cx, cy) * (1/6) 
        self.path.create_random_path(10,cx-margin*6,cy-margin*6,cx,cy) 

    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def flee(self, hunter_pos):
        ''' move away from hunter position '''
        to_target = hunter_pos - self.pos
        panicdist = to_target.length()
       

        if panicdist < 250:
            desired_vel = (hunter_pos - self.pos).normalise() * self.max_speed
            return (-desired_vel - self.vel)
        return Vector2D(0, 0)

    def arrive(self, target_pos, speed):
        ''' this behaviour is similar to seek() but it attempts to arrive at
            the target position with a zero velocity'''
        decel_rate = self.DECELERATION_SPEEDS[speed]
        to_target = target_pos - self.pos
        dist = to_target.length()
        if dist > 0:
            # calculate the speed required to reach the target given the
            # desired deceleration rate
            speed = dist / decel_rate
            # make sure the velocity does not exceed the max
            speed = min(speed, self.max_speed)
            # from here proceed just like Seek except we don't need to
            # normalize the to_target vector because we have already gone to the
            # trouble of calculating its length for dist.
            desired_vel = to_target * (speed / dist)
            return (desired_vel - self.vel)
        return Vector2D(0, 0)

    def pursuit(self, evader):
        ''' this behaviour predicts where an agent will be in time T and seeks
            towards that point to intercept it. '''
        ## OPTIONAL EXTRA... pursuit (you'll need something to pursue!)
        return Vector2D()

    def wander(self, delta):
        ''' random wandering using a projected jitter circle '''
        wt = self.wander_target
        # this behaviour is dependent on the update rate, so this line must
        # be included when using time independent framerate.
        jitter_tts = self.wander_jitter * delta # this time slice
        # first, add a small random vector to the target's position
        wt += Vector2D(uniform(-1,1) * jitter_tts, uniform(-1,1) * jitter_tts)
        # re-project this new vector back on to a unit circle
        wt.normalise()
        # increase the length of the vector to the same as the radius
        # of the wander circle
        wt *= self.wander_radius
        # move the target into a position WanderDist in front of the agent
        target = wt + Vector2D(self.wander_dist, 0)
        # project the target into world space
        wld_target = self.world.transform_point(target, self.pos, self.heading, self.side)
        # and steer towards it
        return self.seek(wld_target)
        

    def follow_path(self):
        to_target = self.path.current_pt() - self.pos
        dist = to_target.length()

        
        if self.path.is_finished():
            speed = dist
            speed = min(speed, self.max_speed)
            desired_vel = to_target * (speed / dist)
        else:
            if dist < self.waypoint_threshold:
                self.path.inc_current_pt()

            desired_vel = (self.path.current_pt() - self.pos).normalise() * self.max_speed

        return (desired_vel - self.vel)


    
        
