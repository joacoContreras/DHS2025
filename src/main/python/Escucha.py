from antlr4 import TerminalNode
from antlr4 import ErrorNode
from compiladorParser import compiladorParser
from compiladorListener import compiladorListener
from tablaDeSimbolos import TS, Variable

class Escucha (compiladorListener):
    indent = 1
    declaracion = 0
    profundidad = 0
    numNodos = 0
    
    def enterPrograma(self, ctx:compiladorParser.ProgramaContext):
        print("Comienza el Parsing")
    
    def exitPrograma(self, ctx:compiladorParser.ProgramaContext):
        print("Fin del Parsing")
        
    def enterIwhile(self, ctx:compiladorParser.IwhileContext):
        print(" "*self.indent + "Comienza while")
        self.indent += 1
    
    def exitIwhile(self, ctx:compiladorParser.IwhileContext):
        self.indent -= 1
        print(" "*self.indent + "Fin while")
        
    def enterDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        from tablaDeSimbolos import TS, Variable
        self.declaracion += 1
        print("Declaracion Enter -> |" + ctx.getText() + "|")
        print(" -- Cant. hijos = " + str(ctx.getChildCount()))
        # Extraer tipo y nombre de variable
        tipo = ctx.getChild(0).getText()  # INT o DOUBLE
        nombre = ctx.getChild(1).getText()  # ID principal
        ts = TS.getInstance()
        var = Variable(nombre, tipo)
        ts.addSimbolo(var)
        print(f"   [TS] Variable agregada: {nombre} ({tipo})")
        
    def exitDeclaration(self, ctx:compiladorParser.DeclaracionContext):
        print("Declaracion EXIT -> |" + ctx.getText() + "|")
        print(" -- Cant. hijos = " + str(ctx.getChildCount()))
    
    def enterListavar(self, ctx:compiladorParser.ListavarContext):
        self.profundidad += 1
    
    def exitListavar(self, ctx:compiladorParser.ListavarContext):
        self.profundidad -= 1
        print("     -- ListaVar(%d) Cant. hijos = %d" % (self.profundidad, ctx.getChildCount()))
        if ctx.getChildCount() == 4 :
            print("          hijo ID --> |%s|" % ctx.getChild(1).getText())
        
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
    
    def enterDeclaration(self, ctx):
        ts = TS.getInstance()
        # Extrae nombre y tipo de la variable del contexto
        # variable = Variable(nombre, tipo)
        # ts.agregarSimbolo(variable)