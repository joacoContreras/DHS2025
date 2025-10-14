from antlr4 import TerminalNode
from compiladorParser import compiladorParser
from compiladorListener import compiladorListener
from tablaDeSimbolos import TS, Variable

class Escucha(compiladorListener):
    indent = 1
    declaracion = 0
    profundidad = 0
    numNodos = 0
    
    tipo_actual = None

    def enterPrograma(self, ctx: compiladorParser.ProgramaContext):
        print("Comienza el parsing")

    def exitPrograma(self, ctx: compiladorParser.ProgramaContext):
        print("Fin del Parsing")
        ts = TS.getInstance()
        print("\n--- TABLA DE SIMBOLOS FINAL ---")
        print(ts)
        
    def enterIwhile(self, ctx:compiladorParser.IwhileContext):
        print("  "*self.indent + "Comienza while")
        self.indent += 1
        ts = TS.getInstance()
        ts.addContexto()

    def exitIwhile(self, ctx:compiladorParser.IwhileContext):
        self.indent -= 1
        print("  "*self.indent + "Fin while")
        ts = TS.getInstance()
        ts.delContexto()
        
    def enterDeclaracion(self, ctx: compiladorParser.DeclaracionContext):
        # --- ¡PROTECCIÓN AÑADIDA! ---
        # Solo procesamos si la declaración no está vacía.
        if ctx.getChildCount() > 0:
            ts = TS.getInstance()
            ts.addContexto()
            self.declaracion += 1
            print("Declaracion ENTER -> | " + ctx.getText() + "|")
            
            # El tipo de dato es el PRIMER hijo (índice 0).
            self.tipo_actual = ctx.getChild(0).getText()
            print("  -- Tipo de dato guardado: " + self.tipo_actual)
        
    def exitDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        # --- ¡PROTECCIÓN AÑADIDA! ---
        # Solo procesamos si la declaración no estaba vacía.
        if ctx.getChildCount() > 0:
            print("Declaracion EXIT  -> |" + ctx.getText() + "|")
            ts = TS.getInstance()
            ts.delContexto()
            self.tipo_actual = None
        
    def enterListavar(self, ctx:compiladorParser.ListavarContext):
        self.profundidad += 1

    def exitListavar(self, ctx:compiladorParser.ListavarContext):
        self.profundidad -= 1
        
        # --- ¡PROTECCIÓN AÑADIDA! ---
        # Nos aseguramos de que listavar no esté vacía antes de procesar.
        if ctx.getChildCount() > 0:
            print("  -- ListaVar(%d) Cant. hijos  = %d" % (self.profundidad + 1, ctx.getChildCount()))
            
            # El nombre de la variable (ID) es el PRIMER hijo (índice 0).
            nombre_variable = ctx.getChild(0).getText()
            
            ts = TS.getInstance()
            
            if self.tipo_actual:
                simbolo = Variable(nombre_variable, self.tipo_actual)
                ts.addSimbolo(simbolo)
                print("      -> Símbolo '{%s: %s}' agregado al contexto actual." % (nombre_variable, self.tipo_actual))
        
    def enterEveryRule(self, ctx):
        self.numNodos += 1

    def __str__(self):
        return "Se hicieron " + str(self.declaracion) + " declaraciones\n" + \
               "Se visitaron " + str(self.numNodos) + " nodos"