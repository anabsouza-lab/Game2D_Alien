
import sys
from typing import Protocol

import pygame
from pygame.sprite import Group

from alien import Alien
from bullet import Bullet
from fast_alien import FastAlien
from game_event_handler import GameEventHandler
from settings import Settings
from ship import Ship


class EventHandler(Protocol):
    """Contrato para o tratamento dos eventos do jogo."""

    def check_events(self) -> None:
        """Processa os eventos do jogo."""
        ...

class AlienInvasion:
    """Gerencia o jogo e seus comportamentos."""

    def __init__(self) -> None:
        """Construtor da classe que inicializa o jogo e cria os recursos básicos"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        # Criando uma instância da classe Ship para representar a nave espacial
        self.ship = Ship(self.screen, self.settings)

        # Mudando a cor do plano de fundo em RGB
        self.bg_color = self.settings.bg_color

        # Criando grupos para armazenar os projéteis e alienígenas
        self.bullets: Group[Bullet] = pygame.sprite.Group()
        self.aliens: Group[Alien] = pygame.sprite.Group()
                # Classe responsável pelo tratamento dos eventos do jogo
        self.event_handler: EventHandler = GameEventHandler(
            self.screen,
            self.settings,
            self.ship,
            self.bullets,
        )

    def create_fleet(self) -> None:
        """Cria uma frota de alienígenas."""
        # Cria um alienígena e calcula o número de alienígenas em uma linha
        # O espaçamento entre os alienígenas é igual a um alienígena
        alien = FastAlien(self.screen, self.settings)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (
            self.settings.screen_height - (3 * alien_height) - ship_height
        )
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            # Cria a primeira linha de alienígenas
            for alien_number in range(number_aliens_x):
                # Cria um alienígena e o posiciona na linha
                alien = FastAlien(self.screen, self.settings)
                alien.x = float(
                    alien_width + 2 * alien_width * alien_number
                )
                alien.rect.x = int(alien.x)
                alien.rect.y = int(
                    alien_height + 2 * alien_height * row_number
                )
                self.aliens.add(alien)

    
        # Atualiza continuamente o estado das teclas
        keys = pygame.key.get_pressed()
        self.ship.moving_right = bool(keys[pygame.K_RIGHT])
        self.ship.moving_left = bool(keys[pygame.K_LEFT])

    

    def _check_bullet_alien_collisions(self) -> None:
        """Verifica colisões entre projéteis e alienígenas."""
        # Verifica se algum projétil atingiu um alienígena
        # Em caso afirmativo, remove o projétil e o alienígena atingido
        pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

    def _update_bullets(self) -> None:
        """Atualiza os projéteis e remove aqueles que saíram da tela."""
        # Atualiza a posição de cada projétil no grupo de projéteis
        self.bullets.update()

        # Verifica se algum projétil saiu da tela
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                # Remove o projétil que saiu da tela
                self.bullets.remove(bullet)

        # Verifica se algum projétil atingiu um alienígena
        # Em caso afirmativo, remove o projétil e o alienígena atingido
        self._check_bullet_alien_collisions()

    def _check_fleet_edges(self) -> None:
        """Verifica se algum alienígena atingiu a borda da tela."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self) -> None:
        """Faz a frota descer e inverte sua direção."""
        # Atualiza a posição de cada alienígena no grupo de alienígenas
        for alien in self.aliens.sprites():
            # Move cada alienígena para baixo com base na velocidade de descida da frota
            alien.rect.y += self.settings.fleet_drop_speed

        # Inverte a direção da frota para que os alienígenas se movam
        # para o lado oposto na próxima atualização
        self.settings.fleet_direction *= -1

    def _check_ship_alien_collisions(self) -> None:
        """Verifica se a nave colidiu com algum alienígena."""
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # Imprime uma mensagem no console indicando que a nave foi atingida
            print("A nave foi atingida!")

            # Encerra o jogo
            sys.exit()

    def _update_aliens(self) -> None:
        """Atualiza a posição e o comportamento dos alienígenas."""
        # Verifica se algum alienígena atingiu a borda da tela
        self._check_fleet_edges()

        # Atualiza a posição de cada alienígena no grupo de alienígenas
        self.aliens.update()

        # Verifica se a nave colidiu com algum alienígena
        self._check_ship_alien_collisions()

    def _update_screen(self) -> None:
        """Atualiza as imagens na tela e muda para a nova tela."""
        # Redesenha a tela a cada passagem pelo laço
        self.screen.fill(self.bg_color)

        # Redesenha a nave em sua posição atual
        self.ship.blitme()

        # alien.drawme() # Desenha os alienígenas presentes no grupo de alienígenas na tela
        self.aliens.draw(
            self.screen
        )  # Desenha os alienígenas presentes no grupo de alienígenas na tela

        # Atualiza a representação visual de cada projétil
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Torna visível a tela mais recente
        pygame.display.flip()

    def run_game(self) -> None:
        """Cria um laço de repetição para a tela sempre ficar visível até
        que o usuário decida fechar a janela."""

        # Cria a frota de alienígenas para ser desenhada na tela
        self.create_fleet()

        while True:
            # Verifica os eventos de teclado e fechamento
            self.event_handler.check_events()

            # Atualiza a posição da nave com base na variável de controle
            self.ship.update()

            # Atualiza os projéteis
            self._update_bullets()

            # Atualiza os alienígenas
            self._update_aliens()

            # Atualiza os elementos visuais do jogo
            self._update_screen()


if __name__ == "__main__":
    alien_invasion = AlienInvasion()
    alien_invasion.run_game()
