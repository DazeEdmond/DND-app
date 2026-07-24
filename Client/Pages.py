import pygame as pg
import Users as u
import random
import pickle as pkl
import os
import shutil
from Utilities import BTN,Dialog,Image,FileDialog,TXTField,ComboBox,Dice,UserBanner,DMUserBanner,Enemy
from Utilities import Green,Red,White,Black,LightGray,Gray,Yellow
from Users import DM

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
        self.UserLen = 0
        self.UsersOffset = 0
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
        self.screenItems.append(BTN(self.W,(515,325),(250,70),self.font,0,"Add Character",Yellow))
        #Iter users
        directory = "chrctrs\\"
        cntnt = os.listdir(directory)
        self.UserLen = len(cntnt)
        for f in range(0,len(cntnt)):
            if(os.path.isfile(directory+cntnt[f]) and cntnt[f].endswith(".CHRCTR")):
                #poner perfiles
                with open(directory+cntnt[f],"rb") as u:
                    user = pkl.load(u)
                    self.screenItems.append(BTN(self.W,(515+(f+1)*270,325),(250,70),self.font,f+4,user.getName(),Yellow))

    def startAddChar(self):
        self.screenItems.append(TXTField(self.W,(420,219),(400,50),self.font,Yellow,Black))
        self.screenItems.append(ComboBox(self.W,(420,319),(400,50),self.font,Yellow,Black))
        self.screenItems[1].setItems(["Humano","Elfo","Reptil","Celestial","Titan"])
        self.screenItems.append(ComboBox(self.W,(420,419),(400,50),self.font,Yellow,Black))
        self.screenItems[2].setItems(["Caballero","Explorador","Alquimista","Mago"])
        self.screenItems.append(BTN(self.W,(725,650),(150,50),self.font,0,"Create",(75,0,125)))
        self.screenItems.append(Image(self.W,(400,20),(150,150),self.font,"Images\\sampleUser.png"))
        self.screenItems.append(FileDialog(self.W,(600,120),(170,50),self.font,"Find a profile picture :p",
                                           (("PNG","*.png"),("JPG","*.jpg"),("All Files","*.*")),"Profile Pic",
                                           self.screenItems[-1],(75,0,125)))
        self.screenItems.append(ComboBox(self.W,(780,20),(100,50),self.font,Yellow,Black))
        self.screenItems[6].setItems(["ADV","DM"])
        self.screenItems.append(BTN(self.W,(570,650),(150,50),self.font,17,"Back",(75,0,125)))

    def showError(self,txt):
        self.screenItems.append(Dialog(self.W,(self.WSize[0]//2-len(txt)*10-10,self.WSize[1]//2-50),(300,100),self.font,txt,
                                                           25,1,self.screenItems,Gray,Black))

    def write(self,key):
        self.selectedTXTField.write(key)

    def verifyFields(self):
        valid = False
        for i in self.screenItems:
            if(type(i)==TXTField and not  i.isEmpty()):
                valid = True

        return valid
    
    def loadLogin(self):
        self.W.fill(Black)

        image = pg.image.load("Images/MainBackground.png")#"Images\\sampleUser.png"
        image = pg.transform.scale(image,(1280,720))
        self.W.blit(image,(0,0))

        #render other thngs
        if(self.creatingChar):
            pg.draw.rect(self.W,Yellow,(390,10,500,700))

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
        pg.draw.rect(self.W,Yellow,(560,335,160,50))
        nameText = self.font.render("Conecting",True,(255,255,255))
        self.W.blit(nameText,(570,333))
        
    def moveUsers(self,direction):
        offset = 0
        change = True
        if direction == 'R':
            offset = -270
            if self.UsersOffset <= self.UserLen-1:
                self.UsersOffset += 1
            else: 
                change = False
        else:
            offset = 270
            if self.UsersOffset > 0:
                self.UsersOffset -= 1
            else: 
                change = False

        if change:
            for i in self.screenItems:
                if(type(i) == BTN and not self.creatingChar):
                    i.pos = (i.pos[0]+offset,i.pos[1])
                    i.centerText()
                               
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
                            if(name == "DM"):
                                continue
                            race = self.screenItems[1].getResult()
                            role = self.screenItems[2].getResult()
                            pp = self.screenItems[4].getResult()
                            fname,ext = os.path.splitext(pp)
                            if(pp != "Images\\sampleUser.png"):
                                npp = "chrctrImages/"+name+"PFP"+ext
                                try:
                                    shutil.copy(pp,npp)
                                except Exception as e:
                                    print("Already in")
                            else:
                                npp = pp
                            if(ext == ".jpg" or ext == ".png"):
                                if(self.screenItems[6].getResult()=="ADV"):
                                    user = u.Adventurer(name,race,role,profPic=npp)
                                else:
                                    user = DM(name,race,role,profPic=npp)

                                with open("chrctrs\\"+name+".CHRCTR","wb") as f:
                                    pkl.dump(user,f)

                                self.selectedCBox = False
                                self.changeCreatingChar()
                            return 2
                        else:
                            self.screenItems.append(Dialog(self.W,(self.WSize[0]//2-150,self.WSize[1]//2-50),(300,100),self.font,"Invalid Username",
                                                           15,2,self.screenItems,Gray,Black))
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
                    elif(a == 17):
                        self.changeCreatingChar()
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
        self.Enemy = []
        self.banner = ""
        self.banners = []
        self.selectedBanner = ""
        self.DMUI = False
        self.msgFieldSelected = False
        self.Turn = False
        self.mode = ""

    def setDMUI(self,flag):
        self.DMUI = flag

    def setUser(self,user):
        self.User = user
        if type(user) == DM:
            self.banner = DMUserBanner(self.W,(15,15),self.font,self.Sfont,user.getProfPic(),Black,(255,255,255),user)
        else:
            self.banner = UserBanner(self.W,(15,15),self.font,self.Sfont,user.getProfPic(),Black,(255,255,255),user)


    def changeConected(self):
        self.conected = not self.conected

    def getUser(self):
        return self.User

    def playersIn(self):
        return self.banners != []

    def getConected(self):
        return self.conected

    def getMsgFieldSelected(self):
        return self.msgFieldSelected
    
    def getMode(self):
        return self.mode

    def onBattle(self):
        return self.Enemy != []
    
    def startGame(self):
        #DICE
        self.screenItems.append(BTN(self.W,(895,430),(50,50),self.font,4,"4",Yellow,enabled=False))
        self.screenItems.append(BTN(self.W,(955,430),(50,50),self.font,6,"6",Yellow,enabled=False))
        self.screenItems.append(BTN(self.W,(1015,430),(50,50),self.font,8,"8",Yellow,enabled=False))
        self.screenItems.append(BTN(self.W,(1075,430),(50,50),self.font,10,"10",Yellow,enabled=False))
        self.screenItems.append(BTN(self.W,(1135,430),(50,50),self.font,12,"12",Yellow,enabled=False))
        self.screenItems.append(BTN(self.W,(1195,430),(50,50),self.font,20,"20",Yellow,enabled=False))
        #Texting
        self.screenItems.append(TXTField(self.W,(170,320),(600,50),self.font,White,Black))
        self.selectedTXTField = self.screenItems[6]
        self.screenItems.append(ComboBox(self.W,(170,380),(200,50),self.font,White,Black))
        self.screenItems[7].setItems(["ALL"])
        self.screenItems.append(BTN(self.W,(870,500),(400,50),self.font,60,"Attack",Red,enabled=False))
        self.screenItems.append(BTN(self.W,(870,560),(400,50),self.font,61,"Action",Yellow,enabled=False))
        
    def setDMUIInterface(self):
        self.screenItems.clear()
        self.screenItems.append(TXTField(self.W,(170,320),(600,50),self.font,White,Black))
        self.selectedTXTField = self.screenItems[0]
        self.screenItems.append(ComboBox(self.W,(170,380),(200,50),self.font,White,Black))
        self.screenItems[1].setItems(["ALL"])
        self.screenItems.append(Image(self.W,(170,470),(120,120),self.font,"Images\\sampleUser.png"))#item 2
        self.screenItems.append(FileDialog(self.W,(170,600),(120,45),self.font,"Find a picture :p",
                                           (("PNG","*.png"),("JPG","*.jpg"),("All Files","*.*")),"Profile",
                                           self.screenItems[-1],(224,224,35)))#item3
        self.screenItems.append(TXTField(self.W,(405,465),(200,45),self.font,White,Black))#item 4
        self.screenItems.append(TXTField(self.W,(405,510),(200,45),self.font,White,Black,AC="1234567890"))#item 5
        self.screenItems.append(TXTField(self.W,(405,555),(200,45),self.font,White,Black,AC="1234567890"))#item 6
        self.screenItems.append(TXTField(self.W,(405,600),(200,45),self.font,White,Black,canWrite=False))#item 7
        self.screenItems.append(FileDialog(self.W,(295,600),(115,45),self.font,"Find a theme",
                                           (("All","*.*"),("mp3","*.mp3")),"Theme",
                                           self.screenItems[-1],(224,224,35)))#item 8
        self.screenItems.append(BTN(self.W,(615,465),(155,55),self.font,31,"Send",Green))#item 9
        self.screenItems.append(BTN(self.W,(615,527),(155,55),self.font,32,"Stop",Red))#item 10
        self.screenItems.append(BTN(self.W,(615,589),(155,55),self.font,33,"Clear",LightGray))#item 11

        self.screenItems.append(TXTField(self.W,(970,420),(300,45),self.font,White,Black,canWrite=False))#item 12
        self.screenItems.append(FileDialog(self.W,(870,420),(95,45),self.font,"Find Music",
                                           (("All","*.*"),("mp3","*.mp3")),"Music",
                                           self.screenItems[-1],(224,224,35)))#item 13
        self.screenItems.append(BTN(self.W,(870,475),(400,40),self.font,41,"Play",Green))#item 14
        self.screenItems.append(BTN(self.W,(870,520),(400,40),self.font,42,"Stop",Red))#item 15
        self.screenItems.append(TXTField(self.W,(970,570),(300,45),self.font,White,Black,canWrite=False))#item 16
        self.screenItems.append(FileDialog(self.W,(870,570),(95,45),self.font,"Find Sound",
                                           (("All","*.*"),("mp3","*.mp3")),"Sound",
                                           self.screenItems[-1],(224,224,35)))#item 17
        self.screenItems.append(BTN(self.W,(870,625),(400,40),self.font,43,"Play",Green))#item 18
        self.screenItems.append(BTN(self.W,(870,670),(400,40),self.font,44,"Clear",LightGray))#item 19
        self.screenItems.append(TXTField(self.W,(775,55),(90,45),self.font,White,Black,AC="1234567890"))#item 20
        self.screenItems.append(BTN(self.W,(775,105),(90,40),self.font,34,"DMG",Green))#item 21
        self.screenItems.append(TXTField(self.W,(775,180),(90,45),self.font,White,Black,AC="1234567890"))#item 22
        self.screenItems.append(BTN(self.W,(775,230),(90,40),self.font,35,"Heal",Green))#item 23
        self.screenItems.append(BTN(self.W,(315,380),(100,50),self.font,36,"Attack",Red))#item 24
        self.screenItems.append(BTN(self.W,(170,650),(250,50),self.font,37,"Send enemy Files",Yellow))#item 24
        self.screenItems.append(BTN(self.W,(430,650),(250,50),self.font,38,"Send sound Files",Yellow))#item 24

    def write(self,key):
        self.selectedTXTField.write(key)

    def sendMessage(self):
        UsersTXTBI = 7
        if(self.DMUI):
            UsersTXTBI = 1

        msg = self.selectedTXTField.getResult()
        rcptr = self.screenItems[UsersTXTBI].getResult()
                
        me = self.User.getName()
        empty = self.selectedTXTField.isEmpty()
        self.selectedTXTField.clean()
        if empty:
            return ""
        self.msgs.append("me|"+msg)
        return rcptr+"|"+me+"|"+msg

    def setTurn(self,flag):
        self.Turn = flag
        self.enableDices(False)
        self.screenItems[8].enable(flag)
        self.screenItems[9].enable(flag)
        self.mode = ""

    def enableDices(self,flag):
        self.screenItems[0].enable(flag)
        self.screenItems[1].enable(flag)
        self.screenItems[2].enable(flag)
        self.screenItems[3].enable(flag)
        self.screenItems[4].enable(flag)
        self.screenItems[5].enable(flag)

    def enableAttackDice(self):
        role = self.User.getRole()
        self.enableDices(False)
        if(role == "Caballero"):
            self.screenItems[5].enable(True)
        if(role == "Explorador"):
            self.screenItems[2].enable(True)
        if(role == "Alquimista"):
            self.screenItems[3].enable(True)
        if(role == "Mago"):
            self.screenItems[4].enable(True)
    #ALL|DM|Action-Value
    def sendSound(self):
        audio = self.screenItems[16].getResult()
        if (audio != ""):
            return "ALL|DM|sound-"+audio
        else:
            return ""

    def sendMusic(self):
        audio = self.screenItems[12].getResult()
        if (audio != ""):
            return "ALL|DM|music-"+audio
        else:
            return ""
    def sendMusicStop(self):
        return "ALL|DM|musicS-"

    def sendCharge(self):
        if self.selectedBanner == "":
            return
        return "ALL|DM|charge-"+self.selectedBanner.getUsername()+"$"+str(self.selectedBanner.getAmount())

    def sendChange(self):
        if self.selectedBanner == "":
            return
        return "ALL|DM|change-"+self.selectedBanner.getResult()

    def sendTurn(self):
        if self.selectedBanner == "":
            return
        return "ALL|DM|turn-"+self.selectedBanner.getUsername()

    def sendEnemy(self):
        name = self.screenItems[4].getResult()
        hp = self.screenItems[5].getResult()
        atq = self.screenItems[6].getResult()
        pfp = self.screenItems[2].getResult()
        theme = self.screenItems[7].getResult()
        return "ALL|DM|enemy-"+name+"$"+hp+"$"+atq+"$"+pfp+"$"+theme

    def sendEnemyS(self):
        return "ALL|DM|enemyS-"

    def sendEnemyAttack(self):
        return "ALL|DM|enemyDMG-"+self.screenItems[20].getResult()

    def sendEnemyHeal(self):
        return "ALL|DM|enemyHeal-"+self.screenItems[22].getResult()

    def sendEnemyFiles(self):
        files = []
        if self.screenItems[2].getResult() != "Images\\sampleUser.png":
            files.append(self.screenItems[2].getResult())
        files.append(self.screenItems[7].getResult())
        return files

    def sendSoundFiles(self):
        files = []
        if self.screenItems[12].getResult() != "":
            files.append(self.screenItems[12].getResult())
        if self.screenItems[16].getResult() != "":
            files.append(self.screenItems[16].getResult())
        return files
        
    def sendUserDMG(self):
        return "ALL|DM|usrDMG-"+self.screenItems[1].getResult()+"$"+str(self.Enemy[0].getAtq())

    def chargeUser(self,charge):
        num = 0
        if("_" in charge[1]):
            num = -1*int(charge[1].replace("_",""))
        else:
            num = int(charge[1])

        if(self.User.getName() == charge[0]):
            self.User.setMoney(int(self.User.getMoney())+num)
            with open("chrctrs\\"+charge[0]+".CHRCTR","wb") as f:
                pkl.dump(self.User,f)
        else:
            user = self.Users[charge[0]]
            user.setMoney(int(user.getMoney())+num)

    def changeUser(self,change):
        if(self.User.getName() == change[0]):
            self.User.setHP(int(change[1]))
            self.User.setTotalHP(int(change[2]))
            self.User.setATQ(int(change[3]))
            self.User.setMana(int(change[4]))
            self.User.setCharisma(int(change[5]))
            with open("chrctrs\\"+change[0]+".CHRCTR","wb") as f:
                pkl.dump(self.User,f)
            if(self.DMUI):
                self.banner.updateUser()
        else:
            user = self.Users[change[0]]
            user.setHP(int(change[1]))
            user.setTotalHP(int(change[2]))
            user.setATQ(int(change[3]))
            user.setMana(int(change[4]))
            user.setCharisma(int(change[5]))
            if(self.DMUI):
                for i in self.banners:
                    if(i.getUsername() == change[0]):
                        i.updateUser()

    def spawnEnemy(self,pos,size,name,HP,ATQ,pfp,theme):
        self.Enemy.append(Enemy(self.W,pos,size,self.font,(240,240,240),name,HP,ATQ,pfp,theme,self.screenItems,self.Enemy))
        self.playMusic(theme)

    def escapeEnemy(self):
        self.screenItems.append(Dialog(self.W,(920,50),(300,50),self.font,"Enemy escaped",
                                                           50,2,self.screenItems,Gray,Black))
        self.Enemy.clear()
        self.stopMusic()

    def DMGEnemy(self,dmg):
        if(self.Enemy == []):
            return
        self.Enemy[0].attack(int(dmg))
        self.screenItems.append(Dialog(self.W,(920,50),(300,50),self.font,"Damage -"+str(dmg),
                                                           50,3,self.screenItems,Red,Black))
        if(self.Enemy[0].getHP() <= 0):
            self.stopMusic()

    def healEnemy(self,heal):
        self.Enemy[0].heal(int(heal))
        self.screenItems.append(Dialog(self.W,(920,50),(300,50),self.font,"Heal +"+heal,
                                                           50,3,self.screenItems,Green,Black))

    def reciveDamage(self,dest,dmg):
        self.screenItems.append(Dialog(self.W,(self.WSize[0]//2-299,self.WSize[1]//2-50),(300,50),self.font,dest+" -"+str(dmg),
                                                           50,3,self.screenItems,Red,Black))

        if((not self.DMUI) and (self.User.getName() == dest or dest == "ALL")):
            self.User.reciveDMG(int(dmg))
            with open("chrctrs\\"+self.User.getName()+".CHRCTR","wb") as f:
                pkl.dump(self.User,f)
            if(self.DMUI):
                self.banner.updateUser()
            
            if self.User.getName() == dest:
                return
            
        for k in self.Users.keys():
            user = self.Users[k]
            user.reciveDMG(int(dmg))

        if(self.DMUI):
            for i in self.banners:
                i.updateUser()


    def playSound(self,sound):
        try:
            Sound = pg.mixer.Sound(sound)
            Sound.set_volume(0.3)
            Sound.play()
        except Exception as e:
            self.screenItems.append(Dialog(self.W,(self.WSize[0]//2-299,self.WSize[1]//2-50),(300,50),"Sound not found",
                                                           50,3,self.screenItems,Red,Black))

    def playMusic(self,music):
        try:
            pg.mixer.music.load(music)
            pg.mixer.music.play(-1)
        except Exception as e:
            self.screenItems.append(Dialog(self.W,(self.WSize[0]//2-299,self.WSize[1]//2-50),(300,50),"Music not found",
                                                           50,3,self.screenItems,Red,Black))

    def stopMusic(self):
        pg.mixer.music.stop()

    def connectUser(self,u):
        UsersTXTBI = 7
        if(type(self.User) == DM):
            UsersTXTBI = 1

        user = u.split("&")
        if user[0] != self.User.getName() and user[0] not in self.Users.keys():
            self.screenItems[UsersTXTBI].appendItem(user[0])
            return 1,user[0]
        return 0,""

    def disconnectUser(self,u):
        UsersTXTBI = 7
        if(self.DMUI):
            UsersTXTBI = 1

        user = u.split("-")
        self.screenItems[UsersTXTBI].removeItem(user[0])
        del self.Users[user[0]]
        ub = ""
        for i in self.banners:
            if(user[0] == i.getUsername()):
               ub = i
        if ub!="":
            self.banners.remove(ub)

    def verifyEnemyFields(self):
        flag = True
        if(self.screenItems[2].getResult() == ""):
            flag = False
        if(self.screenItems[4].getResult() == ""):
            flag = False
        if(self.screenItems[6].getResult() == ""):
            flag = False
        if(self.screenItems[7].getResult() == ""):
            flag = False
        return flag
        
    def appendMSG(self,msg):
        self.msgs.append(msg)

    def appendADV(self,adv):
        Adv = adv.split("=")
        nADV = u.Adventurer(Adv[0],Adv[1],Adv[2],Adv[3],Adv[4],Adv[5],
                            Adv[6],Adv[7],Adv[8])
        self.Users[Adv[0]] = nADV

        if type(self.User) == DM:
            self.banners.append(DMUserBanner(self.W,(15,len(self.banners)*150+135),self.font,self.Sfont,Adv[8],(255,255,255),Black,nADV))
        else:
            self.banners.append(UserBanner(self.W,(15,len(self.banners)*150+135),self.font,self.Sfont,Adv[8],(255,255,255),Black,nADV))

    def throwDice(self,message,flag=False):
        self.diceCooldown = 50
        parts = message.split('|')
        dice = parts[1].split('#')
        num = int(dice[1])
        rang = int(dice[0])
        
        if not flag:
            self.screenItems.append(Dialog(self.W,(920,15),(300,50),self.font,parts[0],
                                                           50,0,self.screenItems,Gray,Black))

        if(not self.DMUI):
            self.setTurn(False)

        if(dice[2] == "Attack"):
            if(int(dice[3])==1):
                self.screenItems.append(Dialog(self.W,(1030,150),(300,50),self.font,"Missed",
                                                           50,3,self.screenItems,LightGray,Black))
                return
            else:
                self.DMGEnemy(num+int(dice[3]))

        self.screenItems.append(Dice(self.W,(1030,150),(80,80),self.font,"Images\\Dice.jpg",30,1,self.screenItems,Gray,(255,44,0),num))

    def loadMSGS(self):
        lenin = len(self.msgs)-1
        yPos = 260
        for m in range(lenin,max(-1,lenin-6),-1):
            parts = self.msgs[m].split("|")
            Text = self.font.render(self.msgs[m],True,Black)
            if(parts[0] == "me"):
                self.W.blit(Text,(765-Text.get_width(),yPos))
            else:
                self.W.blit(Text,(173,yPos))
            yPos-=50
        
    def loadGame(self):
        self.W.fill((75,0,125))

        #Dice zone
        pg.draw.rect(self.W,Yellow,(870,10,400,400),border_radius=20)
        #TextArea
        pg.draw.rect(self.W,White,(170,10,600,300),border_radius=20)
        
        if(self.Enemy != []):
            self.Enemy[0].render()

        for i in self.screenItems:
            i.render()

        self.loadMSGS()

        if(not self.DMUI):
            if self.diceCooldown > 0:
                self.diceCooldown -= 1

        else:
            battleText = self.font.render("Battle",True,(255,255,255))
            self.W.blit(battleText,(170,430))
            nameText = self.font.render("Name:",True,(255,255,255))
            self.W.blit(nameText,(295,460))
            hpText = self.font.render("HP:",True,(255,255,255))
            self.W.blit(hpText,(295,505))
            ATQText = self.font.render("ATQ:",True,(255,255,255))
            self.W.blit(ATQText,(295,550))
            DMGText = self.font.render("DMG",True,(255,255,255))
            self.W.blit(DMGText,(780,10))
            HealText = self.font.render("Heal",True,(255,255,255))
            self.W.blit(HealText,(785,140))

        if(self.selectedCBox):
            self.selectedCombo.showItems()

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
                        self.msgFieldSelected = True
                        self.selectedTXTField = i
                    elif(a == 3):
                        comboClick = True
                        self.selectedCombo = i
                        
                    if a in dice:
                        if(self.diceCooldown == 0):
                            return a
        if(self.DMUI):
            action.append(self.banner.isClicked(x,y))
            if action[-1] == 1:
                self.msgFieldSelected = False
                self.selectedTXTField = self.banner
            if action[-1] != -1:
                self.selectedBanner = self.banner
            for i in self.banners:
                a = i.isClicked(x,y)
                action.append(a)
                if a == 1:
                    self.msgFieldSelected = False
                    self.selectedTXTField = i
                if a != -1:
                    self.selectedBanner = i

        if(self.selectedCBox):
            self.selectedCombo.getItemClick(x,y)
            self.selectedCBox = False

        if comboClick:
            self.selectedCBox = True

        if 31 in action:
            if (self.verifyEnemyFields() and self.Enemy == []):
                return 31

        if 32 in action and self.Enemy != []:
            return 32
            
        if 33 in action:
            self.screenItems[2].setPath("Images\\sampleUser.png")
            self.screenItems[4].setPath("")
            self.screenItems[5].setPath("")
            self.screenItems[6].setPath("")
            self.screenItems[7].setPath("")

        if 34 in action and self.screenItems[20].getResult() != "" and self.Enemy != []:
            return 34
        
        if 35 in action and self.screenItems[22].getResult() != "" and self.Enemy != []:
            return 35

        if 36 in action and self.Enemy != []:
            return 36
        
        if 37 in action and self.verifyEnemyFields():
            imagePath = self.screenItems[2].getResult()
            themePath = self.screenItems[7].getResult()
            
            if(imagePath != "Images\\sampleUser.png"):
                fname,ext = os.path.splitext(imagePath)
                dest = "sessionFiles/images/"+self.screenItems[4].getResult()+"PFP"+ext
                try:
                    shutil.copy(imagePath,dest)
                except Exception as e:
                    print("Already in")
                self.screenItems[2].setPath(dest)

            fname,ext = os.path.splitext(themePath)

            dest = "sessionFiles/music/"+self.screenItems[4].getResult()+"Theme"+ext
            try:
                shutil.copy(themePath,dest)
            except Exception as e:
                    print("Already in")
            self.screenItems[7].setPath(dest)
            return 37

        if 38 in action:
            musicPath = self.screenItems[12].getResult()
            soundPath = self.screenItems[16].getResult()
            if musicPath != "":
                fname,ext = os.path.splitext(musicPath)
                name = os.path.basename(fname)
                dest = "sessionFiles/music/"+name+ext
                try:
                    shutil.copy(musicPath,dest)
                except Exception as e:
                    print("Already in")
                self.screenItems[12].setPath(dest)
                
            if soundPath != "":
                fname,ext = os.path.splitext(soundPath)
                name = os.path.basename(fname)
                dest = "sessionFiles/sound/"+name+ext
                try:
                    shutil.copy(soundPath,dest)
                except Exception as e:
                    print("Already in")
                self.screenItems[16].setPath(dest)

            return 38
        
        if 41 in action:
            return 41

        if 42 in action:
            return 42

        if 43 in action:
            return 43

        if 44 in action:
            self.screenItems[12].setPath("")
            self.screenItems[16].setPath("")

        if 51 in action:
            return 51
        
        if 52 in action:
            return 52

        if 60 in action:
            self.mode = "Attack"
            self.enableAttackDice()

        if 61 in action:
            self.mode = "Action"
            self.enableDices(True)
        
        if 62 in action:
            return 62

        if 1 in action:
            return 1
        elif 2 in action:
            self.selectedTXTField = ""
            return 2
    
        return -1