import xml.etree.ElementTree as ET
import os
import string
import random
from datetime import datetime, timedelta

def init():
    if not os.path.isfile('invitation.xml'):
        emptyXml()
    global tree
    tree = ET.parse('invitation.xml')
    global root
    root = tree.getroot()

def treeWrite():
    tree.write('invitation.xml', encoding="utf-8", xml_declaration=True)

def emptyXml():
    rootEmpty = ET.Element("keys")
    treeEmpty = ET.ElementTree(rootEmpty)
    treeEmpty.write("invitation.xml",
           xml_declaration=True,encoding='utf-8',
           method="xml")

def aliasUnique(aliasValue):
    unique = True
    for elem in root:
        if elem.attrib['alias'] == aliasValue:
            unique = False
    return unique

def getRandomString(length):
    base = string.ascii_lowercase + string.ascii_uppercase + string.digits
    rndStr = ''.join(random.choice(base) for i in range(length))
    return rndStr

#format de la date : 17-03-2021
#verifier les entrees (date (type date, j/m/a ou 0) et uses (type int)
#limiter les durees max des cles ?
def addKey(aliasValue, dateValue, usesValue):
    if aliasUnique(aliasValue) != True:
        return "Error : A key already exists for this alias"
    if int(usesValue) < 0:
        return "Error : Negative uses value"
    invitKey = ET.Element('invitationKey')

    key = getRandomString(12)

    invitKey.set("key", key)
    invitKey.set("alias", aliasValue)
    invitKey.set("date", dateValue)
    invitKey.set("uses", usesValue)
    root.append(invitKey)
    treeWrite()
    return True

#pas de treewrite ici, on le fait à la fin du signup et du cleanup
def removeKey(key):
    for elem in root:
        if elem.attrib['key'] == key:
            root.remove(elem)
            return True
    return "Error : Key not found"

#cleanup régulier pour virer les clés expirées en date -> datetime comparer 2 dates (entre actuel et valeur ds la bdd) -> >
#durée de vie en jours (si 0 infini)
def cleanup():
    presentDate = datetime.now()
    tmpList = []
    for elem in root:
        if elem.attrib['date'] != "0":
            elemDate = datetime.strptime(elem.attrib['date'], '%d-%m-%Y')
            if elemDate < presentDate:
                tmpList.append(elem.attrib['key'])
    for elem in tmpList:
        removeKey(elem)
    treeWrite()
    return True

def signup(key):
    for elem in root:
        if elem.attrib['key'] == key:
            tmp = True
            if int(elem.attrib['uses']) == 1:
                x = removeKey(key)
                treeWrite()
                return x
            if int(elem.attrib['uses'])> 1:
                x = int(elem.attrib['uses']) - 1
                elem.attrib['uses'] = str(x)
                treeWrite()
            return tmp
    return "Error : Key not found"

def main():
    print (cleanup())

if __name__ == "__main__":
    init()
    main()
