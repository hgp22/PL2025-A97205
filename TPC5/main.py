import ply.lex as lex
import ply.yacc as yacc
import maquina

moedas = {"2e": 2.00, "1e": 1.00, "50c": 0.50, "20c": 0.20,
          "10c": 0.10, "5c": 0.05, "2c": 0.02, "1c": 0.01}

#############
# Gramática #
#############

literals = ['.',',']
tokens = ['LISTAR','MOEDA','SELECIONAR','SAIR','PRODUTO','DINHEIRO','SALDO']

t_LISTAR = r'LISTAR'
t_MOEDA = r'MOEDA'
t_DINHEIRO = r'\d{1,2}[ec]'
t_SELECIONAR = r'SELECIONAR'
t_PRODUTO = r'A\d{2}'
t_SAIR = r'SAIR'
t_SALDO = r'SALDO'
t_ignore = ' \t\n'

def t_error(t): print("## TOKEN INVALIDO ", t.value[0]); t.lexer.skip(1); return t

def to_int(s) -> int:
    r = 0
    if (s in moedas):
        r += moedas[s]
        return r
    else:
        raise Exception("Moeda inválida")

def traduz_saldo_em_moedas(saldo):
    saldo = round(saldo, 2)
    resultado = {}

    for moeda, valor in moedas.items():
        qtd = int(saldo // valor)
        if qtd > 0:
            resultado[moeda] = qtd
            saldo -= qtd * valor
            saldo = round(saldo, 2)
    return resultado


"""
P1: MOED -> moeda MOEDS .
P2: MOEDS -> dinheiro
          | , dinheiro

Vou passar para:

P1: MOED   -> moeda MOEDS .
P2: MOEDS  -> dinheiro MOEDS'
P3: MOEDS' -> , dinheiro MOEDS' | vazio

é LL(1) portanto é compatível com LALR
"""

def p_moed(p):
    """moed : MOEDA moeds '.'"""
    print(">> Inserir as moedas:")
    for m_str in p[2]:
        try:
            valor = to_int(m_str)
            m.insereSaldo(valor)
            m.imprimeSaldo()
            print(f"moeda {m_str} aceite")
        except:
            print(f"moeda {m_str} rejeitada")

def p_moeds(p):
    """moeds : DINHEIRO moedsl"""
    p[0] = [p[1]] + p[2]

def p_moedsl(p):
    """moedsl : ',' DINHEIRO moedsl"""
    p[0] = [p[2]] + p[3]

def p_moeds_vazio(p):
    "moedsl : "
    p[0] = []

def p_error(p):
    if p:
        print(f"## Erro sintaxe {p.value}")
    else:
        print(f"## Erro sintaxe fim de input")

if __name__ == "__main__":
    lexer = lex.lex()
    parser = yacc.yacc()

    m = maquina.Maquina()
    print(m.greet())

    while 1:
        command = input(">> ")
        lexer.input(command)
        tok = lexer.token()
        match tok.type:
            case "SALDO":
                m.imprimeSaldo()
            case "SAIR":
                m.saveState()
                m.imprimeSaldo()
                print(traduz_saldo_em_moedas(m.saldo))
                break
            case _ if command[0:5]=="MOEDA":
                try:
                    parser.parse(command)
                except Exception as e:
                    print(f"Erro ao processar as moedas: {e}")
            case "LISTAR":
                m.imprimeProdutos()
            case "SELECIONAR":
                for tok in lexer:
                    if(tok.type == "PRODUTO"):
                        m.compraProduto(tok.value)
