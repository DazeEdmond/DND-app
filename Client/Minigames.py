import pygame as pg
from tkinter import filedialog as tkfd
from random import randint

from Utilities import FieldTool,Dialog
from Utilities import Green,Red,White,Black,LightGray,Gray,Yellow


def getCollision(x,y,xs,ys,xc,yc,click=False):
    if(click):
        xc,yc = pg.mouse.get_pos()
    if xc > x and xc < x+xs and yc > y and yc < y+ys:
        return True
    return False


#class Enemy
class Enemy:
    def __init__(self,window,pos,size,font,fontColor,name,HP,ATQ,pfp,theme,Slist,Me):
        self.W = window
        self.font = font
        self.fontColor = fontColor
        self.Slist = Slist
        self.pos = pos
        self.size = size
        self.name = name
        text_surface = font.render(name, True, fontColor)
        self.namePos = (pos[0]+(size[0]-text_surface.get_width())//2,pos[1])
        self.ATQ = int(ATQ)
        self.HPC = int(HP)
        self.HP = int(HP)
        self.HPBarSize = size[0]
        self.HPColor = Green
        self.HPBackColor = Red
        self.HPPos = (pos[0],pos[1]+size[1]+60)
        self.pfp = pfp
        self.pfpPos = (pos[0],pos[1]+50)
        self.deadCooldown = 50
        self.deadFlag = False
        self.theme = theme
        self.Me = Me

        try:
            self.image = pg.image.load(pfp)
        except FileNotFoundError:
            self.image = pg.image.load("Images\\sampleUser.png")
        self.image = pg.transform.scale(self.image,size)

    def render(self):
        nameText = self.font.render(self.name,True,self.fontColor)
        self.W.blit(nameText,self.namePos)
        
        self.W.blit(self.image,self.pfpPos)

        pg.draw.rect(self.W,self.HPBackColor,(self.HPPos[0],self.HPPos[1],self.size[0],40),border_radius=10)
        pg.draw.rect(self.W,self.HPColor,(self.HPPos[0],self.HPPos[1],self.HPBarSize,40),border_radius=10)

        if(self.deadFlag):
            self.deadCooldown -= 1

        if(self.deadCooldown <= 0):
            self.Me.clear()

    def getAtq(self):
        return randint(1,self.ATQ)
    
    def getHP(self):
        return self.HP

    def attack(self,dmg):
        self.HP = max(self.HP - dmg,0)
        if(self.HP == 0):
            self.Slist.append(Dialog(self.W,(920,100),(300,50),self.font,"Enemy beated",
                                                           50,3,self.Slist,Gray,Black))
            self.deadFlag = True
        self.HPBarSize = self.size[0]*self.HP/self.HPC

    def heal(self,heal):
        self.HP = min(self.HP + heal,self.HPC)
        self.HPBarSize = self.size[0]*self.HP/self.HPC

#Class TextDialog
class TextDialog:
    def __init__(self,window,pos,size,font,name,text,VL,Slist):
        self.W = window
        self.font = font
        self.fontColor = White
        self.Slist = Slist
        self.pos = pos
        self.size = size
        self.textSize = size[0]-20
        self.name = name
        self.text = self.textWrap(text)
        self.VL = VL
        print(self.text)
        
    def render(self):    
        pg.draw.rect(self.W,Black,(self.pos[0],self.pos[1],self.size[0],self.size[1]),border_radius=5)

        nameText = self.font.render(self.name,True,self.fontColor)
        self.W.blit(nameText,(self.pos[0]+10,self.pos[1]))

        tpos=1
        for t in self.text:
            Text = self.font.render(t,True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+10,self.pos[1]+10+tpos*30))
            tpos+=1

    def playVoiceLine(self):
        try:
            Sound = pg.mixer.Sound(self.VL)
            Sound.set_volume(0.3)
            Sound.play()
        except Exception as e:
            self.Slist.append(Dialog(self.W,(490,295),(300,50),"Sound not found",
                                                           50,3,self.Slist,Red,Black))

    def textWrap(self,text):
        lines = []
        line = ""
        for c in text:
            line += c
            if(self.font.size(line)[0] > self.textSize):
                ch = line[-1]
                line = line[:-1]
                lines.append(line)
                line = ""+ch
        lines.append(line)
        return lines
        # self.ptd = TextDialog(self.W,(10,520),(1260,190),self.font,"Daze","Texto muy muy muy largo que quiero desplegar a ver que muestra este text dialog y ver si sirve el wrrap Texto muy muy muy largo que quiero desplegar a ver que muestra este text dialog y ver si sirve el wrrap","Images\\GV1.mp3",self.screenItems);
        # self.ptd.playVoiceLine()
        # self.ptd.render()