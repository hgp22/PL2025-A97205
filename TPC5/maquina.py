import json

class Maquina:

    def __init__(self):
        with open('stock.json', 'r') as file:
            self.produtos = json.load(file)
        self.saldo = 0
        self.localizacao = "Departamento de Informática - Piso 2"
        self.proprietario = "HGP"

    def greet(self) -> str:
        return f"""maq: A inicializar...\nmaq: Pode inserir o seu pedido"""

    def imprimeProdutos(self):
        print("maq:" + '\n')
        for p in self.produtos:
            print('| {:1} | {:^10} | {:>4} | {:<3} |'
                  .format(p['nome'], p['preco'],
                          p['cod'], p['quant']))
            
    def insereSaldo(self, saldo):
        self.saldo += saldo

    # ainda falta adicionar o caso onde a quantidade vá para 0
    # apago o produto??
    def compraProduto(self, nomeProd) -> int:
        for p in self.produtos:
            if(p['nome'] == nomeProd
               and self.saldo >= p['preco']
               and p['quant'] > 0):
                p['quant'] -= 1
                Maquina.insereSaldo(-p['preco'])
                print(f"maq: Pode retirar o produto {p['nome']}")
                print(f"maq: Saldo = {self.saldo}")
                return 1
        return -1

    


## Notas
# preciso de fazer um conversor de 1e30c para 1.30 ou 1,30
# qual e a convencao dos returns??
# a maquina apenas retorna o troco quando o utilizador sai
#   do programa