import ply.lex as lex
import ply.yacc as yacc
import sys

#tokens list specifying all of the possible tokens
tokens = [
   'NUMBER',
   'PLUS',
   'MINUS',
   'MULT',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'ID',
   'COMMA',
   'SEMICOLON',
   'LEFTBRACE',
   'RIGHTBRACE',
   'ASSIGN',
   'EQUAL',
]

reserved = {
	'malloc' : 	'MALLOC',
	'sizeof' : 'SIZEOF',
    'while' : 'WHILE',
    'else' : 'ELSE',
    'if' : 'IF',
    'for' : 'FOR',
    'switch':'SWITCH',
    'case':'CASE',
    'do' : 'DO',
    'break': 'BREAK',
    'return' : 'RETURN',
    'int' : 'INT',
    'float' : 'FLOAT',
    'double' : 'DOUBLE',
    'continue' : 'CONTINUE',
    'struct' : 'STRUCT',
    'union' : 'UNION',
    'char' : 'CHAR',
    'printf':'PRINTF',
    'scanf' : 'SCANF'   
}

tokens += reserved.values()
 
# Regular expression rules for simple tokens
t_CONTINUE = r'continue'
t_CASE = r'case'
t_ELSE = r'else'
t_BREAK = r'break'
t_INT = r'int'
t_SCANF = r'scanf'
t_UNION = r'union'
t_PRINTF = r'printf'
t_CHAR = r'char'
t_ASSIGN = r'='
t_EQUAL = r'=='
t_LEFTBRACE = r'{'
t_RIGHTBRACE = r'}'
t_PLUS = r'\+'
t_MINUS   = r'-'
t_MULT   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'
t_FOR = r'for'
t_WHILE = r'while'
t_SWITCH = r'switch'
t_STRUCT = r'struct'
t_RETURN = r'return'
t_IF = r'if'
t_DO = r'do'
t_FLOAT = 'float'
t_DOUBLE = r'double'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t
	

def t_NUMBER(t):
  r'\d+'
  try:
    t.value = int(t.value)
  except ValueError:
    print("line %d: number %s is too large!" ,(t.lineno,t.value))
    t.value = 0
  return t


def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)
   

#ignored characters such as spaces
t_ignore  = ' \t'


def t_error(t):
  print ("illegal character '%s'" , t.value[0])
  t.lexer.skip(1)
  
  
def t_COMMENT(t):
    r'\#.*'
    pass

#build the lexer
lexer = lex.lex()
lexer.input("malloc(sizeof(int)*5)")


while True:
	token = lexer.token()
	if not token:
		break
	else:
		print(token)


