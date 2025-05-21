from tokens import Token, TokenType
from lexer import Lexer
from emitter import Emitter

# parser: https://austinhenley.com/blog/teenytinycompiler2.html
# need to make sure code follows correct grammar
class Parser:
  
  def __init__(self, lexer, emitter):
    self.lexer = lexer
    self.emitter = emitter

    self.symbols = set()
    self.labelsDeclared = set()
    self.labelsGotoed = set()

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
    self.emitter.headerLine("#include <stdio.h>")
    self.emitter.headerLine("int main(void) {")

    while(self.checkToken(TokenType.NEWLINE)):
      self.nextToken()

    while not self.checkToken(TokenType.EOF):
      self.statement()

    self.emitter.emitLine("return 0;")
    self.emitter.emitLine("}")

    for label in self.labelsGotoed:
      if label not in self.labelsDeclared:
        self.abort("Cannot GOTO undeclared label " + label)
  
  def statement(self):
    # statement ::= "PRINT" (expression | string) nl
    if self.checkToken(TokenType.PRINT):
      self.nextToken()
      if self.checkToken(TokenType.STRING):
        self.emitter.emitLine("printf(\"" + self.curToken.text + "\\n\");")
        self.nextToken()
      else:
        # print expression result as a float
        self.emitter.emit("printf(\"%" + ".2f\\n\", (float)(")
        self.expression()
        self.emitter.emitLine("));")
    
    # "IF" comparison "THEN" {statement} "ENDIF"
    elif self.checkToken(TokenType.IF):
      self.nextToken()
      self.emitter.emit("if (")
      self.comparison()
      
      self.match(TokenType.THEN)
      self.newline()
      self.emitter.emitLine("}")

      while not self.checkToken(TokenType.ENDIF):
        self.statement()
      self.match(TokenType.ENDIF)
      self.emitter.emitLine("}")
    
    # "WHILE" comparison "REPEAT" {statement} "ENDWHILE"
    elif self.checkToken(TokenType.WHILE):
      self.nextToken()
      self.emitter.emit("while (")
      self.comparison()
      
      self.match(TokenType.REPEAT)
      self.newline()
      self.emitter.emitLine("){")

      while not self.checkToken(TokenType.ENDWHILE):
        self.statement()
      self.match(TokenType.ENDWHILE)
      self.emitter.emitLine("}")

    # "LABEL" ident nl
    elif self.checkToken(TokenType.LABEL):
      self.nextToken()
      
      if self.curToken.text in self.labelsDeclared:
        self.abort("Label already exists" + self.curToken.text)
      self.labelsDeclared.add(self.curToken.text)

      self.emitter.emitLine(self.curToken.text + ":")
      self.match(TokenType.IDENT)

    # "GOTO" ident nl
    elif self.checkToken(TokenType.GOTO):
      self.nextToken()
      self.labelsGotoed.add(self.curToken.text)
      
      self.emitter.emitLine("goto " + self.curToken.text)
      self.match(TokenType.IDENT)

    # "LET" ident "=" expression
    elif self.checkToken(TokenType.LET):
      self.nextToken()

      if self.curToken.text not in self.symbols:
        self.symbols.add(self.curToken.text)
        self.emitter.headerLine("float " + self.curToken.text + ";")

      self.emitter.emit(self.curToken.text + " = ")
      self.match(TokenType.IDENT)
      self.match(TokenType.EQ)

      self.expression()
      self.emitter.emitLine(";")

    # "INPUT" ident
    elif self.checkToken(TokenType.INPUT):
      self.nextToken()

      if self.curToken.text not in self.symbols:
        self.symbols.add(self.curToken.text)

      self.match(TokenType.IDENT)

    self.newline()

  # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
  def comparison(self):
    self.expression()
    if self.isComparisonOperator():
      self.nextToken()
      self.expression()
    else:
      self.abort("Expected comparison operator at: " + self.curToken.text)
    
    while self.isComparisonOperator():
      self.nextToken()
      self.expression()

  def isComparisonOperator(self):
    return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)
  
  # expression ::= term {( "-" | "+" ) term}
  def expression(self):
    self.term()
    while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
      self.nextToken()
      self.term()
  
  # term ::= unary {( "/" | "*" ) unary}
  def term(self):
    self.unary()

    while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
      self.nextToken()
      self.unary()

  # unary ::= ["+" | "-"] primary
  def unary(self):
    if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
      self.nextToken()
    self.primary()
  
  # primary ::= number | ident
  def primary(self):
    if self.checkToken(TokenType.NUMBER):
      self.nextToken()
    elif self.checkToken(TokenType.IDENT):
      if self.curToken.text not in self.symbols:
        self.abort("Referencing variable before assignment: " + self.curToken.text)
      self.nextToken()
    else:
      self.abort("Unexpected token at " + self.curToken.text)
  
  # advance token pointers for each newline. 
  def newline(self):
    self.match(TokenType.NEWLINE)
    while self.checkToken(TokenType.NEWLINE):
      self.nextToken()

