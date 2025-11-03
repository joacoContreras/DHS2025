import sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from compiladorLexer import compiladorLexer
from compiladorParser import compiladorParser
from Escucha import Escucha

class CustomErrorListener(ErrorListener):
    """Listener personalizado para capturar errores sintácticos de ANTLR"""
    def __init__(self, escucha):
        super().__init__()
        self.escucha = escucha
    
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # Simplificar el mensaje de error
        mensaje_simple = msg
        if "mismatched input" in msg:
            mensaje_simple = "Token inesperado o falta de un símbolo esperado"
        elif "missing" in msg:
            if "';'" in msg:
                mensaje_simple = "Falta un punto y coma (;)"
            elif "'('" in msg:
                mensaje_simple = "Falta un paréntesis de apertura '('"
            elif "')'" in msg:
                mensaje_simple = "Falta un paréntesis de cierre ')'"
            else:
                mensaje_simple = f"Falta: {msg.split('missing')[1].strip()}"
        elif "extraneous input" in msg:
            mensaje_simple = "Símbolo adicional no esperado"
        elif "no viable alternative" in msg:
            mensaje_simple = "Sintaxis incorrecta"
        
        self.escucha.reportarErrorSintactico(line, mensaje_simple)

def main(argv):
    archivo = "/home/joacontreras/Documents/GitHub/DHS2025_JC/input/conErrores.txt"
    if len(argv) > 1 :
        archivo = argv[1]
    
    print(f"Analizando archivo: {archivo}\n")
    
    # Abrir el archivo de entrada con codificación UTF-8
    input = FileStream(archivo, encoding='utf-8')
    lexer = compiladorLexer(input)
    stream = CommonTokenStream(lexer)
    parser = compiladorParser(stream)
    
    # Crear el listener (escucha)
    escucha = Escucha()
    
    # Remover los listeners por defecto y agregar el personalizado
    parser.removeErrorListeners()
    parser.addErrorListener(CustomErrorListener(escucha))
    
    # Parsear el programa
    tree = parser.programa()
    
    # RECORRER EL ÁRBOL con el listener 
    from antlr4.tree.Tree import ParseTreeWalker
    walker = ParseTreeWalker()
    walker.walk(escucha, tree)
    
    print("\n" + "="*60)
    print(escucha)
    print("="*60)
    
    # Solo mostrar el árbol si NO hay errores
    if not escucha.tieneErrores():
        print("\nÁRBOL SINTÁCTICO:")
        print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main(sys.argv)