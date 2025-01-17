import sys, threading, os, datetime, time, socket
import xmlManager as xmlM
import invitationKeyManager as iKM
from pairUtils import *
import rsaUtils as ru
import jpysocket

crypted = False


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
    if sys.argv[1] == "crypted":
        HOST = '192.168.1.44'
        PORT = 50002
        crypted = True
    if sys.argv[1] == "localhost2":
        HOST = 'localhost'
        PORT = 50002
        crypted = True
print("HOST: " + HOST + " Port: " + str(PORT))



class ThreadClient(threading.Thread):
    """class tha manage client connection
    """
    def __init__(self, conn):
        """the initialization of a ThreadClient object
        Args:
            conn: the object that contain de pipe open with a client
        """
        threading.Thread.__init__(self)
        self.connection = conn
        self.logged = False
        self.alias = None


    def callBack(self, commande):
        """analyse and respond to a client request
        Args:
            commande (list of string): the callback and its agruments
        """
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
            if len(cmd) == 1:
                self.sendMessage("martin")
                return
            if len(cmd) != 3:
                print("ERROR 3_|_Wrong input format: getInvitationKey_|_*end_date(jj-mm-yyyy)*_|_*nbOfUse*")
                self.sendMessage("ERROR 3_|_Wrong input format: getInvitationKey_|_*end_date(jj-mm-yyyy)*_|_*nbOfUse*")
                return

            res = iKM.addKey(self.alias, cmd[1], cmd[2])
            if res == "Error : A key already exists for this alias":
                print("ERROR 9_|_you already have an invitation key")
                self.sendMessage("ERROR 9_|_you already have an invitation key")
                return
            if res == "Error : Date format incorrect":
                print("ERROR 9_|_Date format incorrect")
                self.sendMessage("ERROR 9_|_Date format incorrect")
                return
            if res == "Error : Negative uses value":
                print("ERROR 9_|_nbOfUse can't be negative")
                self.sendMessage("ERROR 9_|_nbOfUse can't be negative")
                return
            if res == "Error : number of uses is not an integer":
                print("ERROR 9_|_number of uses should be an integer")
                self.sendMessage("ERROR 9_|_number of uses should be an integer")
                return

            self.sendMessage(res)



        elif cmd[0] == "signIn":
            if self.logged:
                print("ERROR 1_|_Already logged my friend!")
                self.sendMessage("ERROR 1_|_Already logged my friend!")
                return
            if len(cmd) != 5:
                print("ERROR 3_|_Wrong input format: signIn_|_*alias*_|_*password*_|_*phoneNum*_|_*invitationKey*")
                self.sendMessage("ERROR 3_|_Wrong input format: signIn_|_*alias*_|_*password*_|_*phoneNum*_|_*invitationKey*")
                return
            resKey = iKM.signup(cmd[4])
            if resKey == "Error : Key not found":
                if cmd[4] != "martin":
                    print("ERROR 8_|_Wrong invitation key")
                    self.sendMessage("ERROR 8_|_Wrong invitation key")
                    return

            client_pair(cmd[1])
            cert_str = open(cmd[1]+"_crt.pem", 'rt').read()
            key_str = open(cmd[1]+"_key.pem", 'rt').read()

            os.remove(cmd[1]+"_crt.pem")
            os.remove(cmd[1]+"_key.pem")

            res = xmlM.addUser(cmd[1], cmd[2], cmd[3], cert_str)
            if res == "Error : Alias already exists":
                print("ERROR 5_|_Alias already exists")
                self.sendMessage("ERROR 5_|_Alias already exists")
                return
            elif res == "Error : Number already exists":
                print("ERROR 5_|_Number already exists")
                self.sendMessage("ERROR 5_|_Number already exists")
                return
            elif res == "Error : Key already exists":
                print("ERROR 5_|_Key already exists")
                self.sendMessage("ERROR 5_|_Key already exists")
                return
            elif res == "Error : Number format incorrect":
                print("ERROR 3_|_Number format incorrect")
                self.sendMessage("ERROR 3_|_Number format incorrect")
                return
            else:
                keyCert = cert_str + "_|_" + key_str + "_|_" + ca_cert_str
                self.sendMessage(keyCert)

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
            if list == "Error : Tree empty":
                print("ERROR 7_|_Database error: Data base empty")
                self.sendMessage("ERROR 7_|_Database error: Data base empty")
                return
            if list == "Error : Not enough numbers in database...":
                print("ERROR 7_|_Database error: Not enough numbers in database")
                self.sendMessage("ERROR 7_|_Database error: Not enough numbers in database")
                return
            if list == "Error : Index Error" or list == "Error : Sender is not in the tree":
                print("ERROR 7_|_Database error: error on database side")
                self.sendMessage("ERROR 7_|_Database error: error on database side")
                return

            if len(list) <1:
                return False
            if len(list) == 1:
                strList = ""
                strList += list[0][0]
                strList += list[0][1]
            else:
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
                return
            if sys.argv[1] == "test":
                xmlM.reset()
                iKM.reset()


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
        """receive communication from client, analyse and format it
        Returns:
            list of string : the request and its parameters
        """
        global crypted
        try:
            msg=connection.recv(1024)
        except:
            print("error while receive")
            return "error while receive"

        try:
            msg=msg.decode("utf-8", errors="ignore")
        except:
            print("error while decode received message: " + str(msg))
            return False
        msg = msg.split("_|_")
        if len(msg)>1:
            del msg[0]
        if msg[0] == "" or msg[0] == '':
            self.connection.close()
            del conn_client[self.getName()]
            print("Client disconnected unexpectedly:", self.getName())
            sys.exit()
        if msg[0] != "BEGIN_COMMUNICATION":
            self.connection.close()
            del conn_client[self.getName()]
            print("Forced disconnection caused by no BEGIN_COMMUNICATION found : ", self.getName())
            sys.exit()
        while msg[-1] != "END_COMMUNICATION":
            try:
                tmp = connection.recv(1024)

                try:
                    tmp = tmp.decode("utf-8", errors="ignore")
                    msg += tmp.split("_|_")
                except:
                    print("error while decode received message: " + str(msg) + " + " + str(tmp))
                    return False
            except:
                print("error while receive 2")
                return "error while receive 2"
        del msg[-1]
        if(crypted and self.logged):
            to_decrypt = ""
            for i in range(1,len(msg)):
                to_decrypt += msg[i]
            tmp = ru.decrypt(to_decrypt)
            to_return = msg[0].split("_|_")
            to_return += tmp.decode("utf-8").split("_|_")
            del to_return[0]
            return to_return
        del msg[0]
        return msg


    def sendMessage(self, msg):
        """Send a message to the client
        Args:
            msg: the string to be sent
        """
        global crypted
        to_send = "_|_BEGIN_COMMUNICATION_|_"
        if crypted and self.logged:
            msg = msg.encode()
            print("tosendmessage :" + str(msg))
            tmp = ru.encrypt(msg, self.alias)
            tmp = tmp.decode("utf-8")
            to_send += tmp
        else:
            to_send += msg
        to_send += "_|_END_COMMUNICATION"
        to_send=jpysocket.jpyencode(to_send)
        try:
            connection.send(to_send)
        except:
            print("ERROR while sending message")

    def run(self):
        """the function that is called after the creation of a thread.
        """
        nom = self.getName()
        while 1:
            msgClient = self.receive()
            message = str(datetime.datetime.now())
            message += " : %s> %s:" % (nom, msgClient)
            print(message)
            if msgClient == "error while receive":
                break
            if msgClient == False:
                print("decode/split error")
                self.sendMessage("ERROR")
            else:
                if str(msgClient[-1]).upper() == "FIN" or msgClient == None:
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
    iKM.init()
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
    iKM.cleanup()
    th = ThreadClient(connection)
    th.start()
    print("\n" + str(datetime.datetime.now()) + " Connected To: " + str(address[0]) + " on port: " + str(address[1]) + " on thread: " + str(th.getName()) + "\n")
    it = th.getName()
    conn_client[it] = connection
    msgsend=jpysocket.jpyencode("_|_BEGIN_COMMUNICATION_|_You are connected._|_END_COMMUNICATION")
    try:
        connection.send(msgsend)
    except:
        print("client disconnected before welcome")

s.close() #Close connection
print("Connection Closed.")
