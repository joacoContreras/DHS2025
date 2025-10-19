from antlr4 import TerminalNode
from compiladorParser import compiladorParser
from compiladorListener import compiladorListener
from tablaDeSimbolos import TS, Variable, Funcion

class Escucha(compiladorListener):
    indent = 1
    declaracion = 0
    profundidad = 0
    numNodos = 0
    numFunciones = 0
    numWhiles = 0
    numFors = 0
    numIfs = 0
    
    tipo_actual = None

    def enterPrograma(self, ctx: compiladorParser.ProgramaContext):
        print("Comienza el parsing")

    def exitPrograma(self, ctx: compiladorParser.ProgramaContext):
        print("Fin del Parsing")
        ts = TS.getInstance()
        print("\n--- TABLA DE SIMBOLOS FINAL ---")
        print(ts)
        
    def enterIwhile(self, ctx:compiladorParser.IwhileContext):
        self.numWhiles += 1
        print("  "*self.indent + "╔═ WHILE ENTER")
        self.indent += 1
        ts = TS.getInstance()
        ts.addContexto()

    def exitIwhile(self, ctx:compiladorParser.IwhileContext):
        self.indent -= 1
        print("  "*self.indent + "╚═ WHILE EXIT")
        ts = TS.getInstance()
        ts.delContexto()
        
    def enterDeclaracion(self, ctx: compiladorParser.DeclaracionContext):
        self.declaracion += 1
        print("Declaracion ENTER -> |" + ctx.getText() + "|")
        
    def exitDeclaracion(self, ctx:compiladorParser.DeclaracionContext):
        print("Declaracion EXIT  -> |" + ctx.getText() + "|")
        
        if ctx.getChildCount() >= 3:
            # Estructura: tipo ID inic listavar PYC
            ts = TS.getInstance()
            
            # Obtener el tipo (primer hijo)
            tipo = ctx.getChild(0).getText()
            print(f"  -- Tipo detectado: {tipo}")
            
            # Obtener el primer ID (segundo hijo)
            primer_id = ctx.getChild(1).getText()
            var = Variable(primer_id, tipo)
            ts.addSimbolo(var)
            print(f"  -> Variable '{primer_id}' de tipo '{tipo}' agregada")
            
            # Procesar listavar para variables adicionales
            # listavar está en la posición 3
            self.tipo_actual = tipo
            self.procesar_listavar(ctx.getChild(3), ts)
            self.tipo_actual = None
    
    def procesar_listavar(self, ctx, ts):
        """Procesa recursivamente los nodos listavar para extraer variables adicionales"""
        if ctx is None or ctx.getChildCount() < 2:
            return
        
        # Estructura de listavar: COMA ID inic listavar
        if ctx.getChildCount() >= 2:
            nombre_var = ctx.getChild(1).getText()
            if nombre_var and nombre_var != ',':
                var = Variable(nombre_var, self.tipo_actual)
                ts.addSimbolo(var)
                print(f"  -> Variable '{nombre_var}' de tipo '{self.tipo_actual}' agregada")
            
            # Procesar el siguiente listavar recursivamente (posición 3)
            if ctx.getChildCount() >= 4:
                self.procesar_listavar(ctx.getChild(3), ts)
        
    def enterListavar(self, ctx:compiladorParser.ListavarContext):
        self.profundidad += 1

    def exitListavar(self, ctx:compiladorParser.ListavarContext):
        self.profundidad -= 1
        if ctx.getChildCount() > 0:
            print("  -- ListaVar(%d) Cant. hijos  = %d" % (self.profundidad + 1, ctx.getChildCount()))
    
    # ============== RECONOCIMIENTO DE FUNCIONES ==============
    def enterFuncion(self, ctx:compiladorParser.FuncionContext):
        self.numFunciones += 1
        print("  " * self.indent + "╔═ FUNCION ENTER")
        self.indent += 1
        ts = TS.getInstance()
        ts.addContexto()  # Nuevo contexto para el scope de la función
    
    def exitFuncion(self, ctx:compiladorParser.FuncionContext):
        # Estructura: tipo ID PA parametros PC bloque
        if ctx.getChildCount() >= 6:
            tipo_retorno = ctx.getChild(0).getText()
            nombre_funcion = ctx.getChild(1).getText()
            
            # Extraer parámetros (esto se puede mejorar)
            params = []
            parametros_ctx = ctx.getChild(3)
            if parametros_ctx and parametros_ctx.getChildCount() > 0:
                # Simplificado: solo muestra que tiene parámetros
                params.append("...")
            
            ts = TS.getInstance()
            funcion = Funcion(nombre_funcion, tipo_retorno, params)
            ts.delContexto()  # Salir del scope de la función
            ts.addSimbolo(funcion)  # Agregar función al contexto externo
            
            self.indent -= 1
            print("  " * self.indent + f"╚═ FUNCION EXIT: {nombre_funcion}() -> {tipo_retorno}")
        else:
            self.indent -= 1
            print("  " * self.indent + "╚═ FUNCION EXIT (incompleta)")
    
    # ============== RECONOCIMIENTO DE IF ==============
    def enterIif(self, ctx:compiladorParser.IifContext):
        self.numIfs += 1
        print("  " * self.indent + "╔═ IF ENTER")
        self.indent += 1
        ts = TS.getInstance()
        ts.addContexto()  # Nuevo contexto para el scope del if
    
    def exitIif(self, ctx:compiladorParser.IifContext):
        self.indent -= 1
        ts = TS.getInstance()
        ts.delContexto()
        print("  " * self.indent + "╚═ IF EXIT")
    
    # ============== RECONOCIMIENTO DE FOR ==============
    def enterIfor(self, ctx:compiladorParser.IforContext):
        self.numFors += 1
        print("  " * self.indent + "╔═ FOR ENTER")
        self.indent += 1
        ts = TS.getInstance()
        ts.addContexto()  # Nuevo contexto para el scope del for
    
    def exitIfor(self, ctx:compiladorParser.IforContext):
        self.indent -= 1
        ts = TS.getInstance()
        ts.delContexto()
        print("  " * self.indent + "╚═ FOR EXIT")
        
    # ============== RECONOCIMIENTO DE WHILE (ya existente, mejorado) ==============
        
    def enterEveryRule(self, ctx):
        self.numNodos += 1

    def __str__(self):
        resultado = f"Se hicieron {self.declaracion} declaraciones\n"
        resultado += f"Se reconocieron {self.numFunciones} funciones\n"
        resultado += f"Se reconocieron {self.numWhiles} bucles while\n"
        resultado += f"Se reconocieron {self.numFors} bucles for\n"
        resultado += f"Se reconocieron {self.numIfs} estructuras if\n"
        resultado += f"Se visitaron {self.numNodos} nodos"
        return resultado