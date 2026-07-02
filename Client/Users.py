
#############
##ADVENTURER#
#############

class Adventurer:
    def __init__(self,name,race,role,hp=0,mana=0,charisma=0,atq=0,money=0,profPic="None"):
        self.name = name
        self.race = race
        self.role = role
        self.HP = hp
        self.Mana = mana
        self.Charisma = charisma
        self.ATQ = atq
        self.Money = money
        self.items = []
        self.profPic = profPic

    #############
    ###GETTERS###
    #############

    def getName(self):
        return self.name
    def getRace(self):
        return self.race
    def getRole(self):
        return self.role
    def getHP(self):
        return self.HP
    def getMana(self):
        return self.Mana
    def getCharisma(self):
        return self.Charisma
    def getATQ(self):
        return self.ATQ
    def getMoney(self):
        return self.Money
    def getProfPic(self):
        return self.profPic
    def getSelf(self):
        s = self.name+"="+self.race+"="+self.role+"="+str(self.HP)+"="+str(self.Mana)+"="+str(self.Charisma)+"="+str(self.ATQ)+"="+str(self.Money)+"="+self.profPic
        return s

    #############
    ###SETTERS###
    #############

    def setHP(self,value):
        self.HP = value
    def setMana(self,value):
        self.Mana = value
    def setCharisma(self,value):
        self.Charisma = value
    def setATQ(self,value):
        self.ATQ = value
    def setMoney(self,value):
        self.Money = value
    def setProcPic(self,value):
        self.profPic = value
    def addMoney(self,value):
        self.Money += value

#############
######DM#####
#############
