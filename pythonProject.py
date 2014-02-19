import re
import time

archivoXML = open('xml.xml')
arbol = None

class Device:
    """ Objeto que almacena el contenido de un Device del archivo XML.
    
    Estructura:
    id -- id del Device
    attrs -- dictionario de Atributos
    groups -- dictionario de groups
    
    """
    
    def __init__(self, idDevice):
        self.id = idDevice
        self.attrs = {}
        self.groups = {}
    
    def setAttr(self,name,value):
        """Set an Attribute for the Device."""
        self.attrs[name] = value
    
    def getAttrVal(self,name):
        """Get the Value of an Attribute."""
        return self.attrs[name]
    
    def setGroup(self, group ):
        """ Set a Group for the Device."""
        self.groups[group.id] = group
    
    def getGroup(self,id ):
        """Return a group given the id"""
        return self.groups[id]

class Group:
    """ Objeto que almacena el contenido de un Group del archivo XML
    
    Estructura:
    id -- id del Group
    capabilities -- dictionario de capabilities
    
    """
    def __init__(self, idGroup):
        """Constructor.
        
        idGroup -- el valor del id del Grupo
        """
        self.id = idGroup
        self.capabilities = {}
    
    def setCapability(self, name, value):
        """Set capability for the Group."""
        self.capabilities[name] = value
    
    def getCapability(self, name):
        """ Return capability given the name."""
        return self.capabilities[name]    
    
    
    
     

class XMLTree:
    """Objeto Que representa un arbol parseado de un archivo XML.
    
    Estructura:
    id = id del Arbol
    attrs = dictionario de atributos
    childs = lista de tags hijos del arbol
    
    """
    def __init__(self,idDevice):
        self.id = idDevice
        self.attrs = {}
        self.childs = []

    def setAttr(self,name,value):
        self.attrs[name] =  value

    def getAttrVal(self,name):
        return self.attrs[name]

def prepararLectura():
    """Lee el archivo XML hasta encontrar el inicio de la lista de devices."""
    palabra = ""
    while(re.match(r"<devices",palabra) == None):
        palabra = leerPalabra()

def leerPalabra():
    """Lee y devuelve una palabra del archivo XML."""
    s = archivoXML.read(1)
    palabra=""
    while(s == ' ' or s=='\n'):
        s=archivoXML.read(1)
    while(s != ' ' and s!='\n' and len(s) != 0):
        palabra= palabra + s
        s = archivoXML.read(1)
    return palabra

def crearCapability(group):
    """Crea una capability para el grupo."""
    palabra = leerPalabra()
    if (not isAttribute(palabra)):
        palabra = getFullAttribute(palabra)
    name = getAttrValue(palabra)
    palabra = leerPalabra()
    if (not isAttribute(palabra)):
        palabra = getFullAttribute(palabra)
    value = getAttrValue(palabra)
    group.setCapability(name,value)
    print "\n\t\t\tCapability: Name= "+name+" Value= "+value

def crearGroup():
    """Crea un Grupo y lo retorna."""
    idGroup = getAttrValue(leerPalabra())
    group = Group(idGroup)
    print "\n\t\tGroup ID = "+idGroup
    palabra=leerPalabra()
    print "\n******palabra: "+palabra
    while(palabra!="</group>"):
        if(palabra=="<capability"):
            print " .... es capability.... Creando Capability"
            crearCapability(group)
        palabra = leerPalabra()
        print "\n******palabra: "+palabra
    print ".... Terminando de crear Grupo"
    return group

def crearDevice():
    """Crea un Device y lo retorna."""
    idDevice = getAttrValue(leerPalabra())
    device = Device(idDevice)
    print "\n\tDevice ID = "+idDevice 
    palabra = leerPalabra()
    print "\n******palabra: "+palabra
    while(palabra != "</device>"):
        if(isAttribute(palabra)):
            print " ... Es atributo.. creando Atributo..."
            addAttribute(palabra, device)
            if(isCloseAttrTag(palabra)):
                print "-----El device no contiene Groups...."
                break;
        elif(isTagName(palabra)):
            print "... Es Grupo... creando Grupo.."
            group = crearGroup()
            device.setGroup(group)
        else:
            print ".... Es Atributo... uniendo atributo ... creando Atributo..."
            palabra = getFullAttribute(palabra)
            addAttribute(palabra,device)
            if(isCloseAttrTag(palabra)):
                print "-----El device no contiene Groups...."
                break
        palabra = leerPalabra()
        print "\n******palabra: "+palabra
    print "\n.... terminando de crear Device"
    return device

def createDeviceDictionary():
    """Crea un dictionario de Devices, donde las keys son los ids de los Devices."""
    print "Proyecto XMLParser: "
    print "\n Leyendo archivo"
    devices = {}
    palabra = leerPalabra()
    print "\n******palabra: "+palabra
    while( len(palabra) != 0):
        if(palabra == "<device"):
            print " ... es un Device ... Creando Device"
            device = crearDevice()
            devices[device.id] = device
        else:
            break
        palabra = leerPalabra()
        print "\n******palabra: "+palabra
    print "\n ********** Termino lectura del archivo ********"
    print "\n ******* Devolviendo un dictionario de Devices*********"
    return devices
    
    

def addAttribute(s, device):
    """Agrega un atributo a un Device.
    
    Keyword Arguments:
    s -- el String atributo
    device -- el objeto Device para agregarle atributo
    
    """
    name = getAttrName(s)
    value = getAttrValue(s)
    device.attrs[name] = value
    print "\n\tName = "+name + " Value = "+value
    
def isTagName(s):
    """ Retorna verdadero si s es el nombre de un Tag."""
    return s[0]=='<' and s[1]!='/'

def isCloseTagName(s):
    """Retorna verdadero si s es un tag de cierre."""
    return s[0]=='<' and s[1]=='/'

def isCloseAttrTag(s):
    """retorna verdadero si s es un atributo y posee un tag de cierre."""
    return s[len(s) - 1] == '>' and s[len(s) - 2] == '/'
    
def isAttribute(s):
    """retorna verdadero si s es un atributo de la forma name='value'"""
    return re.match(r".*=\".*\"",s)

def getAttrName(s):
    """ Devuelve el nombre del atributo s."""
    return s[:s.find('"')-1]

def getAttrValue(s):
    """Devuelve el valor del atributo s."""
    return s[s.find('"')+1:s.rfind('"')]

def getFullAttribute(s):
    """Lee archivo XML hasta formar un atributo completo de la forma name='value'
    
    Keyword Arguments:
    s -- la palabra inicial del string atributo a crear
    
    """
    attr = s
    palabra = ""
    while(palabra.find('"') == -1):
        palabra = leerPalabra()
        attr = attr + " " + palabra
    return attr

def crearArbol(arbol):
    s = leerPalabra()
    print "\npalabra: " + s
    while( len(s) != 0 or palabra!="</devices>"):
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
        print "\t\tPalabra: " + s
    print "Finished Reading... returning tree"
    return arbol

def main():
    prepararLectura()
    arbol1 = XMLTree("devices")
    arbol = crearArbol(arbol1)
    return arbol

def start():
    prepararLectura()
    start = time.clock()
    dictionary = createDeviceDictionary()
    end = time.clock()
    print "*************TOTAL AMOUNT OF TIME : "+str(end - start)
    return dictionary

def jerarquia(device,devices):
    while(device != 'root'):
        if device in devices:
            d = devices[device]
            print d.id+"\n"
            device = d.attrs['fall_back']
            
def fallbacks(g,c):
    devices = start()
    cont = 0
    for d in devices:
        device = devices[d]
        groups = device.groups
        if(g in groups):
            group = groups[g]
            capabilities = group.capabilities
            if c in capabilities:
                cont +=1
            else:
                while (True):
                    device_name = device.attrs['fall_back']
                    if (device_name == 'root'):
                        break
                    device = devices[device_name]
                    groups = device.groups
                    if(g in groups):
                        group = groups[g]
                        capabilities = group.capabilities
                        if c in capabilities:
                            cont += 1
                            break
        else:
            while (True):
                device_name = device.attrs['fallback']
                if (device_name == 'root'):
                    break
                device = devices[device_name]
                groups = device.groups
                if(g in groups):
                    group = groups[g]
                    capabilities = group.capabilities
                    if c in capabilities:
                        cont += 1
                        break
            
