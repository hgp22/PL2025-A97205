import sys
from ply.lex import lex

input = """
# DBPedia: obras de Chuck Berry
select ?nome ?desc where {
?s a dbo:MusicalArtist.
?s foaf:name "Chuck Berry"@en .
?w dbo:artist ?s.
?w foaf:name ?nome.
?w dbo:abstract ?desc
} LIMIT 1000
"""

tokens = (
   "COMANDO",
   "VARIAVEL",
   "LCRLYB",
   "RCRLYB",
   "INFO",
   "PONTUACAO",
   "NUM",
   "SEPARADOR",
   "STRING",
   "TIPO",
   "LINGUA"
)

t_LCRLYB = r'\{'
t_RCRLYB = r'\}'
t_PONTUACAO = r'\.'
t_SEPARADOR = r'\:'
t_ignore = ' \t'

def t_COMANDO(t):
    r'(select|where|LIMIT)'
    return t

def t_VARIAVEL(t):
    r'\?\w+'
    return t

def t_TIPO(t):
    r'\ba\b'
    return t

def t_INFO(t):
    r'\w+:\w+'
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'\#.*'
    pass

def t_LINGUA(t):
    r'\@[a-z]+'
    return t

def t_STRING(t):
    r'\".*\"'
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex()

lexer.input(sys.stdin.read())

for tok in lexer:
    print(f"Token ({tok.type}, '{tok.value}')")

