"""UI theme primitives."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Final

DEFAULT_THEME_NAME: Final[str] = "dark"


class ThemeNotFoundError(KeyError):
    """Raised when a requested UI theme is not registered."""


@dataclass(frozen=True, slots=True)
class Theme:
    """A UI color theme.

    Attributes:
        name: Stable theme identifier used in config files.
        label: Human-readable theme label.
        background: Main background color.
        foreground: Main text color.
        accent: Accent color for active controls.
        muted: Muted text color.
        status_background: Status bar background color.
        status_foreground: Status bar text color.
        error: Error text color.
    """

    name: str
    label: str
    background: str
    foreground: str
    accent: str
    muted: str
    status_background: str
    status_foreground: str
    error: str

    def as_css_variables(self) -> dict[str, str]:
        """Return Textual-friendly CSS variables.

        Returns:
            Mapping of CSS variable names to color values.
        """

        return {
            "background": self.background,
            "foreground": self.foreground,
            "accent": self.accent,
            "muted": self.muted,
            "status-background": self.status_background,
            "status-foreground": self.status_foreground,
            "error": self.error,
        }


class ThemeRegistry:
    """Registry of available UI themes."""

    def __init__(self, themes: Iterable[Theme]) -> None:
        """Initialize the registry.

        Args:
            themes: Theme definitions.

        Raises:
            ValueError: If a theme name is empty or duplicated.
        """

        self._themes: dict[str, Theme] = {}
        for theme in themes:
            self.register(theme)

    def register(self, theme: Theme) -> None:
        """Register a theme.

        Args:
            theme: Theme definition.

        Raises:
            ValueError: If the theme name is empty or duplicated.
        """

        if not theme.name:
            raise ValueError("Theme name cannot be empty")
        if theme.name in self._themes:
            raise ValueError(f"Theme already registered: {theme.name}")
        self._themes[theme.name] = theme

    def get(self, name: str) -> Theme:
        """Return a registered theme by name.

        Args:
            name: Theme identifier.

        Returns:
            Registered theme.

        Raises:
            ThemeNotFoundError: If the theme is unknown.
        """

        try:
            return self._themes[name]
        except KeyError as exc:
            raise ThemeNotFoundError(f"Unknown theme: {name}") from exc

    def names(self) -> tuple[str, ...]:
        """Return registered theme names.

        Returns:
            Theme names sorted alphabetically.
        """

        return tuple(sorted(self._themes))


DARK_THEME: Final[Theme] = Theme(
    name="dark",
    label="Dark",
    background="#101216",
    foreground="#d8dee9",
    accent="#88c0d0",
    muted="#7b8496",
    status_background="#1f2430",
    status_foreground="#d8dee9",
    error="#bf616a",
)

LIGHT_THEME: Final[Theme] = Theme(
    name="light",
    label="Light",
    background="#f7f7f2",
    foreground="#222222",
    accent="#305f72",
    muted="#6f6f6f",
    status_background="#e4e4dc",
    status_foreground="#222222",
    error="#a33a3a",
)

SEPIA_THEME: Final[Theme] = Theme(
    name="sepia",
    label="Sepia",
    background="#2b2118",
    foreground="#e8dcc3",
    accent="#d19a66",
    muted="#a89984",
    status_background="#3a2c20",
    status_foreground="#e8dcc3",
    error="#d75f5f",
)

DEFAULT_THEME_REGISTRY: Final[ThemeRegistry] = ThemeRegistry(
    (DARK_THEME, LIGHT_THEME, SEPIA_THEME)
)


def get_theme(name: str | None = None) -> Theme:
    """Return a theme from the default registry.

    Args:
        name: Optional theme name. Uses the default theme when omitted.

    Returns:
        Requested theme.

    Raises:
        ThemeNotFoundError: If the theme is unknown.
    """

    return DEFAULT_THEME_REGISTRY.get(name or DEFAULT_THEME_NAME)
