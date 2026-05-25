class item:
	# state é um bool representando o estado do item, true se tiver sido coletado, false caso contrario 
	def __init__(self, x, y, nome, state):
		self.x = x
		self.y = y
		self.nome = nome
		self.state = state

class inimigo:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def mov(self, novo_x, novo_y, p):
		# move a posicao do inimigo e retorna true caso colida com player
		self.x = novo_x
		self.y = novo_y
		if(self.x == p.x and self.y == p.y):
			return True
		else:
			return False
