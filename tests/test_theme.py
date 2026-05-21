import pytest

from fb2term.ui.theme import Theme, ThemeNotFoundError, ThemeRegistry, get_theme


def test_get_default_theme() -> None:
    theme = get_theme()

    assert theme.name == "dark"
    assert theme.as_css_variables()["background"] == theme.background


def test_theme_registry_returns_sorted_names() -> None:
    registry = ThemeRegistry(
        (
            Theme("b", "B", "#000", "#111", "#222", "#333", "#444", "#555", "#666"),
            Theme("a", "A", "#000", "#111", "#222", "#333", "#444", "#555", "#666"),
        )
    )

    assert registry.names() == ("a", "b")


def test_theme_registry_rejects_duplicates() -> None:
    theme = Theme("x", "X", "#000", "#111", "#222", "#333", "#444", "#555", "#666")

    with pytest.raises(ValueError):
        ThemeRegistry((theme, theme))


def test_unknown_theme_raises_clear_error() -> None:
    with pytest.raises(ThemeNotFoundError):
        get_theme("missing")
