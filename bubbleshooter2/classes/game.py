from random import choice
from .arrow import *
from collections import deque

class Game:
    renderclock = time.Clock()
    Animclock = time.Clock()
    newlinerclock = time.Clock()
    moveClock = time.Clock()
    rendertime = 0
    rendertime = 0
    Animtime = 0
    moveTime = 0
    # newlinertime = 0
    parite = 1
    colorqueue=deque()

    @staticmethod
    def choice_color():                             # chooses colors from color list
        colors = list(Game.colors_count.keys())
        if 'bla' in colors:
            colors.remove('bla')
        return choice(colors)

    @staticmethod
    def init(level=None, initial_score=0, bonus_ball=0, time_indice=120000, test=False): # initializes all values for game
        Game.initial_score = initial_score
        Game.test = test
        Game.time_indice = time_indice
        Game.pause = False
        Animation.clear()
        Game.score = 0
        Game.balls_layer = bg.copy()
        Game.balls_layer.set_alpha(100)
        Game.status = 0
        Game.colors_count = {'red': 0, 'blu': 0, 'yel': 0, 'gre': 0, 'pur': 0, 'bla': 0}   # colors list and count
        Game.pos = {}                           #tuples with images displayed.
        Game.d = {}                             # list of tuples of all the existing grid points with balls on them. Contains keys that come from l
        Game.l = []                             # tuple of ball just fired. if connected to same color it appends the other balls to it.
        Game.l0 = []                            # ball location x, y appended from l[0] so it can apply star3.png
        Game.l1 = []                            # ball location x, y appended from l0[0] so it can apply star3.png

        if level == None:  # si mode == classic
            Game.addline(10)  # <----------------------------------------Number of lines to start
            Game.ball_nb = -1
            Animation.add(Game.newliner)
            Game.newlinerclock.tick()
            Game.newlinertime = 0
        else:
            Game.ball_nb = 10 + bonus_ball  # <---------------------------------------Number of balls in challenge mode
            #Game.colors_count.update({'bla':0})
            for x, y in level[0]:
                color = Game.choice_color()
                Game.d[(x, y)] = color
                Game.pos[(x, y)] = color
                Game.colors_count[color] += 1
                Game.balls_layer.blit(balls[color], (x - beta, y - beta))
            for x, y in level[1]:
                Game.d[(x, y)] = 'bla'
                Game.colors_count['bla'] += 1
                Game.balls_layer.blit(balls['bla'], (x - beta, y - beta))
            # determine la parite
            Game.parite = (min(Game.d, key=lambda x: x[1])[0] // beta) & 1
        [Game.colors_count.pop(c) for c, v in list(Game.colors_count.items()) if not v]
        Game.ball = None
        Animation.add(Game.render)
        Game.dkeys = set(Game.d.keys())
        Game.maintime = time.get_ticks()

    @staticmethod
    def update():
        if not Game.status:
            if not Game.ball:                                     # checks if ball queued up
                if not Game.ball_nb:
                    Game.status = 1                               # need to identify status #'s to remember easier
                    return
                while len(Game.colorqueue) < 2:                   # while loop make sure the queue has 2 color, 1 for dequeue, 1 for next color
                    Game.colorqueue.append(Game.choice_color())
                currentcolor=Game.colorqueue.popleft()
                Game.ball = Ball(currentcolor)

                Game.colors_count[currentcolor] += 1                   # increments balls of that randomized color
            elif Game.ball.fix:
                Game.balls_layer.blit(Game.ball.img, Game.ball)
                Game.d[Game.ball.center] = Game.ball.color
                Game.pos = Game.d.copy();
                l = [Game.ball.center]                                 # adds position of ball on grid to array l <- [(x,y)]
                Game.tmp = {}
                #print Game.dkeys                                # Game.dkeys
                #print l
                for X, Y in l:                                  # checks for surrounding balls
                    for x, y in ((-gamma, 0), (-beta, -alpha), (beta, -alpha), (gamma, 0), (-beta, alpha), (beta, alpha)):
                        # ((-40, 0), (-20, -34), (20, -34), (40, 0), (-20, 34), (20,34))
                        #  order left, bot left, bot right, right, top left, top right
                        # x = 20; y = 34
                        if (X + x, Y + y) in Game.d and Game.d[(X + x, Y + y)] == Game.ball.color and (X + x, Y + y) not in l:
                                l.append((X + x, Y + y))        # appends new position into l if not in already
                                """print "printing l"
                                print l
                                print "printing Game.l0"
                                print Game.l0
                                print "printing Game.l1"
                                print Game.l1"""
                if len(l) >= 3:                                 # checks if there is a color length combo >= 3
                    Game.scoreN = 2                             # Game.scoreN is overall game score. Need to fix totaling
                    for x, y in l:
                        Game.d.pop((x, y))                        # deletes each ball from l that was just popped
                    Game.colors_count[Game.ball.color] -= len(l)  # subtracts balls deleted from grid after connection
                    if not Game.colors_count[Game.ball.color]:
                        Game.colors_count.pop(Game.ball.color)

                    m = Game.d.copy()
                    k = [(x, y) for x, y in m if y == beta]
                    for X, Y in k:
                        m.pop((X, Y))
                        for x, y in (
                        (-gamma, 0), (-beta, -alpha), (beta, -alpha), (gamma, 0), (-beta, alpha), (beta, alpha)):
                            if (X + x, Y + y) in m and not (X + x, Y + y) in k:
                                k.append((X + x, Y + y))
                    Game.l.extend(l)
                    Game.scorebonus = Game.ball.shot / (1000 * (len(Game.l) - 2))
                    for (x, y), color in m.items():
                        Game.tmpy = y
                        if y < Game.tmpy:
                            Game.tmpy = y
                        Game.tmp[(x, y)] = color
                        Game.d.pop((x, y))
                        Game.colors_count[color] -= 1
                        if not Game.colors_count[color]:
                            Game.colors_count.pop(color)
                    Game.l.extend(m.keys())
                    if not Game.colors_count:
                        Game.status = 1
                    #print "UPDATE BEFORE"
                    #print Animation.methods
                    if m:
                        #print "adding Game.drop"
                        Animation.add(Game.drop)
                    #print "adding Game.plop"
                    #print "UPDATE AFTER"
                    #print Animation.methods
                    Game.pos = Game.d.copy()
                    Animation.add(Game.plop)
                    #while Animation.methods.__contains__(Game.plop): THIS WORKS (in the sense that it prints). POSSIBLE WAY TO FIX BUG
                        #print "here"
                elif Game.ball.bottom > eta:
                    Game.status = 1
                Game.dkeys = set(Game.d.keys())
                Game.ball = None
                Game.ball_nb -= 1
            elif Game.ball.lost:
                Game.colors_count[Game.ball.color] -= 1
                if not Game.colors_count[Game.ball.color]:
                    Game.colors_count.pop(Game.ball.color)
                Game.ball = None
                Game.ball_nb -= 1
        elif Game.status == 1:
            if not any((Game.l, Game.l0, Game.l1)):
                if not Game.colors_count:
                    Game.status = 4
                    Game.maintime = time.get_ticks() - Game.maintime
                    Game.final_score = int((Game.score / Game.maintime) * Game.time_indice)
                else:
                    Game.status = 6
                    Game.final_score = 0
                Game.balls_layer.set_alpha(255)
                Game.score = int(Game.score)
                if not Game.test and Game.score != Game.final_score:
                    Animation.add(Game.update_final_score)
                else:
                    Game.score = Game.final_score
        else:
            if Game.render() and Game.score == Game.final_score:
                Game.status //= 2

    @staticmethod
    def update_final_score():
        Game.score += (Game.final_score > Game.score) - (Game.final_score < Game.score)
        if Game.score == Game.final_score:
            Animation.remove(Game.update_final_score)

    # When 3 or more balls connected, blow up balls animation
    # provides the animation for each ball explosion
    @staticmethod
    def plop():
        #print "PLOP"
        #print Animation.methods
        Game.Animtime += Game.Animclock.tick()
        if Game.Animtime >= 80:
            if Game.l1:                 # applies animation of hole and removes from the list
                x, y = Game.l1.pop(0)

                Game.balls_layer.blit(applies_alpha(hole, bg.subsurface(x - beta, y - beta, gamma, gamma)),
                                      (x - beta, y - beta))
            if Game.l0:                 # appends l1[0] to l0 and applies animation of star1 and removes from the list
                x, y = Game.l0.pop(0)
                Game.balls_layer.blit(applies_alpha(star3, bg.subsurface(x - beta, y - beta, gamma, gamma)),
                                      (x - beta, y - beta))
                Game.l1.append((x, y))
            if Game.l:                  # appends l0[0] to l0 and applies animation of star1 and removes from the list
                x, y = Game.l.pop(0)
                Game.balls_layer.blit(applies_alpha(star1, bg.subsurface(x - beta, y - beta, gamma, gamma)),
                                      (x - beta, y - beta))
                Game.l0.append((x, y))
                #print "printing x, y in l"
                #print x, y

                Game.scoreN -= 1
                if Game.scoreN < 0:
                    Game.score += 1 + Game.scorebonus
            elif not Game.l0 and not Game.l1:
                Animation.remove(Game.plop)
            Game.Animtime = 0

    @staticmethod
    def render():
        Game.rendertime += Game.renderclock.tick()
        if Game.rendertime >= 20:
            scr.blit(Game.balls_layer, screen)
            if Game.ball:
                scr.blit(Arrow.image, Arrow.rect)

                scr.blit(Game.ball.img, Game.ball)
                if Game.ball.cmprebour:
                    label = countfont.render(str(Game.ball.cmprebour), 1, (0, 0, 0))
                    rlabel = label.get_rect(center=ball_rect.move(-1, -2).center)
                    scr.blit(label, rlabel)
            label = menu2font.render('Score : ' + str(int(Game.score) + Game.initial_score), 1, (150, 200, 200))
            rlabel = label.get_rect(bottomright=screen.move(-12, -12).bottomright)
            scr.blit(label, rlabel)
            if Game.ball_nb > 0:
                label = menu2font.render('balls remaining : ' + str(int(Game.ball_nb)), 1, (150, 200, 200))
                rlabel = label.get_rect(bottomright=rlabel.topright)
                scr.blit(label, rlabel)

            # render for next color
            nextcolor=menu2font.render("Next ball : ",1,(255,255,255))
            nextcolorpos= label.get_rect(bottomleft=screen.move(5,-110).bottomleft)
            scr.blit(balls[Game.colorqueue[0]],label.get_rect(bottomleft=screen.move(105,-120).bottomleft))
            scr.blit(nextcolor,nextcolorpos)
            display.flip()
            Game.rendertime = 0
            return True

    @staticmethod 
    def updatePos():                            # Updates Graphic
        Game.moveTime += Game.moveClock.tick()
        if Game.moveTime >= 400:
            for(x,y), ipos in Game.pos.items():
                if ipos == 'red':
                    Game.balls_layer.blit(test[ipos], (x - beta, y - beta))
                    Game.pos[(x,y)] = 'one'
                elif ipos == 'one':
                    Game.balls_layer.blit(test[ipos], (x - beta, y - beta))
                    Game.pos[(x,y)] = 'two'
                elif ipos == 'two':
                    Game.balls_layer.blit(test[ipos], (x - beta, y - beta))
                    Game.pos[(x,y)] = 'three'
                elif ipos == 'three':
                    Game.balls_layer.blit(test[ipos], (x - beta, y - beta))
                    Game.pos[(x,y)] = 'red'
            Game.moveTime = 0

    @staticmethod
    def addline(n=1):                                   # adds line when newliner called
        Game.balls_layer.set_alpha(255)
        for n in range(n):
            Game.d = dict([((x, y + alpha), color) for (x, y), color in Game.d.items()])
            Game.pos = dict([((x, y + alpha), ipos) for (x, y), ipos in Game.pos.items()])
            for x in range(beta * Game.parite + beta, screen.w, gamma):
                color = Game.choice_color()
                Game.d[(x, beta)] = color
                Game.pos[(x, beta)] = color
                Game.colors_count[color] += 1
            Game.parite ^= 1
        Game.dkeys = set(Game.d.keys())
        Game.balls_layer.blit(bg, screen)
        for (x, y), color in Game.d.items():
            Game.balls_layer.blit(balls[color], (x - beta, y - beta))
            if y >= zeta:
                Game.status = 1
        Game.balls_layer.set_alpha(100)

    @staticmethod
    def newliner():                                     # checks if timer > 20 seconds and if match was not made with 2 others
        if Game.status:
            Animation.remove(Game.newliner)
            return
        Game.newlinertime += Game.newlinerclock.tick()
        if Game.newlinertime >= 20000 and not Game.ball and not any((Game.l, Game.l0, Game.l1)):
            Game.addline()
            Game.newlinertime -= 20000

    @staticmethod
    def pause_resume():                                 # pauses game when esc pressed
        if Game.pause:
            Game.renderclock.tick()
            Game.Animclock.tick()
            Game.newlinerclock.tick()
            if Game.ball:
                Game.ball.clock.tick()
            mouse.set_pos(Game.pause_mouse_pos)
            Game.maintime += time.get_ticks() - Game.pause_tick             # sets time by subtracting pause time from main time
            Game.pause = False
        else:
            Game.pause_mouse_pos = mouse.get_pos()                          # gets mouse position when unpaused
            Game.pause_tick = time.get_ticks()
            Game.pause = True

    @staticmethod
    def drop():
        #print "in drop"
        #print "DROP"
        #print Animation.methods
        Game.balls_layer.set_alpha(255)
        Game.tmp = dict([((x, y + 3), color) for (x, y), color in Game.tmp.items()])
        Game.balls_layer.blit(bg, screen)
        Game.dropcopy = Game.tmp.copy()
        for (x, y), color in Game.tmp.items():
            Game.balls_layer.blit(balls[color], (x - beta, y - beta))
            if Game.tmpy >= screen.bottom - 200:
                tmplen = len(Game.tmp)
                for (x, y), color in Game.dropcopy.items():
                    #print "printing x, y in Game.tmp"
                    #print Game.tmp
                    #print x, y
                    Game.tmp.pop((x, y))
                    tmplen -= 1
                    Game.balls_layer.blit(applies_alpha(hole, bg.subsurface(x - beta, y - beta, gamma, gamma)),
                                      (x - beta, y - beta))
                Animation.remove(Game.drop)
                break
        for (x, y), color in Game.d.items():
            Game.balls_layer.blit(balls[color], (x - beta, y - beta))

        Game.tmpy += 3

def game_mainloop():
    mouse.set_visible(0)
    mouse.set_pos(screen.center)
    if Game.pause:
        pass
        Game.pause_resume()
        Game.pause = False
    while True:
        ev = event.poll()                               # polls for mouse and keyboard events
        if ev.type == KEYDOWN and ev.key == K_ESCAPE:   # hitting escape key pauses the game
            Game.pause_resume()
            mouse.set_visible(1)
            break
        elif ev.type == QUIT:  # quit the game
            quit()
            exit()
        elif ev.type == MOUSEMOTION:  # move mouse
            Arrow.update(ev.pos, eta)
        Game.update()
        Game.updatePos()
        if Game.status in (2, 3):
            break
        Animation.update()
        mainclock.tick(700)  # <-----------------------------------------Ball Speed
    mouse.set_visible(1)


class Ball(Rect):
    def __init__(self, color):
        self.color = color
        self.img = Surface((0, 0))
        self.px, self.py = self.cxcy = ball_rect.center
        self.cmp = 0
        self.cmprebour = 0
        self.clock = time.Clock()
        self.ipos = 'one'
        self.time = 500
        Animation.add(self.appears)
        Animation.add(self.motion)
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
            Rect.__init__(self, 0, 0, self.cmp * 4, self.cmp * 4)
            self.img = transform.scale(balls[self.color], self.size)
            self.center = self.cxcy
            if self.cmp == 10:
                Animation.remove(self.appears)
                Animation.add(self.rebour)
                self.cmprebour = 0  # change this number to change the timer on the ball
                self.time = 0
                return
            self.time = 0

    def rebour(self):                       # action when clicking mouse to fire ball
        if mouse.get_pressed()[0]:
            # self.shot = 1000 * self.cmprebour - self.time
            self.cmprebour = 1
            self.time = 1000
        # self.time += self.clock.tick()
        if self.time >= 1000:
            self.cmprebour -= 1
            if not self.cmprebour:
                Animation.remove(self.rebour)
                Animation.add(self.move)
                x, y = mouse.get_pos()
                if y > eta:
                    y = eta
                angle = atan2(y - self.centery, x - self.centerx)
                self.vx, self.vy = cos(angle) * 1.5, sin(angle) * 1.5
            # self.time = 0

    def motion(self):
        if self.color == 'red':
            self.time += self.clock.tick()
            if self.time >= 400:
                if self.ipos == 'red':
                    self.img = transform.scale(balls[self.ipos], self.size)
                    self.ipos = 'one'
                else:
                    self.img = transform.scale(test[self.ipos], self.size)
                    if self.ipos == 'one':
                        self.ipos = 'two'
                    elif self.ipos == 'two':
                        self.ipos = 'three'
                    elif self.ipos == 'three':
                        self.ipos = 'red'
                self.time = 0
    
    def move(self):
        r = self.copy()
        r.center = self.px + self.vx, self.py + self.vy
        if r.top >= screen.bottom:                      # checks if ball touches bottom of screen is so you lose
            Game.ball.lost = True
            Animation.remove(self.move)
            return
        if r.right > screen.right:                      # redirects ball if ball hits right wall
            self.px, self.py = screen.right - beta, self.centery + (
            (r.centery - self.centery) / (r.centerx - self.centerx)) * (screen.right - beta - self.centerx)
            self.vx = -self.vx
        elif r.left < screen.left:                      # redirects ball if ball hits left wall
            self.px, self.py = beta, self.centery + ((r.centery - self.centery) / (r.centerx - self.centerx)) * (
            beta - self.centerx)
            self.vx = -self.vx
        else:
            self.px += self.vx
            self.py += self.vy
        if r.top <= 0:                                  # positions ball if touches top of screen
            self.px, self.py = self.centerx + ((r.centerx - self.centerx) / (r.centery - self.centery)) * (
            beta - self.centery), beta
            if self.px < beta:
                self.px = beta
            elif self.px > 29 * beta:
                self.px = 29 * beta
            self.px = int(self.px // beta)
            self.px = (self.px + (self.px & 1 ^ Game.parite)) * beta
            self.fix = True
        self.center = self.px, self.py
        x0 = (self.left // beta) * beta
        x1 = (self.right // beta + 1) * beta + 1
        y0 = ((self.top - beta) // alpha) * alpha + beta
        y1 = ((self.bottom - beta) // alpha + 1) * alpha + 16
        s = set([(x, y) for x in range(x0, x1, beta) for y in range(y0, y1, alpha)])
        w = Game.dkeys.intersection(s)
        for i in w:
            if (i[0] - self.centerx) ** 2 + (i[1] - self.centery) ** 2 < delta:
                g = set([(i[0] + x, i[1] + y) for x, y in
                         ((-gamma, 0), (-beta, -alpha), (beta, -alpha), (gamma, 0), (-beta, alpha), (beta, alpha)) if
                         0 < i[0] + x < screen.right]).intersection(s.difference(w))
                self.center = min(g, key=lambda p: (self.centerx - p[0]) ** 2 + (self.centery - p[1]) ** 2)
                self.fix = True
                break
        if self.fix:
            #print self.px, self.py
            Animation.remove(self.move)


class Animation:
    methods = []

    @staticmethod
    def update():
        [method() for method in Animation.methods]

    @staticmethod
    def add(method):
        Animation.methods.append(method)

    @staticmethod
    def remove(method):
        Animation.methods.remove(method)

    @staticmethod
    def clear():
        Animation.methods = []