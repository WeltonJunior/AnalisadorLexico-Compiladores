import csv
import re

# Definição de tokens e símbolos
reserved_words = {"while", "do"}
operators = {"<", "=", "+"}
terminator = {";"}
identifiers = {"i", "j"}
constants = set(map(str, range(10)))  # "0" to "9"

# Estrutura para armazenar tokens e tabela de símbolos
tokens = []
symbol_table = {}
symbols = {}
symbol_index = 1

# Função para classificar tokens
def classify_token(token):
    global symbol_index  # Declarar a variável global
    if token in reserved_words:
        return "Palavra Reservada", None
    elif token in operators:
        return "Operador", None
    elif token in terminator:
        return "Terminador", None
    elif re.fullmatch(r'\d+', token):
        if token not in symbol_table:
            symbol_table[token] = symbol_index
            symbols[token] = "CONSTANT"
            symbol_index += 1
        return "Constante", symbol_table[token]
    elif re.fullmatch(r'[a-zA-Z_]\w*', token):
        if token not in symbol_table:
            symbol_table[token] = symbol_index
            symbols[token] = "IDENTIFICADOR"
            symbol_index += 1
        return "Identificador", symbol_table[token]
    else:
        raise ValueError(f"Erro léxico: sequência inválida '{token}'")

# Função para análise léxica
def lexical_analysis(source_code):
    # Regex atualizado para capturar todos os tokens incluindo terminadores e símbolos
    token_pattern = re.compile(r'\w+|<=|>=|==|!=|[^\s\w]')
    lines = source_code.split('\n')
    
    for line_num, line in enumerate(lines, start=1):
        position = 0
        while position < len(line):
            match = token_pattern.match(line, position)
            if match:
                token = match.group(0)
                try:
                    token_type, index_or_value = classify_token(token)
                    token_length = len(token)
                    
                    # Formatar a coluna de identificação
                    if index_or_value is not None:
                        identification = f"{token_type} ({index_or_value})"
                    else:
                        identification = token_type
                    
                    tokens.append((token, identification, token_length, line_num, position + 1))
                except ValueError as e:
                    print(e)
                    return False
                position = match.end()
            else:
                position += 1  # Ignorar espaços em branco ou caracteres inválidos
    return True

# Função para salvar tokens e símbolos em um arquivo CSV
def save_to_csv(tokens, symbol_table, filename='output.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Tabela de Tokens
        writer.writerow(["Token", "Identificação", "Tamanho", "Linha", "Coluna"])
        for token in tokens:
            writer.writerow(token)
        
        writer.writerow([])  # Linha em branco para separar tabelas
        
        # Tabela de Símbolos
        writer.writerow(["Índice", "Símbolo"])
        for symbol, index in sorted(symbol_table.items(), key=lambda item: item[1]):
            if symbol in symbols:
                writer.writerow([index, symbol])

# Código-fonte de exemplo
source_code = "while i < 100 do i = i + j;"

# Executar análise léxica
if lexical_analysis(source_code):
    # Salvar resultado em CSV
    save_to_csv(tokens, symbol_table)
    print("Análise léxica concluída. Resultados salvos em output.csv.")
else:
    print("Análise léxica falhou devido a um erro no código-fonte.")
