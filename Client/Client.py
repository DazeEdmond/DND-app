import socket as s
import threading as t
from random import randint
import os
import struct
import pygame as pg
import pickle as pkl
from Pages import Menu
from Pages import Interface

#############
####GLOBAL###
#############

###########
########
####

Host = "192.168.100.26"
Port = 5000
Username = ""
Client = ""


####
########
###########


#############
##CONECTION##
#############

def startConection(interface):
    """
    start a conection with the server, if the conection fails
    return false
    if it works first send the username
    and start two threads
    one to hear
    other to send
    """
    global Client
    Client = s.socket(s.AF_INET,s.SOCK_STREAM)
    flag = True
    try:
        Client.connect((Host,Port))
        print("conected")
        print(Username)
        Client.sendall(struct.pack("<H",len(Username)))
        Client.sendall(Username.encode("utf-8"))
    except Exception as e:
        print(e)
        print("unable to create a conection")
        Client.close()
        flag = False
    if(flag):
        receiveThread = t.Thread(target=reciveMessages,args=(interface,))
        receiveThread.start()

        #sendThread = t.Thread(target=sendMessages)
        #sendThread.start()
    return flag
    
def reciveMessages(interface):
    """
    Recive the length of the message to know how much to recive
    recive the message with the info of who sent it
    """
    while True:
        try:
            messageLen = struct.unpack("<H",Client.recv(2))[0]
            message = Client.recv(messageLen).decode("utf-8")
            print(f"{message}")
            parts = message.split('|')
            if(parts[0] == "server"):
                if '&' in parts[1]:
                    flag,u = interface.connectUser(parts[1])
                    send("server|server|"+u+"+"+str(flag))
                elif '-' in parts[1]:
                    interface.disconnectUser(parts[1])
                elif "=" in parts[1]:
                    interface.appendADV(parts[1])
                elif "getADV" in parts[1]:
                    adv = interface.getUser()
                    send(parts[1].split(",")[1]+"|server|"+adv.getSelf())
                elif parts[1]=="Invalid Username":
                    interface.changeConected()
            elif '#' in parts[1]:
                interface.throwDice(message)
            else:
                interface.appendMSG(message)
            #if(message.split('|')[1] == "SeNDFiLe"):
            #    print("recived File")
            #    reciveFile()

        except ConnectionAbortedError:
            print("disconected")
            Client.close()
            break
        except Exception as e:
            print(e)
            print("\nDisconected from server in recive Message")
            Client.close()
            break
'''
def sendMessages():
    """
    send a message to the server with the info of
    who should recive the message
    who sent it
    and the message
    """
    while True:
        try:
            message = input("Write: ")
            if(message == "file"):
                sendFile("pblock.jpg")
            else:
                Client.sendall(struct.pack("<H",len(message)))
                Client.sendall(message.encode("utf-8"))
        except Exception as e:
            print(e)
            print("\nDisconected from server in send Message")
            Client.close()
            break
'''
def send(msg):
    """
    send a message to the server with the info of
    who should recive the message
    who sent it
    and the message
    """
    try:
        Client.sendall(struct.pack("<H",len(msg)))
        Client.sendall(msg.encode("utf-8"))
    except Exception as e:
        print(e)
        print("\nDisconected from server in send Message")
        Client.close()


def sendFile(Filename):
    """
    send a code to the server that describe to who should be
    send the file with a code that means how should be trated the file
    read the bytes of the file
    """
    filesize = os.path.getsize(Filename)
    try:
        filemess = "AtunValido2|AtunValido|SeNDFiLe"
        Client.sendall(struct.pack("<H",len(filemess)))
        Client.sendall(filemess.encode("utf-8"))
        
        Client.sendall(struct.pack("<H",len("Prueba.jpg")))
        Client.sendall("Prueba.jpg".encode("utf-8"))
        Client.sendall(struct.pack("<Q",filesize))
        
        with open(Filename,"rb") as f:
            while line := f.read(1024):
                Client.sendall(line)
        
    except Exception as e:
        print(e)

#############
####FILE#####
#############

def getFileSize(Client):
    """
    This Func get the size of the file to know
    how much Bytes the user should recive
    return the size of the file as INT
    """
    try:
        expectedBytes = struct.calcsize("<Q")
        recivedBytes = 0
        stream = bytes()
        while recivedBytes < expectedBytes:
            chunk = Client.recv(expectedBytes-recivedBytes)
            stream += chunk
            recivedBytes += len(chunk)
        filesize = struct.unpack("<Q",stream)[0]
        return filesize
    except Exception as e:
        print("Exception in recive FileSize: ")
        print(e)
        return 0

def reciveFile():
    """
    Get the filename with the route and save the recived bytes
    in the route descripted before
    get chunks of 1024 bytes until the filesize
    """
    try:
        nameSize = struct.unpack("<H",Client.recv(2))[0]
        Filename = Client.recv(nameSize).decode("utf-8")
        print("File = ",Filename)
        FileSize = getFileSize(Client)
        print("FileSize = ",FileSize)
        with open(Filename,"wb") as f:
            receivedBytes = 0
            while receivedBytes < FileSize:
                chunk = Client.recv(1024)
                if(chunk):
                    f.write(chunk)
                    receivedBytes += len(chunk)
    except Exception as e:
        print("Exception in recive File: ")
        print(e)

        
#startConection()

#############
####PYGAME###
#############

def getCollision(x,y,xs,ys,xc,yc,click=False):
    if(click):
        xc,yc = pg.mouse.get_pos()
    if xc > x and xc < x+xs and yc > y and yc < y+ys:
        return True
    return False


def loadWindow(window,display,size):
    """
    Charge the window scale, all the changes affect window
    But are shown in display
    """
    
    scaledWindow = pg.transform.scale(window,(size))
    display.blit(scaledWindow,(0,0))
    pg.display.update()

def main():
    """
    Start pygame and show the app interface
    """
    
    pg.init()
    windowSize = (1280,720)
    window = pg.Surface(windowSize)
    display = pg.display.set_mode(windowSize)
    #INTERFACES
    menu = Menu(window,windowSize)
    interface = Interface(window,windowSize)
    clock = pg.time.Clock()
    #FLAGS
    global Username
    login = True
    game = True
    running = True
    conecting = False
    unableToConect = False
    TXTng = False
    ME = ""
    #objects#
    dice = [4,6,8,10,12,20]

    
    menu.startLogin()
    interface.startGame()

    while running:
        
        while login or conecting:
            x,y = pg.mouse.get_pos()

            for e in pg.event.get():
                et = e.type
                print(e,"\n",et,"\n\n")
                if et == pg.QUIT:
                    login = False
                    conecting = False
                    game = False
                    running = False

                if et == pg.KEYDOWN:
                    if e.key == pg.K_RIGHT:
                        menu.moveUsers('R')
                    if e.key == pg.K_LEFT:
                        menu.moveUsers('L')
                
                if et == pg.MOUSEBUTTONDOWN:
                    action = menu.getClickedOnes(x,y)
                    print("tuki?",action)
                    if action == 1: #start reading text
                        TXTng = True
                    elif action == 2: #stop reading texxt
                        TXTng = False
                    elif action == 3: #login a selected user
                        ME = menu.getSelectedUser()
                        interface.setUser(ME)
                        Username = ME.getName()
                        print(Username)
                        login = False
                        conecting = True

                if TXTng:
                    if et == pg.KEYDOWN:
                        if e.key == pg.K_BACKSPACE:
                            menu.write("°")
                        else:
                            menu.write(e.unicode)

            if login:     
                menu.loadLogin()
                if(unableToConect):
                    menu.showError("Unable to conect")
                    unableToConect = False
            elif conecting:
                menu.loadConection()
                loadWindow(window,display,windowSize)
                clock.tick(50)
                flag = startConection(interface)
                if not flag:
                    login = True
                    unableToConect = True

                conecting = False

            loadWindow(window,display,windowSize)
            clock.tick(50)

            
        while game:
            x,y = pg.mouse.get_pos()

            for e in pg.event.get():
                et = e.type
                if et == pg.QUIT:
                    login = False
                    conecting = False
                    game = False
                    running = False
                    Client.close()
                if et == pg.MOUSEBUTTONDOWN:
                    action = interface.getClickedOnes(x,y)
                    print("tuki?",action)
                    if action == 1: #start reading text
                        TXTng = True
                    elif action == 2: #stop reading texxt
                        TXTng = False
                    elif action in dice: #throw a dice
                        num = randint(1,action)
                        print(num)
                        interface.throwDice("|"+str(action)+"#"+str(num),True)
                        msg = "ALL|"+Username+"|"+str(action)+"#"+str(num)
                        send(msg)

                if TXTng:
                    if et == pg.KEYDOWN:
                        if e.key == pg.K_BACKSPACE:
                            interface.write("°")
                        elif e.key == pg.K_RETURN:
                            msg = interface.sendMessage()
                            print(msg)
                            if msg != "":
                                send(msg)
                        else:
                            interface.write(e.unicode)
            
            interface.loadGame()
            if not interface.getConected:
                login = True
                conecting = False
                game = False

            loadWindow(window,display,windowSize)
            clock.tick(50)

    pg.quit()

main()
