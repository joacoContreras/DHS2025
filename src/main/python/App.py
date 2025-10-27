import sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from compiladorLexer import compiladorLexer
from compiladorParser import compiladorParser
from Escucha import Escucha
from ErrorReporter import ErrorReporter

class CustomErrorListener(ErrorListener):
    """Listener personalizado para capturar errores sintácticos de ANTLR"""
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        reporter = ErrorReporter.getInstance()
        
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
        
        reporter.reportarErrorSintactico(line, mensaje_simple)

def main(argv):
    archivo = "/home/joacontreras/Documents/GitHub/DHS2025_JC/input/simple.txt"
    if len(argv) > 1 :
        archivo = argv[1]
    
    print(f"Analizando archivo: {archivo}\n")
    
    # Abrir el archivo de entrada con codificación UTF-8
    input = FileStream(archivo, encoding='utf-8')
    lexer = compiladorLexer(input)
    stream = CommonTokenStream(lexer)
    parser = compiladorParser(stream)
    
    # Remover los listeners por defecto y agregar el personalizado
    parser.removeErrorListeners()
    parser.addErrorListener(CustomErrorListener())
    
    escucha = Escucha()
    parser.addParseListener(escucha)
    tree = parser.programa()
    
    # Imprimir estadísticas
    print("\n" + "="*60)
    print(escucha)
    print("="*60)
    
    # Solo mostrar el árbol si NO hay errores
    reporter = ErrorReporter.getInstance()
    if not reporter.tieneErrores():
        print("\nÁRBOL SINTÁCTICO:")
        print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main(sys.argv)