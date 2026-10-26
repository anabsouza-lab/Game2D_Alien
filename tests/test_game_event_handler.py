
"""Testes automatizados do gerenciador de eventos."""

from unittest.mock import MagicMock, patch

import pygame

from game_event_handler import GameEventHandler
from settings import Settings


def test_keydown_right() -> None:
    """Verifica o evento de pressionar a seta direita."""
    screen = MagicMock()
    ship = MagicMock()
    bullets = pygame.sprite.Group()
    settings = Settings()

    handler = GameEventHandler(screen, settings, ship, bullets)

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
    handler._check_keydown_events(event)

    assert ship.moving_right is True


def test_keyup_right() -> None:
    """Verifica o evento de liberar a seta direita."""
    screen = MagicMock()
    ship = MagicMock()
    bullets = pygame.sprite.Group()
    settings = Settings()

    handler = GameEventHandler(screen, settings, ship, bullets)

    event = pygame.event.Event(pygame.KEYUP, key=pygame.K_RIGHT)
    handler._check_keyup_events(event)

    assert ship.moving_right is False


def test_quit_event() -> None:
    """Verifica se o evento de fechamento encerra o jogo."""
    screen = MagicMock()
    ship = MagicMock()
    bullets = pygame.sprite.Group()
    settings = Settings()

    handler = GameEventHandler(screen, settings, ship, bullets)

    quit_event = pygame.event.Event(pygame.QUIT)

    with (
        patch("pygame.event.get", return_value=[quit_event]),
        patch("sys.exit", side_effect=SystemExit),
    ):
        try:
            handler.check_events()
        except SystemExit:
            pass
        else:
            raise AssertionError("O jogo deveria encerrar.")