"""
Konfiguracja VINTAGE/STEAMPUNK dla Nixie Clock Control
Ciepłe, retro kolory pasujące do lamp Nixie
"""

# ===== WYMIARY OKNA =====
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 1150

# ===== WYMIARY KONTROLEK =====
INPUT_HEIGHT = 38
SLIDER_HEIGHT = 8
CONSOLE_HEIGHT = 180

# Szerokości
TIME_EDIT_WIDTH = 120
TIME_EDIT_FULL_WIDTH = 180
BUTTON_WIDTH = 110
PORT_COMBO_MIN_WIDTH = 200

# ===== ODSTĘPY =====
SECTION_SPACING = 16
ELEMENT_SPACING = 12
TIME_FIELDS_SPACING = 20

# Marginesy
WINDOW_MARGIN = 24
GROUPBOX_PADDING = "20px 14px 14px 14px"
GROUPBOX_MARGIN_TOP = 18
GROUPBOX_TITLE_LEFT = "12px"

# ===== KOLORY VINTAGE/STEAMPUNK =====
# Tło
COLOR_BACKGROUND = "#1a1410"  # Ciemny brąz
COLOR_SURFACE = "#2d2318"     # Brązowy powierzchnia

# Kolory akcentów - pomarańczowe jak Nixie
COLOR_PRIMARY = "#ff8c42"     # Pomarańczowy Nixie
COLOR_PRIMARY_HOVER = "#ff7028"
COLOR_PRIMARY_PRESSED = "#e55a1c"

# Miedź/Metal
COLOR_COPPER = "#b87333"
COLOR_BRASS = "#d4af37"
COLOR_BRONZE = "#cd7f32"

# Status
COLOR_SUCCESS = "#7cb342"     # Zielony vintage
COLOR_WARNING = "#ffb300"     # Złoty
COLOR_DANGER = "#d84315"      # Rdzawy czerwony

# Tekst
COLOR_TEXT_PRIMARY = "#f5deb3"       # Wheat/beżowy
COLOR_TEXT_SECONDARY = "#daa86e"     # Złocisty
COLOR_TEXT_DISABLED = "rgba(245, 222, 179, 0.3)"
COLOR_TEXT_MUTED = "rgba(245, 222, 179, 0.5)"

# Tła elementów
COLOR_GROUPBOX_BG = "rgba(61, 47, 33, 0.8)"
COLOR_INPUT_BG = "rgba(26, 20, 16, 0.6)"
COLOR_CONSOLE_BG = "#0d0a08"

# Obramowania - miedziany metal
COLOR_BORDER = "rgba(184, 115, 51, 0.3)"
COLOR_BORDER_FOCUS = "rgba(184, 115, 51, 0.6)"
COLOR_BORDER_GLOW = "rgba(255, 140, 66, 0.4)"

# ===== CZCIONKI =====
FONT_FAMILY = "'Courier New', 'Monaco', 'Consolas', monospace"
FONT_MONO = "'Courier New', 'Monaco', monospace"

# Rozmiary
FONT_SIZE_HEADER = "26px"
FONT_SIZE_SUBTITLE = "14px"
FONT_SIZE_NORMAL = "14px"
FONT_SIZE_SMALL = "13px"
FONT_SIZE_TINY = "12px"

# ===== ZAOKRĄGLENIA =====
BORDER_RADIUS_LARGE = "4px"   # Ostre kąty, industrial
BORDER_RADIUS_MEDIUM = "3px"
BORDER_RADIUS_SMALL = "2px"

# ===== EFEKTY =====
GLOW_COLOR = "rgba(255, 140, 66, 0.6)"
SHADOW_COLOR = "rgba(0, 0, 0, 0.5)"

# ===== WARTOŚCI DOMYŚLNE =====
DEFAULT_BRIGHTNESS = 100
DEFAULT_NIGHT_BRIGHTNESS = 20
DEFAULT_DIM_START = "22:00"
DEFAULT_DIM_END = "08:00"
DEFAULT_OFF_TIME = "23:00"
DEFAULT_ON_TIME = "07:00"

# ===== SERIAL =====
DEFAULT_BAUD_RATE = 9600
PORT_REFRESH_INTERVAL = 2000
