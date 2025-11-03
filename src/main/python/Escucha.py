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
    
    # Listas para almacenar errores
    errores_sintacticos = []
    errores_semanticos = []

    def enterPrograma(self, ctx: compiladorParser.ProgramaContext):
        print("Comienza el parsing")
        # Reiniciar errores
        Escucha.errores_sintacticos = []
        Escucha.errores_semanticos = []

    def exitPrograma(self, ctx: compiladorParser.ProgramaContext):
        print("Fin del Parsing")
        
        # Verificar variables declaradas pero no usadas
        self.verificarVariablesNoUsadas()
        
        # Generar reporte de errores
        self.generarReporte()
    
    def verificarVariablesNoUsadas(self):
        "Verifica si hay variables declaradas pero no usadas"
        ts = TS.getInstance()
        
        for contexto in ts.contextos:
            for nombre, simbolo in contexto.simbolos.items():
                if isinstance(simbolo, Variable) and not simbolo.getUsado():
                    self.reportarErrorSemantico(
                        simbolo.getLinea(),
                        f"Variable '{nombre}' declarada pero no usada"
                    )
    
    def reportarErrorSintactico(self, linea, mensaje):
        """Reporta un error sintáctico"""
        error = f"[SINTÁCTICO] Línea {linea}: {mensaje}"
        Escucha.errores_sintacticos.append(error)
        print(f" {error}")
    
    def reportarErrorSemantico(self, linea, mensaje):
        """Reporta un error semántico"""
        error = f"[SEMÁNTICO] Línea {linea}: {mensaje}"
        Escucha.errores_semanticos.append(error)
        print(f" {error}")
    
    def tieneErrores(self):
        """Retorna True si hay errores"""
        return len(Escucha.errores_sintacticos) > 0 or len(Escucha.errores_semanticos) > 0
    
    def generarReporte(self):
        """Genera un reporte de errores al final"""
        total_errores = len(Escucha.errores_sintacticos) + len(Escucha.errores_semanticos)
        
        if total_errores == 0:
            # No hay errores, mostrar tabla de símbolos
            ts = TS.getInstance()
            print("\n--- TABLA DE SIMBOLOS FINAL ---")
            print(ts)
            return
        
        # Hay errores, mostrar reporte
        print("\n" + "=" * 60)
        print("         REPORTE DE ERRORES")
        print("=" * 60)
        print(f"Total de errores: {total_errores}")
        print(f"  • Errores sintácticos: {len(Escucha.errores_sintacticos)}")
        print(f"  • Errores semánticos: {len(Escucha.errores_semanticos)}")
        print("=" * 60)
        
        if Escucha.errores_sintacticos:
            print("\n ERRORES SINTÁCTICOS:")
            print("-" * 60)
            for error in Escucha.errores_sintacticos:
                print(f"  {error}")
        
        if Escucha.errores_semanticos:
            print("\n ERRORES SEMÁNTICOS:")
            print("-" * 60)
            for error in Escucha.errores_semanticos:
                print(f"  {error}")
        
        print("\n" + "=" * 60)
        
    def enterIwhile(self, ctx:compiladorParser.IwhileContext):
        self.numWhiles += 1
        print("  "*self.indent + " WHILE ENTER")
        self.indent += 1
        ts = TS.getInstance()
        ts.addContexto()

    def exitIwhile(self, ctx:compiladorParser.IwhileContext):
        self.indent -= 1
        print("  "*self.indent + "WHILE EXIT")
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
            
            # Obtener la línea de la declaración
            linea = ctx.start.line if ctx.start else 0
            
            # Obtener el primer ID (segundo hijo)
            primer_id = ctx.getChild(1).getText()
            var = Variable(primer_id, tipo)
            var.setLinea(linea)
            
            # Verificar si está inicializada
            inic_ctx = ctx.getChild(2)  # nodo 'inic'
            if inic_ctx and inic_ctx.getChildCount() > 0:
                var.setInicializado(linea)
            
            # Intentar agregar a la tabla (detecta doble declaración)
            if not ts.addSimbolo(var):
                self.reportarErrorSemantico(
                    linea,
                    f"Variable '{primer_id}' ya fue declarada en este contexto"
                )
            else:
                print(f"  -> Variable '{primer_id}' de tipo '{tipo}' agregada")
            
            # Procesar listavar para variables adicionales
            self.tipo_actual = tipo
            self.linea_actual = linea
            self.procesar_listavar(ctx.getChild(3), ts)
            self.tipo_actual = None
    
    def procesar_listavar(self, ctx, ts):
        "Procesa recursivamente los nodos listavar para extraer variables adicionales"
        if ctx is None or ctx.getChildCount() < 2:
            return
        
        # Estructura de listavar: COMA ID inic listavar
        if ctx.getChildCount() >= 2:
            nombre_var = ctx.getChild(1).getText()
            if nombre_var and nombre_var != ',':
                var = Variable(nombre_var, self.tipo_actual)
                var.setLinea(self.linea_actual)
                
                # Verificar si está inicializada (inic en posición 2)
                if ctx.getChildCount() >= 3:
                    inic_ctx = ctx.getChild(2)
                    if inic_ctx and inic_ctx.getChildCount() > 0:
                        var.setInicializado(self.linea_actual)
                
                # Intentar agregar (detecta doble declaración)
                if not ts.addSimbolo(var):
                    self.reportarErrorSemantico(
                        self.linea_actual,
                        f"Variable '{nombre_var}' ya fue declarada en este contexto"
                    )
                else:
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
    
    def enterFuncion(self, ctx:compiladorParser.FuncionContext):
        self.numFunciones += 1
        print("  " * self.indent + " FUNCION ENTER")
        self.indent += 1
        ts = TS.getInstance()
        ts.addContexto()
    
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
            ts.delContexto()
            ts.addSimbolo(funcion)
            
            self.indent -= 1
            print("  " * self.indent + f" FUNCION EXIT: {nombre_funcion}() -> {tipo_retorno}")
        else:
            self.indent -= 1
            print("  " * self.indent + " FUNCION EXIT (incompleta)")
    
    def enterIif(self, ctx:compiladorParser.IifContext):
        self.numIfs += 1
        print("  " * self.indent + "IF ENTER")
        self.indent += 1
        ts = TS.getInstance()
        ts.addContexto()  # Nuevo contexto para el scope del if
    
    def exitIif(self, ctx:compiladorParser.IifContext):
        self.indent -= 1
        ts = TS.getInstance()
        ts.delContexto()
        print("  " * self.indent + " IF EXIT")
    
    def enterIfor(self, ctx:compiladorParser.IforContext):
        self.numFors += 1
        print("  " * self.indent + " FOR ENTER")
        self.indent += 1
        ts = TS.getInstance()
        ts.addContexto()  # Nuevo contexto para el scope del for
    
    def exitIfor(self, ctx:compiladorParser.IforContext):
        self.indent -= 1
        ts = TS.getInstance()
        ts.delContexto()
        print("  " * self.indent + "FOR EXIT")
    
    # ============== DETECCIÓN DE USO DE VARIABLES ==============
    def enterAsignacion(self, ctx:compiladorParser.AsignacionContext):
        "Detecta asignaciones y verifica que la variable esté declarada"
        if ctx.getChildCount() >= 3:
            ts = TS.getInstance()
            linea = ctx.start.line if ctx.start else 0
            
            # ID está en la posición 0
            id_nombre = ctx.getChild(0).getText()
            
            # Buscar el símbolo en la tabla
            simbolo = ts.buscarSimbolo(id_nombre)
            
            if simbolo is None:
                # ERROR: Variable no declarada
                self.reportarErrorSemantico(
                    linea,
                    f"Variable '{id_nombre}' no ha sido declarada"
                )
            else:
                # Marcar como inicializada (porque se le asigna un valor)
                # NO marcar como usada aquí, porque la asignación no es "uso"
                simbolo.setInicializado(linea)
                
                # Verificar tipos incompatibles (simplificado)
                # Extraer el tipo del valor asignado (si es un literal)
                if ctx.getChildCount() >= 3:
                    opal_ctx = ctx.getChild(2)  # Obtener la expresión
                    tipo_valor = self.inferirTipo(opal_ctx)
                    
                    if tipo_valor and tipo_valor != simbolo.getTipoDato():
                        # Permitir int -> double (es válido)
                        if not (simbolo.getTipoDato() == "double" and tipo_valor == "int"):
                            self.reportarErrorSemantico(
                                linea,
                                f"Tipo incompatible: se intenta asignar '{tipo_valor}' a variable de tipo '{simbolo.getTipoDato()}'"
                            )
    
    def inferirTipo(self, ctx):
        """Intenta inferir el tipo de una expresión (simplificado)"""
        if ctx is None:
            return None
        
        texto = ctx.getText()
        
        # Si contiene punto decimal, es double
        if '.' in texto:
            return "double"
        
        # Si es solo dígitos, es int
        if texto.isdigit():
            return "int"
        
        # Si es un identificador, buscar su tipo
        ts = TS.getInstance()
        simbolo = ts.buscarSimbolo(texto)
        if simbolo:
            return simbolo.getTipoDato()
        
        # Si tiene hijos, revisar recursivamente
        if hasattr(ctx, 'getChildCount') and ctx.getChildCount() > 0:
            for i in range(ctx.getChildCount()):
                tipo = self.inferirTipo(ctx.getChild(i))
                if tipo:
                    return tipo
        
        return None
    
    def enterFactor(self, ctx:compiladorParser.FactorContext):
        "Detecta uso de variables en expresiones"
        # factor puede ser: PA exp PC | NUMERO | ID | ID PA argumentos? PC
        ts = TS.getInstance()
        linea = ctx.start.line if ctx.start else 0
        
        # Si el primer hijo es un ID (no es '(' ni número)
        if ctx.getChildCount() > 0:
            primer_hijo = ctx.getChild(0).getText()
            
            # Verificar si es un identificador
            if primer_hijo.isidentifier() and primer_hijo not in ['int', 'double', 'if', 'while', 'for', 'return']:
                simbolo = ts.buscarSimbolo(primer_hijo)
                
                if simbolo is None:
                    # ERROR: Variable no declarada
                    self.reportarErrorSemantico(
                        linea,
                        f"Variable '{primer_hijo}' no ha sido declarada"
                    )
                elif not simbolo.getInicializado():
                    # ERROR: Variable no inicializada
                    self.reportarErrorSemantico(
                        linea,
                        f"Variable '{primer_hijo}' usada sin inicializar"
                    )
                else:
                    # Marcar como usada
                    simbolo.setUsado()
                
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