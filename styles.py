"""
Style CSS dla aplikacji Nixie Clock Control
Każdy komponent ma osobny styl - łatwo modyfikować bez ryzyka
"""

from config import *


# ===== GŁÓWNE OKNO =====
STYLE_MAIN_WINDOW = f"""
    QMainWindow {{
        background-color: {COLOR_BACKGROUND};
    }}
"""


# ===== GROUPBOX =====
STYLE_GROUPBOX = f"""
    QGroupBox {{
        border: 1px solid {COLOR_BORDER};
        border-radius: {BORDER_RADIUS_LARGE};
        margin-top: {GROUPBOX_MARGIN_TOP}px;
        padding: {GROUPBOX_PADDING};
        background-color: {COLOR_GROUPBOX_BG};
        font-weight: 500;
        color: {COLOR_TEXT_SECONDARY};
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: {GROUPBOX_TITLE_LEFT};
        padding: 0 8px;
    }}
"""


# ===== PRZYCISKI =====
STYLE_BUTTON = f"""
    QPushButton {{
        background-color: {COLOR_PRIMARY};
        border: none;
        border-radius: {BORDER_RADIUS_MEDIUM};
        padding: 8px 20px;
        color: {COLOR_TEXT_PRIMARY};
        font-weight: 600;
        font-size: {FONT_SIZE_NORMAL};
    }}
    QPushButton:hover {{
        background-color: {COLOR_PRIMARY_HOVER};
    }}
    QPushButton:pressed {{
        background-color: {COLOR_PRIMARY_PRESSED};
    }}
    QPushButton:disabled {{
        background-color: rgba(255, 255, 255, 0.1);
        color: {COLOR_TEXT_DISABLED};
    }}
"""


# ===== COMBOBOX =====
STYLE_COMBOBOX = f"""
    QComboBox {{
        background-color: {COLOR_INPUT_BG};
        border: 1px solid {COLOR_BORDER_FOCUS};
        border-radius: {BORDER_RADIUS_MEDIUM};
        padding: 8px 12px;
        color: {COLOR_TEXT_PRIMARY};
        font-size: {FONT_SIZE_NORMAL};
    }}
    QComboBox::drop-down {{
        subcontrol-origin: border;
        subcontrol-position: right;
        width: 24px;
        border-left: 1px solid {COLOR_BORDER_FOCUS};
        border-top-right-radius: {BORDER_RADIUS_MEDIUM};
        border-bottom-right-radius: {BORDER_RADIUS_MEDIUM};
        background-color: {COLOR_PRIMARY};
    }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 5px solid {COLOR_TEXT_PRIMARY};
        width: 0;
        height: 0;
    }}
"""


# ===== TIME EDIT =====
STYLE_TIME_EDIT = f"""
    QTimeEdit {{
        background-color: {COLOR_INPUT_BG};
        border: 1px solid {COLOR_BORDER_FOCUS};
        border-radius: {BORDER_RADIUS_MEDIUM};
        padding: 8px 28px 8px 12px;
        color: {COLOR_TEXT_PRIMARY};
        font-size: {FONT_SIZE_NORMAL};
    }}
    QTimeEdit::up-button {{
        subcontrol-origin: border;
        subcontrol-position: top right;
        width: 22px;
        background-color: {COLOR_PRIMARY};
        border-left: 1px solid {COLOR_BORDER_FOCUS};
        border-top-right-radius: {BORDER_RADIUS_MEDIUM};
    }}
    QTimeEdit::up-button:hover {{
        background-color: {COLOR_PRIMARY_HOVER};
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
        background-color: {COLOR_PRIMARY_HOVER};
        border-left: 1px solid {COLOR_BORDER_FOCUS};
        border-bottom-right-radius: {BORDER_RADIUS_MEDIUM};
    }}
    QTimeEdit::down-button:hover {{
        background-color: {COLOR_PRIMARY_PRESSED};
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


# ===== SLIDER =====
STYLE_SLIDER = f"""
    QSlider::groove:horizontal {{
        height: {SLIDER_HEIGHT}px;
        background: {COLOR_BORDER_FOCUS};
        border-radius: 3px;
    }}
    QSlider::handle:horizontal {{
        background: {COLOR_TEXT_PRIMARY};
        border: 1px solid rgba(0, 0, 0, 0.2);
        width: 18px;
        margin: -6px 0;
        border-radius: 9px;
    }}
    QSlider::sub-page:horizontal {{
        background: {COLOR_PRIMARY};
        border-radius: 3px;
    }}
"""


# ===== CHECKBOX =====
STYLE_CHECKBOX = f"""
    QCheckBox {{
        color: {COLOR_TEXT_SECONDARY};
        spacing: 8px;
    }}
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border-radius: {BORDER_RADIUS_SMALL};
        border: 1px solid rgba(255, 255, 255, 0.3);
        background-color: {COLOR_INPUT_BG};
    }}
    QCheckBox::indicator:checked {{
        background-color: {COLOR_PRIMARY};
        border-color: {COLOR_PRIMARY};
    }}
"""


# ===== CONSOLE / TEXT EDIT =====
STYLE_CONSOLE = f"""
    QTextEdit {{
        background-color: {COLOR_CONSOLE_BG};
        color: rgba(255, 255, 255, 0.7);
        font-family: {FONT_MONO};
        font-size: {FONT_SIZE_TINY};
        border: 1px solid {COLOR_BORDER};
        border-radius: {BORDER_RADIUS_MEDIUM};
        padding: 8px;
    }}
"""


# ===== ETYKIETY (LABELS) =====
STYLE_LABEL_HEADER = f"""
    font-size: {FONT_SIZE_HEADER};
    font-weight: 600;
    color: {COLOR_TEXT_PRIMARY};
    padding: 8px 0;
"""

STYLE_LABEL_SUBTITLE = f"""
    font-size: {FONT_SIZE_SUBTITLE};
    color: {COLOR_TEXT_MUTED};
    padding-bottom: 12px;
"""

STYLE_LABEL_VALUE_BLUE = f"""
    color: {COLOR_PRIMARY};
    font-weight: 600;
"""

STYLE_LABEL_VALUE_ORANGE = f"""
    color: {COLOR_WARNING};
    font-weight: 600;
"""

STYLE_LABEL_STATUS_CONNECTED = f"""
    color: {COLOR_SUCCESS};
    font-weight: 600;
"""

STYLE_LABEL_STATUS_DISCONNECTED = f"""
    color: {COLOR_TEXT_MUTED};
"""


# ===== KOMPLETNY STYL DLA CAŁEJ APLIKACJI =====
def get_complete_stylesheet():
    """Zwraca kompletny stylesheet dla aplikacji"""
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
