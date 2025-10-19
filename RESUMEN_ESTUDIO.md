# 📚 RESUMEN DE ESTUDIO - COMPILADOR CON ANTLR Y PYTHON

## 🎯 OBJETIVO DEL PROYECTO
Construir un **analizador sintáctico y semántico** para un lenguaje tipo C que:
- Reconoce declaraciones de variables
- Reconoce estructuras de control (if, while, for)
- Reconoce funciones
- Mantiene una **tabla de símbolos** con contextos anidados

---

## 🏗️ ARQUITECTURA DEL SISTEMA

### Componentes Principales

```
┌─────────────────┐
│  Código Fuente  │  (input/simple.txt)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  compilador.g4  │  ← Gramática ANTLR
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     ANTLR       │  ← Genera Lexer y Parser
└────────┬────────┘
         │
         ├──► compiladorLexer.py (Análisis Léxico)
         └──► compiladorParser.py (Análisis Sintáctico)
                      │
                      ▼
         ┌────────────────────────┐
         │    Árbol de Parseo     │
         └────────────────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │      Escucha.py        │  ← Listener (Análisis Semántico)
         └────────────────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │  tablaDeSimbolos.py    │  ← Almacena variables y funciones
         └────────────────────────┘
```

---

## 📖 PARTE 1: GRAMÁTICA (compilador.g4)

### ¿Qué es una gramática?
Define las **reglas sintácticas** del lenguaje. ANTLR la usa para generar el Lexer y Parser.

### Componentes de la Gramática

#### 1️⃣ **TOKENS (Elementos Léxicos)**
```antlr
// Palabras reservadas
INT : 'int' ;
DOUBLE : 'double' ;
IF : 'if' ;
WHILE : 'while' ;
FOR : 'for' ;

// Operadores
ASIG : '=' ;
SUMA : '+' ;
MENOR : '<' ;

// Identificadores y números
ID : (LETRA | '_')(LETRA | DIGITO | '_')* ;
NUMERO : DIGITO+ ;
```

**Explicación:**
- Los tokens son los "átomos" del lenguaje (palabras reservadas, operadores, identificadores).
- El Lexer convierte el texto en una secuencia de tokens.

#### 2️⃣ **REGLAS DE PRODUCCIÓN**

##### Declaración de Variables
```antlr
declaracion : tipo ID inic listavar PYC ;

tipo : INT | DOUBLE ;

inic : ASIG opal
     |                    // ← Puede estar vacío
     ;

listavar: COMA ID inic listavar
        |                // ← Puede estar vacío
        ;
```

**Ejemplo de uso:**
```c
int x, y, z;
```

**¿Cómo se parsea?**
1. `tipo` → reconoce `int`
2. `ID` → reconoce `x`
3. `inic` → vacío (no hay `=`)
4. `listavar` → `, y` luego `, z`
5. `PYC` → `;`

**Estructura del árbol:**
```
declaracion
├── tipo (int)
├── ID (x)
├── inic (vacío)
├── listavar
│   ├── COMA (,)
│   ├── ID (y)
│   ├── inic (vacío)
│   └── listavar
│       ├── COMA (,)
│       ├── ID (z)
│       ├── inic (vacío)
│       └── listavar (vacío)
└── PYC (;)
```

##### Estructura While
```antlr
iwhile : WHILE PA opal PC instruccion ;
```

**Ejemplo:**
```c
while (x < 10)
    x = x + 1;
```

**Componentes:**
- `WHILE` → palabra reservada
- `PA` → `(`
- `opal` → expresión de condición (`x < 10`)
- `PC` → `)`
- `instruccion` → cuerpo del while

##### Estructura If
```antlr
iif : IF PA opal PC instruccion ielse ;

ielse : ELSE instruccion
      |                    // ← ELSE es opcional
      ;
```

##### Estructura For
```antlr
ifor : FOR PA (asignacionFor | declaracionFor) PYC opal PYC asignacionFor PC bloque ;
```

**Ejemplo:**
```c
for (int i = 0; i < 5; i++) {
    y = y + i;
}
```

##### Funciones
```antlr
funcion : tipo ID PA parametros PC bloque ;

parametros : ID lista_param
          ;

lista_param : COMA ID lista_param
            |
            ;

bloque : LLA instrucciones LLC ;
```

**Ejemplo:**
```c
int suma(int a, int b) {
    return a + b;
}
```

---

## 📖 PARTE 2: TABLA DE SÍMBOLOS (tablaDeSimbolos.py)

### ¿Qué es la Tabla de Símbolos?
Es una estructura que almacena **información sobre variables y funciones** declaradas en el programa.

### Estructura de Clases

#### 1️⃣ **Clase TS (Tabla de Símbolos) - Singleton**

```python
class TS:
    _instance = None  # ← Patrón Singleton (una sola instancia)
    
    def __init__(self):
        self.contextos = [Contexto()]  # ← Lista de contextos (scopes)
```

**¿Por qué Singleton?**
- Solo debe existir UNA tabla de símbolos en todo el programa.
- `getInstance()` asegura que siempre se use la misma instancia.

**Métodos principales:**

```python
def addContexto(self):
    """Crea un nuevo scope (por ejemplo, dentro de una función o while)"""
    self.contextos.append(Contexto())

def delContexto(self):
    """Elimina el scope actual al salir de una función o bloque"""
    if len(self.contextos) > 1:
        self.contextos.pop()

def addSimbolo(self, simbolo):
    """Agrega una variable o función al contexto ACTUAL"""
    self.contextos[-1].addSimbolo(simbolo)

def buscarSimbolo(self, nombre):
    """Busca un símbolo en TODOS los contextos (de adentro hacia afuera)"""
    for contexto in reversed(self.contextos):
        simbolo = contexto.buscarSimbolo(nombre)
        if simbolo:
            return simbolo
    return None
```

**Ejemplo de uso:**
```python
ts = TS.getInstance()
ts.addSimbolo(Variable("x", "int"))
ts.addSimbolo(Variable("y", "int"))
```

**Estado de la tabla:**
```
Contexto 0 (Global):
  x: int
  y: int
```

#### 2️⃣ **Clase Contexto**

```python
class Contexto:
    def __init__(self):
        self.simbolos = {}  # ← Diccionario: nombre → símbolo
    
    def addSimbolo(self, simbolo):
        self.simbolos[simbolo.nombre] = simbolo
    
    def buscarSimbolo(self, nombre):
        return self.simbolos.get(nombre)
```

**¿Qué es un contexto?**
- Representa un **scope** o ámbito de visibilidad.
- Variables declaradas en un contexto interno NO son visibles desde afuera.

**Ejemplo:**
```c
int x = 5;        // ← Contexto 0 (global)

while (x < 10) {  // ← Contexto 1 (while)
    int y = 10;   // ← Solo visible dentro del while
    x = x + 1;
}
```

**Estado de contextos:**
```
Contexto 0:
  x: int

Contexto 1 (dentro del while):
  y: int
```

#### 3️⃣ **Clase Variable**

```python
class Variable(ID):
    def __init__(self, nombre, tipoDato, esGlobal=False):
        super().__init__(nombre, tipoDato)
        self.esGlobal = esGlobal
```

**Atributos heredados de ID:**
- `nombre`: nombre de la variable
- `tipoDato`: tipo de dato (int, double)
- `inicializado`: si fue inicializada
- `usado`: si fue usada en el código

#### 4️⃣ **Clase Funcion**

```python
class Funcion(ID):
    def __init__(self, nombre, tipoDato, args=None):
        super().__init__(nombre, tipoDato)
        self.args = args if args is not None else []  # ← Lista de parámetros
```

**Ejemplo:**
```python
funcion = Funcion("suma", "int", ["int a", "int b"])
```

---

## 📖 PARTE 3: LISTENER (Escucha.py)

### ¿Qué es un Listener?
Es una clase que **escucha eventos** mientras ANTLR recorre el árbol de parseo.

### Patrón de Eventos

Para cada regla de la gramática, ANTLR genera dos eventos:
- `enterRegla`: cuando ENTRA a un nodo
- `exitRegla`: cuando SALE de un nodo

**Ejemplo:**
```
enterPrograma
  enterDeclaracion
  exitDeclaracion
  enterWhile
    enterAsignacion
    exitAsignacion
  exitWhile
exitPrograma
```

### Variables de Instancia

```python
class Escucha(compiladorListener):
    indent = 1           # ← Nivel de indentación para impresión
    declaracion = 0      # ← Contador de declaraciones
    numFunciones = 0     # ← Contador de funciones
    numWhiles = 0        # ← Contador de whiles
    numFors = 0          # ← Contador de fors
    numIfs = 0           # ← Contador de ifs
    tipo_actual = None   # ← Tipo de dato actual (para listavar)
```

---

### 🔍 RECONOCIMIENTO DE DECLARACIONES

#### Método: `enterDeclaracion`
```python
def enterDeclaracion(self, ctx: compiladorParser.DeclaracionContext):
    self.declaracion += 1
    print("Declaracion ENTER -> |" + ctx.getText() + "|")
```

**¿Qué hace?**
- Se ejecuta cuando ENTRA a una declaración.
- Incrementa el contador.
- Imprime el texto completo de la declaración.

**Problema:** En `enter`, los hijos del árbol aún NO están disponibles.

#### Método: `exitDeclaracion` ⭐
```python
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
        self.tipo_actual = tipo
        self.procesar_listavar(ctx.getChild(3), ts)
        self.tipo_actual = None
```

**¿Qué hace?**
1. Se ejecuta cuando SALE de la declaración (árbol completo).
2. Verifica que hay al menos 3 hijos (tipo, ID, inic).
3. Extrae el **tipo** del primer hijo.
4. Extrae el **primer identificador** del segundo hijo.
5. Crea una instancia de `Variable` y la agrega a la tabla.
6. Llama a `procesar_listavar` para procesar variables adicionales.

**¿Por qué en `exit` y no en `enter`?**
- En `enterDeclaracion`, `ctx.children` es `None` porque ANTLR aún está construyendo el árbol.
- En `exitDeclaracion`, el árbol ya está completo y podemos acceder a los hijos.

#### Método: `procesar_listavar` (Recursivo) ⭐

```python
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
```

**¿Qué hace?**
1. Caso base: si no hay hijos o son menos de 2, retorna.
2. Extrae el nombre de la variable (hijo en posición 1).
3. Crea una `Variable` con el `tipo_actual` guardado.
4. **RECURSIÓN:** llama a sí misma para procesar el siguiente `listavar` (hijo en posición 3).

**Ejemplo de ejecución:**
```c
int x, y, z;
```

```
exitDeclaracion → procesa 'x'
  procesar_listavar(listavar1) → procesa 'y'
    procesar_listavar(listavar2) → procesa 'z'
      procesar_listavar(listavar3) → vacío, retorna
```

**Resultado en la tabla:**
```
Contexto 0:
  x: int
  y: int
  z: int
```

---

### 🔍 RECONOCIMIENTO DE FUNCIONES

#### Método: `enterFuncion`
```python
def enterFuncion(self, ctx:compiladorParser.FuncionContext):
    self.numFunciones += 1
    print("  " * self.indent + "╔═ FUNCION ENTER")
    self.indent += 1
    ts = TS.getInstance()
    ts.addContexto()  # ← Crea un nuevo contexto para el scope de la función
```

**¿Qué hace?**
- Incrementa el contador de funciones.
- **Crea un nuevo contexto** (scope local de la función).
- Las variables declaradas dentro de la función irán a este contexto.

#### Método: `exitFuncion`
```python
def exitFuncion(self, ctx:compiladorParser.FuncionContext):
    # Estructura: tipo ID PA parametros PC bloque
    if ctx.getChildCount() >= 6:
        tipo_retorno = ctx.getChild(0).getText()
        nombre_funcion = ctx.getChild(1).getText()
        
        # Extraer parámetros
        params = []
        parametros_ctx = ctx.getChild(3)
        if parametros_ctx and parametros_ctx.getChildCount() > 0:
            params.append("...")
        
        ts = TS.getInstance()
        funcion = Funcion(nombre_funcion, tipo_retorno, params)
        ts.delContexto()  # ← Elimina el contexto local
        ts.addSimbolo(funcion)  # ← Agrega la función al contexto EXTERNO
        
        self.indent -= 1
        print("  " * self.indent + f"╚═ FUNCION EXIT: {nombre_funcion}() -> {tipo_retorno}")
```

**¿Qué hace?**
1. Extrae el **tipo de retorno** (hijo 0).
2. Extrae el **nombre de la función** (hijo 1).
3. Extrae los **parámetros** (simplificado).
4. **Elimina el contexto local** de la función.
5. **Agrega la función al contexto externo** (global o del bloque contenedor).

**Flujo de contextos:**
```c
int suma(int a, int b) {
    int resultado;
    return resultado;
}
```

```
Antes de enterFuncion:
  Contexto 0 (global): []

Dentro de la función (después de enterFuncion):
  Contexto 0 (global): []
  Contexto 1 (suma): [resultado: int]

Después de exitFuncion:
  Contexto 0 (global): [suma: int]
```

---

### 🔍 RECONOCIMIENTO DE ESTRUCTURAS DE CONTROL

#### WHILE

```python
def enterIwhile(self, ctx:compiladorParser.IwhileContext):
    self.numWhiles += 1
    print("  "*self.indent + "╔═ WHILE ENTER")
    self.indent += 1
    ts = TS.getInstance()
    ts.addContexto()  # ← Nuevo scope para el while

def exitIwhile(self, ctx:compiladorParser.IwhileContext):
    self.indent -= 1
    print("  "*self.indent + "╚═ WHILE EXIT")
    ts = TS.getInstance()
    ts.delContexto()  # ← Elimina el scope del while
```

**¿Por qué crear un contexto?**
- Las variables declaradas dentro del while NO deben ser visibles fuera.

#### IF

```python
def enterIif(self, ctx:compiladorParser.IifContext):
    self.numIfs += 1
    print("  " * self.indent + "╔═ IF ENTER")
    self.indent += 1
    ts = TS.getInstance()
    ts.addContexto()

def exitIif(self, ctx:compiladorParser.IifContext):
    self.indent -= 1
    ts = TS.getInstance()
    ts.delContexto()
    print("  " * self.indent + "╚═ IF EXIT")
```

#### FOR

```python
def enterIfor(self, ctx:compiladorParser.IforContext):
    self.numFors += 1
    print("  " * self.indent + "╔═ FOR ENTER")
    self.indent += 1
    ts = TS.getInstance()
    ts.addContexto()

def exitIfor(self, ctx:compiladorParser.IforContext):
    self.indent -= 1
    ts = TS.getInstance()
    ts.delContexto()
    print("  " * self.indent + "╚═ FOR EXIT")
```

---

## 📖 PARTE 4: FUNCIONAMIENTO COMPLETO

### Ejemplo de Código de Entrada

```c
int x, y, z;
x = 5;

while (x < 10) {
    int temp;
    temp = x + 1;
    x = temp;
}
```

### Flujo de Ejecución Paso a Paso

#### 1️⃣ **Análisis Léxico (Lexer)**
```
Entrada: "int x, y, z;"
Tokens: [INT, ID(x), COMA, ID(y), COMA, ID(z), PYC]
```

#### 2️⃣ **Análisis Sintáctico (Parser)**
Construye el árbol de parseo según la gramática.

```
declaracion
├── tipo (int)
├── ID (x)
├── inic (vacío)
├── listavar
│   ├── COMA
│   ├── ID (y)
│   ├── inic (vacío)
│   └── listavar
│       ├── COMA
│       ├── ID (z)
│       ├── inic (vacío)
│       └── listavar (vacío)
└── PYC
```

#### 3️⃣ **Análisis Semántico (Listener)**

**Eventos disparados:**
```
enterPrograma
  enterDeclaracion
  exitDeclaracion  ← AQUÍ se agregan x, y, z a la tabla
  enterAsignacion
  exitAsignacion
  enterIwhile  ← Crea Contexto 1
    enterDeclaracion
    exitDeclaracion  ← temp se agrega a Contexto 1
    enterAsignacion
    exitAsignacion
    enterAsignacion
    exitAsignacion
  exitIwhile  ← Elimina Contexto 1
exitPrograma
```

**Estado de la Tabla de Símbolos:**

```
Al salir del programa:
Contexto 0 (global):
  x: int
  y: int
  z: int

Contexto 1 fue eliminado (temp ya no existe)
```

---

## 🎓 CONCEPTOS CLAVE PARA ESTUDIAR

### 1. **Patrón Visitor vs Listener**
- **Listener:** Recorre automáticamente el árbol. Solo defines qué hacer en cada nodo.
- **Visitor:** Tú controlas el recorrido. Más flexible pero más complejo.

### 2. **Contextos Anidados (Scopes)**
```c
int x = 5;           // Contexto 0

{                    // Contexto 1
    int y = 10;
    {                // Contexto 2
        int z = 15;
    }
}
```

**Regla de búsqueda:**
- Buscar de adentro hacia afuera.
- Si `z` no está en Contexto 2, buscar en Contexto 1, luego en Contexto 0.

### 3. **Enter vs Exit**
- **Enter:** El nodo acaba de ser visitado, los hijos pueden no estar disponibles.
- **Exit:** El nodo está completo, todos los hijos fueron procesados.

### 4. **Recursión en Árboles**
```python
def procesar_listavar(self, ctx, ts):
    # Caso base
    if ctx is None or ctx.getChildCount() < 2:
        return
    
    # Procesar nodo actual
    nombre_var = ctx.getChild(1).getText()
    ts.addSimbolo(Variable(nombre_var, self.tipo_actual))
    
    # Llamada recursiva
    self.procesar_listavar(ctx.getChild(3), ts)
```

### 5. **Singleton Pattern**
```python
class TS:
    _instance = None
    
    @staticmethod
    def getInstance():
        if TS._instance is None:
            TS._instance = TS()
        return TS._instance
```

**Garantiza:** Solo UNA tabla de símbolos en todo el programa.

---

## 🧪 EJEMPLOS DE PRUEBA

### Ejemplo 1: Declaración Simple
```c
int x;
```

**Árbol:**
```
declaracion
├── tipo (int)
├── ID (x)
├── inic (vacío)
├── listavar (vacío)
└── PYC
```

**Salida:**
```
Declaracion EXIT -> |intx;|
  -- Tipo detectado: int
  -> Variable 'x' de tipo 'int' agregada
```

### Ejemplo 2: Declaración Múltiple
```c
int x, y, z;
```

**Salida:**
```
Declaracion EXIT -> |intx,y,z;|
  -- Tipo detectado: int
  -> Variable 'x' de tipo 'int' agregada
  -> Variable 'y' de tipo 'int' agregada
  -> Variable 'z' de tipo 'int' agregada
```

### Ejemplo 3: While con Contexto
```c
int x;
while (x < 10) {
    int y;
}
```

**Salida:**
```
Declaracion EXIT -> |intx;|
  -> Variable 'x' de tipo 'int' agregada

╔═ WHILE ENTER
  Declaracion EXIT -> |inty;|
    -> Variable 'y' de tipo 'int' agregada
╚═ WHILE EXIT

Tabla de Símbolos:
Contexto 0:
  x: int
```

**Nota:** `y` NO aparece en la tabla final porque su contexto fue eliminado.

---

## 📌 PREGUNTAS DE REPASO

1. **¿Por qué `exitDeclaracion` y no `enterDeclaracion` para extraer variables?**
   - Porque en `enter` los hijos no están disponibles (`ctx.children` es `None`).

2. **¿Qué es un contexto en la tabla de símbolos?**
   - Un scope o ámbito de visibilidad. Variables en contextos internos no son visibles afuera.

3. **¿Cómo se procesa `int x, y, z;`?**
   - Se extrae `x` directamente, luego se llama recursivamente a `procesar_listavar` para `y` y `z`.

4. **¿Por qué usar Singleton para la tabla de símbolos?**
   - Para garantizar que solo existe UNA tabla en todo el programa.

5. **¿Qué pasa cuando entramos a un `while`?**
   - Se crea un nuevo contexto. Las variables declaradas dentro solo son visibles en ese contexto.

6. **¿Cuál es la diferencia entre `Variable` y `Funcion`?**
   - `Funcion` tiene una lista de parámetros, `Variable` tiene un atributo `esGlobal`.

7. **¿Cómo ANTLR sabe cuándo llamar a `enterDeclaracion`?**
   - ANTLR genera el código automáticamente basándose en la gramática. Cuando el parser reconoce la regla `declaracion`, dispara el evento.

---

## 🚀 MEJORAS FUTURAS

1. **Validación semántica:**
   - Verificar que las variables usadas estén declaradas.
   - Verificar tipos en asignaciones.

2. **Extracción de parámetros de funciones:**
   - Procesar correctamente `int a, int b`.

3. **Detección de errores:**
   - Variables duplicadas en el mismo contexto.
   - Variables no inicializadas.

4. **Generación de código intermedio:**
   - Traducir a código de tres direcciones.

---

## 📚 RECURSOS ADICIONALES

- **Documentación ANTLR:** https://www.antlr.org/
- **Libro "The Definitive ANTLR 4 Reference"** de Terence Parr
- **Tutorial Python + ANTLR:** https://github.com/antlr/antlr4/blob/master/doc/python-target.md

---

**¡Fin del Resumen! 🎉**