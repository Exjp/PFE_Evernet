# Définition d'un client réseau rudimentaire
# Ce client dialogue avec un serveur ad hoc

import socket, sys
import jpysocket
import rsaUtils as ru

def receive():
    global crypted
    global alias
    global logged
    print(logged)
    msg = mySocket.recv(1024)
    print("\n msg received :" + str(msg) + "\n")
    #if crypted and logged:
    #msg = ru.decrypt_with_file(msg, alias)
    msg = msg.decode("utf-8", errors="ignore")
    msg = msg.split("_|_")
    if len(msg)>1:
        del msg[0]
    if msg == "":
        return
    if msg[0] != "BEGIN_COMMUNICATION":
        self.connection.close()
        del conn_client[self.getName()]
        print("Forced disconnection caused by no BEGIN_COMMUNICATION found : ", self.getName())
        sys.exit()
    while msg[-1] != "END_COMMUNICATION":
        print("dans le while")
        tmp = mySocket.recv(1024)
        tmp = tmp.decode("utf-8", errors="ignore")
        msg += tmp.split("_|_")
    del(msg[0])
    del(msg[-1])
    print("\n\ntest\n\n")
    print(msg)
    if crypted and logged:
        tmp = ''.join(msg)
        """
        if len(msg) == 0:
            return msgs
        tmp = msg[0]
        tmp += "_|_"
        """
        print("\n\n\n")
        tmp = tmp.encode()
        print(tmp)
        msg = ru.decrypt_with_file(tmp, alias)

    print(msg)
    return msg

def send(msg):
    global crypted
    global logged
    print(logged)
    msg = msg.replace(" ", "_|_")
    to_send = "_|_BEGIN_COMMUNICATION_|_"
    if crypted and logged:
        print("to_send")
        print("to send lol " + msg)
        msg = msg.encode()
        crypted_msg = ru.encrypt_with_pem(msg, "ca").decode("utf-8")
        print("to_send apres encrypt" + str(crypted_msg))
        #print("to_receive " + ru.decrypt(crypted_msg))
        to_send += crypted_msg
    else:
        to_send += msg
    to_send += "_|_END_COMMUNICATION"
    to_send=jpysocket.jpyencode(to_send)

    print("\nto_send:")
    print(to_send)
    print("\n")
    mySocket.send(to_send)

crypted = False
logged = False
HOST = 'localhost'
PORT = 50001
alias = None
if len(sys.argv)>1:
    if sys.argv[1] == "crypted":
        crypted = True
        if len(sys.argv) > 2:
            alias = sys.argv[2]
    else:
        HOST = sys.argv[1]

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(crypted)


try:
    mySocket.connect((HOST, PORT))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()
print("Connexion établie avec le serveur.")

if crypted:
    receive()
    send("clearDB")
    send("signIn test gsoidfsbv 9876543210 martin")

    print("avant receive")
    receive()
    logged = True
    alias = "test"
    print("après receive")
    send("FIN")
    receive()
    mySocket.close()

    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        mySocket.connect((HOST, PORT))
    except socket.error:
        print("La connexion a échoué.")
        sys.exit()
    print("Connexion établie avec le serveur.")
logged = False
alias = None
if sys.argv[1] == "crypted":
    if len(sys.argv) > 2:
        alias = sys.argv[2]
msgServeur = receive()
if crypted:

    send("signIn " + str(alias) + " gsoiebv 0123456789 martin")
    receive()
    logged = True






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
