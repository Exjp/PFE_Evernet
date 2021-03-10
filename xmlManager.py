import xml.etree.ElementTree as ET

import os
import random
import bcrypt
import re

def init():
    if not os.path.isfile('page.xml'):
        emptyXml()
    global tree
    tree = ET.parse('page.xml')
    global root
    root = tree.getroot()

def reset():
    emptyXml()
    global tree
    tree = ET.parse('page.xml')
    global root
    root = tree.getroot()

def treeWrite():
    tree.write('page.xml', encoding="utf-8", xml_declaration=True)


def emptyXml():
    rootEmpty = ET.Element("users")
    treeEmpty = ET.ElementTree(rootEmpty)
    treeEmpty.write("page.xml",
           xml_declaration=True,encoding='utf-8',
           method="xml")

def aliasUnique(aliasValue):
    unique = True
    for elem in root:
        if elem.attrib['alias'] == aliasValue:
            unique = False
    return unique

def numberUnique(numberValue):
    unique = True
    for elem in root:
        if elem.attrib['number'] == numberValue:
            
            unique = False
    return unique

def formatNumber(number):
    if re.match( r'\+?(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)?\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*(\d{1,2})$', number) == None:
        return False
    return True

def keyUnique(keyValue):
    unique = True
    for elem in root:
        if elem.attrib['key'] == keyValue:
            unique = False
    return unique


# vérifier que les champs sont corrects
# return string sur les fonction selon l'erreur
def addUser(aliasValue, passValue, numberValue, keyValue):
    if aliasUnique(aliasValue) and numberUnique(numberValue) and keyUnique(keyValue) and formatNumber(numberValue):
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
    else :
        return "Error : User already exists"


# return un erreur si pas trouvé, nullptr, verif le nom en entrée
def removeUserFromName(name):
    for elem in root:
        if elem.attrib['alias'] == name:
            root.remove(elem)
    return "Error : User not found"

# return un erreur si pas trouvé, nullptr, verif le nom en entrée
def removeUserFromNumber(number):
    for elem in root:
        if elem.attrib['number'] == number:
            root.remove(elem)
    return "Error : User not found"

# return une info si utilisateur banni
def login(alias, password):
    for elem in root:
        if elem.attrib['alias'] == alias:
            if bcrypt.checkpw(password.encode('utf8'), elem.attrib['password'].encode()):
                return True
    return "Error : Wrong alias or password"


#return erreur si deja unban avant l'ecriture
def banUser(alias):
    for elem in root:
        if elem.attrib['alias'] == alias:
            elem.attrib['banned'] = "True"
    return "Error : alias not found"

#return erreur si deja unban avant l'ecriture
def unBanUser(alias):
    for elem in root:
        if elem.attrib['alias'] == alias:
            elem.attrib['banned'] = "False"
    return "Error : alias not found"

# erreur si existe pas ?
def isBanned(alias):
    for elem in root:
        if elem.attrib['alias'] == alias and elem.attrib['banned'] == "True":
            return True
    return False

def exists(alias):
    for elem in root:
        if elem.attrib['alias'] == alias:
            return True
    return False


# verifier les noms en entrée (nullptr, trop gros, non utf8) / erreur differente si l user est ban
def getNumberFromAlias(name):
    for elem in root:
        if elem.attrib['alias'] == name and elem.attrib['banned'] == "False":
            return elem.attrib['number']
    return "Error : alias not found"


def getAliasFromNumber(number):
    if re.match( r'\+?(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)?\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*(\d{1,2})$', number) == None:
        return "Error : Wrong number format"

    for elem in root:
        if elem.attrib['number'] == number and elem.attrib['banned'] == "False":
            return elem.attrib['alias']
    return "Error : number not found"

#verifier les noms en entrée (nullptr, trop gros, non utf8)
def getKeyFromAlias(name):
    for elem in root:
        if elem.attrib['alias'] == name and elem.attrib['banned'] == "False":
            return elem.attrib['key']
    return "Error : alias not found"


def getAliases():
    listAliases = [elem.attrib['alias'] for elem in root]
    if listAliases == []:
        return "Error : Tree empty"
    return listAliases


def randomUsers(num,sender):
    listAlias = getAliases()
    if listAlias == "Error getAliases() : Tree empty":
        return "Error : randoTree empty"
    try:
        listAlias.pop(listAlias.index(sender))
    except IndexError:
        return "Error : Index Error"
    except ValueError:
        return "Error : Sender is not in the tree"

    num = int(num)
    sizeListAlias = len(listAlias)
    tmpList = [[0 for x in range(2)] for y in range(num)]


    if num > sizeListAlias & num <= 0:
        return "Error : Not enough numbers in database..."

    cnt=0
    aleaIndList = random.sample(range(sizeListAlias), num)

    for i in aleaIndList:
        tmpList[cnt][0] = getNumberFromAlias(listAlias[i])
        tmpList[cnt][1] = getKeyFromAlias(listAlias[i])
        cnt = cnt + 1
    return tmpList


def getInvitationKey(name):
    return "TODO"


def verifyInvitationKey(invitation_key):
    return invitation_key == "martin"


def main():
   print("C'est la faute de Jak.")

if __name__ == "__main__":
    init()
    main()

