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
   'NEWLINE'
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


def t_NEWLINE(t):
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


'''
lexer.input("malloc(sizeof(int)*5)")
while True:
	token = lexer.token()
	if not token:
		break
	else:
		print(token)

'''

#dictionary of values
var_value = {}

#dictionary of types
var_type = {}

def p_primary_expression(p):
	'''
	primary_expression	:	expression SEMICOLON primary_expression
						|	var_assign SEMICOLON primary_expression
						|	var_declare SEMICOLON primary_expression
						|	structure_declare primary_expression
						|	dynamic SEMICOLON primary_expression
						|	expression SEMICOLON 
						|	var_assign SEMICOLON
						|	var_declare SEMICOLON
						|	structure_declare
						|	dynamic SEMICOLON
						
	'''	

def p_var_declare_without_assign(p):
	'''
	var_declare	:	INT ID 
				|	FLOAT ID
	'''
	if(p[2] not in var_type):
		var_type[p[2]] = p[1]
	
	
def p_var_declare(p):
	'''
	var_declare	:	INT	ID ASSIGN expression
				|	FLOAT ID ASSIGN expression 
	'''
	print("variable ", p[2], "of type ", p[1])
	if(p[2] not in var_type):
		var_type[p[2]] = p[1]
	var_value[p[2]] = p[4]
	

def p_var_assign(p):
	'''
	var_assign	:	ID ASSIGN expression
	
	'''
	if(p[1] not in var_type):
		print(p[1], "not declared")
	else:
		var_value[p[1]] = p[3]
	p[0] = (p[2], p[1], p[3])
	
	
def p_dynamic(p):
	'''
	dynamic	:	MALLOC LPAREN size RPAREN
	
	'''
	print("dynamically allocated with", p[1], "where number of size allocated is", p[3])
	
	
def p_size(p):
	'''
	size	:	SIZEOF LPAREN INT RPAREN multiplier
			|	SIZEOF LPAREN FLOAT RPAREN multiplier
			|	SIZEOF LPAREN STRUCT ID RPAREN multiplier
			|	NUMBER	multiplier
	'''
	p[0] = p[3]

def p_multiplier(p):
	'''
	multiplier	:	PLUS NUMBER 
				|	MULT NUMBER 
				|	DIVIDE NUMBER
				|	MINUS NUMBER
				|	empty
	'''
	
	
def p_empty(p):
	'''	
	empty	:	
	'''
	
def p_structure_declare(p):
	'''
	structure_declare	:	STRUCT ID LEFTBRACE content RIGHTBRACE SEMICOLON
					
	'''
	if(p[2] not in var_type):
		var_type[p[2]] = p[1]
	print("This is a structure",p[2])
	
	
def p_content(p):
	'''
	content	:	INT ID SEMICOLON content
			|	FLOAT ID SEMICOLON content
			|	FLOAT ID SEMICOLON
			|	INT ID SEMICOLON
			
	
	'''
	if(p[2] not in var_type):
		var_type[p[2]] = p[1]


def p_expression(p):
	'''
	expression	:	expression MULT expression
				|	expression DIVIDE expression
				|	expression PLUS expression
				|	expression 	MINUS expression
	'''
		

def p_expression_var(p):
	'''
	expression	:	ID
	
	'''
	p[0] = ('var', p[1])
	#print(p[0])


	
def p_expression_int_float(p):
	'''
	expression	:	NUMBER

	'''
	p[0] = p[1]


def p_error(p):
	print("parseError")


#build the parser	
parser = yacc.yacc()


string = ''

f = open("input.txt","r")
for line in f:
	try:
		string += line	
	except EOFError:
		break
parser.parse(string)

print(var_type)
print(var_value)

