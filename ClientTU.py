# Définition d'un client réseau rudimentaire
# Ce client dialogue avec un serveur ad hoc

import socket, sys, os, time
import jpysocket

def receive():
    global mySocket
    msg = mySocket.recv(1024)
    msg = jpysocket.jpydecode(msg)
    msg = msg.split("_|_")
    if len(msg)>1:
        del msg[0]
    if msg == "":
        return
    while msg[-1] != "END_COMMUNICATION":
        tmp = mySocket.recv(1024)
        tmp = jpysocket.jpydecode(tmp)
        msg += tmp.split("_|_")
    for x in msg:
        if x != "BEGIN_COMMUNICATION":
            msg.remove(x)
        else:
            msg.remove('BEGIN_COMMUNICATION')
            break
    del msg[-1]
    return msg

def send(msg):
    global mySocket
    msg = msg.replace(" ", "_|_")
    to_send = "_|_BEGIN_COMMUNICATION_|_"
    to_send += msg
    to_send += "_|_END_COMMUNICATION"
    to_send = jpysocket.jpyencode(to_send)
    mySocket.send(to_send)

def connection():
    global mySocket
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        mySocket.connect((HOST, PORT))
    except socket.error:
        print("La connexion a échoué.")
        return False
    receive()
    return True

def deconnection():
    global mySocket
    send("FIN")
    msg = receive()
    if msg[0] == "FIN":
        mySocket.close()
        mySocket = None




"""
TEST CONNECTION
"""

def testServerConnection():
    res = connection()
    deconnection()
    return res

"""
TEST SIGNIN
"""
def testSignInWorking():
    connection()
    send("clearDB")
    send("signIn alias_test mdp_test 0123456789 martin") #INVITATIONKEY A CHANGER
    msgTmp = receive()
    deconnection()
    time.sleep(0.2)
    connection()
    send("signIn alias_test2 mdp_test2 1123456789 martin")
    msgTmp = receive()
    send("getPhoneNum alias_test")
    msg = receive()
    if msg[0] != "0123456789":
        return False
    deconnection()
    return True

def testSignInErrorFormat():
    connection()
    send("clearDB")
    send("signIn alias_test mdp_test martin")
    msg = receive()
    if msg[0] != "ERROR 3" or msg [1] != "Wrong input format: signIn_|_*alias*_|_*password*_|_*phoneNum*_|_*invitationKey*":
        return False
    send("signIn alias_test mdp_test 0123456789 martin coucou")
    msg = receive()
    if msg[0] != "ERROR 3" or msg[1] != "Wrong input format: signIn_|_*alias*_|_*password*_|_*phoneNum*_|_*invitationKey*":
        return False
    deconnection()
    return True


def testSignInErrorAlreadyLog():
    connection()
    send("clear")
    send("signIn alias_test mdp_test 0123456789 martin")
    msgTmp = receive()
    send("signIn alias_test mdp_test 0123456789 martin")
    msg = receive()
    if msg[0] != "ERROR 1" or msg[1] != "Already logged my friend!":
        return False
    deconnection()
    return True

"""
TEST LOGIN
"""

def testLogInWorking():
    connection()
    send("clear")
    send("signIn alias_test mdp_test 0123456789 martin")
    msgTmp= receive()
    deconnection()
    connection()
    send("logIn alias_test mdp_test")
    msgTmp= receive()
    deconnection()
    return True

def testLogInErrorAlreadyLog():
    return True

def testLogInErrorFormat():
    return True

def testLogInErrorWrongLog():
    return True

"""
TEST GETNB
"""

def testGetNbWorking():
    return True

def testGetNbErrorPermission():
    return True

"""
TEST GETPHONENUMLIST
"""

def testGetPhoneNumListWorking():
    return True

def testGetPhoneNumListErrorPermission():
    return True

def testGetPhoneNumListErrorFormat():
    return True

"""
TEST GETINVITATIONKEY
"""

def testGetInvitationKeyWorking():
    return True

def testGetInvitationKeyErrorPermission():
    return True
time.sleep(3)
if os.path.exists("page.xml"):
    os.remove("page.xml")

HOST = 'localhost' #'192.168.1.44'
PORT = 50001

mySocket = None

print("Début des Tests Unitaires :")
print("----------Fonction connection----------")
print("Connexion au server : " + str(testServerConnection()))
print("----------Fonction signIn----------")
print("Test de signIn : " + str(testSignInWorking()))
#print("Test de l'erreur de format : " + str(testSignInErrorFormat()))
#print("Test de l'erreur already log : " + str(testSignInErrorAlreadyLog()))
print("----------Fonction logIn----------")
print("----------Fonction getNb----------")
print("----------Fonction getPhoneNumList----------")
print("----------Fonction getInvitationalKey----------")



#msg.decode("utf-8")
