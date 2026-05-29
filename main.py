# ----------------------------------------------------
# Responsabilidade: inicializacao e loop principal.
# Cria todas as entidades, define as formulas das portas
# e orquestra os turnos do player e dos inimigos.
# ----------------------------------------------------

import os
from Logic    import avaliar
from dungeon  import loadmapa, loadgame, runplayer, runinimigo
from entities import item, inimigo
from player   import Player

# Tamanho do mapa
LARGURA = 10
ALTURA  = 10

# Cria o mapa vazio
mapa = loadmapa(LARGURA, ALTURA)

# Cria o player na posicao inicial
player = Player(x=1, y=1)

# Cria os inimigos com suas rotas de patrulha
inimigos = [
    inimigo(x=5, y=5),
    inimigo(x=7, y=3),
    inimigo(x=2, y=6),
    inimigo(x=8, y=2)
]

# Cria os exploits disponiveis no mapa
# bypass: novo exploit — permite abrir FIREWALL_A mesmo sem credencial
exploits = [
    item(x=3, y=2, nome="credencial", state=False),
    item(x=6, y=7, nome="firewall",   state=False),
    item(x=1, y=7, nome="bypass",     state=False),
]

# ------------------------------------------------
# PORTAS — cada uma com sua formula proposicional
#
# FIREWALL_A    usa OR  : basta credencial OU bypass
# SERVIDOR_ROOT usa AND + NOT : precisa dos dois e sem alarme
#
# Operadores cobertos: AND, OR, NOT
# Implicacao (->) explicada na tela inicial como equivalencia logica
# ------------------------------------------------

class Porta:
    def __init__(self, x, y, nome, formula):
        self.x       = x
        self.y       = y
        self.nome    = nome
        self.formula = formula

portas = [
    Porta(
        x=9, y=5,
        nome="FIREWALL_A",
        formula="credencial OR bypass"
    ),
    Porta(
        x=8, y=8,
        nome="SERVIDOR_ROOT",
        formula="(credencial AND firewall) AND NOT alarme"
    ),
]

# Cria o firewall (obstaculo fisico fixo)
class Firewall:
    x = 4
    y = 4
firewall_obj = Firewall()

# Cria as paredes fixas (borda superior)
class Parede:
    def __init__(self, x, y):
        self.x = x
        self.y = y

paredes = [
    Parede(0,0), Parede(1,0), Parede(2,0), Parede(3,0),
    Parede(4,0), Parede(5,0), Parede(6,0), Parede(7,0),
    Parede(8,0), Parede(9,0),
]

# Estado do alarme — comeca False
# Ativado futuramente por contato com inimigos
player.inventario["alarme"] = False

# ------------------------------------------------
# TELA INICIAL
# ------------------------------------------------

print("=" * 52)
print("  ROGUEHACKER  —  SISTEMA DE INVASAO")
print("=" * 52)
print("  Controles : w a s d  mover  |  q  sair")
print("  Simbolos  : @=voce  E=antivirus  $=exploit")
print("              P=porta  #=firewall  /=parede")
print("-" * 52)
print("  PORTAS DO SISTEMA:")
for p in portas:
    print(f"    [{p.nome}]")
    print(f"    Formula: {p.formula}")
print("-" * 52)
print("  OPERADORES LOGICOS:")
print("    AND — conjuncao   : ambas as condicoes verdadeiras")
print("    OR  — disjuncao   : ao menos uma verdadeira")
print("    NOT — negacao     : inverte o valor logico")
print("    ->  — implicacao  : A->B equiv. a (NOT A OR B)")
print("=" * 52)
input("  Pressione Enter para iniciar a invasao...")

# ------------------------------------------------
# ROTAS DE PATRULHA DOS INIMIGOS
# ------------------------------------------------

rotas = [
    [(5,5),(5,6),(5,7),(5,6)],   # inimigo 0 — patrulha vertical
    [(7,3),(7,4),(7,3),(7,2)],   # inimigo 1 — patrulha vertical
    [(2,6),(3,6),(4,6),(3,6)],   # inimigo 2 — patrulha horizontal
    [(8,2),(8,3),(8,4),(8,3)]    # inimigo 3 — patrulha vertical
]
indices = [0, 0, 0, 0]

# ------------------------------------------------
# RENDERIZACAO INICIAL
# ------------------------------------------------

mapa = loadgame(mapa, player, inimigos, portas, firewall_obj, paredes, exploits)
for linha in mapa:
    print(' '.join(linha))

# ------------------------------------------------
# LOOP PRINCIPAL
# ------------------------------------------------

rodando = True
while rodando:

    # --- TURNO DO PLAYER ---
    # runplayer exibe o HUD de proposicoes antes de ler a direcao
    resultado = runplayer(mapa, player, exploits, inimigos, portas)

    if resultado == "ganhou":
        print("\n>>> ACESSO ROOT CONCEDIDO. VOCE VENCEU! <<<")
        rodando = False
        break

    if resultado == "perdeu":
        print("\n>>> ANTIVIRUS DETECTADO. GAME OVER. <<<")
        rodando = False
        break

    if resultado == "sair":
        print("\nSaindo do sistema...")
        rodando = False
        break

    # --- TURNO DOS INIMIGOS ---
    # runinimigo exibe a proposicao de comportamento de cada inimigo
    for i, ini in enumerate(inimigos):
        indices[i] = (indices[i] + 1) % len(rotas[i])
        novo_x, novo_y = rotas[i][indices[i]]

        resultado_ini = runinimigo(mapa, player, ini, novo_x, novo_y, inimigos)

        if resultado_ini == "gameover":
            print("\n>>> ANTIVIRUS DETECTADO. GAME OVER. <<<")
            rodando = False
            break

    if not rodando:
        break

    # Limpa o terminal e rerenderiza o mapa atualizado
    os.system('cls' if os.name == 'nt' else 'clear')
    mapa = loadgame(mapa, player, inimigos, portas, firewall_obj, paredes, exploits)
    for linha in mapa:
        print(' '.join(linha))

print("\nFim de sessao.")