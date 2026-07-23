import pygame as pg
from tkinter import filedialog as tkfd
from random import randint

def getCollision(x,y,xs,ys,xc,yc,click=False):
    if(click):
        xc,yc = pg.mouse.get_pos()
    if xc > x and xc < x+xs and yc > y and yc < y+ys:
        return True
    return False

#Colors
Green = (50,207,81)
Red = (207,50,50)
White = (204,204,204)
Black = (0,0,0)
LightGray = (170,170,170)
Gray = (100,100,100)
Yellow = (204,204,35)

#############
####Field####
#############

#FieldTool
class FieldTool:
    def __init__(self,window,pos,size,font,color,fontColor,textPos,selectable=False,text=""):
        self.W = window
        self.pos = pos
        self.size = size
        self.text = text
        self.textPos = textPos
        self.font = font
        self.color = color
        self.ACTcolor = color
        self.fontColor = fontColor
        self.selectable = selectable
    
    def centerText(self):
        text_surface = self.font.render(self.text, True, self.fontColor)
        self.textPos = (self.pos[0]+(self.size[0]-text_surface.get_width())//2,self.pos[1]+(self.size[1]-self.font.get_height())//2)

    def render(self):
        self.ACTcolor = self.color
        if(self.selectable and getCollision(self.pos[0],self.pos[1],self.size[0],self.size[1],0,0,True)):
            self.ACTcolor = (min(self.color[0]+30,255),
                             min(self.color[1]+30,255),
                             min(self.color[2]+30,255))

        pg.draw.rect(self.W,self.ACTcolor,(self.pos[0],self.pos[1],self.size[0],self.size[1]),border_radius=20)
        nameText = self.font.render(self.text,True,self.fontColor)
        self.W.blit(nameText,self.textPos)

    def isClicked(self,x,y):
        return -1

#class Dialog
class Dialog(FieldTool):
    def __init__(self,window,pos,size,font,text,time,speed,Slist,color=Black,fontColor=(255,255,255)):
        super().__init__(window,pos,size,font,color,fontColor,(((size[0]/2)-len(text)*6)/2+pos[0],
                                                                            (size[1]/2)-27+pos[1]),
                                                                             True,text)
        self.time = time
        self.count = 0
        self.speed = speed
        self.Slist = Slist

    def render(self):
        super().render()

        self.count+=1
        self.pos = (self.pos[0],self.pos[1]-self.speed)
        self.textPos = (self.textPos[0],self.textPos[1]-self.speed)
        if self.count >= self.time:
            self.Slist.remove(self)

    def isClicked(self,x,y):
        flag = getCollision(self.pos[0],self.pos[1],self.size[0],self.size[1],x,y)
        if flag:
            self.Slist.remove(self)
        return -1

#class image
class Image(FieldTool):
    def __init__(self,window,pos,size,font,imagePath,color=Black,fontColor=(255,255,255),evt=-1):
        super().__init__(window,pos,size,font,color,fontColor,pos)
        self.path = imagePath
        try:
            self.image = pg.image.load(self.path)
        except FileNotFoundError:
            self.image = pg.image.load("Images\\sampleUser.png")
        self.image = pg.transform.scale(self.image,size)
        self.evt = evt

    def getResult(self):
        return self.path

    def render(self):
        self.W.blit(self.image,self.pos)

    def setPath(self,path):
        if(path!=''):
            self.path = path
            self.image = pg.image.load(self.path)
            self.image = pg.transform.scale(self.image,self.size)

    def isClicked(self,x,y):
        if(getCollision(self.pos[0],self.pos[1],self.size[0],self.size[1],x,y)):
            return self.evt
        return -1

#class FileDialog
class FileDialog(FieldTool):
    def __init__(self,window,pos,size,font,title,types,text,dest,color=Black,fontColor=(255,255,255)):
        super().__init__(window,pos,size,font,color,fontColor,(((size[0]/2)-len(text)*6)/2+pos[0],
                                                                            (size[1]/2)-27+pos[1]),
                                                                             True,text)
        self.path = ""
        self.dest = dest
        self.title = title
        self.types = types

    def isClicked(self,x,y):
        if(getCollision(self.pos[0],self.pos[1],self.size[0],self.size[1],x,y)):
            self.path = tkfd.askopenfilename(title=self.title,filetypes=self.types)
            self.dest.setPath(self.path)
        return -1
    
#class BTN
class BTN(FieldTool):
    def __init__(self,window,pos,size,font,action,text,color=Black,fontColor=(255,255,255),enabled=True,disabledColor=(150,150,150)):
        text_surface = font.render(text, True, fontColor)
        super().__init__(window,pos,size,font,color,fontColor,(pos[0]+(size[0]-text_surface.get_width())//2,pos[1]+(size[1]-font.get_height())//2),
                                                                             True,text)
        self.action = action
        self.enabled = enabled
        self.disabledColor = disabledColor

    def render(self):
        if(self.enabled):
            self.ACTcolor = self.color
            if(self.selectable and getCollision(self.pos[0],self.pos[1],self.size[0],self.size[1],0,0,True)):
                self.ACTcolor = (min(self.color[0]+30,255),
                                min(self.color[1]+30,255),
                                min(self.color[2]+30,255))

            pg.draw.rect(self.W,self.ACTcolor,(self.pos[0],self.pos[1],self.size[0],self.size[1]),border_radius=20)
            nameText = self.font.render(self.text,True,self.fontColor)
            self.W.blit(nameText,self.textPos)
        else:
            pg.draw.rect(self.W,self.disabledColor,(self.pos[0],self.pos[1],self.size[0],self.size[1]),border_radius=20)
            nameText = self.font.render(self.text,True,self.fontColor)
            self.W.blit(nameText,self.textPos)


    def isClicked(self,x,y):
        if(getCollision(self.pos[0],self.pos[1],self.size[0],self.size[1],x,y) and self.enabled):
            return self.action
        return -1

    def enable(self,state):
        self.enabled = state
        
#class TextField():
class TXTField(FieldTool):
    def __init__(self,window,pos,size,font,color=Black,fontColor=(255,255,255),AC="ABCDEFGHIJKLMNOPQRSTUVWXYZ ",canWrite=True):
        text_surface = font.render(" ", True, fontColor)
        super().__init__(window,pos,size,font,color,fontColor,(pos[0]+7,pos[1]+(size[1]-font.get_height())//2),True)
        self.selected = False
        self.action = (1,2)
        self.allowedChars = AC
        self.canWrite = canWrite

    def getResult(self):
        return self.text

    def clean(self):
        self.text = ""

    def isEmpty(self):
        empty = True
        if self.text == "":
            return True
        for t in self.text:
            if t != " ":
                empty = False
        return empty

    def isClicked(self,x,y):
        flag = getCollision(self.pos[0],self.pos[1],self.size[0],self.size[1],x,y)
        if(not self.canWrite):
            return -1

        if flag:
            self.selected = True
            return self.action[0]
        elif self.selected: 
            self.selected = False
            return self.action[1]
        return -1

    def write(self,key):
        if(not self.canWrite):
            return

        if key == '°':
            self.text = self.text[:-1]
        else:
            textSpace = self.font.render(self.text,True,self.fontColor)
            if(key.upper() in self.allowedChars and textSpace.get_width()<self.size[0]-20):
                self.text += key

    def setPath(self,path):
        self.text = path

#class comboBox
class ComboBox(FieldTool):
    def __init__(self,window,pos,size,font,color=Black,fontColor=(255,255,255),action=3):
        super().__init__(window,pos,size,font,color,fontColor,(pos[0]+7,(size[1]/2)-27+pos[1]),True,"None")
        self.items = ["None"]
        self.selectedItem = 0
        self.selected = False
        self.action = action

    def getResult(self):
        return self.items[self.selectedItem]

    def isClicked(self,x,y):
        flag = getCollision(self.pos[0],self.pos[1],self.size[0],self.size[1],x,y)
        if flag:
            self.selected = True
            return self.action
        return -1

    def clearItems(self):
        self.items.clear()
        self.items.append("None")

    def setItems(self,items):
        self.clearItems()
        self.items = self.items[:-1]
        for i in items:
            self.items.append(i)
        self.text = self.items[0]

    def appendItem(self,item):
        self.items.append(item)

    def removeItem(self,item):
        self.items.remove(item)

    def showItems(self):
        YItemPos = self.pos[1] + self.size[1]
        YTextPos = self.textPos[1] + self.size[1]
        for i in range(0,len(self.items)):
            self.ACTcolor = self.color
            if(getCollision(self.pos[0],YItemPos+i*self.size[1],self.size[0],self.size[1],0,0,True)):
                self.ACTcolor = (min(self.color[0]+30,255),
                                 min(self.color[1]+30,255),
                                 min(self.color[2]+30,255))
            pg.draw.rect(self.W,self.ACTcolor,(self.pos[0],YItemPos+i*self.size[1],self.size[0],self.size[1]),border_radius=20)
            nameText = self.font.render(self.items[i],True,self.fontColor)
            self.W.blit(nameText,(self.textPos[0],YTextPos+i*self.size[1]))

    def getItemClick(self,x,y):
        self.selected = False
        for i in range(0,len(self.items)+1):
            if(getCollision(self.pos[0],self.pos[1]+i*self.size[1],self.size[0],self.size[1],x,y)):
                if(i!=0):
                    self.selectedItem = i-1
                    self.text = self.items[i-1]
                return 1
        return 0

    def collideWItems(self,x,y):
        return getCollision(self.pos[0],self.pos[1],self.size[0],(len(self.items)+1)*self.size[1],x,y)
        
#class Dice
class Dice(FieldTool):
    def __init__(self,window,pos,size,font,path,time,speed,Slist,color=Black,fontColor=(255,255,255),defnum=6):
        super().__init__(window,pos,size,font,color,fontColor,(0,0),True)
        self.time = time
        self.number = defnum
        self.numberCount = time+30
        self.count = 0
        self.speed = speed
        self.Slist = Slist
        self.path = path
        self.image = pg.image.load(self.path)#"Images\\sampleUser.png"
        self.image = pg.transform.scale(self.image,size)

    def render(self):
        self.W.blit(self.image,self.pos)

        self.count+=1
        if self.count < self.time:
            self.pos = (self.pos[0],self.pos[1]-self.speed)
            self.textPos = (self.textPos[0],self.textPos[1]-self.speed)
        else:
            nameText = self.font.render(str(self.number),True,self.fontColor)
            self.W.blit(nameText,(self.pos[0]+self.size[1]//2-len(str(self.number))*7,
                                  self.pos[1]+self.size[1]//2-25))

        if self.count >= self.numberCount:
            self.Slist.remove(self)

    def getResult(self):
        return self.path

    def setPath(self,path):
        if(path!=''):
            self.path = path
            self.image = pg.image.load(self.path)
            self.image = pg.transform.scale(self.image,self.size)

#class UserBanner
class UserBanner(FieldTool):
    def __init__(self,window,pos,font,secondFont,imagePath,color=Black,fontColor=(255,255,255),User="",showed=False):
        super().__init__(window,pos,(110,110),font,color,fontColor,pos)
        self.secondFont = secondFont
        self.path = imagePath
        try:
            self.image = pg.image.load(self.path)
        except FileNotFoundError:
            self.image = pg.image.load("Images\\sampleUser.png")
        self.image = pg.transform.scale(self.image,(self.size[0]-20,self.size[1]-20))
        self.imagePos = (pos[0]+10,pos[1]+10)
        self.User = User
        self.username = User.getName()
        self.showed = showed
        self.showing = False

    def getUsername(self):
        return self.username
    
    def getResult(self):
        return self.path

    def render(self,pos):
        self.pos = pos
        if (self.showed or getCollision(self.pos[0],self.pos[1],self.size[0],self.size[1],0,0,True)) or \
           (self.showing and (getCollision(self.pos[0],self.pos[1],self.size[0]+480,self.size[1],0,0,True))):
            if(self.User.getHP() <= 0):
                pg.draw.rect(self.W,Red,(self.pos[0],self.pos[1],self.size[0]+480,self.size[1]),border_radius=20)
            else:
                pg.draw.rect(self.W,self.color,(self.pos[0],self.pos[1],self.size[0]+480,self.size[1]),border_radius=20)

            Text = self.font.render(self.username,True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+120,self.pos[1]+2))

            Text = self.secondFont.render("Race: "+self.User.getRace(),True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+120,self.pos[1]+40))

            Text = self.secondFont.render("Role: "+self.User.getRole(),True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+120,self.pos[1]+65))

            Text = self.secondFont.render("HP: "+str(self.User.getHP())+"/"+str(self.User.getTotalHP()),True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+340,self.pos[1]+15))

            Text = self.secondFont.render("ATQ: "+str(self.User.getATQ()),True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+340,self.pos[1]+40))

            Text = self.secondFont.render("Mana: "+str(self.User.getMana()),True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+340,self.pos[1]+65))

            Text = self.secondFont.render("Charisma: "+str(self.User.getCharisma()),True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+450,self.pos[1]+15))

            Text = self.secondFont.render("Money: "+str(self.User.getMoney()),True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+450,self.pos[1]+40))

            self.showing = True
        else:
            pg.draw.rect(self.W,self.color,(self.pos[0],self.pos[1],self.size[0],self.size[1]),border_radius=20)
            self.showing = False

        self.W.blit(self.image,self.imagePos)

            
    def setPath(self,path):
        if(path!=''):
            self.path = path
            self.image = pg.image.load(self.path)
            self.image = pg.transform.scale(self.image,self.size)

#class DMUsersBanner
class DMUserBanner(FieldTool):
    def __init__(self,window,pos,font,secondFont,imagePath,color=Black,fontColor=(255,255,255),User="",showed=False):
        super().__init__(window,pos,(110,110),font,color,fontColor,pos)
        self.secondFont = secondFont
        self.path = imagePath
        try:
            self.image = pg.image.load(self.path)
        except FileNotFoundError:
            self.image = pg.image.load("Images\\sampleUser.png")
        self.image = pg.transform.scale(self.image,(self.size[0]-20,self.size[1]-20))
        self.imagePos = (pos[0]+10,pos[1]+10)
        self.User = User
        self.username = User.getName()
        self.showed = showed
        self.showing = False
        #Fields
        self.FHP = TXTField(window,(pos[0]+320,pos[1]+5),(70,35),secondFont,AC="1234567890")
        self.FHP.setPath(str(User.getHP()))
        self.FTHP = TXTField(window,(pos[0]+400,pos[1]+5),(70,35),secondFont,AC="1234567890")
        self.FTHP.setPath(str(User.getTotalHP()))
        self.FATQ = TXTField(window,(pos[0]+400,pos[1]+40),(70,35),secondFont,AC="1234567890")
        self.FATQ.setPath(str(User.getATQ()))
        self.FMana = TXTField(window,(pos[0]+400,pos[1]+75),(70,35),secondFont,AC="1234567890")
        self.FMana.setPath(str(User.getMana()))
        self.FCharisma = TXTField(window,(pos[0]+570,pos[1]+5),(70,35),secondFont,AC="1234567890")
        self.FCharisma.setPath(str(User.getCharisma()))
        self.FMoney = TXTField(window,(pos[0]+475,pos[1]+75),(70,35),secondFont,AC="-1234567890")
        self.FMoney.setPath(str(0))
        self.chargeBTN = BTN(window,(pos[0]+550,pos[1]+75),(70,35),secondFont,51,"Charge",color=(227,210,25))
        self.changeUserBTN = BTN(window,(pos[0]+645,pos[1]+5),(70,100),secondFont,52,"Change",color=Green)
        self.turnBTN = BTN(window,(pos[0]+720,pos[1]+5),(70,100),secondFont,62,"Turn",color=Yellow)
        self.items = []
        self.items.append(self.FHP)
        self.items.append(self.FTHP)
        self.items.append(self.FATQ)
        self.items.append(self.FMana)
        self.items.append(self.FCharisma)
        self.items.append(self.FMoney)
        self.items.append(self.chargeBTN)
        self.items.append(self.changeUserBTN)
        if(self.User.getHP() != 9999):
            self.items.append(self.turnBTN)
            

        self.selectedTXTField = ""

    def getUsername(self):
        return self.username

    def getResult(self):
        return self.username+"$"+self.items[0].getResult()+"$"+self.items[1].getResult()+"$"+self.items[2].getResult()+"$"+self.items[3].getResult()+"$"+self.items[4].getResult()

    def getAmount(self):
        return self.FMoney.getResult().replace("-","_")

    def updateUser(self):
        self.items[0].setPath(str(self.User.getHP()))
        self.items[1].setPath(str(self.User.getTotalHP()))
        self.items[2].setPath(str(self.User.getATQ()))
        self.items[3].setPath(str(self.User.getMana()))
        self.items[4].setPath(str(self.User.getCharisma()))

    def render(self,pos):
        self.pos = pos
        if (self.showed or getCollision(self.pos[0],self.pos[1],self.size[0],self.size[1],0,0,True)) or \
           (self.showing and (getCollision(self.pos[0],self.pos[1],self.size[0]+685,self.size[1],0,0,True))):
            pg.draw.rect(self.W,self.color,(self.pos[0],self.pos[1],self.size[0]+685,self.size[1]),border_radius=20)

            Text = self.font.render(self.username,True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+120,self.pos[1]+2))

            Text = self.secondFont.render("Race: "+self.User.getRace(),True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+120,self.pos[1]+40))

            Text = self.secondFont.render("Role: "+self.User.getRole(),True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+120,self.pos[1]+65))

            Text = self.secondFont.render("HP:                     /",True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+275,self.pos[1]+5))

            Text = self.secondFont.render("ATQ: ",True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+340,self.pos[1]+40))

            Text = self.secondFont.render("Mana: ",True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+340,self.pos[1]+75))

            Text = self.secondFont.render("Charisma: ",True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+470,self.pos[1]+5))

            Text = self.secondFont.render("Money:           "+str(self.User.getMoney()),True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+470,self.pos[1]+40))

            for i in self.items:
                i.render()

            self.showing = True
        else:
            pg.draw.rect(self.W,self.color,(self.pos[0],self.pos[1],self.size[0],self.size[1]),border_radius=20)
            self.showing = False
            self.selectedTXTField = ""

        self.W.blit(self.image,self.imagePos)

    
    def isClicked(self,x,y):
        if(self.showing):
            actions = []
            for i in self.items:
                a = i.isClicked(x,y)
                if(a == 1):
                    self.selectedTXTField = i
                actions.append(a)

            if 1 in actions:
                return 1

            self.selectedTXTField = ""            
            if 51 in actions:
                return 51
            if 52 in actions:
                return 52
            if 62 in actions:
                return 62

            elif 2 in actions:
                return 2

        return -1

    def setPath(self,path):
        if(path!=''):
            self.path = path
            self.image = pg.image.load(self.path)
            self.image = pg.transform.scale(self.image,self.size)

    def clean(self):
        self.FHP.clean()
        self.FTHP.clean()
        self.FATQ.clean()
        self.FMana.clean()
        self.FCharisma.clean()
        self.FMoney.clean()

    def isEmpty(self):
        if self.selectedTXTField == "":
            return True
        
        return self.selectedTXTField.isEmpty()

    def write(self,key):
        if(self.selectedTXTField == "" or not self.showing):
            return

        self.selectedTXTField.write(key)
        if self.selectedTXTField.getResult() == "":
            self.selectedTXTField.write("0")

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

        self.font = font
        self.fontColor = fontColor

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
