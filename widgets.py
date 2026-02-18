"""
Osobne widgety dla każdej sekcji - łatwo modyfikować bez ryzyka
Każda sekcja to osobna klasa
"""

from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QComboBox, QSlider, QCheckBox, 
    QTimeEdit, QTextEdit
)
from PyQt6.QtCore import Qt, QTime
from config import *
from styles import *


class ConnectionSection(QGroupBox):
    """Sekcja połączenia z portem szeregowym"""
    
    def __init__(self):
        super().__init__("Port szeregowy")
        self.init_ui()
        
    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(ELEMENT_SPACING)
        
        # ComboBox z portami
        self.port_combo = QComboBox()
        self.port_combo.setMinimumHeight(INPUT_HEIGHT)
        layout.addWidget(self.port_combo, 0, 0, 1, 2)
        
        # Przycisk połącz
        self.connect_btn = QPushButton("Połącz")
        self.connect_btn.setMinimumHeight(INPUT_HEIGHT)
        layout.addWidget(self.connect_btn, 0, 2)
        
        # Status LED
        self.status_label = QLabel("● Niepołączony")
        self.status_label.setStyleSheet(STYLE_LABEL_STATUS_DISCONNECTED)
        layout.addWidget(self.status_label, 1, 0, 1, 2)
        
        # Przycisk wgrywania firmware
        self.flash_btn = QPushButton("⬆ Wgraj firmware")
        self.flash_btn.setMinimumHeight(INPUT_HEIGHT)
        self.flash_btn.setToolTip("Wgrywa oprogramowanie do zegara przez USB\nWymaga arduino-cli: brew install arduino-cli")
        layout.addWidget(self.flash_btn, 1, 2)
        
        # Pasek postępu wgrywania (ukryty domyślnie)
        from PyQt6.QtWidgets import QProgressBar
        self.flash_progress = QProgressBar()
        self.flash_progress.setMinimumHeight(6)
        self.flash_progress.setMaximumHeight(6)
        self.flash_progress.setTextVisible(False)
        self.flash_progress.hide()
        layout.addWidget(self.flash_progress, 2, 0, 1, 3)
        
        self.setLayout(layout)


class TimeSection(QGroupBox):
    """Sekcja ustawiania czasu"""
    
    def __init__(self):
        super().__init__("Ustawienie czasu")
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(ELEMENT_SPACING)
        
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm:ss")
        self.time_edit.setTime(QTime.currentTime())
        self.time_edit.setMinimumHeight(INPUT_HEIGHT)
        self.time_edit.setFixedWidth(TIME_EDIT_FULL_WIDTH)
        layout.addWidget(self.time_edit)
        
        self.set_time_btn = QPushButton("Ustaw")
        self.set_time_btn.setMinimumHeight(INPUT_HEIGHT)
        self.set_time_btn.setFixedWidth(BUTTON_WIDTH)
        self.set_time_btn.setEnabled(False)
        layout.addWidget(self.set_time_btn)
        
        layout.addStretch()
        
        self.setLayout(layout)


class BrightnessSection(QGroupBox):
    """Sekcja jasności"""
    
    def __init__(self):
        super().__init__("Jasność")
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # Header z wartością
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Jasność dzienna"))
        self.brightness_value = QLabel(f"{DEFAULT_BRIGHTNESS}%")
        self.brightness_value.setStyleSheet(STYLE_LABEL_VALUE_BLUE)
        header_layout.addWidget(self.brightness_value)
        layout.addLayout(header_layout)
        
        # Slider
        self.brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setMinimum(0)
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(DEFAULT_BRIGHTNESS)
        self.brightness_slider.setEnabled(False)
        layout.addWidget(self.brightness_slider)
        
        self.setLayout(layout)


class DimmingSection(QGroupBox):
    """Sekcja automatycznego ściemniania"""
    
    def __init__(self):
        super().__init__("Automatyczne ściemnianie")
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(ELEMENT_SPACING)
        
        # Checkbox włączania
        self.dim_enabled = QCheckBox("Włącz automatyczne ściemnianie")
        self.dim_enabled.setEnabled(False)
        layout.addWidget(self.dim_enabled)
        
        # Slider jasności nocnej
        night_header = QHBoxLayout()
        night_header.addWidget(QLabel("Jasność nocna"))
        self.night_brightness_value = QLabel(f"{DEFAULT_NIGHT_BRIGHTNESS}%")
        self.night_brightness_value.setStyleSheet(STYLE_LABEL_VALUE_ORANGE)
        night_header.addWidget(self.night_brightness_value)
        layout.addLayout(night_header)
        
        self.night_brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.night_brightness_slider.setMinimum(0)
        self.night_brightness_slider.setMaximum(100)
        self.night_brightness_slider.setValue(DEFAULT_NIGHT_BRIGHTNESS)
        self.night_brightness_slider.setEnabled(False)
        layout.addWidget(self.night_brightness_slider)
        
        # Czas - obok siebie
        time_layout = QHBoxLayout()
        time_layout.setSpacing(TIME_FIELDS_SPACING)
        time_layout.setContentsMargins(0, ELEMENT_SPACING, 0, 0)
        
        time_layout.addWidget(QLabel("Początek:"))
        self.dim_start_time = QTimeEdit()
        self.dim_start_time.setDisplayFormat("HH:mm")
        h, m = DEFAULT_DIM_START.split(":")
        self.dim_start_time.setTime(QTime(int(h), int(m)))
        self.dim_start_time.setMinimumHeight(INPUT_HEIGHT)
        self.dim_start_time.setFixedWidth(TIME_EDIT_WIDTH)
        time_layout.addWidget(self.dim_start_time)
        
        time_layout.addSpacing(TIME_FIELDS_SPACING)
        
        time_layout.addWidget(QLabel("Koniec:"))
        self.dim_end_time = QTimeEdit()
        self.dim_end_time.setDisplayFormat("HH:mm")
        h, m = DEFAULT_DIM_END.split(":")
        self.dim_end_time.setTime(QTime(int(h), int(m)))
        self.dim_end_time.setMinimumHeight(INPUT_HEIGHT)
        self.dim_end_time.setFixedWidth(TIME_EDIT_WIDTH)
        time_layout.addWidget(self.dim_end_time)
        
        time_layout.addStretch()
        
        layout.addLayout(time_layout)
        
        self.setLayout(layout)


class ScheduleSection(QGroupBox):
    """Sekcja harmonogramu wyłączania"""
    
    def __init__(self):
        super().__init__("Harmonogram wyłączania")
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(ELEMENT_SPACING)
        
        # Checkbox włączania
        self.schedule_enabled = QCheckBox("Włącz harmonogram wyłączania")
        self.schedule_enabled.setEnabled(False)
        layout.addWidget(self.schedule_enabled)
        
        # Pola czasu - obok siebie
        time_layout = QHBoxLayout()
        time_layout.setSpacing(TIME_FIELDS_SPACING)
        time_layout.setContentsMargins(0, ELEMENT_SPACING, 0, 0)
        
        time_layout.addWidget(QLabel("Wyłącz o:"))
        self.off_time = QTimeEdit()
        self.off_time.setDisplayFormat("HH:mm")
        h, m = DEFAULT_OFF_TIME.split(":")
        self.off_time.setTime(QTime(int(h), int(m)))
        self.off_time.setMinimumHeight(INPUT_HEIGHT)
        self.off_time.setFixedWidth(TIME_EDIT_WIDTH)
        time_layout.addWidget(self.off_time)
        
        time_layout.addSpacing(TIME_FIELDS_SPACING)
        
        time_layout.addWidget(QLabel("Włącz o:"))
        self.on_time = QTimeEdit()
        self.on_time.setDisplayFormat("HH:mm")
        h, m = DEFAULT_ON_TIME.split(":")
        self.on_time.setTime(QTime(int(h), int(m)))
        self.on_time.setMinimumHeight(INPUT_HEIGHT)
        self.on_time.setFixedWidth(TIME_EDIT_WIDTH)
        time_layout.addWidget(self.on_time)
        
        time_layout.addStretch()
        
        layout.addLayout(time_layout)
        
        self.setLayout(layout)


class ConsoleSection(QGroupBox):
    """Sekcja konsoli logów"""
    
    def __init__(self):
        super().__init__("Log komunikacji")
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMaximumHeight(CONSOLE_HEIGHT)
        self.console.setStyleSheet(STYLE_CONSOLE)
        layout.addWidget(self.console)
        
        self.setLayout(layout)
