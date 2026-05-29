# ----------------------------------------------------
# Responsabilidade: mapa, renderizacao e loop de turno.
# Carrega entidades no grid, processa movimentos e
# exibe o estado do jogo no terminal.
# ----------------------------------------------------

from Logic import avaliar, diagnosticar, exibir_tabela_verdade, avaliar_regra_inimigo


# ------------------------------------------------
# CONSTRUCAO DO MAPA
# ------------------------------------------------

def loadmapa(tamanhox, tamanhoy):
    """Cria um mapa vazio preenchido com espacos."""
    return [[' ' for _ in range(tamanhox)] for _ in range(tamanhoy)]


def loadplayer(mapa, player):
    mapa[player.y][player.x] = '@'
    return mapa


def loadanti(mapa, inimigos):
    for i in inimigos:
        mapa[i.y][i.x] = 'E'
    return mapa


def loadporta(mapa, portas):
    """Aceita lista de portas ou porta unica."""
    if not isinstance(portas, list):
        portas = [portas]
    for p in portas:
        mapa[p.y][p.x] = 'P'
    return mapa


def loadfirewall(mapa, firewall):
    mapa[firewall.y][firewall.x] = '#'
    return mapa


def loadparede(mapa, paredes):
    for p in paredes:
        mapa[p.y][p.x] = '/'
    return mapa


def loadexploit(mapa, exploits):
    for e in exploits:
        if not e.state:
            mapa[e.y][e.x] = '$'
    return mapa


def loadgame(mapa, player, inimigos, portas, firewall, paredes, exploits):
    """
    Limpa o mapa e recarrega todas as entidades.
    A limpeza evita que sprites antigos fiquem presos no grid
    quando inimigos ou o player se movem.
    """
    # Reseta todas as celulas para espaco vazio
    for y in range(len(mapa)):
        for x in range(len(mapa[0])):
            mapa[y][x] = ' '

    # Carrega na ordem correta — player por cima de tudo
    mapa = loadparede(mapa, paredes)
    mapa = loadfirewall(mapa, firewall)
    mapa = loadexploit(mapa, exploits)
    mapa = loadporta(mapa, portas)
    mapa = loadanti(mapa, inimigos)
    mapa = loadplayer(mapa, player)
    return mapa


# ------------------------------------------------
# HUD — LOGICA PROPOSICIONAL EM TEMPO REAL
# ------------------------------------------------

def exibir_hud(player, portas):

    if not isinstance(portas, list):
        portas = [portas]

    inv = player.inventario

    print("\n" + "=" * 52)
    print("  PROPOSICOES DO SISTEMA")
    print("=" * 52)

    # --- Variaveis proposicionais com valor atual ---
    variaveis = ["credencial", "firewall", "bypass", "alarme"]
    for v in variaveis:
        val     = inv.get(v, False)
        simbolo = "V" if val else "F"
        print(f"  [{simbolo}]  {v:<12} = {val}")

    print("-" * 52)

    # --- Formula de cada porta avaliada com inventario atual ---
    print("  PORTAS:")
    for porta in portas:
        resultado = avaliar(porta.formula, inv)
        simbolo   = "ABERTA " if resultado else "FECHADA"
        print(f"  [{simbolo}]  {porta.nome}")
        print(f"           {porta.formula}")
        print(f"           => {resultado}")

    print("=" * 52)


# ------------------------------------------------
# TURNO DO PLAYER
# ------------------------------------------------

def runplayer(mapa, player, itens, inimigos, portas, formula=None):
 
    if not isinstance(portas, list):
        portas = [portas]

    # Exibe o estado das proposicoes antes de cada jogada
    exibir_hud(player, portas)

    # Apaga sprite da posicao atual no grid
    mapa[player.y][player.x] = ' '

    direcao = input("\n  Direcao (w/a/s/d | q: sair): ").strip().lower()

    if direcao == 'q':
        return "sair"

    des = player.calcular_destino(direcao)

    if des is None:
        return None

    # Valida limites do mapa
    if not (0 <= des[1] < len(mapa) and 0 <= des[0] < len(mapa[0])):
        return None

    # Bloqueia movimento para parede ou firewall
    if player.colidir_parede(mapa[des[1]][des[0]]):
        return None

    # Guarda posicao anterior — necessario para voltar
    # se o player bater numa porta bloqueada
    old_x, old_y = player.x, player.y

    player.mover(des[0], des[1])

    # --- Colisao com inimigo ---
    if player.colidir_inimigo(inimigos):
        return "perdeu"

    # --- Colisao com item ---
    for item in itens:
        if item.x == player.x and item.y == player.y and not item.state:
            player.coletar(item.nome)
            item.state = True
            # Mostra a atualizacao da variavel proposicional
            print(f"\n  [EXPLOIT COLETADO]")
            print(f"  Proposicao atualizada: {item.nome} = False => True")
            input("  Pressione Enter para continuar...")

    # --- Colisao com porta ---
    for porta in portas:
        if player.x == porta.x and player.y == porta.y:
            diag = diagnosticar(porta.formula, player.inventario)

            if diag["resultado"]:
                # Formula satisfeita — porta abre
                return "ganhou"

            # Formula nao satisfeita — exibe diagnostico completo
            print(f"\n  {'=' * 48}")
            print(f"  PORTA BLOQUEADA — {porta.nome}")
            print(f"  {'=' * 48}")
            print(f"  Formula : {porta.formula}")
            print(f"  {'─' * 48}")
            for var, val in diag["variaveis"].items():
                s = "V" if val else "F"
                print(f"  [{s}]  {var:<12} = {val}")
            print(f"  {'─' * 48}")
            print(f"  Resultado: {diag['resultado']}")
            print(f"  {'=' * 48}")

            # Tabela-verdade completa — mostra todos os casos possiveis
            vars_formula = list(diag["variaveis"].keys())
            exibir_tabela_verdade(porta.formula, vars_formula)

            input("  Pressione Enter para continuar...")

            # Volta o player para a posicao anterior (antes da porta)
            player.mover(old_x, old_y)

    return None


# ------------------------------------------------
# TURNO DO INIMIGO
# ------------------------------------------------

def runinimigo(mapa, player, inimigo, novox, novoy, inimigos):
    """
    Move o inimigo e exibe sua regra de comportamento
    como formula proposicional explicita a cada turno.

    Regra: ALERTA = player_visivel OR alarme_ativo
      - player_visivel = distancia Manhattan entre player e inimigo <= 3
      - alarme_ativo   = player.inventario["alarme"]

    Isso torna a logica do inimigo rastreavel e explicita,
    nao apenas um movimento silencioso pelo mapa.
    """
    # Apaga sprite da posicao atual
    mapa[inimigo.y][inimigo.x] = ' '

    # --- REGRA PROPOSICIONAL DO INIMIGO ---
    distancia      = abs(player.x - inimigo.x) + abs(player.y - inimigo.y)
    player_visivel = distancia <= 3
    alarme_ativo   = player.inventario.get("alarme", False)

    em_alerta, descricao = avaliar_regra_inimigo(player_visivel, alarme_ativo)

    # Exibe a proposicao avaliada para este inimigo
    idx    = inimigos.index(inimigo)
    estado = "ALERTA   " if em_alerta else "PATRULHA"
    print(f"  [E{idx}] {descricao}  =>  {estado}")

    # Move o inimigo e verifica colisao com player
    if inimigo.mov(novox, novoy, player):
        return "gameover"

    mapa = loadanti(mapa, inimigos)
    return "continua"