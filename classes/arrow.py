from .constantes import *

class Arrow:
    
    img_origin = image.load('res/mouse.png')
    
    @staticmethod
    def update(pos,limit_bottom):
        x,y = pos
        if y > limit_bottom:
            y = limit_bottom
            mouse.set_pos((x,y))
        Arrow.image = transform.rotate(Arrow.img_origin, -degrees(atan2(y-ball_rect.centery, x-ball_rect.centerx)))
        Arrow.rect = Arrow.image.get_rect(center=(x,y))