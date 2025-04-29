from enum import Enum
from compiler import Token, TokenType

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