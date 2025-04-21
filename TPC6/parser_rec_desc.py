import ply.lex as lex

# analex
tokens = ['PA', 'PF', 'NUM']
literals = ['*', '+', '-']

t_PA = r'\('
t_PF = r'\)'

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(">> Caráter inválido:", t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()


# Parser LL(1) Recursivo Descendente & Semantica
prox_simb = ('Erro', '', 0, 0)

def parserError(simb):
    print("Erro sintático, token inesperado:", simb)
    exit(1)

def rec_term(simb):
    global prox_simb
    if prox_simb is not None and (prox_simb.type == simb or prox_simb.value == simb):
        val = prox_simb.value
        prox_simb = lexer.token()
        return val
    else:
        parserError(prox_simb)


# P8: Factor -> '(' Expr ')'
# P9:         | num
def rec_Factor():
    global prox_simb
    if prox_simb.type == 'PA':
        print("Derivando por P8: Factor -> '(' Expr ')'")
        rec_term('PA')
        val = rec_Expr()
        rec_term('PF')
        print("Reconheci P8: Factor -> '(' Expr ')'")
        return val
    elif prox_simb.type == 'NUM':
        print("Derivando por P9: Factor -> num")
        val = rec_term('NUM')
        print("Reconheci P9: Factor -> num")
        return val
    else:
        parserError(prox_simb)

# P6: Term' -> * Factor Term'
# P7:         | ε
def rec_TermP(inherited):
    global prox_simb
    if prox_simb is not None and prox_simb.value == '*':
        print("Derivando por P6: Term' -> '*' Factor Term'")
        rec_term('*')
        factor_val = rec_Factor()
        result = rec_TermP(inherited * factor_val)
        print("Reconheci P6: Term' -> '*' Factor Term'")
        return result
    elif prox_simb is None or prox_simb.value in ['+', '-', ')']:
        print("Derivando por P7: Term' -> ε")
        print("Reconheci P7: Term' -> ε")
        return inherited
    else:
        parserError(prox_simb)

# P5: Term -> Factor Term'
def rec_Term():
    print("Derivando por P5: Term -> Factor Term'")
    factor_val = rec_Factor()
    result = rec_TermP(factor_val)
    print("Reconheci P5: Term -> Factor Term'")
    return result

# P2: Expr' -> + Term Expr'
# P3:         | - Term Expr'
# P4:         | ε
def rec_ExprP(inherited):
    global prox_simb
    if prox_simb is not None and prox_simb.value == '+':
        print("Derivando por P2: Expr' -> '+' Term Expr'")
        rec_term('+')
        term_val = rec_Term()
        result = rec_ExprP(inherited + term_val)
        print("Reconheci P2: Expr' -> '+' Term Expr'")
        return result
    elif prox_simb is not None and prox_simb.value == '-':
        print("Derivando por P3: Expr' -> '-' Term Expr'")
        rec_term('-')
        term_val = rec_Term()
        result = rec_ExprP(inherited - term_val)
        print("Reconheci P3: Expr' -> '-' Term Expr'")
        return result
    elif prox_simb is None or prox_simb.value == ')':
        print("Derivando por P4: Expr' -> ε")
        print("Reconheci P4: Expr' -> ε")
        return inherited
    else:
        parserError(prox_simb)

# P1: Expr -> Term Expr'
def rec_Expr():
    print("Derivando por P1: Expr -> Term Expr'")
    term_val = rec_Term()
    result = rec_ExprP(term_val)
    print("Reconheci P1: Expr -> Term Expr'")
    return result

def rec_Parser(data):
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    resultado = rec_Expr()
    if prox_simb is not None:
        parserError(prox_simb)
    else:
        print("= ", resultado)

if __name__ == "__main__":
    print("Calculadora de expressões aritméticas:")
    while True:
        entrada = input(">> ")
        rec_Parser(entrada)
