class TS:
    _instance = None
    def __init__(self):
        self.contextos = [Contexto()]
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
        # Verificar si ya existe en el contexto ACTUAL (no en contextos padres)
        if simbolo.nombre in self.contextos[-1].simbolos:
            return False  # Ya existe (doble declaración)
        self.contextos[-1].addSimbolo(simbolo)
        return True  # Agregado exitosamente

    def buscarSimbolo(self, nombre):
        for contexto in reversed(self.contextos):
            simbolo = contexto.buscarSimbolo(nombre)
            if simbolo:
                return simbolo
        return None

    def buscarSimboloEnContextoActual(self, nombre):
        return self.contextos[-1].buscarSimbolo(nombre)

    def __str__(self):
        resultado = "\nTabla de Simbolos:\n"
        for i, contexto in enumerate(self.contextos):
            resultado += f"--- Contexto {i} ---\n"
            resultado += str(contexto)
        return resultado

class Contexto:
    def __init__(self):
        self.simbolos = {}

    def addSimbolo(self, simbolo):
        self.simbolos[simbolo.nombre] = simbolo

    def buscarSimbolo(self, nombre):
        return self.simbolos.get(nombre)

    def __str__(self):
        if not self.simbolos:
            return "  (vacío)\n"
        return "".join([f"  {nombre}: {sim.tipoDato}\n" for nombre, sim in self.simbolos.items()])

class ID:
    def __init__(self, nombre, tipoDato):
        self.nombre = nombre
        self.tipoDato = tipoDato
        self.inicializado = False
        self.usado = False
        self.linea = 0  # Nueva: línea donde se declaró

    def getNombre(self):
        return self.nombre

    def getTipoDato(self):
        return self.tipoDato

    def setInicializado(self, linea=0):
        self.inicializado = True
        if linea > 0:
            self.linea = linea

    def getInicializado(self):
        return self.inicializado

    def setUsado(self):
        self.usado = True

    def getUsado(self):
        return self.usado
    
    def getLinea(self):
        return self.linea
    
    def setLinea(self, linea):
        self.linea = linea

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