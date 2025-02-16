import sys

def extrair_numeros(token):
    nums = []
    atual = ""
    for ch in token:
        if ch.isdigit():
            atual += ch
        else:
            if atual:
                nums.append(int(atual))
                atual = ""
    if atual:
        nums.append(int(atual))
    return nums

soma_ligada = True
soma_total = 0

for linha in sys.stdin:
    tokens = linha.split()
    eco = []
    
    for token in tokens:
        if token.lower() == "on":
            soma_ligada = True
            eco.append(token)
            continue
        elif token.lower() == "off":
            soma_ligada = False
            eco.append(token)
            continue

        if "=" in token:
            partes = token.split("=")
            reconstruido = ""
            for i, parte in enumerate(partes):
                if soma_ligada:
                    nums = extrair_numeros(parte)
                    if nums:
                        soma_total += sum(nums)
                reconstruido += parte
                if i < len(partes) - 1:
                    reconstruido += "="
                    eco.append(reconstruido)
                    print(" ".join(eco))
                    print(">>", soma_total)
                    eco = []
                    reconstruido = ""
            if reconstruido:
                if reconstruido.lower() == "on":
                    soma_ligada = True
                elif reconstruido.lower() == "off":
                    soma_ligada = False
                eco.append(reconstruido)
        else:
            if soma_ligada:
                nums = extrair_numeros(token)
                if nums:
                    soma_total += sum(nums)
            eco.append(token)
    if eco:
        print(" ".join(eco))

print(">>", soma_total)
