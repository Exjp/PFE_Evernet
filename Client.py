# Définition d'un client réseau rudimentaire
# Ce client dialogue avec un serveur ad hoc

import socket, sys
import jpysocket

def receive():
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
    del(msg[-1])
    print(msg)
    return msg

def send(msg):
    msg = msg.replace(" ", "_|_")
    to_send = "_|_BEGIN_COMMUNICATION_|_"
    to_send += msg
    to_send += "_|_END_COMMUNICATION"
    to_send=jpysocket.jpyencode(to_send)
    mySocket.send(to_send)


HOST = '192.168.1.44'
PORT = 50000
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
