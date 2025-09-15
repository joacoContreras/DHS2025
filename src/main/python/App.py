import sys
from antlr4 import *
from compiladorLexer import compiladorLexer
# from compiladorParser import compiladorParser


def main(argv):
    archivo = "input/entrada.txt"
    if len(argv) > 1 :
        archivo = argv[1]
    input = FileStream(archivo)
    lexer = compiladorLexer(input)
    stream = CommonTokenStream(lexer)
    # Print all tokens from the lexer
    token = lexer.nextToken()
    while token.type != Token.EOF:
        print(f'Token: {token.text} (type: {token.type})')
        token = lexer.nextToken()
    # parser = compiladoresParser(stream)
    # tree = parser.s()
    # print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main(sys.argv)