import pygame
import random
import time
from config import (
SCREEN_WIDTH,
SCREEN_HEIGHT,
SPEED,
COLOR_MAX,
COLOR_MIN )


class MoveText:
    """
    Classe responsável por mover um texto na tela, fazendo-o quicar nas bordas e mudar de cor ao colidir.
    """
    def __init__(self, text, fonte, tamanho, cor, x, y, screen_width, screen_height, audio_manager):
        self.text = text
        self.fonte = pygame.font.Font(fonte, tamanho)
        self.cor = cor
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.surface = self.fonte.render(self.text, True, self.cor)
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))

       
        self.speed_x = self._non_zero()
        self.speed_y = self._non_zero()

       
        self.audio_manager = audio_manager

    def _non_zero(self):
        return random.choice([-2, -1, 1, 2])

    def _change_color(self):
        self.cor = (
            random.randint(10, 255),
            random.randint(10, 255),
            random.randint(10, 255),
        )
        self.surface = self.fonte.render(self.text, True, self.cor)

    def quicar_nas_bordas(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.topleft = (self.x, self.y)

        if self.x <= 0 or self.x + self.surface.get_width() >= self.screen_width:
            self.speed_x *= -1
            self._change_color()
            self.audio_manager.play_sound("mola")  

        if self.y <= 0 or self.y + self.surface.get_height() >= self.screen_height:
            self.speed_y *= -1
            self._change_color()
            self.audio_manager.play_sound("mola")  

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def update(self):
        self.quicar_nas_bordas()

class BouncingText(MoveText):
    
    def __init__(self, text, font_size, color, screen_width, screen_height, audio_manager):
        super().__init__(text, None, font_size, color, screen_width // 2, screen_height // 2, screen_width, screen_height, audio_manager)
        self.last_direction_change = time.time()

    def _change_direction(self):
        self.speed_x = random.choice([-abs(self.speed_x), abs(self.speed_x)])
        self.speed_y = random.choice([-abs(self.speed_y), abs(self.speed_y)])

    def update(self):
        super().update()

        if time.time() - self.last_direction_change >= 3:
            self._change_direction()
            self.last_direction_change = time.time()

class VerticalText(MoveText):
    def update(self):
        """Move o texto apenas na vertical"""
        self.rect.y += self.speed_y
        self.check_collision()

class HorizontalText(MoveText):
    def update(self):
        """Move o texto apenas na horizontal"""
        self.rect.x += self.speed_x
        self.check_collision()