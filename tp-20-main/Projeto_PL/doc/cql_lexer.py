import ply.lex as lex

reserved = {
    'import': 'IMPORT',
    'table': 'TABLE',
    'from': 'FROM',
    'as': 'AS',
    'export': 'EXPORT',
    'discard': 'DISCARD',
    'rename': 'RENAME',
    'print': 'PRINT',
    'select': 'SELECT',
    'where': 'WHERE',
    'and': 'AND',
    'or': 'OR',
    'create': 'CREATE',
    'join': 'JOIN',
    'using': 'USING',
    'procedure': 'PROCEDURE',
    'do': 'DO',
    'end': 'END',
    'call': 'CALL',
    'limit': 'LIMIT'
}

# Lista de tokens 
tokens = [
    'ID', 'STRING', 'NUMBER',
    'EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE',
    'COMMA', 'SEMICOLON', 'LPAREN', 'RPAREN', 'STAR', 'ON'
] + list(reserved.values())

# Expressões regulares para tokens 
t_EQ = r'='
t_NEQ = r'<>'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_COMMA = r','
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SELECT = r'SELECT'
t_FROM = r'FROM'
t_WHERE = r'WHERE'
t_STAR = r'\*'
t_ON = r'ON'

t_ignore = ' \t'

def t_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

def t_COMMENT(t):
    r'--[^\n]*'
    pass

def t_MULTILINE_COMMENT(t):
    r'\{-[^*]*-\}'
    pass  

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Carácter ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()