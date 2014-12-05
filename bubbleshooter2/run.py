from classes.game import *
from classes.editor import *
from toolbox.lib.slidemenu import menu
from toolbox.lib.form import Form

def input_name(lastname):
    savebg = scr.copy()
    input_ = Form((0,0),200,14,height=None,font=None,bg=(250,250,250),fgcolor=None,hlcolor=(180,180,200),curscolor=(0xff0000),maxlen=0,maxlines=0)
    input_.center = screen.center
    input_.OUTPUT = lastname
    input_._select = 0,len(lastname)
    input_._adjust()
    newhightscore = menu2font.render('NEW HIGHTSCORE !',1,(200,200,200))
    newhightscorerect = newhightscore.get_rect(midbottom=(screen.centerx,input_.top-10))
    display.update(scr.blit(newhightscore,newhightscorerect))
    input_.show()
    while True:
        ev = event.wait()
        if ev.type == KEYDOWN and ev.key == K_RETURN:
            display.update(scr.blit(savebg,screen))
            return input_.OUTPUT    
        if input_.update(ev): input_.show() 



class Challenge:
    with open('levels','r') as levels:
        levels = levels.readlines()

    @staticmethod
    def init():
        Challenge.level_index = 0
        Challenge.pause = False
        Challenge.status = 0
        Challenge.score = 0

def challenge_mainloop():
    while True:
        if not Challenge.pause: Game.init(eval(Challenge.levels[Challenge.level_index]),Challenge.score)
        else: Challenge.pause = False
        game_mainloop()
        if not Game.status or Game.status == 4:
            Challenge.pause = True
            break
        elif Game.status == 2:
            Challenge.score += Game.score
            Challenge.level_index +=1
            if Challenge.level_index == len(Challenge.levels):
                Challenge.status = 2
                break
        elif Game.status == 3:
            Challenge.status = 3
            break
                


def save_hightscore(choix):
    with open(choix+'_hightscore','r') as hightscore:
        hightscore = hightscore.readlines()
        lastname = hightscore[-2].strip()
        lastscore = hightscore[-1].strip()
    if Game.score > int(lastscore):
        with open(choix+'_hightscore','a') as hightscore:
            name = input_name(lastname)
            hightscore.write('%s\n%i\n'%(name,Game.score))

def endmess():
    label = messfont.render('YOU WIN'if Game.status==2 else'YOU LOSE' ,1,(10,10,10))
    rlabel = label.get_rect(center=ball_rect.center)
    scr.blit(label,rlabel)
    display.flip()

choix = None
resume = False
scr.blit(bg,screen)
display.flip()
while True:
    if not choix:
        if Challenge.levels: menu_ = ('Classic','Challenge','Editor','Quit Game')
        else: menu_ = ('Classic','Editor','Quit Game')
        choix = menu(menu_,color1=(150,150,200),light=10,speed=300)[0]
    if choix == 'Quit Game': break
    elif choix == 'Classic':
        if not resume: Game.init()
        else: resume = False
        game_mainloop()
        if Game.status == 2: save_hightscore('Classic')
        if Game.status in (2,3): endmess()
    elif choix == 'Editor':
        if not resume: Editor.init()
        else: resume = False
        editor_mainloop()
    elif choix == 'Challenge':
        if not resume: Challenge.init()
        else: resume = False
        challenge_mainloop()
        if Challenge.status == 2: save_hightscore('Challenge')
        if Challenge.status in (2,3): endmess()
    else:
        break
    if choix == 'Editor': menu_ = ('Main Menu','Clear/Flip Grid','Save')
    else:  menu_ = ('Main Menu','Replay')
    choix2 = menu(menu_,pos='bottomleft',font1=menu2font,color1=(200,200,200),light=10,justify=False,speed=0)[0]
    if choix2 == 'Main Menu':
        scr.blit(bg,screen)
        display.flip()
        choix = None
    elif choix2 == None: resume = True
    elif choix2 == False: break
    elif choix2 == 'Save' and Editor.d[0]:
        with open('levels','a') as levels:
            levels.write(str(Editor.d)+'\n')
        with open('levels','r') as levels:
            Challenge.levels = levels.readlines()
        
time.wait(500)
quit()
