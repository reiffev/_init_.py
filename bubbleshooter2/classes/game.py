from random import choice
from .arrow import *

class Game:
    renderclock = time.Clock()
    Animclock = time.Clock()
    newlinerclock = time.Clock()
    rendertime = 0
    Animtime = 0
    #newlinertime = 0
    parite = 1

    @staticmethod
    def choice_color():
        colors = list(Game.colors_count.keys())
        if 'bla' in colors: colors.remove('bla')
        return choice(colors)
    
    @staticmethod
    def init(level=None,initial_score=0,bonus_ball=0,time_indice=120000,test=False):
        Game.initial_score = initial_score
        Game.test = test
        Game.time_indice = time_indice
        Game.pause = False
        Animation.clear()
        Game.score = 0
        Game.balls_layer = bg.copy()
        Game.balls_layer.set_alpha(100)
        Game.status = 0 #trying to figure out
        Game.colors_count = {'red':0,'blu':0,'yel':0,'gre':0,'pur':0,'bla':0}
        Game.d = {} #trying to figure out
        Game.l  = [] #trying to figure out
        Game.l0 = [] #trying to figure out
        Game.l1 = [] #trying to figure out
        if level == None: # si mode == classic
            Game.addline(10) # <----------------------------------------Number of lines to start
            Game.ball_nb = -1
            Animation.add(Game.newliner)
            Game.newlinerclock.tick()
            Game.newlinertime = 0
        else:
            Game.ball_nb = 10 + bonus_ball# <---------------------------------------Number of balls in challenge mode
            #Game.colors_count.update({'bla':0})
            for x,y in level[0]:
                color = Game.choice_color()
                Game.d[(x,y)] = color
                Game.colors_count[color] += 1
                Game.balls_layer.blit(balls[color],(x-beta,y-beta))
            for x,y in level[1]:
                Game.d[(x,y)] = 'bla'
                Game.colors_count['bla'] += 1
                Game.balls_layer.blit(balls['bla'],(x-beta,y-beta))
            # determine la parite
            Game.parite = (min(Game.d,key=lambda x: x[1])[0]//beta)&1
        [Game.colors_count.pop(c)for c,v in list(Game.colors_count.items()) if not v]
        Game.ball = None
        Animation.add(Game.render)
        Game.dkeys = set(Game.d.keys())
        Game.maintime = time.get_ticks()
    
    @staticmethod
    def update():
        if not Game.status:
            if not Game.ball:
                if not Game.ball_nb:
                    Game.status = 1
                    return
                color = Game.choice_color()
                Game.ball = Ball(color)
                Game.colors_count[color]+=1
            elif Game.ball.fix:
                Game.balls_layer.blit(Game.ball.img,Game.ball)
                Game.d[Game.ball.center] = Game.ball.color
                l = [Game.ball.center]
                for X,Y in l:
                    for x,y in ((-gamma,0),(-beta,-alpha),(beta,-alpha),(gamma,0),(-beta,alpha),(beta,alpha)):
                        if (X+x,Y+y)in Game.d and Game.d[(X+x,Y+y)] == Game.ball.color and (X+x,Y+y) not in l: l.append((X+x,Y+y))
                if len(l) >= 3:
                    Game.scoreN = 2
                    for x,y in l:
                        Game.d.pop((x,y))
                    Game.colors_count[Game.ball.color] -= len(l)
                    if not Game.colors_count[Game.ball.color]: Game.colors_count.pop(Game.ball.color)
                    
                    m = Game.d.copy()
                    k = [(x,y)for x,y in m if y==beta]
                    for X,Y in k:
                        m.pop((X,Y))
                        for x,y in ((-gamma,0),(-beta,-alpha),(beta,-alpha),(gamma,0),(-beta,alpha),(beta,alpha)):
                            if (X+x,Y+y)in m and not(X+x,Y+y)in k: k.append((X+x,Y+y))
                    Game.l.extend(l)
                    Game.scorebonus = Game.ball.shot/(1000*(len(Game.l)-2))
                    for (x,y),color in m.items():
                        Game.d.pop((x,y))
                        Game.colors_count[color] -= 1
                        if not Game.colors_count[color]: Game.colors_count.pop(color)
                    Game.l.extend(m.keys())
                    if not Game.colors_count: Game.status = 1
                    Animation.add(Game.plop)
                elif Game.ball.bottom > eta:
                    Game.status = 1
                Game.dkeys = set(Game.d.keys())
                Game.ball = None
                Game.ball_nb -= 1
            elif Game.ball.lost:
                Game.colors_count[Game.ball.color] -= 1
                if not Game.colors_count[Game.ball.color]: Game.colors_count.pop(Game.ball.color)
                Game.ball = None
                Game.ball_nb -= 1
        elif Game.status == 1:
            if not any((Game.l,Game.l0,Game.l1)):
                if not Game.colors_count:
                    Game.status = 4
                    Game.maintime = time.get_ticks() - Game.maintime
                    Game.final_score = int((Game.score/Game.maintime)*Game.time_indice)
                else:
                    Game.status = 6
                    Game.final_score = 0
                Game.balls_layer.set_alpha(255)
                Game.score = int(Game.score)
                if not Game.test and Game.score != Game.final_score: Animation.add(Game.update_final_score)
                else: Game.score = Game.final_score
        else:
            if Game.render() and Game.score == Game.final_score: Game.status //= 2
    
    @staticmethod
    def update_final_score():
        Game.score += (Game.final_score>Game.score)-(Game.final_score<Game.score)
        if Game.score == Game.final_score:
            Animation.remove(Game.update_final_score)
        
    
    @staticmethod
    def plop(): 
        Game.Animtime += Game.Animclock.tick()
        if Game.Animtime >= 80:
            if Game.l1:
                print "l1: {}".format(len(Game.l1));
                x,y = Game.l1.pop(0)
                Game.balls_layer.blit(applies_alpha(hole,bg.subsurface(x-beta,y-beta,gamma,gamma)),(x-beta,y-beta))
            if Game.l0:
                print "l0: {}".format(len(Game.l0));
                x,y = Game.l0.pop(0)
                Game.balls_layer.blit(applies_alpha(star3,bg.subsurface(x-beta,y-beta,gamma,gamma)),(x-beta,y-beta))
                Game.l1.append((x,y))
            if Game.l:
                print "l: {}".format(len(Game.l));
                x,y = Game.l.pop(0)
                Game.balls_layer.blit(applies_alpha(star1,bg.subsurface(x-beta,y-beta,gamma,gamma)),(x-beta,y-beta))
                Game.l0.append((x,y))
                Game.scoreN -= 1
                if Game.scoreN < 0: Game.score += 1 + Game.scorebonus
            elif not Game.l0 and not Game.l1:
                Animation.remove(Game.plop)
            Game.Animtime = 0

    @staticmethod
    def render():
        Game.rendertime += Game.renderclock.tick()
        if Game.rendertime >= 20:
            scr.blit(Game.balls_layer,screen)
            if Game.ball:
                scr.blit(Arrow.image,Arrow.rect)

                scr.blit(Game.ball.img,Game.ball)
                if Game.ball.cmprebour:
                    label = countfont.render(str(Game.ball.cmprebour),1,(0,0,0))
                    rlabel = label.get_rect(center=ball_rect.move(-1,-2).center)
                    scr.blit(label,rlabel)
            label = menu2font.render('Score : '+str(int(Game.score)+Game.initial_score),1,(150,200,200))
            rlabel = label.get_rect(bottomright=screen.move(-12,-12).bottomright)
            scr.blit(label,rlabel)
            if Game.ball_nb > 0:
                label = menu2font.render('balls remaining : '+str(int(Game.ball_nb)),1,(150,200,200))
                rlabel = label.get_rect(bottomright=rlabel.topright)
                scr.blit(label,rlabel)
            
            display.flip()
            Game.rendertime = 0
            return True
    
    @staticmethod
    def addline(n=1):
        Game.balls_layer.set_alpha(255)
        for n in range(n):
            Game.d = dict([((x,y+alpha),color)for (x,y),color in Game.d.items()])
            for x in range(beta*Game.parite+beta,screen.w,gamma):
                color = Game.choice_color()
                Game.d[(x,beta)] = color
                Game.colors_count[color] += 1
            Game.parite ^= 1
        Game.dkeys = set(Game.d.keys())
        Game.balls_layer.blit(bg,screen)
        for (x,y),color in Game.d.items():
            Game.balls_layer.blit(balls[color],(x-beta,y-beta))
            if y >= zeta: Game.status = 1
        Game.balls_layer.set_alpha(100)
    
    @staticmethod
    def newliner():
        if Game.status:
            Animation.remove(Game.newliner)
            return
        Game.newlinertime += Game.newlinerclock.tick()
        if Game.newlinertime >= 20000 and not Game.ball and not any((Game.l,Game.l0,Game.l1)):
            Game.addline()
            Game.newlinertime -= 20000
            
    @staticmethod
    def pause_resume():
        if Game.pause:
            Game.renderclock.tick()
            Game.Animclock.tick()
            Game.newlinerclock.tick()
            if Game.ball: Game.ball.clock.tick()
            mouse.set_pos(Game.pause_mouse_pos)
            Game.maintime += time.get_ticks()-Game.pause_tick
            Game.pause = False
        else:
            Game.pause_mouse_pos = mouse.get_pos()
            Game.pause_tick = time.get_ticks()
            Game.pause = True

def game_mainloop():
    mouse.set_visible(0)
    mouse.set_pos(screen.center)
    if Game.pause:
        pass
        Game.pause_resume()
        Game.pause = False
    while True:
        ev = event.poll()
        if ev.type == KEYDOWN and ev.key == K_ESCAPE: #hitting escape key pauses the game
            Game.pause_resume()
            mouse.set_visible(1)
            break
        elif ev.type == QUIT: # quit the game
            quit()
            exit()
        elif ev.type == MOUSEMOTION: #move mouse
            Arrow.update(ev.pos,eta)
        Game.update()
        if Game.status in (2,3):                
            break
        Animation.update()
        mainclock.tick(700) # <-----------------------------------------Ball Speed
    mouse.set_visible(1)
                
class Ball(Rect):
    
    def __init__(self,color):
        self.color = color
        self.img = Surface((0,0))
        self.px,self.py = self.cxcy = ball_rect.center
        self.cmp = 0
        self.cmprebour = 0
        self.clock = time.Clock()
        self.time = 500
        Animation.add(self.appears)
        self.fix = False
        self.lost = False
        self.shot = 0
    """
    def change_color(self,color):
        self.color = color
        self.img = transform.scale(balls[self.color],self.size)
    """
    def appears(self):
        self.time += self.clock.tick()
        if self.time >= 50:
            self.cmp += 1
            Rect.__init__(self,0,0,self.cmp*4,self.cmp*4)
            self.img = transform.scale(balls[self.color],self.size)
            self.center = self.cxcy
            if self.cmp == 10:
                Animation.remove(self.appears)
                Animation.add(self.rebour)
                self.cmprebour = 5 #change this number to change the timer on the ball
                self.time = 0
                return
            self.time = 0
    
    def rebour(self):
        if mouse.get_pressed()[0]:
            self.shot = 1000*self.cmprebour-self.time
            self.cmprebour = 1
            self.time = 1000
        self.time += self.clock.tick()
        if self.time >= 1000:
            self.cmprebour -= 1
            if not self.cmprebour:
                Animation.remove(self.rebour)
                Animation.add(self.move)
                x,y = mouse.get_pos()
                if y > eta: y = eta
                angle = atan2(y-self.centery,x-self.centerx)
                self.vx,self.vy = cos(angle)*1.5,sin(angle)*1.5
            self.time = 0
            
    def move(self):
        r = self.copy()
        r.center = self.px+self.vx,self.py+self.vy
        if r.top >= screen.bottom:
            Game.ball.lost = True
            Animation.remove(self.move)
            return
        if r.right > screen.right:
            self.px,self.py = screen.right-beta,self.centery+((r.centery-self.centery)/(r.centerx-self.centerx))*(screen.right-beta-self.centerx)
            self.vx = -self.vx
        elif r.left < screen.left:
            self.px,self.py = beta,self.centery+((r.centery-self.centery)/(r.centerx-self.centerx))*(beta-self.centerx)
            self.vx = -self.vx
        else:
            self.px += self.vx
            self.py += self.vy
        if r.top <= 0:
            self.px,self.py = self.centerx+((r.centerx-self.centerx)/(r.centery-self.centery))*(beta-self.centery),beta
            if self.px < beta: self.px = beta
            elif self.px > 29*beta: self.px = 29*beta
            self.px = int(self.px//beta)
            self.px = (self.px+(self.px&1^Game.parite))*beta
            self.fix = True
        self.center = self.px,self.py
        x0 = (self.left//beta)*beta
        x1 = (self.right//beta+1)*beta+1
        y0 = ((self.top-beta)//alpha)*alpha+beta
        y1 = ((self.bottom-beta)//alpha+1)*alpha+16
        s = set([(x,y)for x in range(x0,x1,beta)for y in range(y0,y1,alpha)])
        w = Game.dkeys.intersection(s)
        for i in w:
            if (i[0]-self.centerx)**2+(i[1]-self.centery)**2 < delta:
                g = set([(i[0]+x,i[1]+y)for x,y in ((-gamma,0),(-beta,-alpha),(beta,-alpha),(gamma,0),(-beta,alpha),(beta,alpha)) if 0<i[0]+x<screen.right]).intersection(s.difference(w))
                self.center = min(g,key=lambda p:(self.centerx-p[0])**2+(self.centery-p[1])**2)
                self.fix = True
                break
        if self.fix: Animation.remove(self.move)
        

class Animation:
    
    methods = []
    
    @staticmethod
    def update(): [method()for method in Animation.methods]
            
    @staticmethod
    def add(method): Animation.methods.append(method)
    
    @staticmethod
    def remove(method): Animation.methods.remove(method)
    
    @staticmethod
    def clear(): Animation.methods = []
