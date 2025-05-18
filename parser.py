from tokens import Token, TokenType
from lexer import Lexer

# parser: https://austinhenley.com/blog/teenytinycompiler2.html
# need to make sure code follows correct grammar
class Parser:
  
  def __init__(self, lexer):
    self.lexer = lexer
    self.curToken = None
    self.peekToken = None
    self.nextToken()
    self.nextToken()

  # store next token at peek
  def nextToken(self):
    self.curToken = self.peekToken
    self.peekToken = self.lexer.getToken()

  def checkToken(self, kind):
    return self.curToken.kind == kind
  
  def checkPeek(self, kind):
    return self.peekToken.kind == kind

  # grammar expects a token of type 'kind' 
  def match(self, kind):
    if not self.checkToken(kind):
      self.abort(f"Expected token of type {kind}, received {self.curToken.kind}")
    self.nextToken()  

  def abort(self, message):
    sys.exit("Syntax errror. " + message)

  # loop over tokens until we reach end of file
  def program(self):
    while not self.checkToken(TokenType.EOF):
      self.statement()
  
  def statement(self):
    if self.checkToken(TokenType.PRINT):
      self.nextToken()
      if self.checkToken(TokenType.STRING):
        self.nextToken()
      else:
        self.expression()
    self.newline()

  def expression(self):
    pass
  
  # advance token pointers for each newline. 
  def newline(self):
    self.match(TokenType.NEWLINE)
    while self.checkToken(TokenType.NEWLINE):
      self.nextToken()

