# TPC's PL
### Nome: Henrique Guimarães Pereira
### Número: 97205 ![foto](https://github.com/hgp22.png?size=40)
### Resumo: construir um programa que simule uma máquina de vending
No ficheiro `maquina.py` está a representação da entidade máquina de venda
que tem todos os métodos necessários para interagir com a máquina.

No ficheiro `main.py` estão definidos o analisador léxico e semântico. Para
seguir o enunciado, criei a seguinte gramática:
```
P1: MOED   -> moeda MOEDS .
P2: MOEDS  -> dinheiro MOEDS'
P3: MOEDS' -> , dinheiro MOEDS' | vazio
```

Foi acrescentado mais um token 'SALDO' que imprime o saldo no ecrã.

O ficheiro json é atualizado ao invocar o comando `SAIR`.

### lista com resultados:

```
❯ python main.py
maq: A inicializar...
maq: Pode inserir o seu pedido
>> LISTAR
maq:

| Código |   Nome      | Preço | Qt  |
|--------|-------------|-------|-----|
| A23    | água 0.5L   |  0.70 |   7 |
| A22    | amêndoas    |  0.90 |   9 |
>> MOEDA 1e,20c,10c.
>> Inserir as moedas:
maq: Saldo = 1.0
moeda 1e aceite
maq: Saldo = 1.2
moeda 20c aceite
maq: Saldo = 1.3
moeda 10c aceite
>> SELECIONAR
>> SELECIONAR A22
maq: Pode retirar o produto amêndoas
maq: Saldo = 0.4
>> SAIR
maq: Saldo = 0.4
{'20c': 2}
```

### Nota
Python 3.13.1
