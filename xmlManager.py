import xml.etree.ElementTree as ET

import os
import random
import bcrypt

def init():
    if not os.path.isfile('page.xml'):
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
        for var in elem:
            if var.text == numberValue:
                 unique = False
    return unique

def keyUnique(keyValue):
    unique = True
    for elem in root:
        for var in elem:
            if var.text == keyValue:
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
        
        password = ET.SubElement(user, "password")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(passValue.encode('utf-8'), salt)
        password.text = hashed_password.decode('utf8')
        
        number = ET.SubElement(user, "number")
        number.text = numberValue

        key = ET.SubElement(user, "key")
        key.text = keyValue

        root.append(user)
        treeWrite()
    else :
        print("User already exists")


def removeUserFromNumber(number):
    treeWrite()


# return un erreur si pas trouvé, nullptr, verif le nom en entrée
def removeUserFromName(name):
    for elem in root:
        if elem.attrib['alias'] == name:
            root.remove(elem)
    treeWrite()


# return une info si utilisateur banni
def login(alias, password):
    for elem in root:
        if elem.attrib['alias'] == alias:
            for var in elem:
                if var.tag == "password":
                    if bcrypt.checkpw(password.encode('utf8'), (var.text).encode()):
                        return True
    return False


#return erreur si non trouve ou deja ban(et ecrit pas du coup)
def banUser(alias):
    for elem in root:
        if elem.attrib['alias'] == alias:
            elem.attrib['banned'] = "True"
    treeWrite()

#return erreur si non trouve ou deja unban(et ecrit pas du coup)
def unBanUser(alias):
    for elem in root:
        if elem.attrib['alias'] == alias:
            elem.attrib['banned'] = "False"
    treeWrite()

# erreur si existe pas ?
def isBanned(alias):
    for elem in root:
        if elem.attrib['alias'] == alias and elem.attrib['banned'] == "False":
            return True
    return False

# verif que les user soient pas ban avant de les renvoyer
# verifier les noms en entrée (nullptr, trop gros, non utf8)
def getNumberFromAlias(name):
    for elem in root:
        if elem.attrib['alias'] == name and elem.attrib['banned'] == "False":
            for var in elem:
                if var.tag == "number":
                    return var.text
    return "Error : alias not found"

# verifier les numeros en entrée
def getAliasFromNumber(number):
    for elem in root:
        for var in elem:
            if var.tag == "number" and var.text == number:
                return elem.attrib['alias']
    return "Error : number not found"

#verifier les noms en entrée (nullptr, trop gros, non utf8)
def getKeyFromAlias(name):
    for elem in root:
        if elem.attrib['alias'] == name and elem.attrib['banned'] == "False":
            for var in elem:
                if var.tag == "key":
                    return var.text
    return "Error : alias not found"


#return une liste des alias dans la bdd, erreur si y'a personne dans la bdd
#pas teste
def getAliases():
    return [elem.attrib['alias'] for elem in root if elem.attrib[banned]=="False"]


#pas teste, explose si le sender est ban
def randomUsers(num,sender):
    listAlias = getAliases()
    listAlias.pop(listAlias.index(sender))

    for elem in root:
        if elem.attrib['banned'] == "True":
            listAlias.pop(listAlias.index(elem.attrib['alias']))

    num = int(num)
    sizeListAlias = len(listAlias)
    tmpList = [[0 for x in range(num)] for y in range(2)]


    if num > sizeListAlias:
        print("nombre demandé trop grand")
        return

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
    banUser("Roger")
    x = getNumberFromAlias("Roger")
    print(x)

if __name__ == "__main__":
    init()
    main()
