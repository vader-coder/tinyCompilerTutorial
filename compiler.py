from tokens import TokenType
from lexer import Lexer
from emitter import Emitter
from parser import Parser
import sys

class Compiler():
  def __init__(self, source, outputFile):
    self.lexer = Lexer(source)
    self.emitter = Emitter(outputFile)
    self.parser = Parser(self.lexer, self.emitter)
  
  def compile(self):
    self.parser.program()
    self.emitter.writeFile()

# python3 compiler.py test_code.teeny
def main():
  print("Teeny Tiny Compileer")
  
  if len(sys.argv) < 2:
    sys.exit("Error: Compiler needs source file path")

  with(open(sys.argv[1], 'r')) as f:
    source = f.read()

  outputFile = "out.c"
  if len(sys.argv) > 2:
    outputFile = sys.argv[2]

  compiler = Compiler(source, outputFile)
  compiler.compile()
  print("Compiling completed")


main()
