import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self,cor,x,y):
        super().__init__()
        alien_path = 'Assets/' + cor + '.png'
        self.image = pygame.image.load(alien_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))

        if cor == 'red': self.vida = 100
        elif cor == 'green': self.vida = 200
        else: self.vida = 300

    def update(self,direcao):
        self.rect.x += direcao

class Extra(pygame.sprite.Sprite):
	def __init__(self,lado,altura):
		super().__init__()
		self.image = pygame.image.load('Assets/extra.png').convert_alpha()
		
		if lado == 'right':
			x = altura + 50
			self.velocidade = - 3
		else:
			x = -50
			self.velocidade = 3

		self.rect = self.image.get_rect(topleft = (x,80))

	def update(self):
		self.rect.x += self.velocidade