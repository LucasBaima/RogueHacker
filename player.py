
# ----------------------------------------------------
# Responsabilidade: armazenar o estado do hacker
# (posicao, HP, inventario) e calcular seu movimento
# e colisoes com o ambiente.
# Este modulo nao sabe nada de renderizacao ou UI.
# ----------------------------------------------------


class Player:
    """
    Representa o hacker controlado pelo usuario.

    Atributos:
        x          — posicao horizontal no grid
        y          — posicao vertical no grid
        hp         — pontos de vida (health points)
        inventario — dict de booleanos representando
                     os exploits coletados
    """

    def __init__(self, x, y, hp=100):
        # Posicao inicial do player no grid.
        self.x = x
        self.y = y

        # Vida inicial. Padrao 100 se nao informado.
        self.hp = hp

        # Inventario comeca vazio.
        # Cada exploit coletado adiciona uma chave True aqui.
        # Ex: {"credencial": True, "firewall": False}
        self.inventario = {}


   

    def calcular_destino(self, direcao):
        """
        Calcula a celula destino sem mover o player.
        Retorna as coordenadas (x, y) da celula para onde
        o player quer ir, baseado na direcao pressionada.

        Parametros:
            direcao — string: 'w', 's', 'a' ou 'd'

        Retorno:
            Tupla (novo_x, novo_y) ou None se direcao invalida.
        """
        # Mapeia cada tecla ao deslocamento correspondente.
        # dy negativo = norte (linhas diminuem no grid).
        deslocamentos = {
            'w': (0, -1),   # norte
            's': (0,  1),   # sul
            'a': (-1, 0),   # oeste
            'd': (1,  0)    # leste
        }

        # Retorna None se a tecla nao e uma direcao valida.
        if direcao not in deslocamentos:
            return None

        dx, dy = deslocamentos[direcao]
        return (self.x + dx, self.y + dy)


    def mover(self, novo_x, novo_y):
        """
        Atualiza a posicao do player para as coordenadas informadas.
        Deve ser chamado apenas apos validar que a celula destino
        e acessivel (sem parede, porta bloqueada etc).

        Parametros:
            novo_x, novo_y — coordenadas validadas pelo chamador
        """
        self.x = novo_x
        self.y = novo_y






    # ------------------------------------------------
    # COLISAO
    # ------------------------------------------------

    def colidir_parede(self, celula):
        """
        Verifica se a celula destino e uma parede ou firewall.

        Parametros:
            celula — string simbolo da celula destino no grid

        Retorno:
            True se e parede (movimento bloqueado), False caso contrario.
        """
        # '/' representa parede comum, '#' representa firewall.
        # Ambos bloqueiam o movimento do player.
        return celula in ('/', '#')



    def colidir_inimigo(self, inimigos):
        """
        Verifica se o player esta na mesma celula que algum inimigo.
        Se sim, o alarme deve ser disparado pelo chamador.

        Parametros:
            inimigos — lista de objetos com atributos .x e .y

        Retorno:
            True se ha colisao com algum inimigo, False caso contrario.
        """
        for inimigo in inimigos:
            # Compara posicao atual do player com cada inimigo.
            if self.x == inimigo.x and self.y == inimigo.y:
                return True
        return False





    # ------------------------------------------------
    # INVENTARIO do User
    # ------------------------------------------------

    def coletar(self, chave):
        """
        Adiciona um exploit ao inventario do player.

        Parametros:
            chave — string com o nome do exploit.
                    Ex: "credencial", "firewall"

        O inventario e o dict que o logic.py usa como
        atribuicao de verdade para avaliar as portas.
        """
        # Marca a chave como True no inventario.
        # Isso satisfaz a variavel correspondente nas formulas logicas.
        self.inventario[chave] = True




    def tem(self, chave):
        """
        Verifica se o player possui um exploit especifico.

        Parametros:
            chave — string com o nome do exploit

        Retorno:
            True se possui, False caso contrario.
        """
        # .get() retorna False se a chave nao existir no dict,
        # evitando KeyError em chaves nao coletadas ainda.
        return self.inventario.get(chave, False)





    def tomar_dano(self, dano):
        """
        Reduz o HP do player pelo valor de dano recebido.

        Parametros:
            dano — inteiro com o valor do dano

        Retorno:
            True se o player ainda esta vivo, False se HP chegou a zero.
        """
        self.hp -= dano

        # Garante que o HP nao vai abaixo de zero.
        if self.hp < 0:
            self.hp = 0

        # Retorna se o player ainda esta vivo.
        return self.hp > 0


# ----------------------------------------------------
# Bloco de testes rapidos — executar diretamente:
# python player.py
# ----------------------------------------------------

if __name__ == "__main__":

    # Cria player na posicao (2, 3) com HP padrao.
    p = Player(x=2, y=3)

    # Testa calculo de destino
    destino = p.calcular_destino('w')
    print(f"Destino ao pressionar W: {destino}")  # esperado: (2, 2)

    # Testa movimento
    p.mover(2, 2)
    print(f"Posicao apos mover: ({p.x}, {p.y})")  # esperado: (2, 2)

    # Testa colisao com parede
    print(f"Colide com parede '/': {p.colidir_parede('/')}")   # esperado: True
    print(f"Colide com espaco ' ': {p.colidir_parede(' ')}")   # esperado: False

    # Testa inventario
    p.coletar("credencial")
    print(f"Tem credencial: {p.tem('credencial')}")  # esperado: True
    print(f"Tem firewall:   {p.tem('firewall')}")    # esperado: False

    # Testa dano
    vivo = p.tomar_dano(30)
    print(f"HP apos 30 de dano: {p.hp} | Vivo: {vivo}")  # esperado: 70, True

    vivo = p.tomar_dano(999)
    print(f"HP apos dano fatal: {p.hp} | Vivo: {vivo}")  # esperado: 0, False