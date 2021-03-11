import sys, threading, os, datetime, time, socket
import xmlManager as xmlM
from pair_utils import *
import jpysocket


HOST = '192.168.1.44'
PORT = 50000
if len(sys.argv)>1:
    if sys.argv[1] == "test":
        HOST = 'localhost'
        PORT = 50001
        #sys.stdout = open('log_debug_ClientTU.txt', 'w')
    if sys.argv[1] == "localhost":
        HOST = 'localhost'
        PORT = 50000
print("HOST: " + HOST + " Port: " + str(PORT))



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
            if len(cmd) != 2:
                print("ERROR 3_|_Wrong input format: getPhoneNum_|_*alias*")
                self.sendMessage("ERROR 3_|_Wrong input format: getPhoneNum_|_*alias*")
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
            if len(cmd) != 1:
                print("ERROR 3_|_Wrong input format: getInvitationKey")
                self.sendMessage("ERROR 3_|_Wrong input format: getInvitationKey")
                return
            self.sendMessage("martin")



        elif cmd[0] == "signIn":
            if self.logged:
                print("ERROR 1_|_Already logged my friend!")
                self.sendMessage("ERROR 1_|_Already logged my friend!")
                return
            if len(cmd) != 5:
                print("ERROR 3_|_Wrong input format: signIn_|_*alias*_|_*password*_|_*phoneNum*_|_*invitationKey*")
                self.sendMessage("ERROR 3_|_Wrong input format: signIn_|_*alias*_|_*password*_|_*phoneNum*_|_*invitationKey*")
                return
            #verif cmd[3]la clé d'invition
            client_pair(cmd[1])
            cert_str = open(cmd[1]+"_crt.pem", 'rt').read()
            key_str = open(cmd[1]+"_key.pem", 'rt').read()
            os.remove(cmd[1]+"_crt.pem")
            os.remove(cmd[1]+"_key.pem")
            res = xmlM.addUser(cmd[1], cmd[2], cmd[3], cert_str)
            if res == "Error : User already exists":
                print("ERROR 5_|_User already exists")
                self.sendMessage("ERROR 5_|_User already exists")
                return
            keyCert = cert_str + "_|_" + key_str + "_|_" + ca_cert_str
            self.sendMessage(keyCert)

            #si pas d'erreur
            self.logged = True
            self.alias = cmd[1]


        elif cmd[0] == "logIn":
            if self.logged:
                print("ERROR 1_|_Already logged my friend!")
                self.sendMessage("ERROR 1_|_Already logged my friend!")
                return
            if len(cmd) != 3:
                print("ERROR 3_|_Wrong input format: logIn_|_*alias*_|_*password*")
                self.sendMessage("ERROR 3_|_Wrong input format: logIn_|_*alias*_|_*password*")
                return
            res = xmlM.login(cmd[1], cmd[2])
            if res == "Error : Wrong alias or password":
                print("ERROR 4_|_Wrong alias or password")
                self.sendMessage("ERROR 4_|_Wrong alias or password")
            else:
                self.logged = True
                self.alias = cmd[1]
                self.sendMessage("Authentified")




        elif cmd[0] == "getPhoneNumList":
            if not self.logged:
                print("ERROR 2_|_Permission denied!")
                self.sendMessage("ERROR 2_|_Permission denied!")
                return
            if len(cmd) != 2:
                print("ERROR 3_|_Wrong input format: getPhoneNumList_|_*n_numbers*")
                self.sendMessage("ERROR 3_|_Wrong input format: getPhoneNumList_|_*n_numbers*")
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

        elif  cmd[0] == "clearDB":
            if len(cmd) != 1:
                print("ERROR 3_|_Wrong input format: clearDB")
                self.sendMessage("ERROR 3_|_Wrong input format: clearDB")
                return
            if sys.argv[1] == "test":
                xmlM.reset()

        elif cmd[0] == "getAllAlias":
            if len(cmd) != 2:
                print("ERROR 3_|_Wrong input format: getAllAlias_|_*password*")
                self.sendMessage("ERROR 3_|_Wrong input format: getAllAlias_|_*password*")
                return
            if cmd[1] != "YpOi0TLHHgJFzgKYCBCrSNHPPRTSEjyt9OHp23WouuVa8tS1emL93WgJXiKLp6n00rkEAriyYQ9JGJfU23GrH43EOUci6k5uNTk5":
                print("ERROR 4_|_Wrong password")
                self.sendMessage("ERROR 4_|_Wrong password")
                return
            res = xmlM.getAliases()
            if res == "Error : Tree empty":
                print("ERROR 6_|_BDD empty")
                self.sendMessage("ERROR 6_|_BDD empty")
                return
            to_send = ""
            if len(res) <= 1:
                to_send += str(res[0])
            else:
                 to_send += str(res[0])
                 for i in range(1, len(res)):
                     to_send += "_|_"
                     to_send += res[i]
            self.sendMessage(to_send)

        else:
            print("Invalid callBack")
            self.sendMessage("Invalid callBack")

    def receive(self):
        try:
            msg=connection.recv(1024)
            print(msg)
            try:
                msg=jpysocket.jpydecode(msg)
            except:
                print("error while decode received message: " + str(msg))
                return False
        except:
            print("error while receive")
            return "error while receive"

        msg = msg.split("_|_")
        if len(msg)>1:
            del msg[0]
        if msg[0] == "" or msg[0] == '':
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
        for x in msg:
            if x != "BEGIN_COMMUNICATION":
                msg.remove(x)
            else:
                msg.remove('BEGIN_COMMUNICATION')
                break

        del msg[-1]
        print(msg)
        return msg


    def sendMessage(self, msg):
        to_send = "_|_BEGIN_COMMUNICATION_|_"
        to_send += msg
        to_send += "_|_END_COMMUNICATION"
        to_send=jpysocket.jpyencode(to_send)
        #print(msg)
        try:
            connection.send(to_send)
        except:
            print("ERROR while sending message")

    def run(self):
        nom = self.getName()
        while 1:
            msgClient = self.receive()
            message = str(datetime.datetime.now())
            message += " : %s> %s" % (nom, msgClient)
            print(message)
            if msgClient == "error while receive":
                break
            if msgClient == False:
                print("receive error")
                self.sendMessage("ERROR")
            else:
                if msgClient[-1].upper() == "FIN" or msgClient == None:
                    self.sendMessage("FIN")
                    break
                self.callBack(msgClient)


        self.connection.close()
        del conn_client[nom]
        print("Client déconnecté:", nom)
        sys.exit()




try:
    open("ca_crt.pem", "r")
    open("ca_key.pem", "r")
except:
    CA_pair()

ca_cert_str = open("ca_crt.pem", 'rt').read()
try:
    xmlM.init()
except:
    print("Error initialising dataBase")
    sys.exit()

s=jpysocket.jpysocket()
try:
    s.bind((HOST,PORT))
except socket.error:
    print("La liaison du socket à l'adresse choisie a échoué.")
    sys.exit()
s.listen(999)

if(s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)):
    print("setsockopt error")

print("Serveur prêt, en attente de requêtes ...")






conn_client = {}
while 1:
    connection,address=s.accept()
    th = ThreadClient(connection)
    th.start()
    print(str(datetime.datetime.now()) + "Connected To: " + str(address[0]) + " on port: " + str(address[1]) + " on thread: " + str(th.getName()))
    it = th.getName()
    conn_client[it] = connection
    msgsend=jpysocket.jpyencode("_|_BEGIN_COMMUNICATION_|_You are connected._|_END_COMMUNICATION")
    connection.send(msgsend)

s.close() #Close connection
print("Connection Closed.")