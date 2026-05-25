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
  if(!exploit.state):
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


#as posições dos objetos (player, inimigos, items etc) devem ser calculadas ANTES de chamar as funções, esse arquivo não calcula movimento e colisões


