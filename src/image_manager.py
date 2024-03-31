import pygame


class ImageManager:

    def __init__(self):
        self.background = pygame.image.load("images/background.png")
        self.sight = pygame.image.load("images/sight.gif")
        self.dog = pygame.image.load("images/dog.gif")
        self.duck = pygame.image.load("images/greenduck.gif")

        # Optimize images for faster drawing
        self.background.convert()
        self.sight.convert()
        self.dog.convert()
        self.duck.convert()

        self.duck_rect = self.duck.get_rect()
        self.sight_rect = self.sight.get_rect()
        self.dog_rect = self.dog.get_rect()
