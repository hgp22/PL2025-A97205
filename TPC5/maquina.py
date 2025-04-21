import json

class Maquina:

    def __init__(self):
        with open("stock.json", "r", encoding="utf-8") as f:
            produtos_lista = json.load(f)
        self.produtos = {p['cod']: p for p in produtos_lista}
        self.saldo = 0
        self.produtosAlterados = False
        self.localizacao = "Departamento de Informática - Piso 2"
        self.proprietario = "HGP"

    def greet(self) -> str:
        return f"""maq: A inicializar...\nmaq: Pode inserir o seu pedido"""

    def imprimeProdutos(self):
        print("maq:\n")
        print("| Código |   Nome      | Preço | Qt  |")
        print("|--------|-------------|-------|-----|")
        for cod, p in self.produtos.items():
            print('| {:<6} | {:<11} | {:>5.2f} | {:>3} |'
              .format(p["cod"], p["nome"], p["preco"], p["quant"]))

    def insereSaldo(self, saldo):
        self.saldo += saldo

    def imprimeSaldo(self):
        print(f"maq: Saldo = {self.saldo}")

    def compraProduto(self, codProd) -> int:
        produto = self.produtos.get(codProd)

        if not produto:
            print(f"Produto com código {codProd} não encontrado.")
            return -1

        if produto['quant'] == 0:
            print(f"O produto {produto['nome']} está esgotado.")
            return -1

        if self.saldo < produto['preco']:
            print(f"Saldo insuficiente para comprar {produto['nome']}.")
            self.imprimeSaldo()
            return -1

        produto['quant'] -= 1
        self.insereSaldo(-produto['preco'])
        print(f"maq: Pode retirar o produto {produto['nome']}")
        self.imprimeSaldo()

        self.produtosAlterados = True
        return 1

    def saveState(self):
        if self.produtosAlterados:
            with open("stock.json", "w", encoding="utf-8") as f:
                json.dump(list(self.produtos.values()), f, indent=4, ensure_ascii=False)
        self.produtosAlterados = False
