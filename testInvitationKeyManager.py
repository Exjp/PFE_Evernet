from invitationKeyManager import *

def testAddKey():
    cpt = 0
    key = addKey("Thierry","20-04-2021","20")
    
    if signup(key) != True:
        print("error addKey 1")
        cpt = cpt + 1

    if(addKey("Thierry","20-04-2021","20") != "Error : A key already exists for this alias"):
        print("error addKey 2")
        cpt = cpt + 1
    if(addKey("Pierre","00-00-0000","20") != "Error : Date format incorrect"):
        print("error addKey 3")
        cpt = cpt + 1
    if(addKey("Pierre","20-04-2021","-20") != "Error : Negative uses value"):
        print("error addKey 4")
        cpt = cpt + 1
    if(addKey("Pierre","20-04-2021","aaaa") != "Error : number of uses is not an integer"):
        print("error addKey 5")
        cpt = cpt + 1
    
    return cpt

def testRemoveKey():
    cpt = 0
    key = addKey("Oscar","20-04-2021","20")

    if(removeKey(key) != True):
        print("error removeKey 1")
        cpt = cpt + 1
    treeWrite()
    if(signup(key) != "Error : Key not found"):
        print("error removeKey 2")
        cpt = cpt + 1
    if(removeKey("aaaa") != "Error : Key not found"):
        print("error removeKey 3")
        cpt = cpt + 1

    return cpt

def testCleanup():
    cpt = 0
    key = addKey("Clément","20-02-2021","20")
    cleanup()
    if(signup(key) != "Error : Key not found"):
        print("error cleanup 1")
        cpt = cpt + 1

    key = addKey("Jeremy","0","20")
    if(signup(key) != True):
        print("error cleanup 2")
        cpt = cpt + 1

    key = addKey("Clément","20-04-2021","20")
    if(signup(key) != True):
        print("error cleanup 2")
        cpt = cpt + 1
    return cpt

def testSignup():
    cpt = 0
    key = addKey("Alex","20-04-2021","20")
    if(signup(key) != True):
        print("error signup 1")
        cpt = cpt + 1

    if(signup("aaaa") != "Error : Key not found"):
        print("error signup 2")
        cpt = cpt + 1
    
    key = addKey("Jacques","20-04-2021","1")
    signup(key)
    if(signup(key) != "Error : Key not found"):
        print("error signup 3")
        cpt = cpt + 1
    
    return cpt


def initTest():
    init()
    funcList = []
    funcList.append(testAddKey())
    funcList.append(testRemoveKey())
    funcList.append(testCleanup())
    funcList.append(testSignup())
    return funcList

if __name__ == '__main__':
    if os.path.isfile('invitation.xml'):
        os.remove("invitation.xml")
    cpt = 0
    funcList = initTest()
    print("Début des Tests Unitaires : ",len(funcList))
    for func in funcList:
        tmp = func
        if(tmp > 0):
            cpt = cpt + tmp
    print("test non passé : ",cpt)

