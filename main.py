#Inicialização
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
exploits = [
    item(x=3, y=2, nome="credencial", state=False),
    item(x=6, y=7, nome="firewall",   state=False)
]

# Cria a porta com sua formula proposicional
class Porta:
    x = 8
    y = 8
    formula = "(credencial AND firewall) AND NOT alarme"

porta = Porta()

# Cria o firewall (obstaculo fixo)
class Firewall:
    x = 4
    y = 4

firewall_obj = Firewall()

# Cria as paredes fixas do mapa
class Parede:
    def __init__(self, x, y):
        self.x = x
        self.y = y

paredes = [
    Parede(0, 0), Parede(1, 0), Parede(2, 0), Parede(3, 0),
    Parede(4, 0), Parede(5, 0), Parede(6, 0), Parede(7, 0),
    Parede(8, 0), Parede(9, 0),
]

# Estado do alarme — começa falso
player.inventario["alarme"] = False


# ----------------------------------------------------
# LOOP PRINCIPAL
# ----------------------------------------------------

print("=" * 30)
print("  BEM VINDO AO ROGUEHACKER")
print("  w/a/s/d para mover | q para sair")
print("=" * 30)

# Carrega o estado inicial no mapa e exibe
mapa = loadgame(mapa, player, inimigos, porta, firewall_obj, paredes, exploits)

# Imprime o mapa linha por linha
for linha in mapa:
    print(' '.join(linha))

# Rotas de patrulha dos inimigos — lista de (x, y) por turno
rotas = [
    [(5,5),(5,6),(5,7),(5,6)],  # inimigo 0
    [(7,3),(7,4),(7,3),(7,2)],   # inimigo 1
    [(2,6),(3,6),(4,6),(3,6)],  # inimigo 2 — patrulha horizontal
    [(8,2),(8,3),(8,4),(8,3)]   # inimigo 3 — patrulha vertical
]
indices = [0, 0, 0, 0]  # indice atual de cada inimigo na rota

rodando = True

while rodando:

    # --- TURNO DO PLAYER ---
    resultado = runplayer(mapa, player, exploits, inimigos, porta.formula, porta)

    # Verifica se o jogo terminou pelo movimento do player
    if resultado in ("ganhou", "perdeu"):
        if resultado == "ganhou":
            print("\n>>> ACESSO ROOT CONCEDIDO. VOCE VENCEU! <<<")
        else:
            print("\n>>> ANTIVIRUS DETECTADO. GAME OVER. <<<")
        rodando = False
        break

    # Verifica se o player quer sair
    if resultado == "sair":
        print("\nSaindo do sistema...")
        rodando = False
        break

    # --- TURNO DOS INIMIGOS ---
    for i, ini in enumerate(inimigos):

        # Avanca o indice da rota do inimigo
        indices[i] = (indices[i] + 1) % len(rotas[i])
        novo_x, novo_y = rotas[i][indices[i]]

        # Move o inimigo e verifica colisao com player
        resultado_ini = runinimigo(mapa, player, ini, novo_x, novo_y, inimigos)

        if resultado_ini == "gameover":
            print("\n>>> ANTIVIRUS DETECTADO. GAME OVER. <<<")
            rodando = False
            break
    
    if not rodando:
        break
        
    os.system('cls' if os.name == 'nt' else 'clear')
    mapa = loadgame(mapa, player, inimigos, porta, firewall_obj, paredes, exploits)
    for linha in mapa:
        print(' '.join(linha))    

print("\nFim de sessao.")