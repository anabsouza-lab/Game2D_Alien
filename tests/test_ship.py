
"""Testes automatizados para o movimento da nave."""

import os

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame

from settings import Settings
from ship import Ship


def test_ship_initial_position() -> None:
    """Verifica se a nave inicia no centro inferior da tela."""
    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height)
    )

    ship = Ship(screen, settings)

    assert ship.rect.midbottom == screen.get_rect().midbottom

    pygame.quit()


def test_ship_moves_right() -> None:
    """Verifica se a nave se movimenta para a direita."""
    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height)
    )

    ship = Ship(screen, settings)
    initial_x = ship.rect.x

    ship.moving_right = True
    ship.update()

    assert ship.rect.x > initial_x

    pygame.quit()


def test_ship_moves_left() -> None:
    """Verifica se a nave se movimenta para a esquerda."""
    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height)
    )

    ship = Ship(screen, settings)
    initial_x = ship.rect.x

    ship.moving_left = True
    ship.update()

    assert ship.rect.x < initial_x

    pygame.quit()
