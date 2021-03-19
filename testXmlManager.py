from xmlManager import * 
    

        
def testInit(): ###### init()
    cpt = 0
    init()
    ("Martine&Joçelin","mdp", "+33669664628", "kay")
    init()
    if(len(getAliases()) == 1):
        print("error init 1")
        cpt = cpt + 1
    
    return cpt


def testEmptyXml(): ###### emptyXml()
    cpt = 0
    emptyXml()
    addUser("Gérard","mdp", "+336349664628", "koy")
    print(getAliases())
    if(len(getAliases()) != 0):
        print("error emptyXml 1")
        cpt = cpt + 1
    return cpt
def testReset(): ###### reset()
    cpt = 0
    addUser("Gérard","mdp", "+336349664628", "koy")

    reset()

    if(getAliases() != "Error : Tree empty"):
        print("error reset 1")
        cpt = cpt + 1

    return cpt

def testRandomUser(): ###### randomUsers() 
    cpt = 0
    if(randomUsers(2,"Alexa") != "Error : Tree empty"):
        print("error randomUsers 1")
        cpt = cpt + 1

    addUser("Paul","mdp", "+33669664626", "k")

    if(randomUsers(2,"Paul") != "Error : Not enough numbers in database..."):
        print("error randomUsers 2")
        cpt = cpt + 1

    addUser("Martine","mdp", "+33669664628", "k2")

    if(randomUsers(1,"Alexa") != "Error : Sender is not in the tree"):
        print("error randomUsers 3")
        cpt = cpt + 1

    addUser("Quentin","mdp", "+33669164628", "k3")
    addUser("Valentin","mdp", "+33069164628", "k4")

    lst1 = getAliases()
    lst2 = randomUsers(2,"Paul")
    for i in lst2:
        check = False
        for j in lst1:        
            if(getAliasFromNumber(i[0]) == j):
                if(check == True):
                    print("error randomUser 4")
                    cpt = cpt + 1
                check = True
        if(check == False):
            print("error randomUsers 5")
            cpt = cpt + 1
    return cpt


def testGetAliases(): ###### getAliases()
    cpt = 0
    reset()
    if(getAliases() != "Error : Tree empty"):
        print("error getAliases 1")
        cpt = cpt + 1

    addUser("Arnaud","mdp", "+33666646266", "ke1")
    addUser("Aranud","mdp", "+33646666266", "ke2")
    addUser("Arunad","mdp", "+33664666266", "ke3")
    lst1 = ["Arnaud","Aranud","Arunad"]
    lst2 = getAliases()
    for i in range(0,len(lst1)):
        if(lst1[i] != lst2[i]):
            print("error getAliases 2")
            cpt = cpt + 1
            break
    reset()
    if(randomUsers(2,"Alexa") != "Error : Tree empty"):
        print("error getAliases 3")
        cpt = cpt + 1

    return cpt

def testAddUser(): ###### addUser()
    cpt = 0
    addUser("Thierry","mdp", "+33666666266", "key")

    list = getAliases()
    if( list[0] != "Thierry"):
        print("error adduser 1")
        cpt = cpt + 1
    if(login("Thierry","mdp") == "Error : Wrong alias or password"):
        print("error adduser 2")
        cpt = cpt + 1
    if(getNumberFromAlias("Thierry") != "+33666666266"):
        print("error adduser 3")
        cpt = cpt + 1
    if(getKeyFromAlias("Thierry") != "key"):
        print("error adduser 4")
        cpt = cpt + 1

    if( addUser("Thierry","mdp", "+33666666266", "key2") != "Error : Alias already exists"):
        print("error addUser 5")
        cpt = cpt + 1
    if( addUser("Thierry2","mdp", "+33666666266", "key3") != "Error : Number already exists"):
        print("error addUser 6")
        cpt = cpt + 1
    if( addUser("Thierry3","mdp", "+33666666222", "key") != "Error : Key already exists"):
        print("error addUser 7")
        cpt = cpt + 1
    if( addUser("Thierry4","mdp", "+336666662260000000", "key4") != "Error : Number format incorrect"):
        print("error addUser 8")
        cpt = cpt + 1
    if( addUser("Thierry5","", "+33666666229", "key41") != "Error : Empty password"):
        print("error addUser 9")
        cpt = cpt + 1

    return cpt

def testAliasUnique(): ###### aliasUnique()
    cpt = 0
    if(aliasUnique("Pierre") == False):
        print("error aliasUnique 1")
        cpt = cpt + 1

    addUser("Pierre","mdp2", "+33666666226", "key5")

    if(aliasUnique("Pierre") != False):
        print("error aliasUnique 2")
        cpt = cpt + 1

    return cpt

def testnumberUnique(): ###### numberUnique()
    cpt = 0
    if(numberUnique("+33266666222") == False):
        print("error numberUnique 1")
        cpt = cpt + 1

    addUser("Charles","mdp3", "+33266666222", "key6")

    if(numberUnique("+33266666222") != False):
        print("error numberUnique 2")
        cpt = cpt + 1
    
    return cpt

def testKeyUnique() :###### keyUnique() 
    cpt = 0
    if(keyUnique("key") != False):
        print("error keyUnique 1")
        cpt = cpt + 1

    addUser("Marcelin","mdp4", "+33666662222", "key7")    
    if(keyUnique("key7") != False):
        print("error keyUnique 2")
        cpt = cpt + 1

    return cpt

def testRemoveUserFromName(): ###### removeUserFromName()
    cpt = 0
    addUser("Jean","mdp5", "+33662622222", "key8")

    removeUserFromName("Jean")
    if(aliasUnique("Jean") == False):
        print("error removeUserFromName 1")
        cpt = cpt + 1
    if(removeUserFromName("Jean") != "Error : User not found"):
        print("error removeUserFromName 2")
        cpt = cpt + 1
    
    return cpt

def testRemoveUserFromNumber(): ###### removeUserFromNumber()
    cpt = 0
    addUser("Jean","mdp5", "+33662622222", "key9")

    removeUserFromNumber("+33662622222")
    if(aliasUnique("Jean") == False):
        print("error removeUserFromNumber 1")
        cpt = cpt + 1
    if(removeUserFromName("+33662622222") != "Error : User not found"):
        print("error removeUserFromNumber 2")
        cpt = cpt + 1
    
    return cpt

def testLogin(): ###### login()
    cpt = 0
    addUser("Philippe","mdp", "+33662222222", "key10")
    if(login("Philippe","mdp") != True):
        print("error login 1")
        cpt = cpt + 1
    if(login("Philippe","fmdp") != "Error : Wrong alias or password"):
        print("error login 2")
        cpt = cpt + 1
    
    return cpt

def testBanUser(): ###### banUser()
    cpt = 0
    addUser("Alex","mdp","0626575578","key11")
    banUser("Alex")
    if(isBanned("Alex") != True):
        print("error banUser 1")
        cpt = cpt + 1
    if(banUser("Alexa") != "Error : alias not found"):
        print("error banUser 2")
        cpt = cpt + 1
    
    return cpt

def testUnBanUser(): ###### unBanUser()
    cpt = 0
    addUser("Jacques","mdp","0622675578","key12")
    banUser("Jacques")
    unBanUser("Jacques")

    if(isBanned("Jacques") != False):
        print("error unBanUser 1")
        cpt = cpt + 1

    if(unBanUser("Alexa") != "Error : alias not found"):
        print("error banUser 2")
        cpt = cpt + 1
    
    return cpt

def testIsBanned(): ###### isBanned()
    cpt = 0
    addUser("Ghislain","mdp","0626275578","key13")
    if(isBanned("Ghislain") != False):
        print("error isBanned 1")
        cpt = cpt + 1

    banUser("Ghislain")
    if(isBanned("Ghislain") != True):
        print("error isBanned 2")
        cpt = cpt + 1
    
    return cpt

def testExists(): ###### exists()
    cpt = 0
    addUser("Jeremy","mdp","0626275573","key14")
    if(exists("Jeremy") != True):
        print("error exists 1")
        cpt = cpt + 1

    if(exists("Alexa") != False):
        print("error exists 2")
        cpt = cpt + 1

    return cpt


def testgetNumberFromAlias(): ###### getNumberFromAlias()
    cpt = 0
    addUser("Clément","mdp","0622275573","key15")
    if(getNumberFromAlias("Clément") != "0622275573"):
        print("error getNumberFromAlias 1")
        cpt = cpt + 1

    if(getNumberFromAlias("Alexa") != "Error : alias not found"):
        print("error getNumberFromAlias 2")
        cpt = cpt + 1
    
    return cpt

def testgetKeyFromAlias(): ###### getKeyFromAlias()
    cpt = 0
    addUser("Martin","mdp","0622273573","key16")
    if(getKeyFromAlias("Martin") != "key16"):
        print("error getKeyFromAlias 1")
        cpt = cpt + 1

    if(getKeyFromAlias("Alexa") != "Error : alias not found"):
        print("error getKeyFromAlias 2")
        cpt = cpt + 1
    
    return cpt

def testFormatNumber():###### formatNumber()
    cpt = 0
    if(formatNumber("+33626436690") != True):
        print("error formatNumber 1")
        cpt = cpt + 1
        
    if(formatNumber("0626436690") != True):
        print("error formatNumber 2")
        cpt = cpt + 1

    if(formatNumber("0626436690123") != False):
        print("error formatNumber 3")
        cpt = cpt + 1
    
    return cpt

def initTest():
    funcList = []
    funcList.append(testInit())
    # funcList.append(testEmptyXml())   #TODO
    funcList.append(testReset())
    funcList.append(testRandomUser())
    funcList.append(testGetAliases())
    funcList.append(testAddUser())
    funcList.append(testAliasUnique())
    funcList.append(testnumberUnique())
    funcList.append(testKeyUnique())
    funcList.append(testRemoveUserFromName())
    funcList.append(testRemoveUserFromNumber())
    funcList.append(testLogin())
    funcList.append(testBanUser())
    funcList.append(testUnBanUser())
    funcList.append(testIsBanned())
    funcList.append(testExists())
    funcList.append(testgetNumberFromAlias())
    funcList.append(testFormatNumber())
    return funcList

if __name__ == '__main__':
    if os.path.isfile('page.xml'):
        os.remove("page.xml")
    cpt = 0
    funcList = initTest()
    print("Début des Tests Unitaires : ",len(funcList))
    for func in funcList:
        tmp = func
        if(tmp > 0):
            cpt = cpt + tmp
        # reset()
    print("test pas passé : ",cpt)

