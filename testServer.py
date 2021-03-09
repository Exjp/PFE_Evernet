import sys, threading, os
import xmlManager as xmlM
from pair_utils import *
import jpysocket
import datetime, time

HOST = '192.168.1.44' #'192.168.1.44'
PORT = 50000
if len(sys.argv)>1:
    if sys.argv[1] == "test":
        HOST = 'localhost'
        PORT = 50001
        #sys.stdout = open('log_debug_ClientTU.txt', 'w')
    if sys.argv[1] == "localhost":
        HOST = 'localhost'
        PORT = 50000


s=jpysocket.jpysocket() #Create Socket
s.bind((HOST,PORT)) #Bind Port And Host
s.listen(5) #Socket is Listening
print("Socket Is Listening....")
print("HOST: " + HOST + " Port: " + str(PORT))

xmlM.init()

class ThreadClient(threading.Thread):

    '''dérivation d'un objet thread pour gérer la connexion avec un client'''
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connection = conn
        self.logged = False
        self.alias = None


    def callBack(self, commande):
        cmd = commande


        if cmd[0] == "getPhoneNum":
            if not self.logged:
                print("ERROR 2_|_Permission denied!")
                self.sendMessage("ERROR 2_|_Permission denied!")
                return
            #rajouter envoie certif
            toSend = xmlM.getNumberFromAlias(cmd[1])
            toSend += "_|_"
            toSend += xmlM.getKeyFromAlias(cmd[1])
            self.sendMessage(toSend)



        elif cmd[0] == "getInvitationKey":
            if not self.logged:
                print("ERROR 2_|_Permission denied!")
                self.sendMessage("ERROR 2_|_Permission denied!")
                return
            self.sendMessage("martin")



        elif cmd[0] == "signIn":
            if self.logged:
                print("ERROR 1_|_Already logged my friend!")
                self.sendMessage("ERROR 1_|_Already logged my friend!")
                return
            if len(cmd) != 5:
                print("ERROR 3_|_Wrong input format: signIn *alias* *password* *phoneNum* *invitationKey*")
                self.sendMessage("ERROR 3_|_Wrong input format: signIn *alias* *password* *phoneNum* *invitationKey*")
                return
            #verif cmd[3]la clé d'invition
            client_pair(cmd[1])
            cert_str = open(cmd[1]+"_crt.pem", 'rt').read()
            key_str = open(cmd[1]+"_key.pem", 'rt').read()

            xmlM.addUser(cmd[1], cmd[2], cmd[3], cert_str)

            keyCert = cert_str + "_|_" + key_str + "_|_" + ca_cert_str
            self.sendMessage(keyCert)
            os.remove(cmd[1]+"_crt.pem")
            os.remove(cmd[1]+"_key.pem")

            #si pas d'erreur
            self.logged = True
            self.alias = cmd[1]




        elif cmd[0] == "logIn":
            if self.logged:
                print("ERROR 1_|_Already logged my friend!")
                self.sendMessage("ERROR 1_|_Already logged my friend!")
                return
            if len(cmd) != 3:
                print("ERROR 3_|_Wrong input format: logIn *alias* *password*")
                self.sendMessage("ERROR 3_|_Wrong input format: logIn *alias* *password*")
                return
            res = xmlM.login(cmd[1], cmd[2])
            if not res:
                print("ERROR 4_|_Wrong alias or password")
                self.sendMessage("ERROR 4_|_Wrong alias or password")
            else:
                self.logged = True
                self.alias = cmd[1]
                self.sendMessage("Authentified")



        elif cmd[0] == "getPhoneNumList":
            if not self.logged:
                print("Permission denied!")
                self.sendMessage("ERROR 2_|_Permission denied!")
                return
            if len(cmd) != 2:
                print("ERROR 3_|_Wrong input format: getPhoneNumList *n_numbers*")
                self.sendMessage("ERROR 3_|_Wrong input format: getPhoneNumList *n_numbers*")
                return
            list = xmlM.randomUsers(cmd[1], self.alias)
            if len(list) <1:
                return False
            strList = ""
            strList += list[0][0]
            strList += "_|_"
            strList += list[0][1]
            if len(list) >=2:
                for x in range(1, len(list)):
                    strList += "_|_"
                    strList += list[x][0]
                    strList += "_|_"
                    strList += list[x][1]
            self.sendMessage(strList)



        else:
            print("Invalid callBack")
            self.sendMessage("Invalid callBack")


    def receive(self):
        try:
            msg=connection.recv(1024) #Recieve msg
            print("avant decode : " + str(msg))
            try:
                msg=jpysocket.jpydecode(msg)
                print("après decode : ")
                print(str(msg))
            except:
                print("error while decode received message: " + str(msg))
                return False
        except:
            print("error while receive")
            return False

        msg = msg.split("_|_")
        if msg[0] == "":
            self.connection.close()
            del conn_client[self.getName()]
            print("Client disconnected unexpectedly:", self.getName())
            sys.exit()
        while msg[-1] != "END_COMMUNICATION":
            tmp = connection.recv(1024)
            try:
                msg += jpysocket.jpydecode(tmp).split("_|_")
            except:
                print("error while decode received message: " + str(msg) + " + " + str(tmp))
                return False
        print(msg)
        del msg[-1]
        return msg


    def sendMessage(self, msg):

        msg += "_|_END_COMMUNICATION"
        msg=jpysocket.jpyencode(msg) #Encript The Msg
        print(msg)
        connection.send(msg)

    def run(self):
        nom = self.getName()

        while 1:
            msgClient = self.receive()
            print("msgClient : " + str(msgClient))
            if msgClient == False:
                print("receive error")
                self.sendMessage("ERROR")
            else:
                if msgClient[-1].upper() == "FIN" or msgClient == None:
                    self.sendMessage("FIN")
                    break
                #self.connexion.send(str.encode("RECU"))
                self.callBack(msgClient)
                message = str(datetime.datetime.now())
                message += " : %s> %s" % (nom, msgClient)
                print(message)
            # Faire suivre le message à tous les autres clients :
            #for cle in conn_client:
            #    if cle != nom:      # ne pas le renvoyer à l'émetteur
            #        conn_client[cle].send(str.encode(message))

        # Fermeture de la connexion :
        self.connection.close()      # couper la connexion côté serveur
        del conn_client[nom]        # supprimer son entrée dans le dictionnaire
        print("Client déconnecté:", nom)

        # Le thread se termine ici

# Initialisation du serveur - Mise en place du socket :
try:
    open("ca_crt.pem", "r")
    open("ca_key.pem", "r")
except:
    CA_pair()

ca_cert_str = open("ca_crt.pem", 'rt').read()

conn_client = {}
while 1:
    connection,address=s.accept() #Accept the Connection
    print("Connected To ",address)
    th = ThreadClient(connection)
    th.start()
    it = th.getName()
    conn_client[it] = connection
    msgsend=jpysocket.jpyencode("Thank You For Connecting._|_END_COMMUNICATION") #Encript The Msg
    connection.send(msgsend) #Send Msg

s.close() #Close connection
print("Connection Closed.")
