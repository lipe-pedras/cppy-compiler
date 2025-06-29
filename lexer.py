# lexer.py

import ply.lex as lex

# Reserved words and their respective tokens
reserved = {
    'if': 'IF',
    'elif': 'ELIF',
    'else': 'ELSE',
    'while': 'WHILE',
    'print': 'PRINT',
    'read': 'READ',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'int': 'TYPE_INT',
    'float': 'TYPE_FLOAT',
    'string': 'TYPE_STRING',
    'char': 'TYPE_CHAR',
    'bool': 'TYPE_BOOL',
    'true': 'TRUE',
    'false': 'FALSE'
}

# List of all tokens, including the reserved ones
tokens = [
    'IDENTIFIER', 'INTEGER', 'FLOAT_NUM', 'STRING_LITERAL',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
    'ASSIGN',
    'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'COMMA'
] + list(reserved.values())


# Regular expressions for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_POWER = r'\^'
t_ASSIGN = r'='
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_SEMICOLON = r';'
t_COMMA = r','

# Ignore comments (//...) and spaces/tabs
t_ignore_COMMENT = r'//.*'
t_ignore = ' \t'

# Regular expression for identifiers and checking for reserved words
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Check for reserved words
    return t

# Regular expressions for numbers
def t_FLOAT_NUM(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regular expression for string literals
def t_STRING_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1] # Remove quotes
    return t

# Line number tracking
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Lexical error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}' on line {t.lineno}")
    t.lexer.skip(1)

def write_tokens_to_file(lexer, filename="tokens_output.txt"):
    """
    Generates an output file with the recognized tokens,
    as specified in the assignment.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        # Clone the lexer to avoid consuming the tokens from the original
        lexer_clone = lexer.clone()
        for tok in lexer_clone:
            token_type = tok.type
            if tok.type in reserved.values():
                if tok.type in ['IF', 'ELIF', 'ELSE']:
                    token_type = "conditional statement"
                elif tok.type == 'WHILE':
                    token_type = "loop statement"
                else:
                    token_type = "reserved word"
            elif tok.type == 'IDENTIFIER':
                token_type = "identifier"
            elif tok.type == 'ASSIGN':
                token_type = "assignment"
            elif tok.type == 'INTEGER':
                token_type = "integer number"
            elif tok.type == 'FLOAT_NUM':
                token_type = "float number"
            elif tok.type in ['EQ', 'NE', 'LT', 'LE', 'GT', 'GE']:
                token_type = "relational operator"
            elif tok.type in ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER']:
                token_type = "arithmetic operator"
            elif tok.type in ['AND', 'OR', 'NOT']:
                token_type = "logical operator"
            elif tok.type == 'LPAREN':
                token_type = "left parenthesis"
            elif tok.type == 'RPAREN':
                token_type = "right parenthesis"
            elif tok.type == 'LBRACE':
                token_type = "left brace"
            elif tok.type == 'RBRACE':
                token_type = "right brace"
            elif tok.type == 'SEMICOLON':
                token_type = "semicolon"

            f.write(f"{tok.value} -> {token_type}\n")

# Build the lexer
lexer = lex.lex()