"""Theme system for coursework PPT engine.

Adapted from references/mckinsey-pptx/mckinsey_pptx/theme.py (MIT License).
Changes: Chinese font defaults, academic-friendly palettes, coursework sizing.
"""
from dataclasses import dataclass, field, replace
from pptx.dml.color import RGBColor


def rgb(hex_str: str) -> RGBColor:
    h = hex_str.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


@dataclass(frozen=True)
class Palette:
    primary: RGBColor = field(default_factory=lambda: rgb("2B579A"))
    primary_light: RGBColor = field(default_factory=lambda: rgb("4A7CC9"))
    accent: RGBColor = field(default_factory=lambda: rgb("E74C3C"))
    accent_soft: RGBColor = field(default_factory=lambda: rgb("F5B7B1"))
    black: RGBColor = field(default_factory=lambda: rgb("000000"))
    white: RGBColor = field(default_factory=lambda: rgb("FFFFFF"))
    text_dark: RGBColor = field(default_factory=lambda: rgb("1A1A1A"))
    text_secondary: RGBColor = field(default_factory=lambda: rgb("555555"))
    rule_gray: RGBColor = field(default_factory=lambda: rgb("999999"))
    light_gray: RGBColor = field(default_factory=lambda: rgb("E8E8E8"))
    soft_gray: RGBColor = field(default_factory=lambda: rgb("F5F5F5"))
    grid_gray: RGBColor = field(default_factory=lambda: rgb("D0D0D0"))
    footer_gray: RGBColor = field(default_factory=lambda: rgb("888888"))
    placeholder_gray: RGBColor = field(default_factory=lambda: rgb("BFBFBF"))
    status_green: RGBColor = field(default_factory=lambda: rgb("27AE60"))
    status_amber: RGBColor = field(default_factory=lambda: rgb("F39C12"))
    status_red: RGBColor = field(default_factory=lambda: rgb("E74C3C"))


@dataclass(frozen=True)
class Typography:
    family: str = "Microsoft YaHei"
    family_en: str = "Calibri"
    title_size: int = 28
    section_title_size: int = 16
    body_size: int = 14
    small_size: int = 11
    footer_size: int = 9
    big_number_size: int = 72


@dataclass(frozen=True)
class Layout:
    slide_width_in: float = 13.333
    slide_height_in: float = 7.5
    margin_left_in: float = 0.6
    margin_right_in: float = 0.6
    margin_top_in: float = 0.4
    margin_bottom_in: float = 0.35
    title_top_in: float = 0.5
    title_height_in: float = 0.7
    title_underline_top_in: float = 1.2
    body_top_in: float = 1.5
    footer_top_in: float = 7.0


@dataclass(frozen=True)
class Theme:
    palette: Palette = field(default_factory=Palette)
    typography: Typography = field(default_factory=Typography)
    layout: Layout = field(default_factory=Layout)
    copyright_text: str = ""


# --- Preset themes ---

DEFAULT_THEME = Theme()

ACADEMIC_BLUE = Theme(
    palette=Palette(
        primary=rgb("1F4E79"),
        primary_light=rgb("2E75B6"),
        accent=rgb("C0504D"),
        accent_soft=rgb("F2DCDB"),
    ),
)

MINIMAL_GRAY = Theme(
    palette=Palette(
        primary=rgb("404040"),
        primary_light=rgb("666666"),
        accent=rgb("0070C0"),
        accent_soft=rgb("DEEBF7"),
    ),
)

WARM_ORANGE = Theme(
    palette=Palette(
        primary=rgb("BF4B28"),
        primary_light=rgb("E36C09"),
        accent=rgb("1F4E79"),
        accent_soft=rgb("FDE9D9"),
    ),
)


def get_theme_by_name(name: str) -> Theme:
    themes = {
        "default": DEFAULT_THEME,
        "academic_blue": ACADEMIC_BLUE,
        "minimal_gray": MINIMAL_GRAY,
        "warm_orange": WARM_ORANGE,
    }
    return themes.get(name, DEFAULT_THEME)
