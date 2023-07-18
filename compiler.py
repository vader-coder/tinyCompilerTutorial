from enum import Enum
class Lexer:
  def __init__(self, source):
    self.source = source + '\n'
    self.curChar = ''
    self.curPos = -1
    self.nextChar()
  
  def nextChar(self):
    self.curPos += 1
    if self.curPos >= len(self.source):
      self.curChar = '\0' # end of file
    else:
      self.curChar = self.source[self.curPos]

  def peek(self):
    if self.curPos + 1 >= len(self.source):
      return '\0' # end of file
    else:
      return self.source[self.curPos + 1]

  def abort(self, message):
    pass

  def skipWhitespace(self):
    while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
      self.nextChar()

  def skipComment(self):
    pass

  def getToken(self):
    token = None
    self.skipWhitespace()

    if self.curChar == '+':
      token = Token(self.curChar, TokenType.PLUS)
    elif self.curChar == '-':
      token = Token(self.curChar, TokenType.MINUS)
    elif self.curChar == '*':
      token = Token(self.curChar, TokenType.ASTERISK)
    elif self.curChar == '/':
      token = Token(self.curChar, TokenType.SLASH)
    elif self.curChar == '\n':
      token = Token(self.curChar, TokenType.NEWLINE)
    elif self.curChar == '\0':
      token = Token('', TokenType.EOF)
    elif self.curChar == '=':
      if self.peek() == '=':
        lastChar = self.curChar
        self.nextChar()
        token = Token(f"{lastChar}{self.curChar}", TokenType.EQEQ)
      else:
        token = Token(self.curChar, TokenType.EQ)
    elif self.curChar == '>':
      if self.peek() == '=':
        lastChar = self.curChar
        self.nextChar()
        token = Token(f"{lastChar}{self.curChar}", TokenType.GTEQ)
      else:
        token = Token(f"{lastChar}{self.curChar}", TokenType.GT)
    elif self.curChar == '<':
      if self.peek() == '=':
        lastChar = self.curChar
        self.nextChar()
        token = Token(f"{lastChar}{self.curChar}", TokenType.LTEQ)
      else:
        token = Token(f"{lastChar}{self.curChar}", TokenType.LT)
    elif self.curChar == '!':
      if self.peek() == '=':
        lastChar = self.curChar
        self.nextChar()
        token = Token(f"{lastChar}{self.curChar}", TokenType.NOTEQ)
      else:
        self.abort("! is not a valid token")
    elif self.curChar.isdigit():
      startPos = self.curPos
      while self.peek().isdigit():
        self.nextChar()
      if self.peek() == '.':
        self.nextChar()
        if not self.peek().isdigit():
          self.abort("Digit must follow . in number")
          return token
        while self.peek().isdigit():
          self.nextChar()
      tokenText = self.source[startPos:self.curPos+1]
      token = Token(tokenText, TokenType.NUMBER)
    elif self.curChar.isalpha(): # identifiers are alphanumeric 
      startPos = self.curPos
      while self.peek().isalnum() or self.peek() == '_':
        self.nextChar()
      tokenText = self.source[startPos : self.curPos + 1]
      keywordKind = Token.checkIfKeyword(tokenText)
      if keywordKind == None:
        token = Token(tokenText, TokenType.IDENT)
      else:
        token = Token(tokenText, keywordKind)
    else:
      # Unknown token!
      pass
    self.nextChar()
    return token

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

def main():
  source = "LABEL GOTO PRINT INPUT LET IF THEN ENDIF WHILE REPEAT ENDWHILE"
  lexer = Lexer(source)
  token = lexer.getToken()
  
  while token.kind != TokenType.EOF:
    print(token.kind)
    token = lexer.getToken()

main()
