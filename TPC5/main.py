import ply.lex as lex
import maquina

moedas = {
    "2e": 2.00,
    "1e": 1.00,
    "50c": 0.50,
    "20c": 0.20,
    "10c": 0.10,
    "5c": 0.05,
    "2c": 0.02,
    "1c": 0.01
}

literals = ['.',',']
tokens = ['LISTAR','MOEDA','SELECIONAR','SAIR','PRODUTO',
          'DINHEIRO']

t_LISTAR = r'LISTAR'
t_MOEDA = r'MOEDA'
t_DINHEIRO = r'\d{1,2}[ec]'
t_SELECIONAR = r'SELECIONAR'
t_PRODUTO = r'A\d{2}'
t_SAIR = r'SAIR'
t_ignore = ' \t\n'

def t_error(t): print(">> Caracter invalido ", t.value[0]); return t

def to_int(s) -> int:
    r = 0
    if (s in moedas):
        r += moedas[s]
        return r
    else:
        raise Exception("Moeda inválida")
    

lexer = lex.lex()

m = maquina.Maquina()
print(m.greet())

while 1:
    command = input(">> ")
    lexer.input(command)
    tok = lexer.token()
    match tok.type:
        case "SAIR":
            break
        case "MOEDA": # nao tenho as virgulas nem o ponto final a funcionar
            for tok in lexer:
                if(tok.type == "DINHEIRO"):
                    m.insereSaldo(to_int(tok.value))
            print(f"maq: Saldo = {m.saldo}")
        case "LISTAR":
            m.imprimeProdutos()
        case "SELECIONAR":
            for tok in lexer:
                if(tok.type == "PRODUTO"):
                    m.compraProduto(tok.value)

