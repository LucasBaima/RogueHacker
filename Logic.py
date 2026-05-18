## Responsabilidade: receber uma formula proposicional
# em string e um inventario de variaveis booleanas,
# e retornar True ou False.
# Este modulo nao sabe nada sobre dungeon, player ou UI.
# E matematica pura isolada.


# --- Operadores aceitos ---
# AND  → conjuncao         (A AND B)
# OR   → disjuncao         (A OR B)
# NOT  → negacao           (NOT A)
# Parenteses sao suportados para agrupamento.
# Variaveis sao os nomes exatos das chaves do inventario.


def _preparar_formula(formula: str, inventario: dict[str, bool]) -> str:    #Tradução
    
       for variavel, valor in inventario.items():
        formula = formula.replace(variavel, str(valor))

    # Traduz os operadores logicos da notacao legivel
    # para os operadores nativos do Python.
    # A ordem importa: AND antes de NOT para evitar
    # substituicoes parciais incorretas.
       formula = formula.replace("AND", "and")
       formula = formula.replace("OR", "or")
       formula = formula.replace("NOT", "not")

       return formula
   
   
   
   
   
def avaliar(formula: str, inventario: dict[str, bool]) -> bool:    #Avaliação
    

    # Preparação a formula substituindo variaveis e operadores.
    formula_python = _preparar_formula(formula, inventario)

    try:
        # eval() executa a string como expressao Python.
        # E seguro aqui porque controla o conteudo:
        # a formula so contem True, False, and, or, not e parenteses.
        resultado = eval(formula_python)
        # Garante que o retorno e sempre bool puro,
        # mesmo que eval retorne outro tipo truthy/falsy.
        return bool(resultado)

    except Exception:
        # Se a formula estiver malformada (variavel inexistente,
        # parentese faltando, etc.), retorna False por seguranca.
        # A porta permanece fechada em caso de erro.
        return False
    
    
    
 
def diagnosticar(formula: str, inventario: dict[str, bool]) -> dict:
    ##Versao expandida do avaliador que retorna o estado de cada
    #variavel individualmente, alem do resultado final.
 
    #Util para o jogo exibir ao player quais condicoes
    #foram satisfeitas e quais ainda faltam.
    
    # Avalia o resultado final da formula com o inventario atual.
    resultado = avaliar(formula, inventario)
    
    
    # Percorre o inventario completo do player e filtra
    # apenas as variaveis cujo nome aparece na formula.
    # Evita poluir o diagnostico com itens irrelevantes.
    variaveis_na_formula = {}
    for nome, valor in inventario.items():
        if nome in formula:
            variaveis_na_formula[nome] = valor

    # Monta e retorna o dicionario de diagnostico.
    diagnostico = {}
    diagnostico["resultado"] = resultado
    diagnostico["formula"]   = formula
    diagnostico["variaveis"] = variaveis_na_formula

    return diagnostico

 
    
 
   
 
