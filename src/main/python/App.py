import sys
from antlr4 import *
from compiladorLexer import compiladorLexer
from compiladorParser import compiladorParser
from Escucha import Escucha

def main(argv):
    archivo = "input/simple.txt"
    if len(argv) > 1 :
        archivo = argv[1]
    input = FileStream(archivo)
    lexer = compiladorLexer(input)
    stream = CommonTokenStream(lexer)
    parser = compiladorParser(stream)
    escucha = Escucha()
    parser.addParseListener(escucha)
    tree = parser.programa()
    print(escucha)
    # print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main(sys.argv)