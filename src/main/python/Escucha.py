from antlr4 import TerminalNode
from antlr4 import ErrorNode
from compiladorParser import compiladorParser
from compiladorListener import compiladorListener
from tablaDeSimbolos import TS, Variable

class Escucha (compiladorListener) :
    indent = 1
    declaracion = 0
    profundidad = 0
    numNodos = 0

    def enterPrograma(self, ctx:compiladorParser.ProgramaContext):
        print("Comienza el parsing")

    def exitPrograma(self, ctx:compiladorParser.ProgramaContext):
            print("Fin del Parsing")
            from tablaDeSimbolos import TS
            ts = TS.getInstance()
            print(ts)

    def enterIwhile(self, ctx:compiladorParser.IwhileContext):
        print("  "*self.indent + "Comienza while")
        self.indent += 1


        tipo = None
        nombres = []
        for i in range(ctx.getChildCount()):
            hijo = ctx.getChild(i)
            texto = hijo.getText()
            if i == 0:
                tipo = texto
            if texto.isidentifier() and texto != tipo:
                nombres.append(texto)
        print(f"   Tipo detectado: {tipo}")
        print(f"   Identificadores detectados: {nombres}")
        ts = TS.getInstance()
        for nombre in nombres:
            var = Variable(nombre, tipo)
            ts.addSimbolo(var)
            print(f"   [TS] Variable agregada: {nombre} ({tipo})")
        if not nombres:
            print("   [TS] Declaración vacía o incompleta, no se agrega símbolo.")
        self.numNodos += 1
    
    def __str__(self):
        return "Se hicieron " + str(self.declaracion) + " declaraciones\n" + \
                "Se visitaron " + str(self.numNodos) + " nodos"