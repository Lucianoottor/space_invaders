import pygame

from laser import Laser


class Jogador(pygame.sprite.Sprite):
    # Criar image e posição inicial do jogador
    def __init__(self,pos,limite,velocidade):
        super().__init__()
        self.image = pygame.image.load("Assets/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.velocidade = velocidade
        self.limite_tela = limite
        self.pronto = True
        self.laser_timer = 0
        self.laser_recarga = 600
        self.lasers = pygame.sprite.Group()
        self.laser_som = pygame.mixer.Sound("Assets/shoot.wav")
    # Gerar comandos de movimento para o jogador 
    def comandos(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidade #.x pois se move apenas no eixo X (lados)
        elif teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
    # Comandos de disparo
        if teclas[pygame.K_SPACE] and self.pronto:
            self.disparar_laser()
            self.pronto = False
            self.laser_timer = pygame.time.get_ticks()
            self.laser_som.play()  
              
    def limite(self):
        if self.rect.left <=0:
            self.rect.left = 0
        if self.rect.right >= self.limite_tela:
            self.rect.right = self.limite_tela

    def recarga(self):
        if not self.pronto:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_timer >= self.laser_recarga:
                self.pronto = True
    def disparar_laser(self):
        self.lasers.add(Laser(self.rect.center,-8,self.rect.bottom))
    def update(self):
        self.comandos()
        self.limite()
        self.recarga()
        self.lasers.update()
