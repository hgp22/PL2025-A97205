#############################################################
# Neste ficheiro está presente todo o código relativo à     #
# análise léxica; onde se converte código Pascal numa lista #
# de tokens.                                                #
#############################################################

# Nota:
# Foi utilizada como referência:
# https://www.standardpascal.org/iso7185rules.html#Lexography
# Para a construção do analisador léxico.


import sys
import ply.lex as lex
import re

literals = ['+', '-', '*', '/', '=', '<', '>', '[', ']', '.', ',', ':', ';', '^', '(', ')', '@']

tokens = [
    'LE', 'GE', 'NE', 'DOTDOT','ASSIGN',

    # Palavras reservadas com base em ER a pedido do prof. prh
    'AND', 'ARRAY', 'BEGIN', 'CASE', 'CONST', 'DIV', 'DO',
    'DOWNTO', 'ELSE', 'END', 'FILE', 'FOR', 'FUNCTION', 'GOTO',
    'IF', 'IN', 'LABEL', 'MOD', 'NIL', 'NOT', 'OF',
    'OR', 'PACKED', 'PROCEDURE', 'PROGRAM', 'RECORD', 'REPEAT', 'SET',
    'THEN', 'TO', 'TYPE', 'UNTIL', 'VAR', 'WHILE', 'WITH',

    'WRITELN',
    'READLN',

    'ID', 'INTEGER', 'REAL', 'STRING',
    'INTEGER_TYPE', 'REAL_TYPE'
]

##########################################
## Palavras Reservadas
def t_AND(t):       r'and';       return t
def t_ARRAY(t):     r'array';     return t
def t_BEGIN(t):     r'begin';     return t
def t_CASE(t):      r'case';      return t
def t_CONST(t):     r'const';     return t
def t_DIV(t):       r'div';       return t
def t_DO(t):        r'do';        return t
def t_DOWNTO(t):    r'downto';    return t
def t_ELSE(t):      r'else';      return t
def t_END(t):       r'end';       return t
def t_FILE(t):      r'file';      return t
def t_FOR(t):       r'for';       return t
def t_FUNCTION(t):  r'function';  return t
def t_GOTO(t):      r'goto';      return t
def t_IF(t):        r'if';        return t
def t_IN(t):        r'in';        return t
def t_LABEL(t):     r'label';     return t
def t_MOD(t):       r'mod';       return t
def t_NIL(t):       r'nil';       return t
def t_NOT(t):       r'not';       return t
def t_OF(t):        r'of';        return t
def t_OR(t):        r'or';        return t
def t_PACKED(t):    r'packed';    return t
def t_PROCEDURE(t): r'procedure'; return t
def t_PROGRAM(t):   r'program';   return t
def t_RECORD(t):    r'record';    return t
def t_REPEAT(t):    r'repeat';    return t
def t_SET(t):       r'set';       return t
def t_THEN(t):      r'then';      return t
def t_TO(t):        r'to';        return t
def t_TYPE(t):      r'type';      return t
def t_UNTIL(t):     r'until';     return t
def t_VAR(t):       r'var';       return t
def t_WHILE(t):     r'while';     return t
def t_WITH(t):      r'with';      return t
def t_READLN(t): r'readln'; return t 
def t_ASSIGN(t):    r':=';        return t
def t_WRITELN(t):   r'writeln';   return t
def t_INTEGER_TYPE(t): r'[Ii]nteger\b'; return t
def t_REAL_TYPE(t): r'[Rr]eal\b'; return t
##########################################


t_LE      = r'<='
t_GE      = r'>='
t_NE      = r'<>'
t_DOTDOT  = r'\.\.'

def t_comment_brace(t): r'\{[^}]*\}'; pass

def t_comment_parens(t): r'\(\*([^*]|\*[^)])*\*\)'; pass

def t_STRING(t):
    r"'([^']|'')*'"
    t.value = t.value[1:-1].replace("''", "'")
    return t

def t_REAL(t):
    r'\d+\.\d*([eE][-+]?\d+)?|\d+[eE][-+]?\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t): r'\d+'; t.value = int(t.value); return t

def t_ID(t): r'[A-z][A-z0-9]*'; return t

t_ignore = ' \t\r'

def t_newline(t): r'\n+'; t.lexer.lineno += len(t.value)

def t_error(t):
    print(">> Caracter inválido: ", t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == '__main__':
    code = sys.stdin.read()
    lexer.input(code)
    for tok in lexer:
        print(tok)
