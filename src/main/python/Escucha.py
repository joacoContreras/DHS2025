from antlr4 import TerminalNode
from antlr4 import ErrorNode
from compiladorParser import compiladorParser
from compiladorListener import compiladorListener
from tablaDeSimbolos import TS, Variable

class Escucha(compiladorListener):
    def __init__(self):
        self.indent = 1
        self.declaracion = 0
        self.profundidad = 0
        self.numNodos = 0
        self.ts = TS.getInstance()

    def enterPrograma(self, ctx:compiladorParser.ProgramaContext):
        print("Comienza el Parsing")

    def exitPrograma(self, ctx:compiladorParser.ProgramaContext):
        print("Fin del Parsing")
        print(str(self.ts)) # Imprimir la tabla de símbolos al final

    def enterIwhile(self, ctx:compiladorParser.IwhileContext):
        print(" " * self.indent + "Comienza while")
        self.indent += 1

    def exitIwhile(self, ctx:compiladorParser.IwhileContext):
        self.indent -= 1
        print(" " * self.indent + "Fin while")

    # MÉTODO CORREGIDO
    def enterDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        # Comprobación de seguridad para evitar el error
        if ctx.getChildCount() == 0:
            print("ADVERTENCIA: Se encontró una regla de 'declaracion' vacía.")
            return

        self.declaracion += 1
        print("Declaracion Enter -> |" + ctx.getText() + "|")
        print(" -- Cant. hijos = " + str(ctx.getChildCount()))

        # Extraer tipo y nombre de variable
        tipo = ctx.getChild(0).getText()  # INT o DOUBLE
        nombre = ctx.getChild(1).getText()  # ID principal
        
        var = Variable(nombre, tipo)
        self.ts.addSimbolo(var)
        print(f"   [TS] Variable agregada: {nombre} ({tipo})")

    # MÉTODO CORREGIDO
    def exitDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        print("Declaracion EXIT -> |" + ctx.getText() + "|")

    def enterListavar(self, ctx:compiladorParser.ListavarContext):
        self.profundidad += 1

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