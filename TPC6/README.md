# TPC's PL
### Nome: Henrique Guimarães Pereira
### Número: 97205 ![foto](https://github.com/hgp22.png?size=40)
### Resumo:
O ficheiro `parser_rec_desc.py` contêm um analisador léxico,
sintático e semântico para uma calculadora de expressões
aritméticas.

A gramática cumpre os requisitos LL(1), e o parser é recursivo
descendente e foi implementada com base no exemplo das
`listas` das aulas teóricas.

```
P1: Expr    -> Term ExprP
P2: ExprP   -> '+' Term ExprP
P3:         | '-' Term ExprP
P4:         | ε

P5: Term    -> Factor TermP
P6: TermP   -> '*' Factor TermP
P7:         | ε

P8: Factor  -> '(' Expr ')'
P9:         | num
```

### lista com resultados:

```
❯ python parser_rec_desc.py
Calculadora de expressões aritméticas:
>> (9-2)*(13-4)
Derivando por P1: Expr -> Term Expr'
Derivando por P5: Term -> Factor Term'
Derivando por P8: Factor -> '(' Expr ')'
Derivando por P1: Expr -> Term Expr'
Derivando por P5: Term -> Factor Term'
Derivando por P9: Factor -> num
Reconheci P9: Factor -> num
Derivando por P7: Term' -> ε
Reconheci P7: Term' -> ε
Reconheci P5: Term -> Factor Term'
Derivando por P3: Expr' -> '-' Term Expr'
Derivando por P5: Term -> Factor Term'
Derivando por P9: Factor -> num
Reconheci P9: Factor -> num
Derivando por P7: Term' -> ε
Reconheci P7: Term' -> ε
Reconheci P5: Term -> Factor Term'
Derivando por P4: Expr' -> ε
Reconheci P4: Expr' -> ε
Reconheci P3: Expr' -> '-' Term Expr'
Reconheci P1: Expr -> Term Expr'
Reconheci P8: Factor -> '(' Expr ')'
Derivando por P6: Term' -> '*' Factor Term'
Derivando por P8: Factor -> '(' Expr ')'
Derivando por P1: Expr -> Term Expr'
Derivando por P5: Term -> Factor Term'
Derivando por P9: Factor -> num
Reconheci P9: Factor -> num
Derivando por P7: Term' -> ε
Reconheci P7: Term' -> ε
Reconheci P5: Term -> Factor Term'
Derivando por P3: Expr' -> '-' Term Expr'
Derivando por P5: Term -> Factor Term'
Derivando por P9: Factor -> num
Reconheci P9: Factor -> num
Derivando por P7: Term' -> ε
Reconheci P7: Term' -> ε
Reconheci P5: Term -> Factor Term'
Derivando por P4: Expr' -> ε
Reconheci P4: Expr' -> ε
Reconheci P3: Expr' -> '-' Term Expr'
Reconheci P1: Expr -> Term Expr'
Reconheci P8: Factor -> '(' Expr ')'
Derivando por P7: Term' -> ε
Reconheci P7: Term' -> ε
Reconheci P6: Term' -> '*' Factor Term'
Reconheci P5: Term -> Factor Term'
Derivando por P4: Expr' -> ε
Reconheci P4: Expr' -> ε
Reconheci P1: Expr -> Term Expr'
=  63
```

### Nota
Python 3.13.1
