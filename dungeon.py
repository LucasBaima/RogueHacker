from Logic import avaliar

def loadmapa(tamanhox, tamanhoy):
  #preenche o mapa com espaços vazios de acordo com o tamanho (x, y) da sala

  #cria um mapa vazio
  mapa = []
  for a in range(tamanhoy):
    #cria uma nova linha pra cada string do mapa
    linha = []
    for b in range(tamanhox):
      #preenche a linha com espaços vazios
      linha.append(' ')
    #adiciona a linha no eixo y do mapa
    mapa.append(linha)
  return mapa
  
#essas funções preenchem o mapa com as entidades, items etc
#os objetos sendo carregados precisam ser classes com posiçoes .x e .y dentro delas
#no caso de existir multiplos objetos do mesmo tipo (inimigos), a função recebe uma lista de objetos como argumento
def loadplayer(mapa, player):
  mapa[player.y][player.x] = '@'
  return mapa
def loadanti(mapa, inimigos):
  for i in inimigos:
    mapa[i.y][i.x] = 'E'
  return mapa
def loadporta(mapa, porta):
  mapa[porta.y][porta.x] = 'P'
  return mapa
def loadfirewall(mapa, firewall):
  mapa[firewall.y][firewall.x] = '#'
  return mapa
def loadparede(mapa, paredes):
  for i in paredes:
    mapa[i.y][i.x] = '/'
  return mapa
def loadexploit(mapa, exploit):
  for exploit in exploit:
    if not exploit.state:
      mapa[exploit.y][exploit.x] = '$'
  return mapa
  

#essa função combina todos os loads, caso não queira carregar cada entidade individualmente
def loadgame(mapa, player, inimigos, porta, firewall, paredes, exploit):
  mapa = loadplayer(mapa, player)
  mapa = loadanti(mapa, inimigos)
  mapa = loadporta(mapa, porta)
  mapa = loadfirewall(mapa, firewall)
  mapa = loadparede(mapa, paredes)
  mapa = loadexploit(mapa, exploit)
  return mapa


#chamar essa função quando for a vez do jogador se mover
def runplayer(mapa, player, itens, inimigos, formula, porta):
  #apaga o sprite da posição passada
  mapa[player.y][player.x] = ' '
  direcao = input("escolha a direção ")
  des = player.calcular_destino(direcao)
  #caso destino seja valido, checar colisão com inimigos, itens e a porta
  if des is not None and 0 <= des[1] < len(mapa) and 0 <= des[0] < len(mapa[0]) and not player.colidir_parede(mapa[des[1]][des[0]]):
    player.mover(des[0], des[1])
    if(player.colidir_inimigo(inimigos)):
      return "perdeu"
    for item in itens:
      if(item.x == player.x and item.y == player.y):
        #caso o player esteja no mesmo lugar que um item, coleta esse item
        player.coletar(item.nome)
        item.state = True
        
        
    if(player.x == porta.x and player.y == porta.y):
        from Logic import diagnosticar
        resultado = diagnosticar(formula, player.inventario)  
        if resultado["resultado"]:
            return "ganhou"
        else:
            print("\n=== PORTA BLOQUEADA ===")
            print(f"Formula: {resultado['formula']}")   #Lógica proposicional visível para o jogador
            for var, val in resultado["variaveis"].items():
                status = "✓" if val else "✗"
                print(f"  {status} {var}: {val}")
            print("=======================\n")
            input("pressione Enter para continuar...")
            player.mover(player.x - (des[0] - player.x), player.y - (des[1] - player.y))
            
            
  

#rodar essa função para cada inimigo
#novox e novoy são as coordenadas para quais o inimigo vai se mover nesse turno
def runinimigo(mapa, player, inimigo, novox, novoy, inimigos):
  #tira o inimigo da posição passada
  mapa[inimigo.y][inimigo.x] = ' '
  #atualiza a posição do inimigo e checa colião com o player, caso tenha colisão print gameover
  if(inimigo.mov(novox, novoy, player)):
    return "gameover"
  #print o mapa
  mapa = loadanti(mapa, inimigos)
  return "continua"
