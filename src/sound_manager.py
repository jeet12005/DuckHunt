import pygame


class SoundManager:

    def __init__(self):
        pygame.mixer.init(44100, -16, 2, 1024)
        pygame.mixer.music.set_volume(0.8)
        self.flapping = pygame.mixer.Sound('sounds/flapping1.wav')
        self.duck = pygame.mixer.Sound('sounds/duck1.wav')
        self.click = pygame.mixer.Sound('sounds/click.wav')
        self.hit = pygame.mixer.Sound('sounds/hit.wav')
        self.blast = pygame.mixer.Sound('sounds/blast.mp3')
        self.gameover = pygame.mixer.Sound('sounds/gameover.wav')
        self.racking = pygame.mixer.Sound('sounds/racking.wav')