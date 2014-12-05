
from .arrow import *
from .game import *


class Editor:
    
    renderclock = time.Clock()
    rendertime = 0
    ball = balls['whi']
    parite = 1
    
    @staticmethod
    def init():
        Editor.d = [[],[]]
        Editor.balls_layer = bg.copy()
        for x in range(29*15):
            if x&1 == Editor.parite:
                Editor.balls_layer.fill((200,200,200),((x%29)*beta+beta-1,x//29*alpha+beta-1,3,3))
            
        Editor.parite ^= 1            
        
    @staticmethod
    def update(ev):
        if ev.type == MOUSEMOTION:
            x,y = ev.pos
            py = (y-beta+alpha//2)//alpha
            if py < 0: py = 0
            elif py > 14: py = 14
            parite = py&1^Editor.parite^1
            px = (x-beta*parite )//gamma
            if parite:
                if px < 0: px = 0
                if px > 13: px = 13
            Editor.py = py*alpha
            Editor.px = px*gamma+beta*parite
        elif ev.type == MOUSEBUTTONDOWN:
            if ev.pos[1] <= eta:
                if ev.button == 1:
                    r = ball_rect.copy()
                    r.topleft = Editor.px,Editor.py
                    if r.center in Editor.d[0]:
                        Editor.d[0].remove(r.center)
                    elif r.center in Editor.d[1]:
                        Editor.d[1].remove(r.center)
                    else:
                        Editor.balls_layer.blit(Editor.ball,r)
                        Editor.d[Editor.ball == balls['bla']].append(r.center)
                        return
                    Editor.balls_layer.blit(applies_alpha(hole,bg.subsurface(r)),r)
                    Editor.balls_layer.fill((200,200,200),(r.centerx-1,r.centery-1,3,3))
                if ev.button == 3:
                    Editor.ball = balls['bla'] if Editor.ball == balls['whi'] else balls['whi']
        elif ev.type == KEYDOWN and ev.key == K_t and Editor.d[0]:
            Game.init(Editor.d,test=True)
            game_mainloop()
            mouse.set_visible(0)
        else: return
        Editor.rendertime += Editor.renderclock.tick()
        if Editor.rendertime >= 20:
            Editor.render()
            Editor.rendertime = 0
        
    @staticmethod
    def render():
        scr.blit(Editor.balls_layer,screen)
        scr.blit(Editor.ball,(Editor.px,Editor.py))
        scr.blit(Arrow.image,Arrow.rect)
        display.flip()

def editor_mainloop():
    mouse.set_visible(0)
    event.clear()
    event.pump()
    event.post(event.Event(MOUSEMOTION,{'pos':mouse.get_pos()}))
    while True:
        ev = event.wait()
        if ev.type == KEYDOWN and ev.key == K_ESCAPE:
            mouse.set_visible(1)
            break
        elif ev.type == QUIT:
            quit()
            exit()
        elif ev.type == MOUSEMOTION:
            Arrow.update(ev.pos,screen.bottom)
        Editor.update(ev)
    mouse.set_visible(1)