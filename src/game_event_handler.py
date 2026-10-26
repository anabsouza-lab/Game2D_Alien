
import sys

import pygame

from bullet import Bullet
from settings import Settings
from ship import Ship


class GameEventHandler:
    """Gerencia os eventos de teclado e fechamento do jogo."""

    def __init__(
        self,
        screen: pygame.Surface,
        settings: Settings,
        ship: Ship,
        bullets: pygame.sprite.Group[Bullet],
    ) -> None:
        """Inicializa os recursos necessários para tratar eventos."""
        self.screen = screen
        self.settings = settings
        self.ship = ship
        self.bullets = bullets

    def check_events(self) -> None:
        """Responde aos eventos de pressionamento de teclas e mouse."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

        # Atualiza continuamente o estado das teclas
        keys = pygame.key.get_pressed()
        self.ship.moving_right = bool(keys[pygame.K_RIGHT])
        self.ship.moving_left = bool(keys[pygame.K_LEFT])

    def _check_keydown_events(self, event: pygame.event.Event) -> None:
        """Detecta quando uma tecla é pressionada."""
        if event.key == pygame.K_RIGHT:
            # Verifica se a tecla pressionada é a seta para a direita
            self.ship.moving_right = True

        elif event.key == pygame.K_LEFT:
            # Verifica se a tecla pressionada é a seta para a esquerda
            self.ship.moving_left = True

        elif event.key == pygame.K_SPACE:
            # Verifica se a tecla pressionada é a barra de espaço
            self._fire_bullet()

    def _check_keyup_events(self, event: pygame.event.Event) -> None:
        """Detecta quando uma tecla é liberada."""
        if event.key == pygame.K_RIGHT:
            # Verifica se a tecla liberada é a seta para a direita
            self.ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            # Verifica se a tecla liberada é a seta para a esquerda
            self.ship.moving_left = False

    def _fire_bullet(self) -> None:
        """Cria um novo projétil quando o limite permitido não foi atingido."""
        # Verifica se o número de projéteis na tela excede o limite permitido
        if len(self.bullets) < self.settings.bullet_allowed:
            # Cria um novo projétil
            new_bullet = Bullet(
                self.screen, self.settings, self.ship
            )

            # Adiciona o novo projétil ao grupo de projéteis
            self.bullets.add(new_bullet)
