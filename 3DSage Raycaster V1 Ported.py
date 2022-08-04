#------------------------YouTube-3DSage----------------------------------------
#3DSage's video: https://www.youtube.com/watch?v=gYRrGTC7GtA 
#Arrow keys to move player.
#Converted to python by ConnorTippets on github.

from math import *
import pygame, sys
size = (1024,510)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
mapX = 8
mapY = 8
mapS = 64
target = 60
delta = 1
map = [
 1,1,1,1,1,1,1,1,
 1,0,0,1,0,0,0,1,
 1,0,0,1,0,0,0,1,
 1,0,1,1,0,0,0,1,
 1,0,1,0,0,0,0,1,
 1,0,1,0,0,0,0,1,
 1,0,0,0,0,1,0,1,
 1,1,1,1,1,1,1,1,
]
drawtopdown = False
collision = True

def drawMap2D():
    for y in range(mapY):
        for x in range(mapX):
            if map[y*mapX+x]>0:
                color = (255,255,255)
            else:
                color = (0,0,0)
            xo=x*mapS
            yo=y*mapS
            rect = pygame.Rect((xo+1,yo+1), (mapS-1,mapS-1))
            pygame.draw.rect(screen, color, rect)

#------------------------PLAYER------------------------------------------------
degToRad = lambda a: a/180.0*pi
def FixAng(a):
    if a > 359:
        a -= 360
    if a < 0:
        a += 360
    return a

px,py,pa = 230,400,90
pdx,pdy = cos(degToRad(pa)),-sin(degToRad(pa))

def drawPlayer2D():
    color = (255,255,0)
    rect = pygame.Rect((px-4,py-4), (8,8))
    pygame.draw.rect(screen, color, rect)
    pygame.draw.line(screen, color, (px,py), (px+pdx*20,py+pdy*20), 4)

def Buttons(key):
    global pa,pdx,pdy,px,py
    if key=='a':
        pa+=3*delta
        pa=FixAng(pa)
        pdx=cos(degToRad(pa))
        pdy=-sin(degToRad(pa)) 	
    if key=='d':
        pa-=3*delta
        pa=FixAng(pa)
        pdx=cos(degToRad(pa))
        pdy=-sin(degToRad(pa))
    xo = 0
    if pdx < 0:
        xo = -20
    else:
        xo = 20
    yo = 0
    if pdy < 0:
        yo = -20
    else:
        yo = 20
    ipx,ipx_add_xo,ipx_sub_xo = int(px/64),int((px+xo)/64),int((px-xo)/64)
    ipy,ipy_add_yo,ipy_sub_yo = int(py/64),int((py+yo)/64),int((py-yo)/64)
    if key=='w':
        if collision:
            try:
                if map[ipy*mapX+ipx_add_xo]==0:
                    px+=pdx*3*delta
                if map[ipy_add_yo*mapX+ipx]==0:
                    py+=pdy*3*delta
            except: pass
        else:
            px+=pdx*5*delta
            py+=pdy*5*delta
    if key=='s':
        if collision:
            try:
                if map[ipy*mapX+ipx_sub_xo]==0:
                    px-=pdx*3*delta
                if map[ipy_sub_yo*mapX+ipx]==0:
                    py-=pdy*3*delta
            except: pass
        else:
            px-=pdx*5*delta
            py-=pdy*5*delta

#---------------------------Draw Rays and Walls--------------------------------
distance = lambda ax,ay,bx,by,ang: cos(degToRad(ang))*(bx-ax)-sin(degToRad(ang))*(by-ay)

def drawRays2D():
    r,mx,my,mp,dof,side,vx,vy,rx,ry,ra,xo,yo,disV,disH = None,None,None,None,None,None,None,None,None,None,None,None,None,None,None
    if drawtopdown:
        ceiling = pygame.Rect(526,0, 1006-526,320-50)
        floor = pygame.Rect(526,320-50, 1006-526,size[1])
    else:
        ceiling = pygame.Rect(0,0, size[0],int(size[1]/2))
        floor = pygame.Rect(0,int(size[1]/2), size[0],size[1])
    pygame.draw.rect(screen, (0,255,255), ceiling)
    pygame.draw.rect(screen, (0,0,255), floor)
    
    ra=FixAng(pa+30)
    for r in range((60 if drawtopdown else 120)):
        #---Vertical--- 
        dof=0
        side=0
        disV=100000
        Tan=tan(degToRad(ra))
        if cos(degToRad(ra))> 0.001:
            rx = (int((int(px>>6))<<6))+64
            ry = (px-rx)*Tan+py
            xo = 64
            yo = -xo*Tan
        elif cos(degToRad(ra))<-0.001:
            rx = (int((int(px>>6))<<6))-0.0001
            ry = (px-rx)*Tan+py
            xo = -64
            yo = -xo*Tan
        else:
            rx=px
            ry=py
            dof=8
        while dof<8:
            mx=int(int(rx)>>6)
            my=int(int(ry)>>6)
            mp=my*mapX+mx
            if mp>0 and mp<mapX*mapY and map[mp]>0:
                dof = 8
                disV=cos(degToRad(ra))*(rx-px)-sin(degToRad(ra))*(ry-py)
                break
            else:
                rx += xo
                ry += yo
                dof += 1

        vx=rx; vy=ry;
        #---Horizontal---
        dof=0
        disH=100000
        try:
            Tan=1.0/Tan
        except:
            Tan=0
        if sin(degToRad(ra))> 0.001:
            ry = (int((int(py>>6))<<6))-0.0001
            rx = (py-ry)*Tan+px
            yo = -64
            xo = -yo*Tan
        elif sin(degToRad(ra))<-0.001:
            ry = (int((int(py>>6))<<6))+64
            rx = (py-ry)*Tan+px
            yo = 64
            xo = -yo*Tan
        else:
            rx = px
            ry = py
            dof=8
        
        while dof<8:
            mx=int(int(rx)>>6)
            my=int(int(ry)>>6)
            mp=my*mapX+mx
            if mp>0 and mp<mapX*mapY and map[mp]>0:
                dof = 8
                disH=cos(degToRad(ra))*(rx-px)-sin(degToRad(ra))*(ry-py)
            else:
                rx += xo
                ry += yo
                dof += 1        
        color = (0,204,0)
        if disV<disH:
            rx=vx
            ry=vy
            disH=disV
            color = (0,153,0)
        if drawtopdown:
            pygame.draw.line(screen, color, (px,py),(rx,ry), 2)
        ca=FixAng(pa-ra)
        disH=disH*cos(degToRad(ca))
        if drawtopdown:
            lineH = (mapS*320)/(disH)
            lineOff = 320-50 - int(int(lineH)>>1)
        else:
            lineH = (mapS*640)/(disH)
            lineOff = 320 - int(int(lineH)>>1)
        if not lineH <2:
            if drawtopdown:
                pygame.draw.line(screen, color, (r*8+530,lineOff), (r*8+530,lineOff+lineH), 8)
            else:
                pygame.draw.line(screen, color, (r*8,lineOff), (r*8,lineOff+lineH), 8)
        ra=FixAng(ra-(1 if drawtopdown else 0.5))

def display():
    if drawtopdown:
        drawMap2D()
        drawPlayer2D()
    drawRays2D()
    controls(pygame.key.get_pressed())

def controls(keys):
    global drawtopdown
    joystickx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    joysticky = keys[pygame.K_UP] - keys[pygame.K_DOWN]
    keys = []
    if joystickx == -1:
        keys.append("a")
    if joystickx == 1:
        keys.append("d")
    if joysticky == -1:
        keys.append("s")
    if joysticky == 1:
        keys.append("w")
    if keys:
        for key in keys:
            Buttons(key)

def main():
    pygame.init()
    global px, py, drawtopdown, size, screen, collision
    while True:
        px,py = int(px),int(py)
        delta = clock.get_time()
        if not drawtopdown and size == (1024,510):
            size = (960,640)
            screen = pygame.display.set_mode(size)
        if drawtopdown and size == (960,640):
            size = (1024,510)
            screen = pygame.display.set_mode(size)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    drawtopdown = not drawtopdown
                if event.key == pygame.K_k:
                    collision = not collision
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((76,76,76))
        display()
        pygame.display.flip()
        clock.tick(target)
        pygame.display.set_caption("YouTube-3DSage. Converted by Github-ConnorTippets; FPS: " + str(int(clock.get_fps())) + "; Press M to toggle top down view and K to toggle collision")
main()
