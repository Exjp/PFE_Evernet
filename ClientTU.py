# Définition d'un client réseau rudimentaire
# Ce client dialogue avec un serveur ad hoc

import socket, sys, os, time


def receive():
    global mySocket
    msg = mySocket.recv(1024).decode("utf-8").split("_|_")
    if msg == "":
        return
    while msg[-1] != "END_COMMUNICATION":
        msg += mySocket.recv(1024).decode("utf-8").split("_|_")
    return msg

def send(msg):
    global mySocket
    msg += "_|_END_COMMUNICATION"
    mySocket.send(msg.encode("utf-8"))

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
    msg = receive()
    #print(msg)
    deconnection()
    return True

def testSignInCallBack():
    return True

def testSignInErrorFormat():
    connection()
    send("signIn alias_test mdp_test martin")
    msg = receive()
    if msg != "ERROR 3_|_Wrong input format: signIn *alias* *password* *phoneNum* *invitationKey*":
        return False
    send("signIn alias_test mdp_test 0123456789 martin coucou")
    msg = receive()
    if msg != "ERROR 3_|_Wrong input format: signIn *alias* *password* *phoneNum* *invitationKey*":
        return False
    deconnection()
    return True


def testSignInErrorAlreadyLog():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin")
    msg = receive()
    if msg != "ERROR 1_|_Already logged my friend!":
        return False
    deconnection()
    return True

"""
TEST LOGIN
"""

def testLogInWorking():
    connection()
    send("signIn alias_test mdp_test 0123456789 martin")
    deconnection()
    connection()
    send("logIn alias_test mdp_test")
    deconnection()
    return True

def testLogInCallBack():
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

def testGetNbCallBack():
    return True

def testGetNbErrorPermission():
    return True

"""
TEST GETPHONENUMLIST
"""

def testGetPhoneNumListWorking():
    return True

def testGetPhoneNumListCallBack():
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

def testGetInvitationKeyCallBack():
    return True

def testGetInvitationKeyErrorPermission():
    return True
time.sleep(3)
if os.path.exists("page.xml"):
    os.remove("page.xml")

HOST = 'localhost' #'192.168.1.44'
PORT = 50001

mySocket = None
"""
try:
    mySocket.connect((HOST, PORT))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()
print("Connexion établie avec le serveur.")
"""

print("Début des Tests Unitaires :")
print("----------Fonction connection----------")
print("Connexion au server : " + str(testServerConnection()))
print("----------Fonction signIn----------")
print("Test de signIn : " + str(testSignInWorking()))
print("Test de l'erreur de format : " + str(testSignInErrorFormat()))
print("Test de l'erreur already log : " + str(testSignInErrorAlreadyLog()))
print("----------Fonction logIn----------")
print("----------Fonction getNb----------")
print("----------Fonction getPhoneNumList----------")
print("----------Fonction getInvitationalKey----------")

"""
msgServeur = receive()
while 1:
    if msgServeur[0].upper() == "FIN":
        break
    print(msgServeur)
    msgClient = input("Ecrire :")

    send(msgClient)

    msgServeur = receive()
"""



#msg.decode("utf-8")
