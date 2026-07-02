import pygame as pg
import Users as u
import random
import pickle as pkl
import os
from tkinter import filedialog as tkfd

def getCollision(x,y,xs,ys,xc,yc,click=False):
    if(click):
        xc,yc = pg.mouse.get_pos()
    if xc > x and xc < x+xs and yc > y and yc < y+ys:
        return True
    return False

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
    def __init__(self,window,pos,size,font,text,time,speed,Slist,color=(0,0,0),fontColor=(255,255,255)):
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
    def __init__(self,window,pos,size,font,imagePath,color=(0,0,0),fontColor=(255,255,255),evt=-1):
        super().__init__(window,pos,size,font,color,fontColor,pos)
        self.path = imagePath
        self.image = pg.image.load(self.path)#"Images\\sampleUser.png"
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
    def __init__(self,window,pos,size,font,title,types,text,dest,color=(0,0,0),fontColor=(255,255,255)):
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
    def __init__(self,window,pos,size,font,action,text,color=(0,0,0),fontColor=(255,255,255)):
        super().__init__(window,pos,size,font,color,fontColor,(((size[0]/2)-len(text)*6)/2+pos[0],
                                                                            (size[1]/2)-27+pos[1]),
                                                                             True,text)
        self.action = action

    def isClicked(self,x,y):
        if(getCollision(self.pos[0],self.pos[1],self.size[0],self.size[1],x,y)):
            return self.action
        return -1

        
#class TextField():
class TXTField(FieldTool):
    def __init__(self,window,pos,size,font,color=(0,0,0),fontColor=(255,255,255)):
        super().__init__(window,pos,size,font,color,fontColor,(pos[0]+7,(size[1]/2)-27+pos[1]),True)
        self.selected = False
        self.action = (1,2)
        self.allowedChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "

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
        if flag:
            self.selected = True
            return self.action[0]
        elif not flag and self.selected: 
            self.selected = False
            return self.action[1]
        return -1

    def write(self,key):
        if key == '°':
            self.text = self.text[:-1]
        else:
            if(key.upper() in self.allowedChars and len(self.text)<self.size[0]//20):
                self.text += key


#class comboBox
class ComboBox(FieldTool):
    def __init__(self,window,pos,size,font,color=(0,0,0),fontColor=(255,255,255),action=3):
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
    def __init__(self,window,pos,size,font,path,time,speed,Slist,color=(0,0,0),fontColor=(255,255,255),defnum=6):
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
    def __init__(self,window,pos,font,secondFont,imagePath,color=(0,0,0),fontColor=(255,255,255),User="",showed=False):
        super().__init__(window,pos,(110,110),font,color,fontColor,pos)
        self.secondFont = secondFont
        self.path = imagePath
        self.image = pg.image.load(self.path)#"Images\\sampleUser.png"
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
            pg.draw.rect(self.W,self.color,(self.pos[0],self.pos[1],self.size[0]+480,self.size[1]),border_radius=20)

            Text = self.font.render(self.username,True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+120,self.pos[1]+2))

            Text = self.secondFont.render("Race: "+self.User.getRace(),True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+120,self.pos[1]+40))

            Text = self.secondFont.render("Role: "+self.User.getRole(),True,self.fontColor)
            self.W.blit(Text,(self.pos[0]+120,self.pos[1]+65))

            Text = self.secondFont.render("HP: "+str(self.User.getHP()),True,self.fontColor)
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
    
#####################################################################
#///////////////////////////####MENU#####///////////////////////////#
#####################################################################

class Menu:
    def __init__(self,window,WSize):
        self.W = window
        self.WSize = WSize
        self.font = pg.font.Font("dungeon_sn\\DUNGRG__.TTF",48)
        self.creatingChar = False
        self.selectedTXTField = ""
        self.selectedCombo = ""
        self.User = ""
        self.selectedCBox = False
        self.screenItems = []

    def getCreatingChar(self):
        return self.creatingChar

    def changeCreatingChar(self):
        self.cleanScreenItems()
        self.creatingChar = not self.creatingChar
        if self.creatingChar:
            self.startAddChar()
        else:
            self.startLogin()

    def cleanScreenItems(self):
        self.screenItems.clear()

    def getUserByIndex(self,index):
        directory = "chrctrs\\"
        cntnt = os.listdir(directory)
        for f in range(0,len(cntnt)):
            if(os.path.isfile(directory+cntnt[f]) and cntnt[f].endswith(".CHRCTR") and f == index-4):
                #poner perfiles
                with open(directory+cntnt[f],"rb") as u:
                    user = pkl.load(u)
                return user
        
    def getSelectedUser(self):
        return self.User
        
    def startLogin(self):
        self.screenItems.append(BTN(self.W,(515,325),(250,70),self.font,0,"Add Character",(204,204,35)))
        #Iter users
        directory = "chrctrs\\"
        cntnt = os.listdir(directory)
        for f in range(0,len(cntnt)):
            if(os.path.isfile(directory+cntnt[f]) and cntnt[f].endswith(".CHRCTR")):
                #poner perfiles
                with open(directory+cntnt[f],"rb") as u:
                    user = pkl.load(u)
                    self.screenItems.append(BTN(self.W,(515+(f+1)*270,325),(250,70),self.font,f+4,user.getName(),(204,204,35)))

    def startAddChar(self):
        self.screenItems.append(TXTField(self.W,(420,219),(400,50),self.font,(204,204,35),(0,0,0)))
        self.screenItems.append(ComboBox(self.W,(420,319),(400,50),self.font,(204,204,35),(0,0,0)))
        self.screenItems[1].setItems(["Humano","Elfo","Reptil","Celestial","Titan"])
        self.screenItems.append(ComboBox(self.W,(420,419),(400,50),self.font,(204,204,35),(0,0,0)))
        self.screenItems[2].setItems(["Caballero","Explorador","Alquimista","Mago"])
        self.screenItems.append(BTN(self.W,(725,650),(150,50),self.font,0,"Create",(75,0,125)))
        self.screenItems.append(Image(self.W,(400,20),(150,150),self.font,"Images\\sampleUser.png"))
        self.screenItems.append(FileDialog(self.W,(600,120),(170,50),self.font,"Find a profile picture :p",
                                           (("PNG","*.png"),("JPG","*.jpg"),("All Files","*.*")),"Profile Pic",
                                           self.screenItems[-1],(75,0,125)))
        self.screenItems.append(ComboBox(self.W,(780,20),(100,50),self.font,(204,204,35),(0,0,0)))
        self.screenItems[6].setItems(["ADV","DM"])

    def showError(self,txt):
        self.screenItems.append(Dialog(self.W,(self.WSize[0]//2-len(txt)*10-10,self.WSize[1]//2-50),(300,100),self.font,txt,
                                                           25,1,self.screenItems,(100,100,100),(0,0,0)))

    def write(self,key):
        self.selectedTXTField.write(key)

    def verifyFields(self):
        valid = False
        for i in self.screenItems:
            if(type(i)==TXTField and not  i.isEmpty()):
                valid = True

        return valid
    
    def loadLogin(self):
        self.W.fill((75,0,125))

        #render other thngs
        if(self.creatingChar):
            pg.draw.rect(self.W,(204,204,35),(390,10,500,700))

            nameText = self.font.render("Name:",True,(255,255,255))
            self.W.blit(nameText,(420,170))

            nameText = self.font.render("Race:",True,(255,255,255))
            self.W.blit(nameText,(420,270))

            nameText = self.font.render("Role:",True,(255,255,255))
            self.W.blit(nameText,(420,370))

        for i in self.screenItems:
            i.render()

        if(self.selectedCBox):
            self.selectedCombo.showItems()

    def loadConection(self):
        self.W.fill((75,0,125))
        pg.draw.rect(self.W,(204,204,35),(560,335,160,50))
        nameText = self.font.render("Conecting",True,(255,255,255))
        self.W.blit(nameText,(570,333))
        
                               
    def getClickedOnes(self,x,y):
        action = []
        comboClick = False
        goToInterface = False
        
        for i in self.screenItems:
            a = i.isClicked(x,y)
            if(a!=-1):
                if a == 0:
                    if(self.creatingChar):
                        if(self.verifyFields()):
                            #Guardamos personaje
                            name = self.screenItems[0].getResult()
                            race = self.screenItems[1].getResult()
                            role = self.screenItems[2].getResult()
                            pp = self.screenItems[4].getResult()
                            user = u.Adventurer(name,race,role,profPic=pp)
                            
                            with open("chrctrs\\"+name+".CHRCTR","wb") as f:
                                pkl.dump(user,f)

                            self.selectedCBox = False
                            self.changeCreatingChar()
                            return 2
                        else:
                            self.screenItems.append(Dialog(self.W,(self.WSize[0]//2-150,self.WSize[1]//2-50),(300,100),self.font,"Invalid Username",
                                                           15,2,self.screenItems,(100,100,100),(0,0,0)))
                    else:
                        self.changeCreatingChar()
                        return -1

                action.append(a)
                if(self.selectedCBox and self.selectedCombo.collideWItems(x,y)):
                    action = action[:-1]
                else:
                    if(a == 1):
                        self.selectedTXTField = i
                    elif(a == 3):
                        comboClick = True
                        self.selectedCombo = i
                    else:
                        goToInterface = True
                        self.User = self.getUserByIndex(a)

        
        if(self.selectedCBox):
            self.selectedCombo.getItemClick(x,y)
            self.selectedCBox = False

        if comboClick:
            self.selectedCBox = True

        if 1 in action:
            return 1
        elif 2 in action:
            return 2

        if goToInterface:
            return 3
            
        return -1

#####################################################################
#////////////////////////#####Interface#####////////////////////////#
#####################################################################
    
class Interface:
    def __init__(self,window,WSize):
        self.W = window
        self.WSize = WSize
        self.font = pg.font.Font("dungeon_sn\\DUNGRG__.TTF",48)
        self.Sfont = pg.font.Font("dungeon_sn\\DUNGRG__.TTF",30)
        self.selectedTXTField = ""
        self.selectedCombo = ""
        self.selectedCBox = False
        self.conected = True
        self.diceCooldown = 0
        self.User = ""
        self.Users = {}
        self.msgs = []
        self.screenItems = []
        self.banner = ""
        self.banners = []

    def setUser(self,user):
        self.User = user
        self.banner = UserBanner(self.W,(15,15),self.font,self.Sfont,user.getProfPic(),(0,0,0),(255,255,255),user)

    def changeConected(self):
        self.conected = not self.conected

    def getUser(self):
        return self.User

    def getConected(self):
        return self.conected
    
    def startGame(self):
        #DICE
        self.screenItems.append(BTN(self.W,(895,430),(50,50),self.font,4,"  4",(204,204,35)))
        self.screenItems.append(BTN(self.W,(955,430),(50,50),self.font,6,"  6",(204,204,35)))
        self.screenItems.append(BTN(self.W,(1015,430),(50,50),self.font,8,"  8",(204,204,35)))
        self.screenItems.append(BTN(self.W,(1075,430),(50,50),self.font,10,"  10",(204,204,35)))
        self.screenItems.append(BTN(self.W,(1135,430),(50,50),self.font,12,"  12",(204,204,35)))
        self.screenItems.append(BTN(self.W,(1195,430),(50,50),self.font,20,"  20",(204,204,35)))
        #Texting
        self.screenItems.append(TXTField(self.W,(170,430),(600,50),self.font,(204,204,204),(0,0,0)))
        self.selectedTXTField = self.screenItems[6]
        self.screenItems.append(ComboBox(self.W,(170,500),(200,50),self.font,(204,204,204),(0,0,0)))
        self.screenItems[7].setItems(["ALL"])
        

    def write(self,key):
        self.selectedTXTField.write(key)

    def sendMessage(self):
        msg = self.selectedTXTField.getResult()
        rcptr = self.screenItems[7].getResult()
        me = self.User.getName()
        empty = self.selectedTXTField.isEmpty()
        self.selectedTXTField.clean()
        if empty:
            return ""
        self.msgs.append("me|"+msg)
        return rcptr+"|"+me+"|"+msg

    def connectUser(self,u):
        user = u.split("&")
        if user[0] != self.User.getName() and user[0] not in self.Users.keys():
            self.screenItems[7].appendItem(user[0])
            return 1,user[0]
        return 0,""

    def disconnectUser(self,u):
        user = u.split("-")
        self.screenItems[7].removeItem(user[0])
        del self.Users[user[0]]
        ub = ""
        for i in self.banners:
            if(user[0] == i.getUsername()):
               ub = i
        if ub!="":
            self.banners.remove(ub)
        
    def appendMSG(self,msg):
        self.msgs.append(msg)

    def appendADV(self,adv):
        Adv = adv.split("=")
        nADV = u.Adventurer(Adv[0],Adv[1],Adv[2],Adv[3],Adv[4],Adv[5],
                            Adv[6],Adv[7],Adv[8])
        self.Users[Adv[0]] = nADV
        self.banners.append(UserBanner(self.W,(15,len(self.banners)*150+135),self.font,self.Sfont,Adv[8],(255,255,255),(0,0,0),nADV))

    def throwDice(self,message,flag=False):
        self.diceCooldown = 50
        parts = message.split('|')
        dice = parts[1].split('#')
        num = int(dice[1])
        rang = int(dice[0])
        if not flag:
            self.screenItems.append(Dialog(self.W,(920,15),(300,50),self.font,parts[0],
                                                           50,0,self.screenItems,(100,100,100),(0,0,0)))
        self.screenItems.append(Dice(self.W,(1030,150),(80,80),self.font,"Images\\Dice.jpg",20,1,self.screenItems,(100,100,100),(255,44,0),num))

    def loadMSGS(self):
        lenin = len(self.msgs)-1
        yPos = 360
        for m in range(lenin,max(-1,lenin-6),-1):
            parts = self.msgs[m].split("|")
            Text = self.font.render(self.msgs[m],True,(0,0,0))
            if(parts[0] == "me"):
                self.W.blit(Text,(770-len(self.msgs[m])*15-10,yPos))
            else:
                self.W.blit(Text,(173,yPos))
            yPos-=50
        
    def loadGame(self):
        self.W.fill((75,0,125))

        #Dice zone
        pg.draw.rect(self.W,(204,204,35),(870,10,400,400),border_radius=20)
        #TextArea
        pg.draw.rect(self.W,(204,204,204),(170,110,600,300),border_radius=20)
        
        for i in self.screenItems:
            i.render()

        if self.diceCooldown > 0:
            self.diceCooldown -= 1

        if(self.selectedCBox):
            self.selectedCombo.showItems()

        self.loadMSGS()

        self.banner.render((15,15))
        for i in range(0,len(self.banners)):
            self.banners[i].render((15,i*120+135))

    def getClickedOnes(self,x,y):
        action = []
        dice = [4,6,8,10,12,20]
        comboClick = False
        goToInterface = False
        
        for i in self.screenItems:
            a = i.isClicked(x,y)
            action.append(a)
            if(a!=-1):
                if(self.selectedCBox and self.selectedCombo.collideWItems(x,y)):
                    action = action[:-1]
                else:
                    if(a == 1):
                        self.selectedTXTField = i
                    elif(a == 3):
                        comboClick = True
                        self.selectedCombo = i
                        
                    if a in dice:
                        if(self.diceCooldown == 0):
                            return a

        if(self.selectedCBox):
            self.selectedCombo.getItemClick(x,y)
            self.selectedCBox = False

        if comboClick:
            self.selectedCBox = True


        if 1 in action:
            return 1
        elif 2 in action:
            return 2
    
        return -1
        
