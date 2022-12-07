import pygame, sys
from random import choice, randint
import os
from login import login

import pygame

import obstaculo
from inimigos import Alien, Extra
from jogador import Jogador
from laser import Laser

os.system('clear')
print('Rodando o jogo!')


class Jogo:
	def __init__(self):
		# Setup do jogador
		jogador_sprite = Jogador((largura / 2,altura),largura,5)
		self.jogador = pygame.sprite.GroupSingle(jogador_sprite)

		# Vida e pontos
		self.vidas = 3
		self.vida_imagem = pygame.image.load('Assets/player.png').convert_alpha()
		self.vida_posicao_inicial = largura - (self.vida_imagem.get_size()[0] * 2 + 20)
		self.pontos = 0
		self.font = pygame.font.Font('Assets/Pixeled.ttf',20)

		# Obstaculos
		self.formato = obstaculo.formato
		self.bloco_tamanho = 6
		self.blocos = pygame.sprite.Group()
		self.obstaculo_qntd = 4
		self.obstaculo_x_posicoes = [num * (largura / self.obstaculo_qntd) for num in range(self.obstaculo_qntd)]
		self.criar_varios_obstaculos(*self.obstaculo_x_posicoes, x_inicio = largura / 15, y_inicio = 480)

		# Setup do alien
		self.aliens = pygame.sprite.Group()
		self.alien_lasers = pygame.sprite.Group()
		self.alien_setup(rows = 6, cols = 8)
		self.alien_direcao = 1

		# Setup Vida Extra
		self.extra = pygame.sprite.GroupSingle()
		self.extra_spawn_time = randint(40,80)

		# Audios
		self.laser_sound = pygame.mixer.Sound('Assets/shoot.wav')
		self.laser_sound.set_volume(0.5)
		self.explosion_sound = pygame.mixer.Sound('Assets/invaderkilled.wav')
		self.explosion_sound.set_volume(0.3)

	def criar_obstaculo(self, x_inicio, y_inicio,offset_x):
		for row_index, row in enumerate(self.formato):
			for col_index,col in enumerate(row):
				if col == 'x':
					x = x_inicio + col_index * self.bloco_tamanho + offset_x
					y = y_inicio + row_index * self.bloco_tamanho
					bloco = obstaculo.Bloco(self.bloco_tamanho,(241,79,80),x,y)
					self.blocos.add(bloco)

	def criar_varios_obstaculos(self,*offset,x_inicio,y_inicio):
		for offset_x in offset:
			self.criar_obstaculo(x_inicio,y_inicio,offset_x)

	def alien_setup(self,rows,cols,x_distancia = 60,y_distancia = 48,x_offset = 70, y_offset = 100):
		for row_index, row in enumerate(range(rows)):
			for col_index, col in enumerate(range(cols)):
				x = col_index * x_distancia + x_offset
				y = row_index * y_distancia + y_offset
				
				if row_index == 0: alien_sprite = Alien('yellow',x,y)
				elif 1 <= row_index <= 2: alien_sprite = Alien('green',x,y)
				else: alien_sprite = Alien('red',x,y)
				self.aliens.add(alien_sprite)

	def alien_posicao(self):
		all_aliens = self.aliens.sprites()
		for alien in all_aliens:
			if alien.rect.right >= largura:
				self.alien_direcao = -1
				self.alien_para_baixo(2)
			elif alien.rect.left <= 0:
				self.alien_direcao = 1
				self.alien_para_baixo(2)

	def alien_para_baixo(self,distancia):
		if self.aliens:
			for alien in self.aliens.sprites():
				alien.rect.y += distancia

	def alien_disparar(self):
		if self.aliens.sprites():
			random_alien = choice(self.aliens.sprites())
			laser_sprite = Laser(random_alien.rect.center,6,altura)
			self.alien_lasers.add(laser_sprite)
			self.laser_sound.play()

	def extra_alien_timer(self):
		self.extra_spawn_time -= 1
		if self.extra_spawn_time <= 0:
			self.extra.add(Extra(choice(['right','left']),largura))
			self.extra_spawn_time = randint(400,800)

	def colisao_check(self):

		# Disparos do jogador
		if self.jogador.sprite.lasers:
			for laser in self.jogador.sprite.lasers:
				# Disparar em obstaculo
				if pygame.sprite.spritecollide(laser, self.blocos, True):
					laser.kill()
					

				# Disparar em aliens
				aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
				if aliens_hit:
					for alien in aliens_hit:
						self.pontos += alien.vida
					laser.kill()
					self.explosion_sound.play()

				# Disparar na vida extra
				if pygame.sprite.spritecollide(laser,self.extra,True):
					self.pontos += 500
					laser.kill()

		# Lasers dos aliens
		if self.alien_lasers:
			for laser in self.alien_lasers:
				# obstaculo colisaos
				if pygame.sprite.spritecollide(laser,self.blocos,True):
					laser.kill()

				if pygame.sprite.spritecollide(laser,self.jogador,False):
					laser.kill()        
					self.vidas -= 1
					if self.vidas <= 0:
						pygame.quit()
						sys.exit()

		# Aliens
		if self.aliens:
			for alien in self.aliens:
				pygame.sprite.spritecollide(alien,self.blocos,True)

				if pygame.sprite.spritecollide(alien,self.jogador,False):
					pygame.quit()
					sys.exit()
	
	def mostrar_vidas(self):
		for live in range(self.vidas - 1):
			x = self.vida_posicao_inicial + (live * (self.vida_imagem.get_size()[0] + 10))
			tela.blit(self.vida_imagem,(x,8))

	def mostrar_pontos(self):
		pontos_mostrar = self.font.render(f'Pontuaçao: {self.pontos}',False,'white')
		pontos_rect = pontos_mostrar.get_rect(topleft = (10,-10))
		tela.blit(pontos_mostrar,pontos_rect)

	def mensagem_de_vitoria(self):
		if not self.aliens.sprites():
			tela_vitoria = self.font.render('Voce venceu!',False,'white')
			vitoria_rect = tela_vitoria.get_rect(center = (largura / 2, altura / 2))
			tela.blit(tela_vitoria,vitoria_rect)

	def iniciar(self):
		self.jogador.update()
		self.alien_lasers.update()
		self.extra.update()
		
		self.aliens.update(self.alien_direcao)
		self.alien_posicao()
		self.extra_alien_timer()
		self.colisao_check()
		
		self.jogador.sprite.lasers.draw(tela)
		self.jogador.draw(tela)
		self.blocos.draw(tela)
		self.aliens.draw(tela)
		self.alien_lasers.draw(tela)
		self.extra.draw(tela)
		self.mostrar_vidas()
		self.mostrar_pontos()
		self.mensagem_de_vitoria()

if __name__ == '__main__':
	pygame.init()
	pygame.display.set_caption('Space Invaders - Facul Edition')
	largura = 600
	altura = 600
	tela = pygame.display.set_mode((largura,altura))
	relogio = pygame.time.Clock()
	jogo = Jogo()

	ALIENLASER = pygame.USEREVENT + 1
	pygame.time.set_timer(ALIENLASER,800)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == ALIENLASER:
				jogo.alien_disparar()

		tela.fill((30,30,30))
		jogo.iniciar()
        
			
		pygame.display.flip()
		relogio.tick(60)
