import os
import socket as s
import threading as t
import struct
#Podria usar flet para hacer la apk

#Variables
Host = "0.0.0.0"
Port = int(os.environ.get("PORT",5000))

#Iniciacion del servidor
server = s.socket(s.AF_INET,s.SOCK_STREAM)
server.bind((Host,Port))
server.listen()

clients = {} #Username,Client#

def sendEveryone(username,msg):
    UN = clients.keys()
    for u in UN:
        if u != username:
            send(msg,u,username)

def send(message, receptor, messager):
    try:
        mess = messager+'|'+message
        clients[receptor].sendall(struct.pack("<H",len(mess)))
        clients[receptor].sendall(mess.encode("utf-8"))
    except Exception as e:
        print(receptor + " Left error in send:\n")
        print(f"{e}")
        clients[receptor].close()
        del clients[receptor]
        sendEveryone("server",receptor+"-")

"""
Formato de  mensajes
Receptor|Messager|Message
"""

def reciveAndSend(client,username):
    while True:
        try:
            messageLen = struct.unpack("<H",clients[username].recv(2))[0]
            message = clients[username].recv(messageLen).decode("utf-8")
            print(message," ",messageLen)
            parts = message.split('|')
            #Aqui va logica de gestor de receptor
            if(parts[0] != "server" and parts[1] != "server"):
                if parts[0]=="ALL":
                    sendEveryone(parts[1],parts[2])
                else:
                    send(parts[2]+"(Wisper)",parts[0],parts[1])
                #if(parts[2] == "SeNDFiLe"):
                #    sendFile(clients[username],clients[parts[0]])
                    #reciveFile(clients[username])
            else:
                print(f"Message for testing: {message}")
                if "+" in parts[2]:
                    ms = parts[2].split("+")
                    if(int(ms[1]) == 1):
                        print("getADV,"+username,ms[0],"server este es el mensaje antes de getADV")
                        send("getADV,"+username,ms[0],"server")
                else:
                    send(parts[2],parts[0],parts[1])

        except IndexError:
            print(f"Invalid message format from {username}")
            send("Invalid message format",username,"Server")

        except ConnectionResetError:
            print(f"{username} disconected")
            clients[username].close()
            del clients[username]
            sendEveryone("server",username+"-")
            print(clients)
            break
            
        except Exception as e:
            print(username + " Left error in recive and send: \n")
            print(f"{e}\n")
            clients[username].close()
            del clients[username]
            sendEveryone("server",username+"-")
            break

def sendFile(Client,Reciver):
    try:
        byteFilenameSize = Client.recv(2)
        nameSize = struct.unpack("<H",byteFilenameSize)[0]
        Filename = Client.recv(nameSize)
        FileSize = getFileSize(Client)
        
        Reciver.sendall(byteFilenameSize)
        Reciver.sendall(Filename)
        Reciver.sendall(struct.pack("<Q",FileSize))
        
        receivedBytes = 0
        while receivedBytes < FileSize:
            chunk = Client.recv(1024)
            if(chunk):
                Reciver.sendall(chunk)
                receivedBytes += len(chunk)

    except Exception as e:
        print("Error in SendFile")
        print(e)

def getFileSize(Client):
    try:
        expectedBytes = struct.calcsize("<Q")
        #<Q significa agarrar desde el bit menos significativo primero
        #y la Q significa Unsigned Long long
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

def reciveFile(Client):
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

def reciveUsers():
    print(f"Server is runing on host: {Host} and port: {Port}")
    while True:
        username = "|"
        client, adress = server.accept()
        try:
            usernameLen = struct.unpack("<H",client.recv(2))[0]
            code = client.recv(usernameLen).decode("utf-8")
            username = code
            
            print(username + " Conected")
        except Exception as e:
            print("Error in recive users:")
            print(e)
            client.close()
            
        #Hilos para escuchar y enviar mensajes a destinatarios
        if(username in clients.keys()):
            try:
                IUM = "server|Already conected"
                client.sendall(struct.pack("<H",len(IUM)))
                client.sendall(IUM.encode("utf-8"))
            except Exception as e:
                print("Error sending: User already conected")
            print(f"{username} disconected")
            client.close()    

        elif("|" not in username):
            clients[username] = client
            thread = t.Thread(target=reciveAndSend,args=(client,username,))
            thread.start()
            sendEveryone("server",username+"&")
            for u in clients.keys():
                send(u+"&",username,"server")
        
        else:
            try:
                IUM = "server|Invalid Username"
                client.sendall(struct.pack("<H",len(IUM)))
                client.sendall(IUM.encode("utf-8"))
            except Exception as e:
                print("Error sending: invaid username")
            print(f"{username} disconected")
            client.close()

reciveUsers()
