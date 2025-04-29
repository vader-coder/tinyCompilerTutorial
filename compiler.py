from enum import Enum

class Token:
  def __init__(self, tokenText, tokenKind):
    self.text = tokenText
    self.kind = tokenKind

  @staticmethod
  def checkIfKeyword(tokenText):
    for kind in TokenType:
      if kind.name == tokenText and kind.value >= 100:
        return kind
    return None

# TokenType is our enum for all the types of tokens.
class TokenType(Enum):
	EOF = -1
	NEWLINE = 0
	NUMBER = 1
	IDENTIFIER = 2
	STRING = 3

	# Keywords.
	LABEL = 101
	GOTO = 102
	PRINT = 103
	INPUT = 104
	LET = 105
	IF = 106
	THEN = 107
	ENDIF = 108
	WHILE = 109
	REPEAT = 110
	ENDWHILE = 111
	
  # Operators.
	EQ = 201  
	PLUS = 202
	MINUS = 203
	ASTERISK = 204
	SLASH = 205
	EQEQ = 206
	NOTEQ = 207
	LT = 208
	LTEQ = 209
	GT = 210
	GTEQ = 211

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
