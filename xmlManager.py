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

def keyUnique(keyValue):
    unique = True
    for elem in root:
        if elem.attrib['key'] == keyValue:
            unique = False
    return unique


# vérifier que les champs sont corrects
# return string sur les fonction selon l'erreur, ou un string (ou juste true) qui dit que c'est bon / message si l'alias dans login() existe
# -> a faire dans toutes les fonctions appelees par le client
def addUser(aliasValue, passValue, numberValue, keyValue):
    if aliasUnique(aliasValue) and numberUnique(numberValue) and keyUnique(keyValue):
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
        return "User already exists"


# return un erreur si pas trouvé, nullptr, verif le nom en entrée
def removeUserFromName(name):
    for elem in root:
        if elem.attrib['alias'] == name:
            root.remove(elem)
    return "Error : User not found"

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
    return "Wrong alias or password"


#return erreur si non trouve ou deja ban(et ecrit pas du coup)
def banUser(alias):
    for elem in root:
        if elem.attrib['alias'] == alias:
            elem.attrib['banned'] = "True"
    return "Error : alias not found or already ban"

#return erreur si non trouve ou deja unban(et ecrit pas du coup)
def unBanUser(alias):
    for elem in root:
        if elem.attrib['alias'] == alias:
            elem.attrib['banned'] = "False"
    return "Error : alias not found or already unban"

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


# verif que les user soient pas ban avant de les renvoyer
# verifier les noms en entrée (nullptr, trop gros, non utf8)
def getNumberFromAlias(name):
    for elem in root:
        if elem.attrib['alias'] == name and elem.attrib['banned'] == "False":
            return elem.attrib['number']
    return "Error : alias not found"

# verifier les numeros en entrée
def getAliasFromNumber(number):
    if re.match( r'/([0-9\s\-]{7,})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?$/', number, re.M|re.I):
        return "Wrong number format"
    
    for elem in root:
        if elem.attrib['number'] == number and elem.attrib['banned'] == "False":
            return elem.attrib['alias']
    return "Error : number not found"

#verifier les noms en entrée (nullptr, trop gros, non utf8)
def getKeyFromAlias(name):
    for elem in root:
        if elem.attrib['alias'] == name and elem.attrib['banned'] == "False":
            return elem.attrib['key']
    return "Error getKeyFromAlias : alias not found"


#return une liste des alias dans la bdd, erreur si y'a personne dans la bdd
#pas teste
def getAliases():
    listAliases = [elem.attrib['alias'] for elem in root]
    if listAliases == []:
        return "Error getAliases() : Tree empty"
    return listAliases

#erreur si le sender est ban (try catch avec isBanned(sender) / erreur si le sender existe pas
def randomUsers(num,sender):
    listAlias = getAliases()
    if listAlias == "Error getAliases() : Tree empty":
        return "Error randomUsers() : randoTree empty"
    try:    
        listAlias.pop(listAlias.index(sender))
    except IndexError:
        return "Error randomUsers() : Index Error"
    except ValueError:
        return "Error randomUsers() : Sender is not ine the tree"
    
    num = int(num)
    sizeListAlias = len(listAlias)
    tmpList = [[0 for x in range(2)] for y in range(num)]


    if num > sizeListAlias & num <= 0:
        return "Error randomUsers() : Not enough numbers in database..."

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
    
if __name__ == "__main__":
    init()
    main()
