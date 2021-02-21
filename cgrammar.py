def cgrammarfunc(inp):
    import ply.lex as lex
    import ply.yacc as yacc
    import json
    import sys
    import copy
    from secondparser import secondparser


    var_dict= [{}]
    var_type = {}
    flag = {"dflag" : 0}
    counter = {"dcount"  :   0}

    line_list = []

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
        'NOTEQUAL',
        'LESSER',
        'GREATER',
        'LESSEREQ',
        'GREATEREQ',
        'AND',
        'OR',
        'NOT',
        'INCREMENT',
        'DECREMENT',
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
        'NULL' : 'NULL',
        'free' : 'FREE',
        'main' : 'MAIN'
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
    t_NOTEQUAL = r'!='
    t_LESSER = r'<'
    t_GREATER = r'>'
    t_LESSEREQ = r'<='
    t_GREATEREQ = r'>='
    t_AND = r'\&\&'
    t_OR = r'\|\|'
    t_NOT = r'!'
    t_INCREMENT = r'\+\+'
    t_DECREMENT = r'--'
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
    t_FREE = r'free'


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
    t_ignore  = ' \t\r'


    def t_error(t):
        print ("illegal character '%s'" , t.value[0])
        t.lexer.skip(1)

    def t_COMMENT(t):
        r'\//.*'
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

    precedence = (
        ('left', 'ARROW'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQUAL', 'NOTEQUAL'),
        ('left', 'LESSER', 'LESSEREQ', 'GREATER', 'GREATEREQ'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULT', 'DIVIDE'),
        ('left', 'LPAREN', 'RPAREN', 'INCREMENT', 'DECREMENT')
    )

    def p_primary_expression(p):
        '''
        primary_expression	:	expression SEMICOLON primary_expression
                            |	var_assign SEMICOLON primary_expression
                            |	var_declare SEMICOLON primary_expression
                            |	pointer_declare_without_assign SEMICOLON primary_expression
                            |	pointer_declare SEMICOLON primary_expression
                            |	pointer_declare1 SEMICOLON primary_expression
                            |	pointer_init SEMICOLON primary_expression
                            |	pointer_assign SEMICOLON primary_expression
                            |	structure_declare SEMICOLON primary_expression
                            |	struct_pointer_declare SEMICOLON primary_expression
                            |	struct_pointer_assign SEMICOLON primary_expression
                            |	struct_pointer_assign_dynamic SEMICOLON primary_expression
                            |	struct_assign1 SEMICOLON primary_expression
                            |	dynamic SEMICOLON primary_expression
                            |   dynamic_init SEMICOLON primary_expression
                            |   dynamic_init1 SEMICOLON primary_expression
                            |   free SEMICOLON primary_expression
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3])


    def p_primary_expression1(p):
        '''
        primary_expression  :       while primary_expression
                                |   if primary_expression
                                |   if_else primary_expression
                                |	expression SEMICOLON
                                |	var_assign SEMICOLON
                                |	var_declare SEMICOLON
                                |	pointer_declare_without_assign SEMICOLON
                                |	pointer_assign SEMICOLON
                                |	pointer_declare SEMICOLON
                                |	pointer_declare1 SEMICOLON
                                |	pointer_init SEMICOLON
                                |	structure_declare SEMICOLON
                                |	struct_pointer_declare SEMICOLON
                                |	struct_pointer_assign SEMICOLON
                                |	struct_pointer_assign_dynamic SEMICOLON
                                |   dynamic_init SEMICOLON
                                |   dynamic_init1 SEMICOLON
                                |	struct_assign1 SEMICOLON
                                |	dynamic SEMICOLON
                                |   free SEMICOLON
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2])
        #line_list.append(var_dict[0])


    def p_primary_expression2(p):
        '''
        primary_expression  :   while
                            |   if
                            |   if_else
        '''
        if(flag["dflag"]):
            p[0] = str(p[1])


    def p_var_declare_without_assign(p):
        '''
        var_declare	:	INT ID
                    |	FLOAT ID
        '''
        if(p[2] not in var_dict[0]):
            var_dict[0][p[2]] = [p[1]]
            var_dict[0][p[2]].insert(1,'?')
            #print("in declare",var_dict[0])
            line_list.append(copy.deepcopy(var_dict[0]))


    def p_var_declare(p):
        '''
        var_declare	:	INT	ID ASSIGN expression
                    |	FLOAT ID ASSIGN expression
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + " " + str(p[2]) + str(p[3]) + str(p[4])
        else:
            #print("var  :",var_dict[0])
            if(p[2] not in var_dict[0]):
                var_dict[0][p[2]] = [p[1]]
            var_dict[0][p[2]].insert(1,p[4])
            #print("in assignment",var_dict[0])
            line_list.append(copy.deepcopy(var_dict[0]))


    def p_var_assign(p):
        '''
        var_assign	:	ID ASSIGN expression
                    |   ID ASSIGN NULL

        '''
        #global var_dict[0]
        #print("var     :",var_dict[0])
        if(flag["dflag"] == 0):
            if("*" in var_dict[0][p[1]][0] and "struct" in var_dict[0][p[1]][0]):
                if(p[3] == "?"):
                    var_dict[0][p[1]][1] = "?"
                elif(p[3] == "NULL" or var_dict[0][p[3]][1] != "?"):
                    x = p[3]
                    while(x != "NULL" and isinstance(var_dict[0][x][1], str)):
                        print("inside while", x)
                        x = var_dict[0][x][1]
                    if(x == "NULL"):
                        var_dict[0][p[1]][1] = "NULL"
                    else:
                        var_dict[0][p[1]][1] = x
                else:
                    print("in else1")
                    var_dict[0][p[1]][1] = p[3]

            elif("*" in var_dict[0][p[1]][0]):
                if(p[3] == "NULL" or var_dict[0][p[3]][1] != "?"):
                    x = p[3]
                    while(x != "NULL" and isinstance(var_dict[0][x][1], str)):
                        if("addr" not in var_dict[0][x][1] and not(isinstance(var_dict[0][x][1],dict))):
                            x = var_dict[0][x][1]
                        else:
                            break
                    if(x == "NULL"):
                        var_dict[0][p[1]][1] = "NULL"
                    else:
                        var_dict[0][p[1]][1] = x
                else:
                    var_dict[0][p[1]][1] = "?"
            else:
                var_dict[0][p[1]][1] = p[3]
            #print("vardict   ",var_dict[0])
            line_list.append(copy.deepcopy(var_dict[0]))
        else:
            if(p[3]!= "NULL"):
                p[0] = str(p[1]) + str(p[2]) + str(p[3])
            else:
                p[0] = str(p[1]) + str(p[2])


    def p_pointer_declare_without_assign(p):
        '''
        pointer_declare_without_assign  :   INT MULT ID
                                        |   FLOAT MULT ID
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2])
        else:
            var_dict[0][p[3]] = [p[1] + p[2]]
            var_dict[0][p[3]].insert(1,'?')
            line_list.append(copy.deepcopy(var_dict[0]))


    def p_pointer_assign(p):
        '''
        pointer_assign : ID ASSIGN ADDR ID

        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3]) + str(p[4])
        else:
            var_dict[0][p[1]][1] = "addr" + p[4]
            line_list.append(copy.deepcopy(var_dict[0]))


    def p_pointer_declare(p):
        '''
        pointer_declare : INT MULT ID ASSIGN ADDR ID
                        | FLOAT MULT ID ASSIGN ADDR ID
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3]) + str(p[4]) + str(p[5]) + str(p[6])
        else:
            var_dict[0][p[3]] = [p[1] + p[2]]
            var_dict[0][p[3]].insert(1, "addr" + p[6])
            line_list.append(copy.deepcopy(var_dict[0]))


    def p_pointer_declare1(p):
        '''
        pointer_declare1 : INT MULT ID ASSIGN ID
                        |	INT MULT ID ASSIGN NULL
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3]) + str(p[4]) + str(p[5])
        else:
            var_dict[0][p[3]] = [p[1] + p[2]]
            if(p[5] == "NULL" or var_dict[0][p[5]][1] != "?"):
                x = p[5]
                while(x!= "NULL" and isinstance(var_dict[0][x][1], str)):
                    if("addr" not in var_dict[0][x][1] and not(isinstance(var_dict[0][x][1],dict))):
                        x = var_dict[0][x][1]
                    else:
                        break
                print(x)
                if(x == "NULL"):
                    var_dict[0][p[3]].insert(1, "NULL")
                else:
                    var_dict[0][p[3]].insert(1, x)
            else:
                print("in else")
                var_dict[0][p[3]].insert(1,"?")
            line_list.append(copy.deepcopy(var_dict[0]))


    def p_pointer_init(p):
        '''
        pointer_init : MULT ID ASSIGN expression
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3]) + str(p[4])
        else:
            x = var_dict[0][p[2]][1]
            if(isinstance(x,str)):
                if("addr" in x):
                    x = x[4:]
                    var_dict[0][x][1] = p[4]
                elif(isinstance(var_dict[0][x][1],dict)):
                    var_dict[0][x][1][x][1] = p[4]
                else:
                    x = var_dict[0][x][1]
                    x = x[4:]
                    var_dict[0][x][1] = p[4]
            else:
                x[p[2]][1] = p[4]
            line_list.append(copy.deepcopy(var_dict[0]))


    def p_dynamic(p):
        '''
        dynamic	:	INT MULT ID ASSIGN MALLOC LPAREN size1 RPAREN
                |	FLOAT MULT ID ASSIGN MALLOC LPAREN size1 RPAREN
                |	INT MULT ID ASSIGN MALLOC LPAREN size3 RPAREN
                |	FLOAT MULT ID ASSIGN MALLOC LPAREN size3 RPAREN

        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + " " + str(p[3]) + str(p[4]) + str(p[5]) + str(p[6]) + str(p[7]) + str(p[8])
        else:
            var_dict[0][p[3]] = [p[1] + "*"]
            var_dict[0][p[3]].insert(1,{p[3] : [p[1]+p[2] , "?"]})
            line_list.append(copy.deepcopy(var_dict[0]))


    def p_dynamic_init1(p):
        '''
        dynamic_init1   :   ID ASSIGN MALLOC LPAREN size1 RPAREN
                        |   ID ASSIGN MALLOC LPAREN size3 RPAREN
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3]) + str(p[4]) + str(p[5]) + str(p[6])
        else:
            var_dict[0][p[1]][1] = {p[1] : [var_dict[0][p[1]][0] , "?"]}
            line_list.append(copy.deepcopy(var_dict[0]))


    def p_struct_pointer_declare(p):
        '''
        struct_pointer_declare	:	STRUCT ID MULT ID
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + " " + str(p[2]) + str(p[3]) + " " + str(p[4])
        else:
            var_dict[0][p[4]] = [p[1] + " " + p[2] + p[3]]
            var_dict[0][p[4]].insert(1,'?')
            line_list.append(copy.deepcopy(var_dict[0]))


    def p_struct_pointer_assign(p):
        '''
        struct_pointer_assign	:	STRUCT ID MULT ID ASSIGN expression
                                |   STRUCT ID MULT ID ASSIGN NULL

        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + " " + str(p[2]) + str(p[3]) + " " + str(p[4]) + " " + str(p[5]) + " " + str(p[6])
        else:
            var_dict[0][p[4]] = [p[1] + " " + p[2] + p[3]]
            if(p[6] == "?"):
                var_dict[0][p[4]].insert(1,"?")
            elif(p[6] == "NULL" or var_dict[0][p[6]][1] != "?"):
                x = p[6]
                while( x!= "NULL" and isinstance(var_dict[0][x][1], str)):
                    x = var_dict[0][x][1]
                if(x == "NULL"):
                    var_dict[0][p[4]].insert(1, "NULL")
                else:
                    var_dict[0][p[4]].insert(1, x)
            else:
                var_dict[0][p[4]].insert(1,p[6])
            line_list.append(copy.deepcopy(var_dict[0]))
            print(line_list)


    def p_struct_pointer_assign_dynamic(p):
        '''
        struct_pointer_assign_dynamic	:	STRUCT ID MULT ID ASSIGN MALLOC LPAREN size2 RPAREN
        '''
        var_dict[0][p[4]] = [p[1] + " " + p[2] + p[3]]
        tempdict = copy.deepcopy(var_type[p[2]])
        var_dict[0][p[4]].insert(1,tempdict)
        line_list.append(copy.deepcopy(var_dict[0]))


    def p_dynamic_init(p):
        '''
        dynamic_init :  ID ASSIGN MALLOC LPAREN size2 RPAREN

        '''
        # check if identifier is already present in var_dict[0] which was previously declared with malloc
        if(flag["dflag"]):
            p[0] = str(p[1])+ str(p[2]) + str(p[3]) +str(p[4])  + str(p[5]) + str(p[6])
        else:
            if(p[1] in var_dict[0] and isinstance(var_dict[0][p[1]][1], dict)):
                counter["dcount"] += 1
                var_dict[0][str(counter["dcount"]) + p[1]] = copy.deepcopy(var_dict[0][p[1]])
                for i in var_dict[0]:
                    if(var_dict[0][i][1] == p[1]):
                        var_dict[0][i][1] = str(counter["dcount"]) + p[1]
            name = var_dict[0][p[1]][0].strip("struct")
            name = name.strip("*").strip()
            tempdict = copy.deepcopy(var_type[name])
            var_dict[0][p[1]][1] = tempdict
            line_list.append(copy.deepcopy(var_dict[0]))


    def p_struct_assign1(p):
        '''
        struct_assign1  : ID ARROW ID ASSIGN expression
                        | ID ARROW ID ASSIGN NULL
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3]) + str(p[4]) + str(p[5])
        else:
            x = var_dict[0][p[1]][1]
            if(x != '?' and x != 'NULL'):
                if(isinstance(x, dict)):
                    if(p[5] == 'NULL'):
                        x[p[3]][1] = p[5]
                    elif(isinstance(p[5], str)):
                        if(isinstance(var_dict[0][p[5]][1], dict)):
                            x[p[3]][1] = p[5]
                        else:
                            x[p[3]][1] = var_dict[0][p[5]][1]
                    else:
                        x[p[3]][1] = p[5]
                else:
                    if(isinstance(p[5], str)):
                        if(isinstance(var_dict[0][p[5]][1], dict)):
                            var_dict[0][x][1][p[3]][1] = p[5]
                        else:
                            var_dict[0][x][1][p[3]][1] = var_dict[0][p[5]][1]
                    else:
                        var_dict[0][x][1][p[3]][1] = p[5]
            line_list.append(copy.deepcopy(var_dict[0]))


    def p_size1(p):
        '''
        size1	:	SIZEOF LPAREN INT RPAREN multiplier
                |	SIZEOF LPAREN FLOAT RPAREN multiplier
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3]) + str(p[4]) + str(p[5])
        else:
            p[0] = p[3] + str(p[5])


    def p_size2(p):
        '''
        size2	:	SIZEOF LPAREN STRUCT ID RPAREN multiplier
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3]) + " " + str(p[4]) + str(p[5]) + str(p[6])
        else:
            p[0] = p[4]


    def p_size3(p):
        '''
        size3	:	NUMINT multiplier
                |   NUMFLOAT multiplier
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2])
        else:
            p[0] = p[1] + str(p[2])


    def p_multiplier(p):
        '''
        multiplier	:	PLUS NUMINT
                    |	MULT NUMINT
                    |	DIVIDE NUMINT
                    |	MINUS NUMINT
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2])


    def p_multiplier_empty(p):
        '''
        multiplier  :   empty
        '''
        if(flag["dflag"]):
            p[0] = ""


    def p_structure_declare(p):
        '''
        structure_declare	:	STRUCT ID LEFTBRACE content RIGHTBRACE

        '''
        if(p[2] not in var_type):
            var_type[p[2]] = dict()
            for i in det:
                var,ty = i.split(':')
                var_type[p[2]][var] = [ty,'?']
            del det[:]
        line_list.append(copy.deepcopy(var_dict[0]))

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
                det.append(p[2] + ":" + p[1])
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
                det.append(p[4] + ":" + p[1] + " " + p[2] + p[3])
        except:
            pass


    def p_expression(p):
        '''
        expression  :   LPAREN expression RPAREN
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3])
        else:
            p[0] = p[2]


    def p_expression_mult(p):
        '''
        expression	:	expression MULT expression
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3])
        else:
            p[0] = p[1] * p[3]


    def p_expression_plus(p):
        '''
        expression	:	expression PLUS expression
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3])
        else:
            p[0] = p[1] + p[3]
        #print("in expression2", p[0])


    def p_expression_divide(p):
        '''
        expression	:	expression DIVIDE expression
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3])
        else:
            p[0] = p[1] / p[3]


    def p_expression_minus(p):
        '''
        expression	:	expression MINUS expression
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3])
        else:
            p[0] = p[1] - p[3]


    def p_expression_lesser(p):
        '''
        expression	:	expression LESSER expression
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3])
        else:
            if(p[1] < p[3]):
                p[0] = 1
            else:
                p[0] = 0


    def p_expression_greater(p):
        '''
        expression	:	expression GREATER expression
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3])
        else:
            if(p[1] > p[3]):
                p[0] = 1
            else:
                p[0] = 0


    def p_expression_greatereq(p):
        '''
        expression	:	expression GREATEREQ expression
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3])
        else:
            if(p[1] >= p[3]):
                p[0] = 1
            else:
                p[0] = 0


    def p_expression_lessereq(p):
        '''
        expression	:	expression LESSEREQ expression
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3])
        else:
            if(p[1] <= p[3]):
                p[0] = 1
            else:
                p[0] = 0


    def p_expression_equal(p):
        '''
        expression	:	expression EQUAL expression
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3])
        else:
            if(p[1] == p[3]):
                p[0] = 1
            else:
                p[0] = 0


    def p_expression_notequal(p):
        '''
        expression	:	expression NOTEQUAL expression
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3])
        else:
            if(p[1] != p[3]):
                p[0] = 1
            else:
                p[0] = 0


    def p_expression_and(p):
        '''
        expression	:	expression AND expression
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3])
        else:
            if(p[1] and p[3]):
                p[0] = 1
            else:
                p[0] = 0


    def p_expression_or(p):
        '''
        expression	:	expression OR expression
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3])
        else:
            if(p[1] or p[3]):
                p[0] = 1
            else:
                p[0] = 0


    def p_expression_not(p):
        '''
        expression	:	NOT expression
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2])
        else:
            if(not(p[2])):
                p[0] = 1
            else:
                p[0] = 0


    def p_expression_var(p):
        '''
        expression	:	ID
        '''
        if(flag["dflag"]):
            p[0] = str(p[1])
        else:
            if("*" in var_dict[0][p[1]][0]):
                p[0] = p[1]
            else:
                p[0] = var_dict[0][p[1]][1]
        #print("in expression_var", p[0])


    def p_expression_structvar(p):
        '''
        expression	:	ID ARROW ID
        '''
        if(flag["dflag"]):
            p[0] = str(p[1]) + str(p[2]) + str(p[3])
            print(p[0])
        else:
            if(isinstance(var_dict[0][p[1]][1], dict)):
                p[0] = var_dict[0][p[1]][1][p[3]][1]
            else:
                x = var_dict[0][p[1]][1]
                p[0] = var_dict[0][x][1][p[3]][1]
                print(p[0])
        #print(p[0])


    def p_expression_int_float(p):
        '''
        expression	:	NUMINT
                    |   NUMFLOAT
        '''
        if(flag["dflag"]):
            p[0] = str(p[1])
        else:
            p[0] = p[1]
        #print("in expression_int_float", p[0])


    def p_empty(p):
        '''
        empty	:
        '''
        if(flag["dflag"]):
            p[0] = ""


    def p_null(p):
        '''
        expression	: NULL
        '''
        if(flag["dflag"]):
            p[0] = str(p[1])
        else:
            p[0] = p[1]


    def p_free(p):
        '''
        free : FREE LPAREN ID RPAREN
        '''
        if(isinstance(var_dict[0][p[3]][1], dict)):
            var_dict[0][p[3]][1] = "$"
            for i in var_dict[0]:
                if(var_dict[0][i][1] == p[3]):
                    var_dict[0][i][1] = "$"
        else:
            x = var_dict[0][p[3]][1]
            var_dict[0][p[3]][1] = "$"
            var_dict[0][x][1] = "$"
             #del var_dict[0][x]
            for i in var_dict[0]:
                if(var_dict[0][i][1] == x):
                    var_dict[0][i][1] = "$"
        line_list.append(copy.deepcopy(var_dict[0]))


    def myeval(string, local):
        string = string + ";"
        result = secondparser(string, local, var_type,counter)
        print("result", result[0])
        return result[0][0]


    def p_while(p):
        '''
        while : seen_a WHILE LPAREN cond RPAREN block
        '''
        #global var_dict[0]
        loop = dict()
        print("condition as a string", p[4])
        # create var loop with all elements of var_dict[0]
        print("block as a string", p[6])
        #loop = copy.deepcopy(var_dict[0])

        #print("1:",var_dict[0])
        while(myeval(p[4], line_list[-1])):
            # implement block
            L = secondparser(p[6], line_list[-1], var_type,counter)
            line_list.extend(copy.deepcopy(L[1]))
            #print("LINEEEEEE                 ",line_list)
            #print("in first:", var_dict[0])
            #loop = copy.deepcopy(var_dict[0])
        #print(L[1], line_list)
        #line_list.extend(copy.deepcopy(L[1]))

        var_dict[0] = copy.deepcopy(line_list[-1])
        #print("outside while vardict:  ",var_dict[0])
        #print("outside while:  ",line_list)
        flag["dflag"] = 0


    def p_block1(p):
        '''
        block : LEFTBRACE primary_expression RIGHTBRACE
        '''
        p[0] = p[2]


    def p_seen_a(p):
        '''
        seen_a  :   empty
        '''
        flag["dflag"] = 1


    def p_if(p):
        '''
        if : seen_a IF LPAREN cond RPAREN block
        '''
        loop = dict()
        print("cond as a string", p[4])
        # create var loop with all elements of var_dict[0]
        #loop = copy.deepcopy(var_dict[0])
        if(myeval(p[4], line_list[-1])):
            # implement block
            #secondparser(p[6], var_dict[0], var_type,counter)
            L = secondparser(p[6], line_list[-1], var_type,counter)
            line_list.extend(copy.deepcopy(L[1]))
        flag["dflag"] = 0


    def p_if_else(p):
        '''
        if_else : seen_a IF LPAREN cond RPAREN block ELSE block
        '''
        loop = dict()
        print("cond as a string", p[3])
        # create var loop with all elements of var_dict[0]
        if(myeval(p[4], line_list[-1])):
            # implement block
            L = secondparser(p[6], line_list[-1], var_type,counter)
            line_list.extend(copy.deepcopy(L[1]))
        else:
            L = secondparser(p[8], line_list[-1], var_type,counter)
            line_list.extend(copy.deepcopy(L[1]))
        flag["dflag"] = 0

    def p_cond(p):
        '''
        cond    :   expression
        '''
        p[0] = str(p[1])


    def p_error(p):
        print("parseError")


    #build the parser
    parser = yacc.yacc()

    """
    string = ''
    f = open("input.c","r")
    for line in f:
        try:
            string += line
        except EOFError:
            break

    parser.parse(string, lexer = lexer)
    """

    parser.parse(inp)
    #print("final var:    ",var_dict[0])
    #print("final:   ",line_list)
    return line_list
    #return json.dumps(var_dict[0])
