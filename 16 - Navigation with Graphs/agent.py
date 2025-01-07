


from graphics import egi
import math
import random
from searches import SEARCHES

class Agent(object):


    def __init__(self, world=None, kind = 'slow',x=0,y=0):
        
        self.world = world

        
        self.start = self.world.get_box_by_pos(int(x),int(y))
   
        self.x = self.start._vc.x
        self.y = self.start._vc.y

        

        
        self.path = None
        self.currentpt = 0
        self.kind = kind
        self.currentbox = self.start
        



    def update(self, delta):

        currentbox = self.world.get_box_by_pos(int(self.x),int(self.y))
        self.currentbox = currentbox
        

        if self.path != None:

            if self.currentpt < len(self.path.path):
                
        
            
                pathindex = self.path.path[self.currentpt]

                nextbox = self.world.boxes[pathindex]._vc
                

                if self.kind == 'slow':

                    if currentbox.kind == '~':
                        penalty = 0.3
                    elif currentbox.kind == 'm':
                        penalty = 0.6
                    else:
                        penalty = 1
                else:
                    if currentbox.kind == '.':
                        penalty = 1.5
                    else:
                        penalty = 1.3
                    
                
                if abs(self.x-nextbox.x) > 1:
                    self.x -= math.copysign(1,self.x-nextbox.x) * penalty

                if abs(self.y-nextbox.y) > 1: 
                    self.y -= math.copysign(1,self.y-nextbox.y) * penalty

                
               

                if abs(self.x - nextbox.x) < 5 and abs(self.y - nextbox.y) < 5:
                    self.currentpt += 1
            else:
                self.x = self.start._vc.x
                self.y = self.start._vc.y
                self.resetpath()
                


            

    def resetpath(self):
        cls = SEARCHES['AStar']
        self.path = cls(self.world.graph, self.start.idx, self.world.target.idx, 0)
        self.currentpt = 0


    def draw(self):
        if self.kind == 'slow':
            egi.set_pen_color(name='BLUE')
            
        else:
            egi.set_pen_color(name='RED')
        egi.circle(self, 10)
            

    
