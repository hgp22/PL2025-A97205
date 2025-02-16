import sys

# Nota: este programa faz apenas uma travessia ao
#       dataset.
#       D(K,V) -> distribuicao de obras, apenas
#       preciso de contar quantos elementos existe
#       na lista do dicionario de D(Periodo, Lista de Obras)

def parse_csv(text) -> list:
    rows = []
    current_row = []
    current_field = []
    in_quotes = False
    i = 0
    while i < len(text):
        c = text[i]
        if in_quotes:
            if c == '"':
                if i + 1 < len(text) and text[i + 1] == '"':
                    current_field.append('"')
                    i += 1
                else:
                    in_quotes = False
            else:
                current_field.append(c)
        else:
            if c == '"':
                in_quotes = True
            elif c == ';':
                current_row.append(''.join(current_field))
                current_field = []
            elif c == '\n':
                current_row.append(''.join(current_field))
                rows.append(current_row)
                current_row = []
                current_field = []
            elif c == '\r':
                if i + 1 < len(text) and text[i + 1] == '\n':
                    i += 1
                current_row.append(''.join(current_field))
                rows.append(current_row)
                current_row = []
                current_field = []
            else:
                current_field.append(c)
        i += 1

    if current_field or current_row:
        current_row.append(''.join(current_field))
        rows.append(current_row)
    return rows

def main():
    text = sys.stdin.read()
    rows = parse_csv(text)
    if not rows:
        return

    header = rows[0]
    data_rows = rows[1:]
    
    compositores = []
    periodo_obras = {}

    for row in data_rows:
        if len(row) < 7:
            continue
        obra = row[0].strip()
        periodo = row[3].strip()
        compositor = row[4].strip()
        
        if compositor and compositor not in compositores:
            compositores.append(compositor)
        
        if periodo:
            periodo_obras.setdefault(periodo, []).append(obra)

    compositores.sort()
    for p in periodo_obras:
        periodo_obras[p].sort()

    dist_obras_periodo = {p: len(obr) for p, obr in periodo_obras.items()}

    print("--Resultados--")
    print("Lista Ordenada de Compositores:", compositores)
    print("Dicionario Periodo -> Lista Ordenada de Titulos:", periodo_obras)
    print("Distribuicao de Obras por Periodo:", dist_obras_periodo)
    print("--------------")

if __name__ == "__main__":
    main()
