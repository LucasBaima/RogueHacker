# ----------------------------------------------------
# Responsabilidade: matematica proposicional pura.
# Avalia formulas, gera diagnosticos e tabelas-verdade.
# Este modulo nao sabe nada de dungeon, player ou UI.
#
# --- Operadores aceitos ---
# AND  — conjuncao         (A AND B)
# OR   — disjuncao         (A OR B)
# NOT  — negacao           (NOT A)
# ->   — implicacao        (A -> B)  equivale a (NOT A OR B)
# Parenteses sao suportados para agrupamento.
# ----------------------------------------------------

import re
from itertools import product


def _preparar_formula(formula: str, inventario: dict) -> str:
  
    # Passo 1: A -> B  =>  (NOT A OR B)
    # Processar ANTES da substituicao de variaveis,
    # enquanto os nomes das variaveis ainda estao na formula.
    formula = re.sub(r'(\w+)\s*->\s*(\w+)', r'(NOT \1 OR \2)', formula)

    # Passo 2: substituir cada variavel pelo seu valor booleano
    for variavel, valor in inventario.items():
        formula = formula.replace(variavel, str(valor))

    # Passo 3: traduzir para Python
    formula = formula.replace("AND", "and")
    formula = formula.replace("OR",  "or")
    formula = formula.replace("NOT", "not")
    return formula


def avaliar(formula: str, inventario: dict) -> bool:
    """
    Avalia a formula com os valores do inventario.
    Retorna True se satisfeita, False caso contrario ou erro.
    """
    formula_python = _preparar_formula(formula, inventario)
    try:
        return bool(eval(formula_python))
    except Exception:
        # Formula malformada — porta permanece fechada por seguranca
        return False


def diagnosticar(formula: str, inventario: dict) -> dict:
   
    resultado = avaliar(formula, inventario)
    variaveis_na_formula = {
        nome: valor
        for nome, valor in inventario.items()
        if nome in formula
    }
    return {
        "resultado": resultado,
        "formula":   formula,
        "variaveis": variaveis_na_formula
    }


# ----------------------------------------------------
# TABELA-VERDADE
# ----------------------------------------------------

def gerar_tabela_verdade(formula: str, nomes_variaveis: list) -> list:
    """
    Gera todas as 2^n combinacoes de valores para as variaveis
    e avalia a formula em cada linha.

    Parametros:
        formula          — formula proposicional em string
        nomes_variaveis  — lista com os nomes das variaveis

    Retorno:
        Lista de dicts representando cada linha da tabela.
        Ex: [{"credencial": False, "alarme": True, "resultado": False}, ...]
    """
    tabela = []
    for combinacao in product([False, True], repeat=len(nomes_variaveis)):
        inventario_temp = dict(zip(nomes_variaveis, combinacao))
        resultado       = avaliar(formula, inventario_temp)
        linha           = dict(inventario_temp)
        linha["resultado"] = resultado
        tabela.append(linha)
    return tabela


def exibir_tabela_verdade(formula: str, nomes_variaveis: list):
  
    tabela = gerar_tabela_verdade(formula, nomes_variaveis)
    col_w  = 14
    total  = len(nomes_variaveis) * col_w + 10
    sep    = "  " + "-" * total

    print(f"\n  Tabela-verdade: {formula}")
    print(sep)

    # Cabecalho
    header = "  " + "".join(f"{v:<{col_w}}" for v in nomes_variaveis) + "RESULTADO"
    print(header)
    print(sep)

    # Uma linha por combinacao
    for row in tabela:
        cells = "  " + "".join(f"{str(row[v]):<{col_w}}" for v in nomes_variaveis)
        cells += str(row["resultado"])
        print(cells)

    print(sep + "\n")


# ----------------------------------------------------
# REGRA PROPOSICIONAL DO INIMIGO
# ----------------------------------------------------

def avaliar_regra_inimigo(player_visivel: bool, alarme_ativo: bool) -> tuple:
    
    em_alerta = player_visivel or alarme_ativo

    descricao = (
        f"player_visivel({player_visivel}) "
        f"OR alarme_ativo({alarme_ativo}) "
        f"=> ALERTA={em_alerta}"
    )
    return em_alerta, descricao


# ----------------------------------------------------
# Bloco de testes rapidos — executar: python Logic.py
# ----------------------------------------------------



if __name__ == "__main__":

    inv_teste = {"credencial": True, "firewall": False, "alarme": False, "bypass": False}

    # --- Teste 1: avaliar AND / OR / NOT ---
    f1 = "(credencial AND firewall) AND NOT alarme"
    print(f"Formula 1: {avaliar(f1, inv_teste)}")   # False (firewall=False)

    f2 = "credencial OR bypass"
    print(f"Formula 2: {avaliar(f2, inv_teste)}")   # True  (credencial=True)

    # --- Teste 2: implicacao ---
    f3 = "credencial -> alarme"
    # credencial=True, alarme=False => True->False = False
    print(f"Formula 3 (implicacao): {avaliar(f3, inv_teste)}")   # False

    # --- Teste 3: diagnosticar ---
    diag = diagnosticar(f1, inv_teste)
    print(f"Diagnostico: {diag}")

    # --- Teste 4: tabela-verdade ---
    exibir_tabela_verdade("credencial AND NOT alarme", ["credencial", "alarme"])

    # --- Teste 5: regra do inimigo ---
    em_alerta, desc = avaliar_regra_inimigo(player_visivel=True, alarme_ativo=False)
    print(f"Inimigo: {desc}")