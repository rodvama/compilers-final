
import ply.lex as lex
keywords = {
    # MAIN 
    'PROGRAM' : 'program',
    'PRINCIPAL' : 'principal',
    # DECLARATIONS
    'VAR' : 'var',
    'INT' : 'int',
    'VOID' : 'void',
    'CHAR' : 'char',
    'FLOAT' : 'float',
    'STRING' : 'string',
    'REGRESA' : 'regresa',
    'FUNCION' : 'funcion',
    'DATAFRAME' : 'dataframe',
    # UPLOAD
    'LEE' : 'lee',
    'CARGA' : 'carga', 
    'ESCRIBE' : 'escribe',
    # CONDITIONS
    'SI' : 'si',
    'HAZ' : 'haz',
    'SINO' : 'sino',
    'MIENTRAS' : 'mientras',
    'ENTONCES' : 'entonces',
    # LOOPS
    'DESDE' : 'desde',
    'HASTA' : 'hasta',
    'HACER' : 'hacer'
}

tokens = [
    # OPERATOR
    'ADD',
    'SUB',
    'MUL',
    'DIV',
    'OR',
    'AND',
    'LT',
    'LE',
    'GT',
    'GE',
    'EQUAL',
    'ASSIGN'
    'NOT_EQUAL',
    # COMMENT AND WHITESPACE
    'COMMENT',
    'WS',
    # SEPARATORS
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACK',
    'RBRACK',
    'SEMICOLON',
    'COMMA',
    'DOT'
    # LITERALS
    'ID',
    'CTE_INT',
    'CTE_FLOAT',
    'CTE_CHAR',
    'CTE_STR',
    'CTE_DF'
] + list(keywords.values())

t_ADD           = r'\+'
t_SUB           = r'-'
t_MUL           = r'\*'
t_DIV           = r'/'
t_OR            = r'||'
t_AND           = r'&'
t_LT            = r'<'
t_LE            = r'<='
t_GT            = r'>'
t_GE            = r'=>'
t_EQUAL         = r'=='
t_NOT_EQUAL     = r'!='
t_ASSIGN        = r'='
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LBRACE        = r'{'
t_RBRACE        = r'}'
t_LBRACK        = r'\['
t_LBRACK        = r'\]'
t_SEMICOLON     = r';'
t_COMMA         = r','
t_DOT           = r'.'
t_TWO_DOTS      = r':'
t_PRINT         = r'print'
t_ignore        = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'ID')
    return t

def t_CTE_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CTE_FLOAT(t):
    r'([0-9]+[.])[0-9]+'
    t.value = float(t.value)
    return t

def t_CTE_CHAR(t):
    r'[A-Za-z]'
    t.value = chr(t.value)
    return t

def t_CTE_STR(t):
    r'\".*"'
    t.value = str(t.value)
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    if t:
        print("Illegal character '{}' at: {}".format(t.value[0], t.lexer.lineno))
        t.lexer.skip(1)
    else:
        print ("Error from lex")

lex.lex()