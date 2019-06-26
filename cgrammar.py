import ply.lex as lex
import ply.yacc as yacc
import sys

#tokens list specifying all of the possible tokens
tokens = [
   'NUMINT',
   'NUMFLOAT',
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
   'NEWLINE',
   'ADDR',
   'ARROW'
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
    'scanf' : 'SCANF',
	'NULL' : 'NULL'
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
t_ADDR = r'\&'
t_ARROW	 = r'->'
t_COMMA = r','
t_SEMICOLON = r';'
t_FOR = r'for'
t_WHILE = r'while'
t_SWITCH = r'switch'
t_STRUCT = r'struct'
t_RETURN = r'return'
t_IF = r'if'
t_DO = r'do'
t_FLOAT = r'float'
t_DOUBLE = r'double'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t
	
def t_NUMFLOAT(t):
	r'\d+\.\d+'
	t.value = float(t.value)
	return t

def t_NUMINT(t):
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
						|	pointer_declare_without_assign SEMICOLON primary_expression
						|	pointer_declare SEMICOLON primary_expression
						|	pointer_assign SEMICOLON primary_expression
						|	structure_declare SEMICOLON primary_expression
						|	struct_pointer_declare SEMICOLON primary_expression
						|	struct_pointer_assign SEMICOLON primary_expression
                        |	struct_pointer_assign_dynamic SEMICOLON primary_expression
						|	struct_assign1 SEMICOLON primary_expression
						|	dynamic SEMICOLON primary_expression
						|	expression SEMICOLON 
						|	var_assign SEMICOLON
						|	var_declare SEMICOLON
						|	pointer_declare_without_assign SEMICOLON
						|	pointer_assign SEMICOLON 
						|	pointer_declare SEMICOLON
						|	structure_declare SEMICOLON
						|	struct_pointer_declare SEMICOLON
						|	struct_pointer_assign SEMICOLON
                        |	struct_pointer_assign_dynamic SEMICOLON 
						|	struct_assign1 SEMICOLON
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
	#print("variable ", p[2], "of type ", p[1])
	if(p[2] not in var_type):
		var_type[p[2]] = p[1]
	var_value[p[2]] = p[4]
	

def p_var_assign(p):
	'''
	var_assign	:	ID ASSIGN expression
	
	'''
	var_value[p[1]] = p[3]
	#p[0] = (p[2], p[1], p[3])


def p_pointer_declare_without_assign(p):
	'''
	pointer_declare_without_assign : INT MULT ID
				    | FLOAT MULT ID
	'''
	
	#print("pointer ", p[3] , " of type ", p[1])
	var_type[p[3]] = p[1] + "*"


def p_pointer_assign(p):
	'''
	pointer_assign : ID ASSIGN ADDR ID
				   
	'''
	var_value[p[1]] = "&" + p[4]


def p_pointer_declare(p):
	'''
	pointer_declare : INT MULT ID ASSIGN ADDR ID
				   | FLOAT MULT ID ASSIGN ADDR ID
	'''
	
	#print("pointer ", p[3] , " of type ", p[1])
	var_type[p[3]] = p[1] + "*"
	var_value[p[3]] = "&" + p[6]
	
	
def p_struct_pointer_declare(p):
	'''
	struct_pointer_declare	:	STRUCT ID MULT ID 
	'''
	var_type[p[4]] = p[2] + "*"
	

def p_struct_pointer_assign(p):
	'''
	struct_pointer_assign	:	STRUCT ID MULT ID ASSIGN ID
				   
	'''
	var_type[p[4]] = p[2] + "*"
	var_value[p[4]] = "&" + p[6]



def p_struct_pointer_assign_dynamic(p):
	'''
	struct_pointer_assign_dynamic	:	STRUCT ID MULT ID ASSIGN MALLOC LPAREN size2 RPAREN 
	'''
	var_type[p[4]] = p[2] + "*"

def p_struct_assign1(p):
	'''
	struct_assign1 : ID ARROW ID ASSIGN NUMINT 
				   | ID ARROW ID ASSIGN NUMFLOAT
				   | ID ARROW ID ASSIGN NULL
				   | ID ARROW ID ASSIGN ID
	'''
	if(p[1] not in var_value):
		var_value[p[1]] = dict()
	var_value[p[1]][p[3]] = p[5]
	


def p_dynamic(p):
	'''
	dynamic	:	INT MULT ID ASSIGN MALLOC LPAREN size1 RPAREN
			|	FLOAT MULT ID ASSIGN MALLOC LPAREN size1 RPAREN
			|	INT MULT ID ASSIGN MALLOC LPAREN size3 RPAREN
			|	FLOAT MULT ID ASSIGN MALLOC LPAREN size3 RPAREN

	'''
	var_type[p[3]] = p[1] + "*"
	#print("dynamically allocated ",p[3]," with malloc of size", p[7])


def p_size1(p):
	'''
	size1	:	SIZEOF LPAREN INT RPAREN multiplier
			|	SIZEOF LPAREN FLOAT RPAREN multiplier
	'''
	p[0] = p[3] + str(p[5])


def p_size2(p):
	'''
	size2	:	SIZEOF LPAREN STRUCT ID RPAREN multiplier
	'''
	p[0] = p[3] + " " + p[4] + str(p[6])


def p_size3(p):
	'''
	size3	:	NUMINT	multiplier
			|   NUMFLOAT	multiplier
	'''
	p[0] = p[1] + str(p[2])
	
	
def p_dynamic_init(p):
	'''
	dynamic :	ID ASSIGN MALLOC LPAREN size1 RPAREN
				 |  ID ASSIGN MALLOC LPAREN size2 RPAREN
				 |  ID ASSIGN MALLOC LPAREN size3 RPAREN
	'''
	#print("dynamically allocated ",p[1]," with malloc of size", p[5])
		

def p_multiplier(p):
	'''
	multiplier	:	PLUS NUMINT
				|	MULT NUMINT 
				|	DIVIDE NUMINT
				|	MINUS NUMINT
				|	empty
	'''
	
	
def p_structure_declare(p):
	'''
	structure_declare	:	STRUCT ID LEFTBRACE content RIGHTBRACE 
					
	'''
	if(p[2] not in var_type):
		var_type[p[2]] = dict()
		var_type[p[2]]['type']=p[1]
		for i in det:
			var,ty = i.split(':')
			var_type[p[2]][var]=ty
		del det[:]
		#print(det)
	#print("This is a structure",p[2])
	
det = []	
def p_content(p):
	'''
	content	:	struct_content
			|	INT ID SEMICOLON content
			|	FLOAT ID SEMICOLON content
			|	FLOAT ID SEMICOLON
			|	INT ID SEMICOLON
			
	
	'''
	
	try:
		if(p[2] not in var_type):
			det.append(p[2]+":"+p[1])
			#print(det)
	except:
		pass

	
		

def p_struct_content(p):
	'''
	struct_content	:	STRUCT ID MULT ID SEMICOLON struct_content content
			 		|	STRUCT ID MULT ID SEMICOLON content
			 		|	STRUCT ID MULT ID SEMICOLON
	'''
	try:
		if(p[4] not in var_type):
			det.append(p[4]+":"+p[1]+" "+p[2]+p[3])
			#print(det)
	except:
		pass


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
	expression	:	NUMINT
				|   NUMFLOAT

	'''
	p[0] = p[1]


def p_empty(p):
	'''	
	empty	:	
	'''

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
