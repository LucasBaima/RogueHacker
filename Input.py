
# ----------------------------------------------------
# Responsabilidade: capturar a tecla pressionada pelo
# usuario e traduzi-la para uma acao do jogo.
# Esse modulo nao sabe nada de logica, mapa ou player.
# So captura e traduz — nada mais.
# ----------------------------------------------------
 
 

MAPA_TECLAS = {
    'w': 'move_norte',
    's': 'move_sul',
    'a': 'move_oeste',
    'd': 'move_leste',
    'e': 'interagir',
    'q': 'sair'
}
 
 
def capturar_acao():
    """
    Aguarda o usuario pressionar uma tecla e retorna
    a acao correspondente como string.
 
    Retorno:
        String com o nome da acao, ex: 'move_norte'.
        None se a tecla nao tiver acao mapeada.
    """
    # input() aguarda o usuario digitar e pressionar Enter.
    # .strip() remove espacos acidentais.
    # .lower() garante que maiusculas funcionem igual.
    tecla = input("Sua jogada (w/a/s/d | e: interagir | q: sair): ").strip().lower()
 
    # Busca a acao no dicionario de mapeamento.
    # Retorna None se a tecla nao estiver mapeada.
    return MAPA_TECLAS.get(tecla, None)
 
 
def acao_para_direcao(acao):
  
    conversao = {
        'move_norte': 'w',
        'move_sul':   's',
        'move_oeste': 'a',
        'move_leste': 'd'
    }
 
    return conversao.get(acao, None)
 
 
# ----------------------------------------------------
# Bloco de testes rapidos — executar diretamente:
# python input.py antes de criar a main (LEMBRAR)
# ----------------------------------------------------
 
if __name__ == "__main__":
 
    print("Teste de captura — pressione uma tecla:\n")
 
    acao = capturar_acao()
    print(f"Acao capturada : {acao}")
 
    direcao = acao_para_direcao(acao)
    print(f"Direcao gerada : {direcao}")
