# parser.py

import ply.yacc as yacc
from lexer import tokens

# Operator precedence
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'POWER'),
    ('right', 'UMINUS'),
)

# --- GRAMMAR RULES AND PYTHON TRANSLATION ---

def p_program(p):
    'program : statement_list'
    p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

# Defines a 'statement' as one of the possible command types.
def p_statement(p):
    '''statement : assignment_or_declaration
                 | conditional_statement
                 | repetition_statement
                 | print_statement
                 | read_statement'''
    p[0] = p[1]

# Rule for the optional type specifier.
def p_optional_type(p):
    '''optional_type : TYPE_INT
                     | TYPE_FLOAT
                     | TYPE_STRING
                     | TYPE_CHAR
                     | TYPE_BOOL
                     | empty'''
    pass

# Rule that combines declaration (with optional type) and assignment.
def p_assignment_or_declaration(p):
    'assignment_or_declaration : optional_type IDENTIFIER ASSIGN expression SEMICOLON'
    # The translation to Python is a simple assignment, ignoring the type.
    p[0] = f"{p[2]} = {p[4]}\n"

def p_conditional_statement(p):
    '''conditional_statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE elif_list else_optional'''
    p[0] = f"if {p[3]}:\n{indent(p[6])}{p[8]}{p[9]}"

def p_elif_list(p):
    '''elif_list : elif_list ELIF LPAREN expression RPAREN LBRACE statement_list RBRACE
                 | empty'''
    if len(p) > 2:
        if p[1] is None: p[1] = ""
        p[0] = f"{p[1]}elif {p[4]}:\n{indent(p[7])}"
    else:
        p[0] = ""

def p_else_optional(p):
    '''else_optional : ELSE LBRACE statement_list RBRACE
                     | empty'''
    if len(p) > 2:
        p[0] = f"else:\n{indent(p[3])}"
    else:
        p[0] = ""

def p_repetition_statement(p):
    'repetition_statement : WHILE LPAREN expression RPAREN LBRACE statement_list RBRACE'
    p[0] = f"while {p[3]}:\n{indent(p[6])}"

def p_print_statement(p):
    'print_statement : PRINT LPAREN expression RPAREN SEMICOLON'
    p[0] = f"print({p[3]}, end='')\n"

def p_read_statement(p):
    'read_statement : READ LPAREN identifier_list RPAREN SEMICOLON'
    # Gera uma linha "variavel = input()" para cada identificador na lista.
    # p[3] conterá a lista de nomes de variáveis, por exemplo: ['nome', 'idade']
    python_code = ""
    for var_name in p[3]:
        # Para cada variável, criamos uma solicitação de entrada.
        # Poderíamos tornar a mensagem mais descritiva, mas por simplicidade usamos input().
        python_code += f"{var_name} = input()\n"
    p[0] = python_code

# Nova regra para lidar com uma lista de identificadores separados por vírgula.
# Esta é uma regra recursiva.
def p_identifier_list(p):
    '''identifier_list : identifier_list COMMA IDENTIFIER
                       | IDENTIFIER'''
    if len(p) == 4:
        # Se for uma lista seguida de vírgula e outro identificador (ex: a, b)
        # p[1] é a lista anterior, p[3] é o novo identificador
        p[0] = p[1] + [p[3]] # Adiciona o novo identificador à lista
    else:
        # Se for apenas um identificador (o primeiro da lista)
        # p[1] é o identificador
        p[0] = [p[1]] # Cria uma nova lista com esse identificador


def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression POWER expression
                  | expression EQ expression
                  | expression NE expression
                  | expression LT expression
                  | expression LE expression
                  | expression GT expression
                  | expression GE expression
                  | expression AND expression
                  | expression OR expression'''
    op_map = {'^': '**'}
    op = op_map.get(p[2], p[2])
    p[0] = f"({p[1]} {op} {p[3]})"

def p_expression_not(p):
    'expression : NOT expression'
    p[0] = f"(not {p[2]})"

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = f"(-{p[2]})"

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_value(p):
    '''expression : INTEGER
                  | FLOAT_NUM
                  | STRING_LITERAL
                  | IDENTIFIER
                  | TRUE
                  | FALSE'''
    token_type = p.slice[1].type
    if token_type == 'TRUE':
        p[0] = 'True'
    elif token_type == 'FALSE':
        p[0] = 'False'
    elif token_type == 'STRING_LITERAL':
         p[0] = f'"{p[1]}"'
    else:
         p[0] = str(p[1])

def p_empty(p):
    'empty :'
    pass

# Syntax error handling
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' on line {p.lineno}")
    else:
        print("Syntax error at EOF")

def indent(text):
    """Adds 4 spaces of indentation to each line of text."""
    if text is None: return ""
    return "".join([f"    {line}" for line in text.splitlines(True)])

# Build the parser
parser = yacc.yacc()