import re

archivoXML = open('test.xml')
arbol = None

class XMLTree:
    def __init__(self,name):
        self.name = name
        self.attrs = {}
        self.childs = []

    def setAttr(self,name,value):
        self.attrs[name] =  value

    def getAttrVal(self,name):
        return self.attrs[name]

def prepararLectura():
    palabra = ""
    while(palabra != "<devices"):
        palabra = leerPalabra()

def leerPalabra():
    s = archivoXML.read(1)
    palabra=""
    while(s == ' ' or s=='\n'):
        s=archivoXML.read(1)
    while(s != ' ' and s!='\n' and len(s) != 0):
        palabra= palabra + s
        s = archivoXML.read(1)
    return palabra


    
def isTagName(s):
    return s[0]=='<' and s[1]!='/'

def isCloseTagName(s):
    return s[0]=='<' and s[1]=='/'

def isCloseAttrTag(s):
    return s[len(s) - 1] == '>' and s[len(s) - 2] == '/'
    
def isAttribute(s):
    return re.match(r".*=\".*\"",s)

def getAttrName(s):
    return s[:s.find('"')-1]

def getAttrValue(s):
    return s[s.find('"')+1:s.rfind('"')]

def getFullAttribute(s):
    attr = s
    palabra = ""
    while(palabra.find('"') == -1):
        palabra = leerPalabra()
        attr = attr + " " + palabra
    return attr

def crearArbol(arbol):
    s = leerPalabra()
    print "\npalabra: " + s
    while( len(s) != 0):
        if(isTagName(s)):
            print "\nis TagName .... creating child"
            arbol.childs = arbol.childs + [crearArbol(XMLTree(s[1:]))]
        elif(isAttribute(s)):
            print "\n is Attribute .. adding attr"
            name = getAttrName(s)
            value = getAttrValue(s)
            arbol.setAttr(name,value)
            if(isCloseAttrTag(s)):
                print "\n is close attrTag ... Finishing this tree.........."
                return arbol
        elif(isCloseTagName(s)):
            print "\n is CloseTagName ........ Finishing this tree......"
            return arbol
        else:
            print "\n is part of an attribute .. joining pieces"
            attr = getFullAttribute(s)
            print "attr = " + attr
            name = getAttrName(attr)
            value = getAttrValue(attr)
            arbol.setAttr(name,value)
            if(isCloseAttrTag(attr)):
                print "\n isCloseAttrTag ... Finishing this tree"
                return arbol
        s = leerPalabra()
        print "\n\n\n Palabra: " + s
    print "Finished Reading... returning tree"
    return arbol

def main():
    prepararLectura()
    arbol1 = XMLTree("devices")
    arbol = crearArbol(arbol1)
    return arbol

