from pygame import *
import pygame
from pygame.locals import *
from math import sin,cos,atan2,degrees,radians

font.init()
pygame.mixer.init(22050, -16, 2, 4096)

def applies_alpha(surface1, surface2):
    output = surface2.copy().convert_alpha()
    surfarray.pixels_alpha(output)[:] = surfarray.array_alpha(surface1)
    return output


hole = image.load('res/erase.png')
star1 = image.load('res/plop.png')
star3 = image.load('res/plop3.png')
mainclock = time.Clock()

blop = pygame.mixer.Sound('res/blop.wav')

balls = {'red': image.load('res/bubblerougetest.png'),
         'blu': image.load('res/bubblebleutest.png'),
         'yel': image.load('res/bubblejaunetest.png'),
         'gre': image.load('res/bubbleverttest.png'),
         'pur': image.load('res/bubbleviolettest.png'),
         'bla': image.load('res/bubblenoirtest.png'),
         'whi': image.load('res/bubbleblanctest.png')}

ball_rect = balls['red'].get_rect()
alpha = int(cos(radians(30)) * ball_rect.height)        # alpha = 34
screen = Rect(0, 0, 15 * ball_rect.width, 16 * ball_rect.height + alpha)

beta = ball_rect.centerx                                # beta  = 20
gamma = ball_rect.width                                 # gamma = 40
delta = ball_rect.width ** 2 * 0.6                      # delta = 960
zeta = 15 * alpha                                       # zeta  = 510
eta = 14 * alpha + ball_rect.width                      # eta   = 516

scr = display.set_mode(screen.size)

bg = image.load('res/darktest.jpg').convert()
ball_rect.center = bg.fill((128, 128, 128), (0, eta, screen.width, 2 * ball_rect.width), special_flags=BLEND_ADD).center

countfont = font.Font('res/MonospaceTypewriter.ttf', 24)
messfont = font.Font(None, 80)
menu2font = font.Font(None, 30)