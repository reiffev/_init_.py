# -*- coding: utf-8 -*-
#!/usr/bin/env python
from sys import path
import os.path
thisrep = os.path.dirname(os.path.abspath(__file__))
path.append(os.path.dirname(thisrep))


from lib import Entry
fiche = """<#ffffff><+b>n<-b><#>ame :       <20,20>
<#ffffff><+b>f<-b><#>irst <#ffffff><+b>n<-b><#>ame : <20,20>
<#ffffff><+b>o<-b><#>ld :        <3,3> <#ffffff><+b>y<-b><#>ears"""

import pygame
pygame.display.set_mode((400,200))
e = Entry.get(fiche,'<centered <+i>Entry Test<-i> >',position=(10,10),fontsize=15,bgcolor=(20,20,20),fgcolor=(200,100,10))
while True:
    ev = pygame.event.wait()
    if ev.type == QUIT: break
    e.update(ev)
