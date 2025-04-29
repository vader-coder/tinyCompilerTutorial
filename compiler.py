from tokens import TokenType
from lexer import Lexer

class Compiler():
  def __init__(self, source):
    lexer = Lexer(source)
  
  def compile(self):
    token = lexer.getToken()
    
    while token.kind != TokenType.EOF:
      print(token.kind)
      token = lexer.getToken()


def main():
  source = "LABEL GOTO PRINT INPUT LET IF THEN ENDIF WHILE REPEAT ENDWHILE"
  compiler = Compiler(source)

main()
