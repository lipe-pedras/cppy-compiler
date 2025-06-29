# parser.py

import ply.yacc as yacc
from lexer import tokens

# Create a symbol table (a dictionary) to store variable types
symbol_table = {}

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
    '''statement : declaration
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
    # Pass the token type up if it exists
    if len(p) > 1 and p.slice[1].type != 'empty':
        p[0] = p.slice[1].type
    else:
        p[0] = None


def p_optional_assignment(p):
    '''optional_assignment : ASSIGN expression
                           | empty'''
    if len(p) == 3:
        p[0] = p[2]  # Return the expression value if assignment exists
    else:
        p[0] = 'None' # Default value for declaration-only statements (e.g., int age;)


def p_declaration(p):
    'declaration : optional_type IDENTIFIER optional_assignment SEMICOLON'
    var_type = p[1]
    var_name = p[2]
    var_value = p[3]

    # Populate symbol table ONLY if a type is explicitly declared
    if var_type is not None:
        symbol_table[var_name] = var_type

    # Generate Python code
    p[0] = f"{var_name} = {var_value}\n"


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
    python_code = ""
    for var_name in p[3]:
        var_type = symbol_table.get(var_name, 'TYPE_STRING') 
        prompt = f"Enter value for {var_name} ({var_type.replace('TYPE_', '').lower()}): "
        if var_type == 'TYPE_INT':
            python_code += f"{var_name} = int(input('{prompt}'))\n"
        elif var_type == 'TYPE_FLOAT':
            python_code += f"{var_name} = float(input('{prompt}'))\n"
        else:
            python_code += f"{var_name} = input('{prompt}')\n"
            
    p[0] = python_code


# New rule to handle a list of identifiers separated by a comma.
def p_identifier_list(p):
    '''identifier_list : identifier_list COMMA IDENTIFIER
                       | IDENTIFIER'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


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