"""
Style VINTAGE/STEAMPUNK dla Nixie Clock Control
Metaliczne tekstury, pomarańczowe świecenie, retro wygląd
"""

from config_vintage import *


# ===== GŁÓWNE OKNO =====
STYLE_MAIN_WINDOW = f"""
    QMainWindow {{
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 {COLOR_BACKGROUND},
            stop:1 #0d0a08
        );
    }}
"""


# ===== GROUPBOX - Metaliczne panele =====
STYLE_GROUPBOX = f"""
    QGroupBox {{
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(61, 47, 33, 0.9),
            stop:0.5 rgba(45, 35, 24, 0.8),
            stop:1 rgba(38, 29, 20, 0.9)
        );
        border: 2px solid {COLOR_BORDER};
        border-radius: {BORDER_RADIUS_LARGE};
        margin-top: {GROUPBOX_MARGIN_TOP}px;
        padding: {GROUPBOX_PADDING};
        font-weight: 600;
        color: {COLOR_TEXT_SECONDARY};
        font-family: {FONT_FAMILY};
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: {GROUPBOX_TITLE_LEFT};
        padding: 0 8px;
        color: {COLOR_BRASS};
    }}
"""


# ===== PRZYCISKI - Industrial style =====
STYLE_BUTTON = f"""
    QPushButton {{
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 {COLOR_PRIMARY},
            stop:0.5 {COLOR_PRIMARY_HOVER},
            stop:1 {COLOR_PRIMARY}
        );
        border: 2px solid {COLOR_COPPER};
        border-radius: {BORDER_RADIUS_MEDIUM};
        padding: 10px 24px;
        color: #1a1410;
        font-weight: 700;
        font-size: {FONT_SIZE_NORMAL};
        font-family: {FONT_FAMILY};
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    QPushButton:hover {{
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 {COLOR_PRIMARY_HOVER},
            stop:1 {COLOR_PRIMARY_PRESSED}
        );
        border: 2px solid {COLOR_BRASS};
        box-shadow: 0 0 10px {GLOW_COLOR};
    }}
    QPushButton:pressed {{
        background: {COLOR_PRIMARY_PRESSED};
        border: 2px solid {COLOR_BRONZE};
    }}
    QPushButton:disabled {{
        background: rgba(61, 47, 33, 0.4);
        border: 2px solid rgba(184, 115, 51, 0.2);
        color: {COLOR_TEXT_DISABLED};
    }}
"""


# ===== COMBOBOX - Retro dropdown =====
STYLE_COMBOBOX = f"""
    QComboBox {{
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(26, 20, 16, 0.8),
            stop:1 rgba(20, 15, 12, 0.9)
        );
        border: 2px solid {COLOR_BORDER};
        border-radius: {BORDER_RADIUS_MEDIUM};
        padding: 10px 14px;
        color: {COLOR_TEXT_PRIMARY};
        font-size: {FONT_SIZE_NORMAL};
        font-family: {FONT_FAMILY};
        font-weight: 600;
    }}
    QComboBox:focus {{
        border: 2px solid {COLOR_BORDER_FOCUS};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 30px;
        background: {COLOR_COPPER};
        border-top-right-radius: {BORDER_RADIUS_MEDIUM};
        border-bottom-right-radius: {BORDER_RADIUS_MEDIUM};
    }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid {COLOR_TEXT_PRIMARY};
        margin-right: 8px;
    }}
"""


# ===== TIME EDIT - Terminal style =====
STYLE_TIME_EDIT = f"""
    QTimeEdit {{
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 {COLOR_CONSOLE_BG},
            stop:1 rgba(13, 10, 8, 0.95)
        );
        border: 2px solid {COLOR_BORDER};
        border-radius: {BORDER_RADIUS_MEDIUM};
        padding: 10px 28px 10px 14px;
        color: {COLOR_PRIMARY};
        font-size: 16px;
        font-family: {FONT_MONO};
        font-weight: 700;
    }}
    QTimeEdit:focus {{
        border: 2px solid {COLOR_BORDER_GLOW};
    }}
    QTimeEdit::up-button {{
        subcontrol-origin: border;
        subcontrol-position: top right;
        width: 22px;
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 {COLOR_COPPER},
            stop:1 {COLOR_BRONZE}
        );
        border-left: 1px solid {COLOR_BORDER};
        border-top-right-radius: {BORDER_RADIUS_MEDIUM};
    }}
    QTimeEdit::up-button:hover {{
        background: {COLOR_BRASS};
    }}
    QTimeEdit::up-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-bottom: 5px solid {COLOR_TEXT_PRIMARY};
        width: 0;
        height: 0;
    }}
    QTimeEdit::down-button {{
        subcontrol-origin: border;
        subcontrol-position: bottom right;
        width: 22px;
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 {COLOR_BRONZE},
            stop:1 {COLOR_COPPER}
        );
        border-left: 1px solid {COLOR_BORDER};
        border-bottom-right-radius: {BORDER_RADIUS_MEDIUM};
    }}
    QTimeEdit::down-button:hover {{
        background: {COLOR_BRASS};
    }}
    QTimeEdit::down-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 5px solid {COLOR_TEXT_PRIMARY};
        width: 0;
        height: 0;
    }}
"""


# ===== SLIDER - Industrial gauge =====
STYLE_SLIDER = f"""
    QSlider::groove:horizontal {{
        height: {SLIDER_HEIGHT}px;
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 rgba(26, 20, 16, 0.8),
            stop:1 rgba(20, 15, 12, 0.8)
        );
        border: 1px solid {COLOR_BORDER};
        border-radius: 4px;
    }}
    QSlider::handle:horizontal {{
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 {COLOR_BRASS},
            stop:0.5 {COLOR_COPPER},
            stop:1 {COLOR_BRONZE}
        );
        border: 2px solid #5a3d1f;
        width: 24px;
        height: 24px;
        margin: -9px 0;
        border-radius: 12px;
        box-shadow: 0 2px 4px {SHADOW_COLOR};
    }}
    QSlider::handle:horizontal:hover {{
        box-shadow: 0 0 10px {GLOW_COLOR};
    }}
    QSlider::sub-page:horizontal {{
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 {COLOR_PRIMARY},
            stop:1 {COLOR_PRIMARY_HOVER}
        );
        border: 1px solid {COLOR_COPPER};
        border-radius: 4px;
    }}
"""


# ===== CHECKBOX - Vintage toggle =====
STYLE_CHECKBOX = f"""
    QCheckBox {{
        color: {COLOR_TEXT_SECONDARY};
        spacing: 10px;
        font-family: {FONT_FAMILY};
        font-weight: 600;
    }}
    QCheckBox::indicator {{
        width: 22px;
        height: 22px;
        border-radius: {BORDER_RADIUS_SMALL};
        border: 2px solid {COLOR_BORDER};
        background: {COLOR_INPUT_BG};
    }}
    QCheckBox::indicator:checked {{
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:1,
            stop:0 {COLOR_PRIMARY},
            stop:1 {COLOR_PRIMARY_HOVER}
        );
        border: 2px solid {COLOR_COPPER};
        box-shadow: inset 0 0 6px {GLOW_COLOR};
    }}
    QCheckBox::indicator:checked:hover {{
        box-shadow: 0 0 10px {GLOW_COLOR};
    }}
"""


# ===== CONSOLE - Terminal CRT style =====
STYLE_CONSOLE = f"""
    QTextEdit {{
        background: {COLOR_CONSOLE_BG};
        color: {COLOR_PRIMARY};
        font-family: {FONT_MONO};
        font-size: {FONT_SIZE_SMALL};
        font-weight: 600;
        border: 2px solid {COLOR_BORDER};
        border-radius: {BORDER_RADIUS_MEDIUM};
        padding: 12px;
        line-height: 1.6;
        letter-spacing: 0.5px;
    }}
"""


# ===== ETYKIETY =====
STYLE_LABEL_HEADER = f"""
    font-size: {FONT_SIZE_HEADER};
    font-weight: 700;
    color: {COLOR_BRASS};
    padding: 10px 0;
    font-family: {FONT_FAMILY};
    text-transform: uppercase;
    letter-spacing: 2px;
    text-shadow: 0 2px 4px {SHADOW_COLOR};
"""

STYLE_LABEL_SUBTITLE = f"""
    font-size: {FONT_SIZE_SUBTITLE};
    color: {COLOR_TEXT_MUTED};
    padding-bottom: 14px;
    font-family: {FONT_FAMILY};
    font-style: italic;
"""

STYLE_LABEL_VALUE_ORANGE = f"""
    color: {COLOR_PRIMARY};
    font-weight: 700;
    font-size: 16px;
    font-family: {FONT_MONO};
    text-shadow: 0 0 8px {GLOW_COLOR};
"""

STYLE_LABEL_VALUE_GOLD = f"""
    color: {COLOR_BRASS};
    font-weight: 700;
    font-size: 16px;
    font-family: {FONT_MONO};
    text-shadow: 0 0 8px rgba(212, 175, 55, 0.6);
"""

STYLE_LABEL_STATUS_CONNECTED = f"""
    color: {COLOR_SUCCESS};
    font-weight: 700;
    font-family: {FONT_FAMILY};
"""

STYLE_LABEL_STATUS_DISCONNECTED = f"""
    color: {COLOR_TEXT_MUTED};
    font-family: {FONT_FAMILY};
"""


# ===== KOMPLETNY STYL =====
def get_complete_stylesheet():
    """Zwraca kompletny vintage stylesheet"""
    return (
        STYLE_MAIN_WINDOW +
        STYLE_GROUPBOX +
        STYLE_BUTTON +
        STYLE_COMBOBOX +
        STYLE_TIME_EDIT +
        STYLE_SLIDER +
        STYLE_CHECKBOX +
        STYLE_CONSOLE
    )
