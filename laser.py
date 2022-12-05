import pygame 

class Laser(pygame.sprite.Sprite):
	def __init__(self,pos,velocidade,altura):
		super().__init__()
		self.image = pygame.Surface((4,20))
		self.image.fill('white')
		self.rect = self.image.get_rect(center = pos)
		self.velocidade = velocidade
		self.limite_tela_y = altura

	def destruir(self):
		if self.rect.y <= -50 or self.rect.y >= self.limite_tela_y + 50:
			self.kill()
	def update(self):
		self.rect.y += self.velocidade
		self.destruir()