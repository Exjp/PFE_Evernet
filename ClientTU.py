# Définition d'un client réseau rudimentaire
# Ce client dialogue avec un serveur ad hoc

import socket, sys, os


def receive():
    msg = mySocket.recv(1024).decode("utf-8").split("_|_")
    if msg == "":
        return
    while msg[-1] != "END_COMMUNICATION":
        msg += mySocket.recv(1024).decode("utf-8").split("_|_")
    return msg

def send(msg):
    msg += "_|_END_COMMUNICATION"
    mySocket.send(msg.encode("utf-8"))

"""
TEST CONNECTION
"""

def testServerConnection():
    try:
        mySocket.connect((HOST, PORT))
    except socket.error:
        return False
    return True

"""
TEST SIGNIN
"""
def testSignInWorking():
    try:
        mySocket.connect((HOST, PORT))
    except socket.error:
        sys.exit()
    send("signIn alias_test mdp_test 0123456789 martin") #INVITATIONKEY A CHANGER
    return (getNumberFromAlias("alias_test") == "0123456789")

def testSignInCallBack():
    return True

def testSignInErrorFormat():
    return True

def testSignInErrorAlreadyLog():
    return True

"""
TEST LOGIN
"""

def testLogInWorking():
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


os.remove("page.xml")
os.System('python Server.py')
HOST = 'localhost' #'192.168.1.44'
PORT = 50000

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    mySocket.connect((HOST, PORT))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()
print("Connexion établie avec le serveur.")

print("Début des Tests Unitaires :\n")
print("Fonction connection :\n")

print("Fonction signIn :\n")
print("Fonction logIn :\n")
print("Fonction getNb :\n")
print("Fonction getPhoneNumList :\n")
print("Fonction getInvitationalKey :\n")

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




# 4) Fermeture de la connexion :
print("Connexion interrompue.")
mySocket.close()


#msg.decode("utf-8")
