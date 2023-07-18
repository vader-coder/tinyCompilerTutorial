import unittest
from compiler import Lexer, Token, TokenType

class TestLexer(unittest.TestCase):
  def test_upper(self):
    self.assertEqual('foo'.upper(), 'FOO')

  def test_character_detection(self):
    source = "LET foobar = 123"
    lexer = Lexer(source)
    output = []
    while lexer.peek() != '\0':
      output.append(lexer.curChar)
      lexer.nextChar()
    self.assertEqual(''.join(output), source)

  def test_single_character_tokens(self):
    source = "+- */="
    lexer = Lexer(source)
    self.assertEqual(lexer.getToken().kind, TokenType.PLUS)
    self.assertEqual(lexer.getToken().kind, TokenType.MINUS)
    self.assertEqual(lexer.getToken().kind, TokenType.ASTERISK)
    self.assertEqual(lexer.getToken().kind, TokenType.SLASH)
    self.assertEqual(lexer.getToken().kind, TokenType.EQ)
    self.assertEqual(lexer.getToken().kind, TokenType.NEWLINE) # Unknown token!

  def test_multi_character_tokens(self):
    source = "== >= <= !="
    lexer = Lexer(source)
    self.assertEqual(lexer.getToken().kind, TokenType.EQEQ)
    self.assertEqual(lexer.getToken().kind, TokenType.GTEQ)
    self.assertEqual(lexer.getToken().kind, TokenType.LTEQ)
    self.assertEqual(lexer.getToken().kind, TokenType.NOTEQ)

  def test_number_tokens(self):
    source = "123 9.8654"
    lexer = Lexer(source)
    self.assertEqual(lexer.getToken().kind, TokenType.NUMBER)
    self.assertEqual(lexer.getToken().kind, TokenType.NUMBER)
    self.assertEqual(lexer.getToken().kind, TokenType.NEWLINE)

  def test_nonumber_tokens(self):
    source = " 9. "
    lexer = Lexer(source)
    self.assertEqual(lexer.getToken(), None)

  def test_keywords(self):
    source = "LABEL GOTO PRINT INPUT LET IF THEN ENDIF WHILE REPEAT ENDWHILE"
    lexer = Lexer(source)
    self.assertEqual(lexer.getToken().kind, TokenType.LABEL)
    self.assertEqual(lexer.getToken().kind, TokenType.GOTO)
    self.assertEqual(lexer.getToken().kind, TokenType.PRINT)
    self.assertEqual(lexer.getToken().kind, TokenType.INPUT)
    self.assertEqual(lexer.getToken().kind, TokenType.LET)
    self.assertEqual(lexer.getToken().kind, TokenType.IF) 
    self.assertEqual(lexer.getToken().kind, TokenType.THEN)
    self.assertEqual(lexer.getToken().kind, TokenType.ENDIF)
    self.assertEqual(lexer.getToken().kind, TokenType.WHILE)
    self.assertEqual(lexer.getToken().kind, TokenType.REPEAT)
    self.assertEqual(lexer.getToken().kind, TokenType.ENDWHILE) 
    self.assertEqual(lexer.getToken().kind, TokenType.NEWLINE) 


if __name__ == '__main__':
  unittest.main()
