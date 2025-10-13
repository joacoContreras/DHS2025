from antlr4 import TerminalNode
from compiladorParser import compiladorParser
from compiladorListener import compiladorListener
from tablaDeSimbolos import TS, Variable

class Escucha(compiladorListener):
    indent = 1
    declaracion = 0
    numNodos = 0

    def enterPrograma(self, ctx: compiladorParser.ProgramaContext):
        print("Comienza el parsing")

    def exitPrograma(self, ctx: compiladorParser.ProgramaContext):
        print("Fin del Parsing")
        ts = TS.getInstance()
        print(ts)

    def enterDeclaracion(self, ctx: compiladorParser.DeclaracionContext):
        """
        Este método se activa cuando el parser entra en una regla de declaración.
        Extrae el tipo y los nombres de todas las variables declaradas y las
        agrega a la tabla de símbolos en el contexto actual.
        """
        print("  " * self.indent + "Procesando declaracion...")
        self.indent += 1
        self.declaracion += 1
        
        # --- FIX STARTS HERE ---
        # Primero, verificamos si el contexto 'tipo' existe. Si no, es probable
        # que haya un error de sintaxis en el archivo de entrada y debemos salir.
        if not ctx.tipo():
            print("   [Error] Declaracion mal formada o incompleta detectada.")
            self.indent -= 1
            return
        # --- FIX ENDS HERE ---

        tipo = ctx.tipo().getText()
        
        nombres = []
        if ctx.ID():
            nombres.append(ctx.ID().getText())
        
        if ctx.listavar():
            for id_node in ctx.listavar().ID():
                nombres.append(id_node.getText())

        print(f"   Tipo detectado: {tipo}")
        print(f"   Identificadores detectados: {nombres}")
        
        ts = TS.getInstance()
        for nombre in nombres:
            if ts.buscarSimboloEnContextoActual(nombre):
                print(f"   [Error] La variable '{nombre}' ya ha sido declarada en este contexto.")
            else:
                var = Variable(nombre, tipo)
                ts.addSimbolo(var)
                print(f"   [TS] Variable agregada: {nombre} ({tipo})")
        self.indent -=1

    def enterBloque(self, ctx: compiladorParser.BloqueContext):
        """
        Se activa al entrar a un bloque '{'.
        Crea un nuevo contexto (ámbito) en la tabla de símbolos.
        """
        print("  " * self.indent + "Entrando a un nuevo bloque, creando contexto.")
        self.indent += 1
        ts = TS.getInstance()
        ts.addContexto()

    def exitBloque(self, ctx: compiladorParser.BloqueContext):
        """
        Se activa al salir de un bloque '}'.
        Elimina el contexto actual de la tabla de símbolos.
        """
        self.indent -= 1
        print("  " * self.indent + "Saliendo del bloque, eliminando contexto.")
        ts = TS.getInstance()
        ts.delContexto()
        
    def visitTerminal(self, node: TerminalNode):
        self.numNodos += 1

    def __str__(self):
        return "Se hicieron " + str(self.declaracion) + " declaraciones\n" + \
               "Se visitaron " + str(self.numNodos) + " nodos"