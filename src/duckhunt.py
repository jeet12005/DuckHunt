import pygame
import time, math
from pygame.locals import *
import random
from src.image_manager import ImageManager
from src.sound_manager import SoundManager

"""
    This is the main class for the game.
    It handles the main game loop and the game state.
"""

class DuckHunt:

    def __init__(self, screensize = (1200, 768)):
        self.verbose = False
        pygame.init()
        self.black, self.white = (0,0,0), (255,255,255)
        self.screensize = screensize
        self.screenrect = pygame.Rect(0,0, self.screensize[0], self.screensize[1])
        pygame.display.set_caption("Duck Hunt")
        self.screen = pygame.display.set_mode(self.screensize)
        self.images = ImageManager()
        self.sounds = SoundManager()
        self.mouse_position = (0,0)
        self.click_position = (-100, -100)
        self.shells, self.capacity, self.reloading_time = 3, 3, 0
        self.is_reloading, self.is_game_over = False, False
        self.y_move = 0
        self.new_game()

    def new_game(self):
        self.score = 0
        self.duck_velocity = 1
        self.duck_angle = 60
        self.is_alive = False
        self.new_duck()
        self.lives = 3
        self.is_game_over = False

    def loop(self):
        self.handle_events()
        pygame.mouse.set_visible(False)

        if self.lives <= 0 and not self.is_game_over:
            self.game_over()
        elif not self.is_alive:
            self.new_duck()
        elif not self.is_game_over:
            self.move_duck()
        self.handle_reloading()

        self.screen.blit(pygame.transform.scale(self.images.background, self.screensize), (0, 0))
        if self.is_game_over:
            self.screen.blit(self.images.dog, self.images.dog_rect)
        else:
            self.screen.blit(self.images.duck, self.images.duck_rect)
        self.screen.blit(self.images.sight, self.images.sight_rect)
        self.screen.blit(pygame.font.SysFont("Avenir", 36).render(
            f"Shells: {'I' * self.shells:3s}   Points: {self.score}", True, self.white),
            (self.screensize[0] * .55, self.screensize[1] * 0.9
        ))

        self.screen.convert_alpha()
        pygame.display.update()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEMOTION:
                self.mouse_position = pygame.mouse.get_pos()
                self.images.sight_rect.center = self.mouse_position
            elif event.type == MOUSEBUTTONDOWN:
                self.click_position = pygame.mouse.get_pos()
                self.fire()
            elif event.type == KEYDOWN:
                if pygame.key.name(event.key) == "r":
                    self.is_reloading = True
                    self.reloading_time = 20 * self.capacity - (20 * self.shells)
                elif pygame.key.name(event.key) == "space" and self.is_game_over:
                    self.new_game()

    def fire(self):
        if self.shells > 0 and not self.is_reloading:
            self.sounds.blast.play()
            self.shells -= 1
            if self.images.duck_rect.colliderect(self.images.sight_rect):
                self.score += 1
                self.duck_velocity += 1
                self.new_duck()
        else:
            self.sounds.click.play()

    def handle_reloading(self):
        if self.is_reloading:
            if self.reloading_time > 0:
                self.reloading_time -= 1
            else:
                self.sounds.racking.play()
                self.shells = self.capacity
                self.is_reloading = False

    def new_duck(self):
        self.is_alive = True
        x, y = 0, 0
        if random.randint(0, 100) % 2 == 0:
            x = int(self.screensize[0] * 0.2)
            self.duck_angle = -random.randint(5, 35)
        else:
            x = int(self.screensize[0] * 0.8)
            self.duck_angle = -random.randint(145, 175)
        y = int(self.screensize[1] * 0.66)
        self.images.duck_rect.center = x, y
        if self.verbose:
            print("Duck center: ", self.images.duck_rect.center)

    def move_duck(self):
        x = self.images.duck_rect.center[0] + self.duck_velocity * math.cos(math.radians(self.duck_angle))
        y = self.images.duck_rect.centery
        self.y_move += self.duck_velocity * math.sin(math.radians(self.duck_angle)) # coordinate has to be in integers
        if self.y_move <= -1:
            y+=self.y_move // 1
            self.y_move %= 1

        self.images.duck_rect.center = x, y
        if not self.screenrect.colliderect(self.images.duck_rect):
            self.lives -= 1
            if self.lives > 0 and not self.is_game_over:
                self.new_duck()


    def game_over(self):
        if self.verbose:
            print("Game Over!")
        self.is_alive = False
        self.images.duck_rect.center = (-100, -100)
        self.images.dog_rect.center = int(self.screensize[0]/2), int(self.screensize[1]*0.62)
        self.sounds.gameover.play()
        self.is_game_over = True


    def run(self):
        while True:
            self.loop()


if __name__ == "__main__":
    game = DuckHunt()
    game.run()
