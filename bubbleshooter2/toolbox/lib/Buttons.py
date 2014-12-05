from pygame import Rect,display,image,font,Surface
font.init()
from pygame.locals import *
import os
thisrep = os.path.dirname(os.path.abspath(__file__))
imagesrep = os.path.join(thisrep,'images')

class Button0(Rect):
    def __init__(self,image):
        self.scr = display.get_surface()
        w,h = image.get_size()
        w //= 3
        self.images = [image.subsurface(x,0,w,h).copy() for x in range(0,w*3,w)]
        Rect.__init__(self,0,0,w,h)
        self.ACTIV = True
        self.status = False
        self.over = False
        
    def update(self,ev):
        if ev.type == MOUSEMOTION:
            if self.collidepoint(ev.pos) and not self.over:
                self.over = True
                return self.ACTIV
            elif not self.collidepoint(ev.pos) and self.over:
                self.over = False
                return self.ACTIV
        elif ev.type == MOUSEBUTTONUP and ev.button == 1 and self.collidepoint(ev.pos) and self.ACTIV:
            self.status = True
            return True
        elif ev.type == ACTIVEEVENT:
            self.over = False
            return True
        
    def screen(self):
        self.scr.blit(self.images[self.over if self.ACTIV else 2],self)
        return self  
    
    def show(self):
        display.update(self.screen())
        return self

class Coche(Rect):
    coche0 = image.load(os.path.join(imagesrep,'button0.png'))
    coche1 = image.load(os.path.join(imagesrep,'button1.png'))
    font = font.Font(os.path.join(thisrep,'MonospaceTypewriter.ttf'),8)

    def __init__(self,label='',fgcolor=(255,255,255),font=None):
        if not font: font = Coche.font
        Rect.__init__(self,Coche.coche0.get_rect())
        self.scr = display.get_surface()
        self.status = False
        label = Coche.font.render(label,1,fgcolor)
        Rlabel = label.get_rect()
        Rlabel.midleft = self.midright
        self.label = Surface(self.union(Rlabel).size,SRCALPHA)
        self.label.blit(label,Rlabel)
        
    
    def update(self,ev):
        if ev.type == MOUSEBUTTONUP and self.collidepoint(ev.pos):
            self.status ^= 1
            return True
    
    def screen(self):
        self.scr.blit(Coche.coche1 if self.status else Coche.coche0,self)
        self.scr.blit(self.label,self)
