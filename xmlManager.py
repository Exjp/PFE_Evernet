import xml.etree.ElementTree as ET

import os
import random
import bcrypt
import re

def init():
    """initialize the database
    """
    if not os.path.isfile('page.xml'):
        emptyXml()
    global tree
    tree = ET.parse('page.xml')
    global root
    root = tree.getroot()

def reset():
    """erase and recreate the tree in the database 
    """
    emptyXml()
    global tree
    tree = ET.parse('page.xml')
    global root
    root = tree.getroot()

def treeWrite():
    """write the current tree in the database
    """
    tree.write('page.xml', encoding="utf-8", xml_declaration=True)


def emptyXml():
    """empty the tree in the database
    """
    rootEmpty = ET.Element("users")
    treeEmpty = ET.ElementTree(rootEmpty)
    treeEmpty.write("page.xml",
           xml_declaration=True,encoding='utf-8',
           method="xml")

def aliasUnique(aliasValue):
    """test if the alias is not already in the database

    Args:
        aliasValue (String)

    Returns:
        Boolean
    """
    unique = True
    for elem in root:
        if elem.attrib['alias'] == aliasValue:
            unique = False
    return unique

def numberUnique(numberValue):
    """test if the phone number is not already in the database

    Args:
        numberValue (String): the phone number

    Returns:
        Boolean
    """
    unique = True
    for elem in root:
        if elem.attrib['number'] == numberValue:
            unique = False
    return unique

def formatNumber(number):
    """test if the phone number have a good format

    Args:
        number (String): the phone number

    Returns:
        Boolean
    """
    if re.match( r'\+?(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)?\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*(\d{1,2})$', number) == None:
        return False
    return True

def keyUnique(keyValue):
    """test if the certificate is not already in the database

    Args:
        keyValue (String): the certificate

    Returns:
        Boolean
    """
    unique = True
    for elem in root:
        if elem.attrib['key'] == keyValue:
            unique = False
    return unique


def addUser(aliasValue, passValue, numberValue, keyValue):
    """function to add an user in the database

    Args:
        aliasValue (String)
        passValue (String): the password
        numberValue (String): the phone number
        keyValue (String): the certificate

    Returns:
        Boolean
    """
    if aliasUnique(aliasValue) != True:
        return "Error : Alias already exists"
    if numberUnique(numberValue) != True:
        return "Error : Number already exists"
    if keyUnique(keyValue) != True:
        return "Error : Key already exists"
    if formatNumber(numberValue) != True:
        return "Error : Number format incorrect"
    if len(passValue) == 0:
        return "Error : Empty password"
    user = ET.Element('user')
    user.set("alias", aliasValue)
    user.set("banned", "False")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(passValue.encode('utf-8'), salt)
    user.set("password", hashed_password.decode('utf8'))
    user.set("number", numberValue)
    user.set("key", keyValue)
    root.append(user)
    treeWrite()
    return True



def removeUserFromName(name):
    """remove an user with his alias

    Args:
        name (String): the alias

    Returns:
        Boolean
    """
    for elem in root:
        if elem.attrib['alias'] == name:
            root.remove(elem)
            treeWrite()
            return True
    return "Error : User not found"

def removeUserFromNumber(number):
    """remove an user with his phone number

    Args:
        number (String): the phone number

    Returns:
        Boolean
    """
    for elem in root:
        if elem.attrib['number'] == number:
            root.remove(elem)
            treeWrite()
            return True
    return "Error : User not found"

def login(alias, password):
    """test the login parameters if they belong to an user in the database

    Args:
        alias (String)
        password (String)

    Returns:
        Boolean
    """
    for elem in root:
        if elem.attrib['alias'] == alias:
            if bcrypt.checkpw(password.encode('utf8'), elem.attrib['password'].encode()):
                return True
    return "Error : Wrong alias or password"


def banUser(alias):
    """ban the alias of the network

    Args:
        alias (String)

    Returns:
        Boolean
    """
    for elem in root:
        if elem.attrib['alias'] == alias:
            elem.attrib['banned'] = "True"
            treeWrite()
            return True
    return "Error : alias not found"

def unBanUser(alias):
    """unban the alias of the network

    Args:
        alias (String)

    Returns:
        Boolean
    """

    for elem in root:
        if elem.attrib['alias'] == alias:
            elem.attrib['banned'] = "False"
            treeWrite()
            return True
    return "Error : alias not found"

def isBanned(alias):
    """test if the alias is banned of the network

    Args:
        alias (String)

    Returns:
        Boolean
    """
    for elem in root:
        if elem.attrib['alias'] == alias and elem.attrib['banned'] == "True":
            return True
    return False

def exists(alias):
    """test if the alias is in the database

    Args:
        alias (String)

    Returns:
        Boolean
    """
    for elem in root:
        if elem.attrib['alias'] == alias:
            return True
    return False


def getNumberFromAlias(name):
    """get the phone number from alias 

    Args:
        name (String): the alias

    Returns:
        String: the phone number
    """
    for elem in root:
        if elem.attrib['alias'] == name and elem.attrib['banned'] == "False":
            return elem.attrib['number']
    return "Error : alias not found"


def getAliasFromNumber(number):
    """get the alias from a phone number

    Args:
        number (String): phone number

    Returns:
        String: the alias
    """
    if re.match( r'\+?(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)?\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*(\d{1,2})$', number) == None:
        return "Error : Wrong number format"

    for elem in root:
        if elem.attrib['number'] == number and elem.attrib['banned'] == "False":
            return elem.attrib['alias']
    return "Error : number not found"

def getKeyFromAlias(name):
    """get the certificate of the alias

    Args:
        name (String): the alias

    Returns:
        String: the certificate
    """
    for elem in root:
        if elem.attrib['alias'] == name and elem.attrib['banned'] == "False":
            return elem.attrib['key']
    return "Error : alias not found"


def getAliases():
    """get all alias of the database

    Returns:
        list[alias]: list of alias
    """
    listAliases = [elem.attrib['alias'] for elem in root]
    if listAliases == []:
        return "Error : Tree empty"
    return listAliases

def randomUsers(num,sender):
    """give a list of a number of receptor, randomly sort

    Args:
        num (integer): the number of receptor
        sender (String): the alias of the sender

    Returns:
        list[receptor][number,key]: a list with receptor data
    """
    listAlias = getAliases()
    if listAlias == "Error : Tree empty":
        return "Error : Tree empty"
    
    num = int(num)
    sizeListAlias = len(listAlias) - 1
    
    if num > sizeListAlias & num <= 0:
        return "Error : Not enough numbers in database..."
    
    try:
        listAlias.pop(listAlias.index(sender))
    except IndexError:
        return "Error : Index Error"
    except ValueError:
        return "Error : Sender is not in the tree"

    tmpList = [[0 for x in range(2)] for y in range(num)]

    cnt=0
    aleaIndList = random.sample(range(sizeListAlias), num)

    for i in aleaIndList:
        try:
            tmpList[cnt][0] = getNumberFromAlias(listAlias[i])
        except "Error : alias not found":
            return "Error : alias not found"
        try:
            tmpList[cnt][1] = getKeyFromAlias(listAlias[i])
        except "Error : alias not found":
            return "Error : alias not found"
        cnt = cnt + 1
    return tmpList


def getInvitationKey(name):
    return "TODO"


def verifyInvitationKey(invitation_key):
    return invitation_key == "martin"


if __name__ == "__main__":
    init()

