#!/usr/bin/env python3
"""
Nixie Clock Control - UNIFIED EDITION
Przełączanie między MODERN i VINTAGE style

Przycisk w headerze przełącza style w locie
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPalette, QColor

from serial_handler import SerialHandler


class NixieClockControl(QMainWindow):
    def __init__(self):
        super().__init__()
        self.serial_handler = SerialHandler()
        self.current_style = "vintage"  # Domyślnie vintage
        
        # Załaduj odpowiednie moduły
        self.load_style_modules()
        
        # Utworzenie sekcji
        self.create_sections()
        
        self.init_ui()
        self.setup_connections()
        self.refresh_ports()
        
        # Auto-refresh portów
        self.port_timer = QTimer()
        self.port_timer.timeout.connect(self.refresh_ports)
        self.port_timer.start(2000)
        
    def load_style_modules(self):
        """Ładowanie modułów stylu"""
        if self.current_style == "vintage":
            import config_vintage as cfg
            import styles_vintage as sty
            import widgets_vintage as wdg
            self.config = cfg
            self.styles = sty
            self.widgets = wdg
        else:  # modern
            import config as cfg
            import styles as sty
            import widgets as wdg
            self.config = cfg
            self.styles = sty
            self.widgets = wdg
            
    def create_sections(self):
        """Tworzenie sekcji z odpowiednich modułów"""
        self.connection_section = self.widgets.ConnectionSection()
        self.time_section = self.widgets.TimeSection()
        self.brightness_section = self.widgets.BrightnessSection()
        self.dimming_section = self.widgets.DimmingSection()
        self.schedule_section = self.widgets.ScheduleSection()
        self.console_section = self.widgets.ConsoleSection()
        
    def init_ui(self):
        title = "Zegar Nixie Z5700M" if self.current_style == "vintage" else "Sterowanie Zegarem Nixie"
        self.setWindowTitle(title)
        self.setFixedSize(self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT)
        
        # Główny widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(self.config.SECTION_SPACING)
        main_layout.setContentsMargins(
            self.config.WINDOW_MARGIN, self.config.WINDOW_MARGIN, 
            self.config.WINDOW_MARGIN, self.config.WINDOW_MARGIN
        )
        
        # Header z przyciskiem przełączania
        header_container = QHBoxLayout()
        
        header_text = "ZEGAR NIXIE Z5700M" if self.current_style == "vintage" else "Sterowanie Zegarem Nixie"
        header = QLabel(header_text)
        header.setStyleSheet(self.styles.STYLE_LABEL_HEADER)
        if self.current_style == "vintage":
            header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_container.addWidget(header)
        
        header_container.addStretch()
        
        # Przycisk przełączania stylu
        switch_text = "🎨 MODERN" if self.current_style == "vintage" else "🔥 RETRO"
        self.style_switch_btn = QPushButton(switch_text)
        self.style_switch_btn.setMinimumHeight(36)
        self.style_switch_btn.setMaximumWidth(140)
        self.style_switch_btn.clicked.connect(self.switch_style)
        header_container.addWidget(self.style_switch_btn)
        
        main_layout.addLayout(header_container)
        
        subtitle_text = "Panel sterowania i konfiguracji" if self.current_style == "vintage" else "Konfiguracja i harmonogram wyświetlacza"
        subtitle = QLabel(subtitle_text)
        subtitle.setStyleSheet(self.styles.STYLE_LABEL_SUBTITLE)
        if self.current_style == "vintage":
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
        
        # Zastosowanie theme
        self.apply_theme()
        
    def switch_style(self):
        """Przełączanie stylu"""
        # Zapisz aktualny stan
        was_connected = self.serial_handler.is_connected()
        current_port = self.connection_section.port_combo.currentText() if hasattr(self.connection_section, 'port_combo') else None
        
        # Przełącz styl
        self.current_style = "modern" if self.current_style == "vintage" else "vintage"
        
        # Rozłącz serial
        if was_connected:
            self.serial_handler.disconnect()
        
        # Zatrzymaj timer
        self.port_timer.stop()
        
        # Usuń stary central widget
        old_widget = self.centralWidget()
        if old_widget:
            old_widget.deleteLater()
        
        # Przeładuj moduły
        self.reload_modules()
        self.load_style_modules()
        
        # Utwórz nowe sekcje
        self.create_sections()
        
        # Przebuduj UI
        self.init_ui()
        self.setup_connections()
        
        # Przywróć porty
        self.refresh_ports()
        if current_port:
            self.connection_section.port_combo.setCurrentText(current_port)
        
        # Restart timer
        self.port_timer.start(2000)
        
        self.log(f"=== PRZEŁĄCZONO NA {self.current_style.upper()} ===")
        
    def reload_modules(self):
        """Przeładowanie modułów Pythona"""
        import importlib
        
        if self.current_style == "vintage":
            import config_vintage, styles_vintage, widgets_vintage
            importlib.reload(config_vintage)
            importlib.reload(styles_vintage)
            importlib.reload(widgets_vintage)
        else:
            import config, styles, widgets
            importlib.reload(config)
            importlib.reload(styles)
            importlib.reload(widgets)
        
    def setup_connections(self):
        """Połączenia sygnałów i slotów"""
        self.connection_section.connect_btn.clicked.connect(self.toggle_connection)
        self.connection_section.flash_btn.clicked.connect(self.flash_firmware)
        self.time_section.set_time_btn.clicked.connect(self.set_time)
        self.brightness_section.brightness_slider.valueChanged.connect(self.on_brightness_changed)
        self.dimming_section.night_brightness_slider.valueChanged.connect(self.on_night_brightness_changed)
        self.dimming_section.dim_enabled.stateChanged.connect(self.toggle_dimming)
        self.dimming_section.dim_start_time.timeChanged.connect(self.on_dim_schedule_changed)
        self.dimming_section.dim_end_time.timeChanged.connect(self.on_dim_schedule_changed)
        self.schedule_section.schedule_enabled.stateChanged.connect(self.toggle_schedule)
        self.schedule_section.off_time.timeChanged.connect(self.on_schedule_changed)
        self.schedule_section.on_time.timeChanged.connect(self.on_schedule_changed)

    def flash_firmware(self):
        """Wgrywanie firmware do zegara"""
        from flasher import Flasher

        port = self.connection_section.port_combo.currentText()
        if not port:
            self.log("BŁĄD: Wybierz port szeregowy")
            return

        # Rozłącz serial przed wgrywaniem
        was_connected = self.serial_handler.is_connected()
        if was_connected:
            self.serial_handler.disconnect()
            self.log("Rozłączono serial przed wgrywaniem")

        # Zablokuj przyciski na czas wgrywania
        self.connection_section.flash_btn.setEnabled(False)
        self.connection_section.connect_btn.setEnabled(False)
        self.connection_section.flash_progress.setValue(0)
        self.connection_section.flash_progress.show()

        def on_progress(value):
            self.connection_section.flash_progress.setValue(value)

        def on_done(success):
            # Przywróć przyciski (musi być w wątku GUI)
            from PyQt6.QtCore import QMetaObject, Qt
            QMetaObject.invokeMethod(
                self,
                "_flash_done",
                Qt.ConnectionType.QueuedConnection,
            )

        flasher = Flasher(
            log_callback=self.log,
            progress_callback=on_progress
        )
        flasher.flash(port, done_callback=on_done)

    def _flash_done(self):
        """Wywoływane po zakończeniu wgrywania (w wątku GUI)"""
        self.connection_section.flash_btn.setEnabled(True)
        self.connection_section.connect_btn.setEnabled(True)
        # Schowaj pasek po 3 sekundach
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(3000, self.connection_section.flash_progress.hide)
        
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
            btn_text = "POŁĄCZ" if self.current_style == "vintage" else "Połącz"
            status_text = "◉ NIEPOŁĄCZONY" if self.current_style == "vintage" else "● Niepołączony"
            self.connection_section.connect_btn.setText(btn_text)
            self.connection_section.status_label.setText(status_text)
            self.connection_section.status_label.setStyleSheet(self.styles.STYLE_LABEL_STATUS_DISCONNECTED)
            self.set_controls_enabled(False)
            log_msg = "=== ROZŁĄCZONO ===" if self.current_style == "vintage" else "Rozłączono"
            self.log(log_msg)
        else:
            port = self.connection_section.port_combo.currentText()
            if self.serial_handler.connect(port):
                btn_text = "ROZŁĄCZ" if self.current_style == "vintage" else "Rozłącz"
                status_text = "◉ POŁĄCZONO" if self.current_style == "vintage" else "● Połączono"
                self.connection_section.connect_btn.setText(btn_text)
                self.connection_section.status_label.setText(status_text)
                self.connection_section.status_label.setStyleSheet(self.styles.STYLE_LABEL_STATUS_CONNECTED)
                self.set_controls_enabled(True)
                log_msg = f"=== POŁĄCZONO Z {port} ===" if self.current_style == "vintage" else f"Połączono z {port}"
                self.log(log_msg)
            else:
                log_msg = f"!!! BŁĄD POŁĄCZENIA Z {port} !!!" if self.current_style == "vintage" else f"Błąd połączenia z {port}"
                self.log(log_msg)
                
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
            log_msg = f">> USTAWIONO CZAS: {time_str}" if self.current_style == "vintage" else f"Ustawiono czas: {time_str}"
            self.log(log_msg)
        else:
            log_msg = "!! BŁĄD WYSYŁANIA KOMENDY CZASU" if self.current_style == "vintage" else "Błąd wysyłania komendy czasu"
            self.log(log_msg)
            
    def on_brightness_changed(self, value):
        """Zmiana jasności dziennej"""
        self.brightness_section.brightness_value.setText(f"{value}%")
        if self.serial_handler.is_connected():
            self.serial_handler.send_command(f"SET_BRIGHTNESS:{value}")
            log_msg = f">> JASNOŚĆ: {value}%" if self.current_style == "vintage" else f"Jasność: {value}%"
            self.log(log_msg)
            
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
                log_msg = ">> WŁĄCZONO AUTOMATYCZNE ŚCIEMNIANIE" if self.current_style == "vintage" else "Włączono automatyczne ściemnianie"
                self.log(log_msg)
            else:
                self.serial_handler.send_command("DIM_DISABLE")
                log_msg = ">> WYŁĄCZONO AUTOMATYCZNE ŚCIEMNIANIE" if self.current_style == "vintage" else "Wyłączono automatyczne ściemnianie"
                self.log(log_msg)
                
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
            if self.current_style == "vintage":
                self.log(f">> ŚCIEMNIANIE: {start}-{end}, JASNOŚĆ {brightness}%")
            else:
                self.log(f"Ściemnianie: {start}-{end}, jasność {brightness}%")
            
    def toggle_schedule(self, state):
        """Włączanie/wyłączanie harmonogramu"""
        enabled = state == Qt.CheckState.Checked.value
        
        if self.serial_handler.is_connected():
            if enabled:
                self.send_schedule_settings()
                log_msg = ">> WŁĄCZONO HARMONOGRAM WYŁĄCZANIA" if self.current_style == "vintage" else "Włączono harmonogram wyłączania"
                self.log(log_msg)
            else:
                self.serial_handler.send_command("SCHEDULE_DISABLE")
                log_msg = ">> WYŁĄCZONO HARMONOGRAM WYŁĄCZANIA" if self.current_style == "vintage" else "Wyłączono harmonogram wyłączania"
                self.log(log_msg)
                
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
            if self.current_style == "vintage":
                self.log(f">> HARMONOGRAM: WYŁĄCZ {off}, WŁĄCZ {on}")
            else:
                self.log(f"Harmonogram: wyłącz {off}, włącz {on}")
            
    def log(self, message):
        """Dodanie wpisu do logu"""
        from datetime import datetime
        if self.current_style == "vintage":
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.console_section.console.append(f"[{timestamp}] {message}")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.console_section.console.append(f"{timestamp} - {message}")
        
    def apply_theme(self):
        """Zastosowanie theme"""
        app = QApplication.instance()
        app.setStyle("Fusion")
        
        if self.current_style == "vintage":
            # Vintage palette
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
        else:
            # Modern palette
            dark_palette = QPalette()
            dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
            dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
            dark_palette.setColor(QPalette.ColorRole.Base, QColor(20, 20, 20))
            dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(40, 40, 40))
            dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
            dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
            dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
            dark_palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
            dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
            dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
            dark_palette.setColor(QPalette.ColorRole.Link, QColor(10, 132, 255))
            dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(10, 132, 255))
            dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        app.setPalette(dark_palette)
        self.setStyleSheet(self.styles.get_complete_stylesheet())
        
    def closeEvent(self, event):
        """Obsługa zamknięcia aplikacji"""
        if self.serial_handler.is_connected():
            self.serial_handler.disconnect()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Nixie Clock Control")
    
    window = NixieClockControl()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
