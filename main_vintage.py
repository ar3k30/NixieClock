#!/usr/bin/env python3
"""
Nixie Clock Control - VINTAGE/STEAMPUNK Edition
Retro wygląd pasujący do lamp Nixie

Ciepłe kolory, metaliczne tekstury, pomarańczowe świecenie
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPalette, QColor

from config_vintage import *
from styles_vintage import *
from widgets_vintage import *
from serial_handler import SerialHandler


class NixieClockControl(QMainWindow):
    def __init__(self):
        super().__init__()
        self.serial_handler = SerialHandler()
        
        # Utworzenie sekcji vintage
        self.connection_section = ConnectionSection()
        self.time_section = TimeSection()
        self.brightness_section = BrightnessSection()
        self.dimming_section = DimmingSection()
        self.schedule_section = ScheduleSection()
        self.console_section = ConsoleSection()
        
        self.init_ui()
        self.setup_connections()
        self.refresh_ports()
        
        # Auto-refresh portów
        self.port_timer = QTimer()
        self.port_timer.timeout.connect(self.refresh_ports)
        self.port_timer.start(PORT_REFRESH_INTERVAL)
        
    def init_ui(self):
        self.setWindowTitle("Zegar Nixie Z5700M")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Główny widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(SECTION_SPACING)
        main_layout.setContentsMargins(
            WINDOW_MARGIN, WINDOW_MARGIN, 
            WINDOW_MARGIN, WINDOW_MARGIN
        )
        
        # Header - vintage style
        header = QLabel("ZEGAR NIXIE Z5700M")
        header.setStyleSheet(STYLE_LABEL_HEADER)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)
        
        subtitle = QLabel("Panel sterowania i konfiguracji")
        subtitle.setStyleSheet(STYLE_LABEL_SUBTITLE)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle)
        
        # Dodanie sekcji
        main_layout.addWidget(self.connection_section)
        main_layout.addWidget(self.time_section)
        main_layout.addWidget(self.brightness_section)
        main_layout.addWidget(self.dimming_section)
        main_layout.addWidget(self.schedule_section)
        main_layout.addWidget(self.console_section)
        
        main_layout.addStretch()
        
        # Zastosowanie vintage theme
        self.apply_vintage_theme()
        
    def setup_connections(self):
        """Połączenia sygnałów i slotów"""
        self.connection_section.connect_btn.clicked.connect(self.toggle_connection)
        self.time_section.set_time_btn.clicked.connect(self.set_time)
        self.brightness_section.brightness_slider.valueChanged.connect(self.on_brightness_changed)
        self.dimming_section.night_brightness_slider.valueChanged.connect(self.on_night_brightness_changed)
        self.dimming_section.dim_enabled.stateChanged.connect(self.toggle_dimming)
        self.dimming_section.dim_start_time.timeChanged.connect(self.on_dim_schedule_changed)
        self.dimming_section.dim_end_time.timeChanged.connect(self.on_dim_schedule_changed)
        self.schedule_section.schedule_enabled.stateChanged.connect(self.toggle_schedule)
        self.schedule_section.off_time.timeChanged.connect(self.on_schedule_changed)
        self.schedule_section.on_time.timeChanged.connect(self.on_schedule_changed)
        
    def refresh_ports(self):
        """Odświeżanie listy portów"""
        combo = self.connection_section.port_combo
        current = combo.currentText()
        ports = self.serial_handler.get_available_ports()
        
        combo.clear()
        combo.addItems(ports)
        
        if current in ports:
            combo.setCurrentText(current)
            
    def toggle_connection(self):
        """Przełączanie połączenia"""
        if self.serial_handler.is_connected():
            self.serial_handler.disconnect()
            self.connection_section.connect_btn.setText("POŁĄCZ")
            self.connection_section.status_label.setText("◉ NIEPOŁĄCZONY")
            self.connection_section.status_label.setStyleSheet(STYLE_LABEL_STATUS_DISCONNECTED)
            self.set_controls_enabled(False)
            self.log("=== ROZŁĄCZONO ===")
        else:
            port = self.connection_section.port_combo.currentText()
            if self.serial_handler.connect(port):
                self.connection_section.connect_btn.setText("ROZŁĄCZ")
                self.connection_section.status_label.setText("◉ POŁĄCZONO")
                self.connection_section.status_label.setStyleSheet(STYLE_LABEL_STATUS_CONNECTED)
                self.set_controls_enabled(True)
                self.log(f"=== POŁĄCZONO Z {port} ===")
            else:
                self.log(f"!!! BŁĄD POŁĄCZENIA Z {port} !!!")
                
    def set_controls_enabled(self, enabled):
        """Włączanie/wyłączanie kontrolek"""
        self.time_section.set_time_btn.setEnabled(enabled)
        self.brightness_section.brightness_slider.setEnabled(enabled)
        self.dimming_section.night_brightness_slider.setEnabled(enabled)
        self.dimming_section.dim_enabled.setEnabled(enabled)
        self.dimming_section.dim_start_time.setEnabled(enabled)
        self.dimming_section.dim_end_time.setEnabled(enabled)
        self.schedule_section.schedule_enabled.setEnabled(enabled)
        self.schedule_section.off_time.setEnabled(enabled)
        self.schedule_section.on_time.setEnabled(enabled)
        
    def set_time(self):
        """Ustawienie czasu na zegarku"""
        time = self.time_section.time_edit.time()
        time_str = time.toString("HH:mm:ss")
        
        if self.serial_handler.send_command(f"SET_TIME:{time_str}"):
            self.log(f">> USTAWIONO CZAS: {time_str}")
        else:
            self.log("!! BŁĄD WYSYŁANIA KOMENDY CZASU")
            
    def on_brightness_changed(self, value):
        """Zmiana jasności dziennej"""
        self.brightness_section.brightness_value.setText(f"{value}%")
        if self.serial_handler.is_connected():
            self.serial_handler.send_command(f"SET_BRIGHTNESS:{value}")
            self.log(f">> JASNOŚĆ: {value}%")
            
    def on_night_brightness_changed(self, value):
        """Zmiana jasności nocnej"""
        self.dimming_section.night_brightness_value.setText(f"{value}%")
        if self.serial_handler.is_connected() and self.dimming_section.dim_enabled.isChecked():
            self.send_dim_settings()
            
    def toggle_dimming(self, state):
        """Włączanie/wyłączanie ściemniania"""
        enabled = state == Qt.CheckState.Checked.value
        
        if self.serial_handler.is_connected():
            if enabled:
                self.send_dim_settings()
                self.log(">> WŁĄCZONO AUTOMATYCZNE ŚCIEMNIANIE")
            else:
                self.serial_handler.send_command("DIM_DISABLE")
                self.log(">> WYŁĄCZONO AUTOMATYCZNE ŚCIEMNIANIE")
                
    def on_dim_schedule_changed(self):
        """Zmiana harmonogramu ściemniania"""
        if self.serial_handler.is_connected() and self.dimming_section.dim_enabled.isChecked():
            self.send_dim_settings()
            
    def send_dim_settings(self):
        """Wysłanie wszystkich ustawień ściemniania"""
        start = self.dimming_section.dim_start_time.time().toString("HH:mm")
        end = self.dimming_section.dim_end_time.time().toString("HH:mm")
        brightness = self.dimming_section.night_brightness_slider.value()
        
        cmd = f"SET_DIM:{start},{end},{brightness}"
        if self.serial_handler.send_command(cmd):
            self.log(f">> ŚCIEMNIANIE: {start}-{end}, JASNOŚĆ {brightness}%")
            
    def toggle_schedule(self, state):
        """Włączanie/wyłączanie harmonogramu"""
        enabled = state == Qt.CheckState.Checked.value
        
        if self.serial_handler.is_connected():
            if enabled:
                self.send_schedule_settings()
                self.log(">> WŁĄCZONO HARMONOGRAM WYŁĄCZANIA")
            else:
                self.serial_handler.send_command("SCHEDULE_DISABLE")
                self.log(">> WYŁĄCZONO HARMONOGRAM WYŁĄCZANIA")
                
    def on_schedule_changed(self):
        """Zmiana harmonogramu wyłączania"""
        if self.serial_handler.is_connected() and self.schedule_section.schedule_enabled.isChecked():
            self.send_schedule_settings()
            
    def send_schedule_settings(self):
        """Wysłanie ustawień harmonogramu"""
        off = self.schedule_section.off_time.time().toString("HH:mm")
        on = self.schedule_section.on_time.time().toString("HH:mm")
        
        cmd = f"SET_SCHEDULE:{off},{on}"
        if self.serial_handler.send_command(cmd):
            self.log(f">> HARMONOGRAM: WYŁĄCZ {off}, WŁĄCZ {on}")
            
    def log(self, message):
        """Dodanie wpisu do logu - vintage style"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console_section.console.append(f"[{timestamp}] {message}")
        
    def apply_vintage_theme(self):
        """Zastosowanie vintage/steampunk theme"""
        app = QApplication.instance()
        app.setStyle("Fusion")
        
        # Ciemna paleta z ciepłymi tonami
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(26, 20, 16))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(245, 222, 179))
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(13, 10, 8))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 35, 24))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(245, 222, 179))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(26, 20, 16))
        dark_palette.setColor(QPalette.ColorRole.Text, QColor(245, 222, 179))
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(61, 47, 33))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(245, 222, 179))
        dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 140, 66))
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(255, 140, 66))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(184, 115, 51))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(26, 20, 16))
        
        app.setPalette(dark_palette)
        
        # Zastosowanie vintage stylesheet
        self.setStyleSheet(get_complete_stylesheet())
        
    def closeEvent(self, event):
        """Obsługa zamknięcia aplikacji"""
        if self.serial_handler.is_connected():
            self.serial_handler.disconnect()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Nixie Clock Z5700M - Vintage Edition")
    
    window = NixieClockControl()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
