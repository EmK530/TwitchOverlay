messages=[]
launched=[False]

messageLifetime=5
messageFadeoutTime=2

old=print
def print(string):
   old("[Render] "+string)

def main():
   global messages
   global running
   fps = int(input("[2/3] Input desired FPS: "))
   div = float(input("[3/3] Resolution division (1 for fullscreen, 2 for half and so on): "))
   import os
   from os import system
   import math
   import time
   from screeninfo import get_monitors
   from TwitchSocket import running
   os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
   print("Importing pygame...")
   try:
      import pygame
   except ImportError:
      os.system('pip install pygame')
      import pygame
   mon = None
   for m in get_monitors():
      if m.is_primary:
         mon = m
         break
   launched[0]=True
   #ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
   resX=mon.width/div
   resY=mon.height/div
   pygame.font.init()
   font = pygame.font.SysFont('bahnschrift', math.floor(resY/36))
   twitch = pygame.image.load("twitch.png")
   imgoffset = resY/20
   twitch = pygame.transform.scale(twitch,(imgoffset,imgoffset))
   screen = pygame.display.set_mode((resX,resY))
   pygame.display.set_caption("Twitch Overlay")
   texts=[]
   textdata=[]
   def clamp(num, min_value, max_value):
       return max(min(num, max_value), min_value)
   def addText(string):
      fnt=font.render(string,True,(255,255,255))
      texts.append(fnt)
      textdata.append([fnt.get_height(),time.time()])
   clock=pygame.time.Clock()
   running = True
   while running:
       for event in pygame.event.get():
           if event.type == 256:
               running=False
               break
       screen.fill((0,0,0))
       for i in range(len(messages)):
          print("Received "+messages[i])
          addText(messages[i])
       messages.clear()
       size = len(texts)
       toRemove1=[]
       toRemove2=[]
       for i in range(size):
           lifetime=clamp(time.time()-textdata[size-i-1][1]-messageLifetime,0,2)
           if 255-((255/messageFadeoutTime)*lifetime) <= 2:
               toRemove1.append(textdata[size-i-1])
               toRemove2.append(texts[size-i-1])
               #print("Removing "+str(size-i-1))
       for i in range(len(toRemove1)):
           textdata.remove(toRemove1[i])
       for i in range(len(toRemove2)):
           texts.remove(toRemove2[i])
       size = len(texts)
       for i in range(size):
           lifetime=clamp(time.time()-textdata[size-i-1][1]-messageLifetime,0,2)
           twitch.set_alpha(255-(127*lifetime))
           texts[size-i-1].set_alpha(255-(127*lifetime))
           screen.blit(twitch,(0,resY-imgoffset*(i+1)))
           screen.blit(texts[size-i-1],(imgoffset,resY-(imgoffset)*(i+1)+(textdata[size-i-1][0]/2.5)))
       pygame.display.flip()
       clock.tick(fps)
