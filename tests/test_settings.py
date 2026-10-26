"""Testes automatizados das configurações do jogo."""

from settings import Settings


def test_settings_screen_dimensions() -> None:
    """Verifica se as dimensões da tela são positivas."""
    settings = Settings()
    assert settings.screen_width > 0
    assert settings.screen_height > 0


def test_settings_ship_speed() -> None:
    """Verifica se a velocidade da nave é positiva."""
    settings = Settings()
    assert settings.ship_speed > 0


def test_settings_bullet_limit() -> None:
    """Verifica se o limite de projéteis é válido."""
    settings = Settings()
    assert settings.bullet_allowed > 0