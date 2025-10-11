from antlr4 import TerminalNode
from antlr4 import ErrorNode
from compiladorParser import compiladorParser
from compiladorListener import compiladorListener
from tablaDeSimbolos import TS, Variable

class Escucha(compiladorListener):
    def __init__(self):
        self.ts = TS.getInstance()
        # Guardo el tipo de la declaración actual para usarlo en listavar
        self.tipo_actual = None

    def enterPrograma(self, ctx:compiladorParser.ProgramaContext):
        print("Comienza el Parsing")

    def exitPrograma(self, ctx:compiladorParser.ProgramaContext):
        print("Fin del Parsing")
        print("="*20)
        print(str(self.ts))
        print("="*20)
        
    def enterIwhile(self, ctx:compiladorParser.IwhileContext):
        print(" " * self.indent + "Comienza while")
        self.indent += 1

    def exitIwhile(self, ctx:compiladorParser.IwhileContext):
        self.indent -= 1
        print(" " * self.indent + "Fin while")

    def enterDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        # Extraer el tipo y guardarlo
        self.tipo_actual = ctx.tipo().getText()
        
        # Extraer el ID principal de la declaración
        nombre_var = ctx.ID().getText()
        
        # Añadir la variable a la tabla de símbolos
        variable = Variable(nombre_var, self.tipo_actual)
        self.ts.addSimbolo(variable)
        print(f"✔️ Variable declarada: {nombre_var} ({self.tipo_actual})")
        
    def exitDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        # Limpiar el tipo actual cuando salimos de la regla de declaración
        self.tipo_actual = None
        
    def enterListavar(self, ctx:compiladorParser.ListavarContext):
        # Esta regla maneja las variables adicionales en una declaración
        # ej: int x, >>y, z<<;
        
        # Iteramos sobre todos los ID que encuentre en la lista
        for id_node in ctx.ID():
            nombre_var = id_node.getText()
            if self.tipo_actual:
                variable = Variable(nombre_var, self.tipo_actual)
                self.ts.addSimbolo(variable)
                print(f"✔️ Variable declarada: {nombre_var} ({self.tipo_actual})")

    def exitListavar(self, ctx:compiladorParser.ListavarContext):
        self.profundidad -= 1
        # Lógica para procesar la lista de variables si es necesario
        if ctx.getChildCount() > 1:
            nombre = ctx.getChild(1).getText()
            # Aquí necesitarías saber el tipo de la declaración original para agregarla a la TS
            # print(f"   [TS] Variable de lista agregada: {nombre}")

    def visitErrorNode(self, node:ErrorNode):
        print(" ---> ERROR")

    def enterEveryRule(self, ctx):
        self.numNodos += 1

    def __str__(self):
        return "Se hicieron " + str(self.declaracion) + " declaraciones\n" + \
               "Se visitaron " + str(self.numNodos) + " nodos\n"

    def exitEveryRule(self, ctx):
        pass

    def visitTerminal(self, node:TerminalNode):
        pass