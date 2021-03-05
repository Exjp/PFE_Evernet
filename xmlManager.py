import xml.etree.ElementTree as ET

import os
import random
#champ xml pour banni ou non, à exclure des fonctions getAliases, getnumberfromalias et random

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

# vérifier que les champs sont uniques, vérifier que les champs sont corrects -> return une erreur sinon
# hash les mdps
def addUser(aliasValue, passValue, numberValue, keyValue):
    if aliasUnique(aliasValue) and numberUnique(numberValue) and keyUnique(keyValue):
        user = ET.Element('user')
        user.set("alias", aliasValue)
        password = ET.SubElement(user, "password")
        password.text = passValue
        number = ET.SubElement(user, "number")
        number.text = numberValue
        key = ET.SubElement(user, "key")
        key.text = keyValue
        root.append(user)
        treeWrite()
    else :
        print("User already exists")


# return un erreur si pas trouvé, nullptr, verif le nom en entrée
def removeUserFromName(name):
    for elem in root:
        if elem.attrib['alias'] == name:
            root.remove(elem)
    treeWrite()

def login(alias, password):
    for elem in root:
        if elem.attrib['alias'] == alias:
            for var in elem:
                if var.tag == "password":
                    if var.text == password:
                        return True
    return False

def removeUserFromNumber(number):
    treeWrite()

def banUser():
    treeWrite()

def unbanUser():
    treeWrite()

#verifier les noms en entrée, return un erreur si ça trouve rien, nullptr
def getNumberFromAlias(name):
    for elem in root:
        if elem.attrib['alias'] == name:
            for var in elem:
                if var.tag == "number":
                    return var.text
            break

#verifier les clés publiques en entrée, return un erreur si ça trouve rien, nullptr
def getKeyFromAlias(name):
    for elem in root:
        if elem.attrib['alias'] == name:
            for var in elem:
                if var.tag == "key":
                    return var.text
            break


#return une liste des alias dans la bdd, erreur si y'a personne dans la bdd
def getAliases():
    return [elem.attrib['alias'] for elem in root]


#on peut avoir le destinataire final
def randomUsers(num,sender):
    listAlias = getAliases()
    listAlias.pop(listAlias.index(sender))
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

def verifyInvitationKey(invitation_key):
    return invitation_key == "martin"



def main():
    x = getAliases()

if __name__ == "__main__":
    init()
    main()
