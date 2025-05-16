import ply.yacc as yacc
from cql_lexer import lexer, tokens
from utils import parse_csv, write_csv
from tables import TableManager

table_manager = TableManager()

precedence = (
    ('left', 'AND', 'OR'),
    ('nonassoc', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NEQ'),
)

def p_program(p):
    '''program : command_list'''
    p[0] = p[1]

def p_command_list(p):
    '''command_list : command SEMICOLON
                   | command SEMICOLON command_list'''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_command(p):
    '''command : import_command
               | export_command
               | discard_command
               | rename_command
               | print_command
               | select_command
               | create_command
               | procedure_declaration
               | procedure_call'''
    p[0] = p[1]

def p_import_command(p):
    'import_command : IMPORT TABLE ID FROM STRING'
    p[0] = ('IMPORT', p[3], p[5])

def p_export_command(p):
    'export_command : EXPORT TABLE ID AS STRING'
    p[0] = ('EXPORT', p[3], p[5])

def p_discard_command(p):
    'discard_command : DISCARD TABLE ID'
    p[0] = ('DISCARD', p[3])

def p_rename_command(p):
    'rename_command : RENAME TABLE ID ID'
    print(f"[DEBUG] Comando RENAME: {p[3]}, {p[4]}") 
    p[0] = ('RENAME', p[3], p[4])

def p_print_command(p):
    'print_command : PRINT TABLE ID'
    p[0] = ('PRINT', p[3])

def p_select_command(p):
    '''select_command : SELECT select_fields FROM ID
                     | SELECT select_fields FROM ID WHERE condition
                     | SELECT select_fields FROM ID WHERE condition LIMIT NUMBER'''
    if len(p) == 5:
        p[0] = ('SELECT', p[2], p[4], None, None)
    elif len(p) == 7:
        p[0] = ('SELECT', p[2], p[4], p[6], None)
    else:
        p[0] = ('SELECT', p[2], p[4], p[6], p[8])

def p_select_fields(p):
    '''select_fields : STAR
                    | field_list'''
    p[0] = p[1]

def p_field_list(p):
    '''field_list : ID
                 | ID COMMA field_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_condition(p):
    '''condition : expression
                | condition AND condition
                | condition OR condition'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_expression(p):
    '''expression : ID operator value'''
    p[0] = (p[2], p[1], p[3])

def p_operator(p):
    '''operator : EQ
               | NEQ
               | LT
               | GT
               | LE
               | GE'''
    p[0] = p[1]

def p_value(p):
    '''value : ID
            | NUMBER
            | STRING'''
    p[0] = p[1]

def p_create_command(p):
    '''create_command : CREATE TABLE ID select_command
                     | CREATE TABLE ID FROM ID JOIN ID USING LPAREN ID RPAREN
                     | CREATE TABLE ID FROM ID JOIN ID ON ID'''
    if len(p) == 5:
        p[0] = ('CREATE_FROM_SELECT', p[3], p[4])
    elif p[6] == 'JOIN' and p[8] == 'USING':
        p[0] = ('CREATE_FROM_JOIN', p[3], p[5], p[7], p[10])


def p_procedure_declaration(p):
    'procedure_declaration : PROCEDURE ID DO command_list END'
    p[0] = ('PROCEDURE_DECLARE', p[2], p[4])

def p_procedure_call(p):
    'procedure_call : CALL ID'
    p[0] = ('PROCEDURE_CALL', p[2])

def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe no final do comando")

parser = yacc.yacc()
