# Définition d'un client réseau rudimentaire
# Ce client dialogue avec un serveur ad hoc

import socket, sys


def receive():
    msg = mySocket.recv(1024).decode("utf-8")
    tmp = msg
    msg = msg.split("_|_")
    if msg == "":
        return
    while msg[-1] != "END_COMMUNICATION":
        tmp2= mySocket.recv(1024).decode("utf-8")
        tmp += tmp2
        msg += tmp2.split("_|_")
    print(tmp)
    return msg

def send(msg):
    msg += "_|_END_COMMUNICATION"
    mySocket.send(msg.encode("utf-8"))


HOST = '192.168.1.44'
PORT = 50001
if len(sys.argv)>1:
    HOST = sys.argv[1]

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



try:
    mySocket.connect((HOST, PORT))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()
print("Connexion établie avec le serveur.")


msgServeur = receive()
while 1:
    if msgServeur[0].upper() == "FIN":
        break
    #print(msgServeur)
    msgClient = input("Ecrire :")

    send(msgClient)

    msgServeur = receive()



# 4) Fermeture de la connexion :
print("Connexion interrompue.")
mySocket.close()


#msg.decode("utf-8")
