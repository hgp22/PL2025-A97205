import ply.lex as lex
import ply.yacc as yacc
import sys
import re


tokens = (
    # Palavras reservadas com base em er a pedido do prof. prh
    'PROGRAM', 'VAR', 'INTEGER', 'BOOLEAN', 'BEGIN', 'END', 'IF', 'THEN', 'ELSE',
    'WHILE', 'FOR', 'TO', 'DOWNTO', 'DO', 'READLN', 'WRITELN', 'WRITE', 'TRUE', 'FALSE',
    'AND', 'OR', 'NOT', 'DIV', 'MOD', 'ID', 'NUMBER', 'STRING', 'ASSIGN', 'EQUAL',
    'NOTEQUAL', 'LT', 'GT', 'LE', 'GE', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODOP',
    'COMMA', 'COLON', 'SEMI', 'DOT', 'LPAREN', 'RPAREN', 'COMMENT'
)

############################################
# Operadores (literals?)
t_ASSIGN = r':='
t_EQUAL = r'='
t_NOTEQUAL = r'<>'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODOP = r'mod'
t_COMMA = r','
t_COLON = r':'
t_SEMI = r';'
t_DOT = r'\.'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_STRING = r'\"[^\"\n]*\"|\'[^\'\n]*\''
############################################

t_ignore = ' \t\r'

def t_COMMENT(t):
    r'\(\*[\s\S]*?\*\)|\{[\s\S]*?\}|//.*'
    t.lexer.lineno += t.value.count('\n')
    pass

# integer // Integer
# flag global (?i) não funciona???
def t_FOR(t):       r'[Ff][Oo][Rr]'                 ; return t
def t_TO(t):        r'[Tt][Oo]'                     ; return t
def t_DOWNTO(t):    r'[Dd][Oo][Ww][Nn][Tt][Oo]'     ; return t
def t_PROGRAM(t):   r'[Pp][Rr][Oo][Gg][Rr][Aa][Mm]' ; return t
def t_VAR(t):       r'[Vv][Aa][Rr]'                 ; return t
def t_INTEGER(t):   r'[Ii][Nn][Tt][Ee][Gg][Ee][Rr]' ; return t
def t_BOOLEAN(t):   r'[Bb][Oo][Oo][Ll][Ee][Aa][Nn]' ; return t
def t_BEGIN(t):     r'[Bb][Ee][Gg][Ii][Nn]'         ; return t
def t_END(t):       r'[Ee][Nn][Dd]'                 ; return t
def t_IF(t):        r'[Ii][Ff]'                     ; return t
def t_THEN(t):      r'[Tt][Hh][Ee][Nn]'             ; return t
def t_ELSE(t):      r'[Ee][Ll][Ss][Ee]'             ; return t
def t_WHILE(t):     r'[Ww][Hh][Ii][Ll][Ee]'         ; return t
def t_DO(t):        r'[Dd][Oo]'                     ; return t
def t_READLN(t):    r'[Rr][Ee][Aa][Dd][Ll][Nn]'     ; return t
def t_WRITELN(t):   r'[Ww][Rr][Ii][Tt][Ee][Ll][Nn]' ; return t
def t_WRITE(t):     r'[Ww][Rr][Ii][Tt][Ee]'         ; return t
def t_TRUE(t):      r'[Tt][Rr][Uu][Ee]'             ; t.value = 'true' ; return t
def t_FALSE(t):     r'[Ff][Aa][Ll][Ss][Ee]'         ; t.value = 'false'; return t
def t_AND(t):       r'[Aa][Nn][Dd]'                 ; return t
def t_OR(t):        r'[Oo][Rr]'                     ; return t
def t_NOT(t):       r'[Nn][Oo][Tt]'                 ; return t
def t_DIV(t):       r'[Dd][Ii][Vv]'                 ; return t
def t_MOD(t):       r'[Mm][Oo][Dd]'                 ; return t
def t_ID(t):        r'[a-zA-Z_][a-zA-Z0-9_]*'       ; return t
def t_NUMBER(t):    r'\d+'                          ; t.value = int(t.value); return t
def t_newline(t):   r'\n+'                          ; t.lexer.lineno += len(t.value)
def t_error(t):     print(f"Illegal character '{t.value[0]}' at line {t.lineno}"); t.lexer.skip(1)

lexer = lex.lex(reflags=re.UNICODE) # flag para aceitar acentos e afins...

symbol_table = {}
current_address = 0
label_counter = 0

def new_label(prefix="label"):
    global label_counter
    label_counter += 1
    return f"{prefix}{label_counter}"


# resolver ambiguidades da gramática....
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('nonassoc', 'LT', 'LE', 'GT', 'GE', 'EQUAL', 'NOTEQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'DIV', 'MOD'),
    ('right', 'UMINUS'),
)

def p_program(p):
    '''program : PROGRAM ID SEMI declarations compound_stmt DOT
               | PROGRAM ID SEMI compound_stmt DOT'''
    init_code = [f"pushi 0 // alocar espaço para {i}" for i in range(current_address)]
    compound_code = p[5] if len(p) == 7 else p[4]
    if compound_code is None:
        compound_code = ""
    output_lines = init_code + ["start"] + [compound_code] + ["stop"]
    p[0] = "\n".join(line for line in output_lines if line)

def p_declarations(p):
    '''declarations : VAR var_decl_list
                    | empty'''
    p[0] = ""

def p_var_decl_list(p):
    '''var_decl_list : var_decl SEMI
                     | var_decl SEMI var_decl_list'''
    p[0] = ""

def p_var_decl(p):
    'var_decl : id_list COLON type'
    global current_address
    for var_name in p[1]:
        symbol_table[var_name] = current_address
        current_address += 1
    p[0] = ""

def p_id_list(p):
    '''id_list : ID
               | ID COMMA id_list'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

def p_type(p):
    '''type : INTEGER
            | BOOLEAN'''
    p[0] = ""

def p_compound_stmt(p):
    'compound_stmt : BEGIN stmt_list END'
    p[0] = p[2] if p[2] else ""

def p_stmt_list(p):
    '''stmt_list : stmt
                 | stmt SEMI stmt_list'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]}\n{p[3]}" if p[1] and p[3] else p[1] or p[3]

def p_stmt(p):
    '''stmt : assignment
            | if_stmt
            | while_stmt
            | for_stmt
            | readln_stmt
            | writeln_stmt
            | compound_stmt
            | empty'''
    p[0] = p[1] if len(p) > 1 else ""

def p_assignment(p):
    'assignment : ID ASSIGN expr'
    var_name = p[1]
    if var_name in symbol_table:
        addr = symbol_table[var_name]
        p[0] = f"{p[3]}\nstoreg {addr} // ir à stack para atribuir o valor a {var_name}"
    else:
        print(f"!!Erro: variável - {var_name} - não declarada!!")
        p[0] = ""

def p_if_stmt(p):
    '''if_stmt : IF expr THEN stmt
               | IF expr THEN stmt ELSE stmt'''
    if len(p) == 5:
        end_label = new_label("ifend")
        p[0] = f"{p[2]}\njz {end_label} // If condição falsa\n{p[4]}\n{end_label}:"
    else:
        else_label = new_label("else")
        end_label = new_label("ifend")
        p[0] = f"{p[2]}\njz {else_label} // If condição falsa\n{p[4]}\njump {end_label}\n{else_label}:\n{p[6]}\n{end_label}:"

def p_while_stmt(p):
    'while_stmt : WHILE expr DO stmt'
    start_label = new_label("whileloop")
    end_label = new_label("whileend")
    p[0] = f"{start_label}:\n{p[2]}\njz {end_label} // While condição falsa\n{p[4]}\njump {start_label}\n{end_label}:"

def p_for_stmt(p):
    'for_stmt : FOR ID ASSIGN expr TO expr DO stmt'
    loop_var = p[2]
    global current_address
    if loop_var not in symbol_table:
        symbol_table[loop_var] = current_address
        current_address += 1
    addr_loop = symbol_table[loop_var]
    addr_bound = current_address
    current_address += 1
    loop_label = new_label("forloop")
    end_label = new_label("forend")
    init_code = f"{p[4]}\nstoreg {addr_loop} // inicializar {loop_var}\n"
    bound_code = f"{p[6]}\nstoreg {addr_bound} // limite do ciclo\n"
    start_code = f"{loop_label}:\n"
    cond_code = (
        f"pushg {addr_loop} // ir à stack para atribuir o valor a {loop_var}\n"
        f"pushg {addr_bound} // carrega o limite\n"
        "infeq // verifica a condição do ciclo\n"
        f"jz {end_label} // sai se: loop_var > bound\n"
    )
    body_code = f"{p[8]}\n"
    inc_code = (
        f"pushg {addr_loop} // carrega {loop_var}\n"
        "pushi 1 // Push 1\n"
        "add\n"
        f"storeg {addr_loop} // acaba logica da var do ciclo\n"
    )
    jump_code = f"jump {loop_label}\n"
    end_code = f"{end_label}:\n"
    p[0] = init_code + bound_code + start_code + cond_code + body_code + inc_code + jump_code + end_code

def p_readln_stmt(p):
    'readln_stmt : READLN LPAREN ID RPAREN'
    var_name = p[3]
    if var_name in symbol_table:
        addr = symbol_table[var_name]
        p[0] = f"read\natoi\nstoreg {addr} // carregar {var_name}"
    else:
        print(f"!!Erro: variável - {var_name} - não declarada!!")
        p[0] = ""

def p_writeln_stmt(p):
    '''writeln_stmt : WRITELN LPAREN writeln_args RPAREN
                    | WRITE LPAREN writeln_args RPAREN
                    | WRITELN LPAREN RPAREN
                    | WRITE LPAREN RPAREN'''
    if len(p) == 5:
        if p[1].lower() == 'writeln':
            p[0] = f"{p[3]}\nWRITELN"
        else:
            p[0] = p[3]
    else:
        if p[1].lower() == 'writeln':
            p[0] = "WRITELN"
        else:
            p[0] = ""

def p_writeln_args(p):
    '''writeln_args : arg
                    | arg COMMA writeln_args'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]}\n{p[3]}"

def p_arg(p):
    '''arg : expr
           | STRING'''
    if isinstance(p[1], str) and (p[1].startswith('"') or p[1].startswith("'")):
        s = p[1][1:-1]
        p[0] = f'pushs "{s}"\nwrites // escreve string'
    else:
        p[0] = f"{p[1]}\nwritei // escreve inteiro"

def p_expr(p):
    '''expr : simple_expr
            | simple_expr relop simple_expr'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        op_map = {'=': 'equal', '<>': 'equal\nnot', '<': 'inf', '>': 'sup', '<=': 'infeq', '>=': 'supeq'}
        p[0] = f"{p[1]}\n{p[3]}\n{op_map[p[2]]} // lógica"

def p_relop(p):
    '''relop : EQUAL
             | NOTEQUAL
             | LT
             | GT
             | LE
             | GE'''
    p[0] = p[1]

def p_simple_expr(p):
    '''simple_expr : term
                   | simple_expr addop term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        op_map = {'+': 'add', '-': 'sub', 'or': 'or'}
        p[0] = f"{p[1]}\n{p[3]}\n{op_map[p[2]]} // maths"

def p_addop(p):
    '''addop : PLUS
             | MINUS
             | OR'''
    p[0] = p[1]

def p_term(p):
    '''term : factor
            | term mulop factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        op_map = {'*': 'mul', '/': 'div', 'div': 'div', 'mod': 'mod', 'and': 'and'}
        p[0] = f"{p[1]}\n{p[3]}\n{op_map[p[2]]} // operação"

def p_mulop(p):
    '''mulop : TIMES
             | DIVIDE
             | DIV
             | MOD
             | AND'''
    p[0] = p[1]

def p_factor(p):
    '''factor : ID
              | NUMBER
              | LPAREN expr RPAREN
              | NOT factor
              | TRUE
              | FALSE
              | MINUS factor %prec UMINUS'''
    if len(p) == 2:
        if isinstance(p[1], int):
            p[0] = f"pushi {p[1]} // coloca numero na stack"
        elif p[1] == 'true':
            p[0] = f"pushi 1 // coloca booleano como true"
        elif p[1] == 'false':
            p[0] = f"pushi 0 // coloca booleano como false"
        else:  # ID
            var_name = p[1]
            if var_name in symbol_table:
                addr = symbol_table[var_name]
                p[0] = f"pushg {addr} // carrega da stack {var_name}"
            else:
                print(f"!!Erro: variável - {var_name} - não declarada!!")
                p[0] = ""
    elif len(p) == 3:
        if p[1] == 'not':
            p[0] = f"{p[2]}\nnot"
        elif p[1] == '-':
            p[0] = f"pushi 0\n{p[2]}\nsub"
    else:
        p[0] = p[2]

def p_empty(p):
    'empty :'
    p[0] = ""

def p_error(p):
    if p:
        print(f"Erro de sintaxe na linha {p.lineno}: {p.value}")
    else:
        print("Erro no fim do ficheiro")

parser = yacc.yacc()

if __name__ == '__main__':
    data = sys.stdin.read()
    if not data:
        print("No input provided")
        sys.exit(1)

    symbol_table.clear()
    current_address = 0
    label_counter = 0

    result = parser.parse(data)
    if result:
        print(result)
