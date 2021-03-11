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
    receive()
    deconnection()
    connection()
    send("signIn alias_test2 mdp_test2 1123456789 martin")
    receive()
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
    receive()
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
    receive()
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
    receive()
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
    receive()
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
    receive()
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
    receive()
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
    receive()
    deconnection()
    connection()
    send("signIn alias_test2 mdp_test2 1123456789 martin")
    receive()
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
    receive()
    deconnection()
    connection()
    send("signIn alias_test2 mdp_test2 1123456789 martin")
    receive()
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
    receive()
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
    receive()
    deconnection()
    connection()
    send("signIn alias_test2 mdp_test2 1123456789 martin")
    receive()
    deconnection()
    connection()
    send("signIn alias_test3 mdp_test3 2123456789 martin")
    receive()
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
    receive()
    deconnection()
    connection()
    send("signIn alias_test2 mdp_test2 1123456789 martin")
    receive()
    deconnection()
    connection()
    send("signIn alias_test3 mdp_test3 2123456789 martin")
    receive()
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
    receive()
    deconnection()
    connection()
    send("signIn alias_test2 mdp_test2 1123456789 martin")
    receive()
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
    receive()
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
    receive()
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
    receive()
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

"""
TEST GETINVITATIONKEY
"""

def testGetAllAliasWorking():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin") #INVITATIONKEY A CHANGER
    receive()
    deconnection()
    connection()
    send("signIn alias_test2 mdp_test2 1123456789 martin") #INVITATIONKEY A CHANGER
    receive()
    deconnection()
    connection()
    send("signIn alias_test3 mdp_test3 2123456789 martin") #INVITATIONKEY A CHANGER
    receive()
    deconnection()
    connection()
    send("getAllAlias YpOi0TLHHgJFzgKYCBCrSNHPPRTSEjyt9OHp23WouuVa8tS1emL93WgJXiKLp6n00rkEAriyYQ9JGJfU23GrH43EOUci6k5uNTk5")
    msg = receive()
    if "alias_test" not in msg or "alias_test2" not in msg or "alias_test3" not in msg:
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True

def testGetAllAliasErrorFormat():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin") #INVITATIONKEY A CHANGER
    receive()
    deconnection()
    connection()
    send("getAllAlias YpOi0TLHHgJFzgKYCBCrSNHPPRTSEjyt9OHp23WouuVa8tS1emL93WgJXiKLp6n00rkEAriyYQ9JGJfU23GrH43EOUci6k5uNTk5 coucou")
    msg = receive()
    if msg[0] != "ERROR 3":
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True

def testGetAllAliasWrongPassword():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin") #INVITATIONKEY A CHANGER
    receive()
    deconnection()
    connection()
    send("getAllAlias coucou")
    msg = receive()
    if msg[0] != "ERROR 4":
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True

def testGetAllAliasEmptyTree():
    connection()
    send("getAllAlias YpOi0TLHHgJFzgKYCBCrSNHPPRTSEjyt9OHp23WouuVa8tS1emL93WgJXiKLp6n00rkEAriyYQ9JGJfU23GrH43EOUci6k5uNTk5")
    msg = receive()
    if msg[0] != "ERROR 6":
        send("clearDB")
        deconnection()
        return False
    send("clearDB")
    deconnection()
    return True

cpt = 0
total = 21

def printValide(b):
    global cpt
    if b:
        print("VALIDE")
        cpt = cpt + 1
    else:
        print("INVALIDE")

time.sleep(3)
if os.path.exists("page.xml"):
    os.remove("page.xml")

HOST = 'localhost' #'192.168.1.44'
PORT = 50001

mySocket = None


print("Début des Tests Unitaires :")
print("----------Fonction connection----------")
print("1 Test de connexion au serveur : ", end='')
printValide(testServerConnection())
print("----------Fonction signIn----------")
print("2 Test de signIn : ", end='')
printValide(testSignInWorking())
print("3 Test de l'erreur de format : ", end='')
printValide(testSignInErrorFormat())
print("4 Test de l'erreur already log : ", end='')
printValide(testSignInErrorAlreadyLog())
print("5 Test de l'erreur user already exists : ", end='')
printValide(testSignInErrorAlreadyExists())
print("----------Fonction logIn----------")
print("6 Test de logIn : ", end='')
printValide(testLogInWorking())
print("7 Test de l'erreur de format : ", end='')
printValide(testLogInErrorFormat())
print("8 Test de l'erreur wrong log : ", end='')
printValide(testLogInErrorWrongLog())
print("----------Fonction getPhoneNum----------")
print("9 Test getPhoneNum : ", end='')
printValide(testGetPhoneNumWorking())
print("10 Test de l'erreur de format : ", end='')
printValide(testGetPhoneNumErrorFormat())
print("11 Test de l'erreur de permission : ", end='')
printValide(testGetPhoneNumErrorPermission())
print("----------Fonction getPhoneNumList----------")
print("12 Test de getPhoneNumList : ", end='')
printValide(testGetPhoneNumListWorking())
print("13 Test de l'erreur de format : ", end='')
printValide(testGetPhoneNumListErrorFormat())
print("14 Test de l'erreur de permission : ", end='')
printValide(testGetPhoneNumListErrorPermission())
print("----------Fonction getInvitationKey----------")
print("15 Test de getInvitationKey : ", end='')
printValide(testGetInvitationKeyWorking())
print("16 Test de l'erreur de format : ", end='')
printValide(testGetInvitationKeyErrorFormat())
print("17 Test de l'erreur de permission : ", end='')
printValide(testGetInvitationKeyErrorPermission())
print("----------Fonction getAllAlias----------")
print("18 Test de getAllAlias : ", end='')
printValide(testGetAllAliasWorking())
print("19 Test de l'erreur de format : ", end='')
printValide(testGetAllAliasErrorFormat())
print("20 Test de l'erreur wrong password : ", end='')
printValide(testGetAllAliasWrongPassword())
print("21 Test de l'erreur empty tree : ", end='')
printValide(testGetAllAliasEmptyTree())
if cpt != total:
    if total - cpt == 1:
        print("1 test est invalide !")
    else:
        print(str(total - cpt) + " tests sont invalides !")
else:
    print("Tous les tests sont valides !")
