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
    send("signIn alias_test mdp_test 0123456789 martin") #INVITATIONKEY A CHANGER
    msgTmp = receive()
    deconnection()
    connection()
    send("signIn alias_test2 mdp_test2 1123456789 martin")
    msgTmp = receive()
    send("getPhoneNum alias_test")
    msg = receive()
    if msg[0] != "0123456789":
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True

def testSignInErrorFormat():
    connection()
    send("signIn alias_test mdp_test martin")
    msg = receive()
    if msg[0] != "ERROR 3":
        send("clearDB")
        deconnection()
        return False
    send("signIn alias_test mdp_test 0123456789 martin coucou")
    msg = receive()
    if msg[0] != "ERROR 3":
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True


def testSignInErrorAlreadyLog():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin")
    msgTmp = receive()
    send("signIn alias_test mdp_test 0123456789 martin")
    msg = receive()
    if msg[0] != "ERROR 1":
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True

def testSignInErrorAlreadyExists():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin")
    msgTmp = receive()
    deconnection()
    connection()
    send("signIn alias_test mdp_test 0123456789 martin")
    msg = receive()
    if msg[0] != "ERROR 5":
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True

"""
TEST LOGIN
"""

def testLogInWorking():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin")
    msgTmp= receive()
    deconnection()
    connection()
    send("logIn alias_test mdp_test")
    msg = receive()
    if msg[0] != ("Authentified"):
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True

def testLogInErrorFormat():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin")
    msgTmp= receive()
    deconnection()
    connection()
    send("logIn alias_test mdp_test coucou")
    msg = receive()
    if msg[0] != ("ERROR 3"):
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True

def testLogInErrorAlreadyLog():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin")
    msgTmp= receive()
    send("logIn alias_test mdp_test")
    msg = receive()
    if msg[0] != ("ERROR 1"):
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True
    return True

def testLogInErrorWrongLog():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin")
    msgTmp= receive()
    deconnection()
    connection()
    send("logIn alias_test wrong_mdp_test")
    msg = receive()
    if msg[0] != ("ERROR 4"):
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True
    return True

"""
TEST GETPHONENUM
"""

def testGetPhoneNumWorking():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin") #INVITATIONKEY A CHANGER
    msgTmp = receive()
    deconnection()
    connection()
    send("signIn alias_test2 mdp_test2 1123456789 martin")
    msgTmp = receive()
    send("getPhoneNum alias_test")
    msg = receive()
    if msg[0] != "0123456789":
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True

def testGetPhoneNumErrorFormat():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin") #INVITATIONKEY A CHANGER
    msgTmp = receive()
    deconnection()
    connection()
    send("signIn alias_test2 mdp_test2 1123456789 martin")
    msgTmp = receive()
    send("getPhoneNum alias_test coucou")
    msg = receive()
    if msg[0] != "ERROR 3":
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True

def testGetPhoneNumErrorPermission():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin") #INVITATIONKEY A CHANGER
    msgTmp = receive()
    deconnection()
    connection()
    send("getPhoneNum alias_test")
    msg = receive()
    if msg[0] != "ERROR 2":
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True

"""
TEST GETPHONENUMLIST
"""

def testGetPhoneNumListWorking():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin") #INVITATIONKEY A CHANGER
    msgTmp = receive()
    deconnection()
    connection()
    send("signIn alias_test2 mdp_test2 1123456789 martin")
    deconnection()
    connection()
    send("signIn alias_test3 mdp_test3 2123456789 martin")
    msgTmp = receive()
    send("getPhoneNumList 2")
    msg = receive()
    if (msg[0] != "0123456789" and msg[0] != "1123456789") or (msg[3] != "0123456789" and msg[3] != "1123456789"):
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True

def testGetPhoneNumListErrorFormat():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin") #INVITATIONKEY A CHANGER
    msgTmp = receive()
    deconnection()
    connection()
    send("signIn alias_test2 mdp_test2 1123456789 martin")
    deconnection()
    connection()
    send("signIn alias_test3 mdp_test3 2123456789 martin")
    msgTmp = receive()
    send("getPhoneNumList 2 coucou")
    msg = receive()
    #print(msg)
    if msg[0] != "ERROR 3":
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True

def testGetPhoneNumListErrorPermission():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin") #INVITATIONKEY A CHANGER
    msgTmp = receive()
    deconnection()
    connection()
    send("signIn alias_test2 mdp_test2 1123456789 martin")
    deconnection()
    connection()
    send("getPhoneNumList 2")
    msg = receive()
    #print(msg)
    if msg[0] != "ERROR 2":
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True


"""
TEST GETINVITATIONKEY
"""

def testGetInvitationKeyWorking():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin") #INVITATIONKEY A CHANGER
    msgTmp = receive()
    send("getInvitationKey")
    msg = receive()
    if msg[0] != "martin":
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True

def testGetInvitationKeyErrorFormat():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin") #INVITATIONKEY A CHANGER
    msgTmp = receive()
    send("getInvitationKey coucou")
    msg = receive()
    if msg[0] != "ERROR 3":
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True

def testGetInvitationKeyErrorPermission():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin") #INVITATIONKEY A CHANGER
    msgTmp = receive()
    deconnection()
    connection()
    send("getInvitationKey")
    msg = receive()
    if msg[0] != "ERROR 2":
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True


time.sleep(3)
if os.path.exists("page.xml"):
    os.remove("page.xml")

HOST = 'localhost' #'192.168.1.44'
PORT = 50001

mySocket = None

print("Début des Tests Unitaires :")
print("----------Fonction connection----------")
print("Test de connexion au server : " + str(testServerConnection()))
print("----------Fonction signIn----------")
print("Test de signIn : " + str(testSignInWorking()))
print("Test de l'erreur de format : " + str(testSignInErrorFormat()))
print("Test de l'erreur already log : " + str(testSignInErrorAlreadyLog()))
print("Test de l'erreur user already exists : " + str(testSignInErrorAlreadyExists()))
print("----------Fonction logIn----------")
print("Test de logIn : " + str(testLogInWorking()))
print("Test de l'erreur de format : " + str(testLogInErrorFormat()))
print("Test de l'erreur already log : " + str(testLogInErrorAlreadyLog()))
print("Test de l'erreur wrong log : " + str(testLogInErrorWrongLog()))
print("----------Fonction getPhoneNum----------")
print("Test getPhoneNum : " + str(testGetPhoneNumWorking()))
print("Test de l'erreur de format : " + str (testGetPhoneNumErrorFormat()))
print("Test de l'erreur de permission : " + str(testGetPhoneNumErrorPermission()))
print("----------Fonction getPhoneNumList----------")
print("Test de getPhoneNumList : " + str(testGetPhoneNumListWorking()))
print("Test de l'erreur de format : " + str(testGetPhoneNumListErrorFormat()))
print("Test de l'erreur de permission : " + str(testGetPhoneNumListErrorPermission()))
print("----------Fonction getInvitationKey----------")
print("Test de getInvitationKey : " + str(testGetInvitationKeyWorking()))
print("Test de l'erreur de format : " + str(testGetInvitationKeyErrorFormat()))
print("Test de l'erreur de permission : " + str(testGetInvitationKeyErrorPermission()))
