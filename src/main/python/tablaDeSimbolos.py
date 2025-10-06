class TS:
    _instance = None
    def __init__(self):
        self.contextos = [Contexto()]  # contexto global

    @staticmethod
    def getInstance():
        if TS._instance is None:
            TS._instance = TS()
        return TS._instance

    def addContexto(self):
        self.contextos.append(Contexto())

    def delContexto(self):
        if len(self.contextos) > 1:
            self.contextos.pop()

    def addSimbolo(self, simbolo):
        self.contextos[-1].addSimbolo(simbolo)

    def buscarSimbolo(self, nombre):
        for contexto in reversed(self.contextos):
            simbolo = contexto.buscarSimbolo(nombre)
            if simbolo:
                return simbolo
        return None

class Contexto:
    def __init__(self):
        self.simbolos = {}

    def addSimbolo(self, simbolo):
        self.simbolos[simbolo.nombre] = simbolo

    def buscarSimbolo(self, nombre):
        return self.simbolos.get(nombre)

class ID:
    def __init__(self, nombre, tipoDato):
        self.nombre = nombre
        self.tipoDato = tipoDato
        self.inicializado = False
        self.usado = False

    def getNombre(self):
        return self.nombre

    def getTipoDato(self):
        return self.tipoDato

    def setInicializado(self):
        self.inicializado = True

    def getInicializado(self):
        return self.inicializado

    def setUsado(self):
        self.usado = True

    def getUsado(self):
        return self.usado

class Variable(ID):
    def __init__(self, nombre, tipoDato, esGlobal=False):
        super().__init__(nombre, tipoDato)
        self.esGlobal = esGlobal

    def getEsGlobal(self):
        return self.esGlobal

class Funcion(ID):
    def __init__(self, nombre, tipoDato, args=None):
        super().__init__(nombre, tipoDato)
        self.args = args if args is not None else []

    def getListaArgs(self):
        return self.args
class TS:
    __instance = None
    
    @staticmethod
    def getInstance():
        if TS.__instance == None:
            TS()
        return TS.__instance
    
    def __init__(self):
        if TS.__instance != None:
            raise Exception("Esta clase es un singleton!")
        else:
            TS.__instance = self
            self.tabla = {}
    
    def agregarContexto(self, id, tipo):
        if id in self.tabla:
            raise Exception("Error: variable " + id + " ya declarada")
        self.tabla[id] = tipo
    
    def buscarSimbolo(self, id):
        if id not in self.tabla:
            raise Exception("Error: variable " + id + " no declarada")
        return self.tabla[id]
    
    def __str__(self):
        resultado = "Tabla de Simbolos:\n"
        for id, tipo in self.tabla.items():
            resultado += f"{id}: {tipo}\n"
        return resultado
    
class Contexto:
    def __init__(self):
        self.simbolos = {}
    
    def addSimbolo(self, simbolo):
        self.simbolos[simbolo.nombre] = simbolo
        #print(f"Simbolo {simbolo.nombre} agregado al contexto")
        
    
    def buscarSimbolo(self, nombre):
        return self.simbolos.get(nombre, None)

class ID:
    def __init__(self, nombre, tipoDato):
        self.nombre = nombre
        self.tipoDato = tipoDato
        self.inicializado = False
        self.usado = False

class Variable(ID):
    def __init__(self, nombre, tipoDato, esGlobal = False):
        super().__init__(nombre, tipoDato)
        self.esGlobal = esGlobal
        
class Function(ID):
    def __init__(self, nombre, tipo_retorno, parametros):
        self.nombre = nombre
        self.tipo_retorno = tipo_retorno
        self.parametros = parametros