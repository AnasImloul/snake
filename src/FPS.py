from pygame.font import Font
from math import ceil
class Fps :
    def __init__(self,refreshTime):
        self.fpsList=[]
        self.refreshTime=refreshTime
        self.time=0
        self.fps=60
        self.hide=False

    def update(self,screen, dt):
        self.time+=dt
        if self.time<self.refreshTime:
            self.fpsList.append(1/dt)

        else:
            try:
                self.fps = round(sum(self.fpsList)/len(self.fpsList))
            except:
                self.fps = round(1/self.refreshTime)
            self.time=0
            self.fpsList=[]

        self.show(screen)

    def show(self, screen):
        if not self.hide:
            font = Font('freesansbold.ttf', 16)

            Fps= font.render('FPS', True, (255,255,255))
            Rect = Fps.get_rect()
            Rect.center = (30, 20)
            screen.blit(Fps, Rect)

            FpsCount = font.render(str(self.fps), True, (255,255,255))
            FpsRect = FpsCount.get_rect()
            FpsRect.center = (70, 20)
            screen.blit(FpsCount, FpsRect)