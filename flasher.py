"""
flasher.py - Wgrywanie firmware do zegara Nixie
Używa arduino-cli do kompilacji i wgrywania bez Arduino IDE

Wymagania (instalowane automatycznie):
- arduino-cli (przez Homebrew lub bezpośrednio)
- MiniCore board package (dla ATMega328P standalone)
"""

import os
import sys
import subprocess
import tempfile
import shutil
import threading
from firmware import FIRMWARE_SOURCE, FIRMWARE_VERSION, BOARD_FQBN, UPLOAD_BAUD


class Flasher:
    """Obsługuje kompilację i wgrywanie firmware"""

    ARDUINO_CLI_PATH = None  # Cache znalezionej ścieżki

    def __init__(self, log_callback=None, progress_callback=None):
        """
        log_callback(str)      - funkcja do logowania wiadomości
        progress_callback(int) - funkcja do raportowania postępu 0-100
        """
        self.log = log_callback or print
        self.progress = progress_callback or (lambda x: None)

    # ================================================================
    # GŁÓWNA FUNKCJA - wywoływana przez przycisk w GUI
    # ================================================================
    def flash(self, port, done_callback=None):
        """Uruchamia wgrywanie w osobnym wątku (nie blokuje GUI)"""
        thread = threading.Thread(
            target=self._flash_thread,
            args=(port, done_callback),
            daemon=True
        )
        thread.start()

    def _flash_thread(self, port, done_callback):
        """Cały proces wgrywania w wątku"""
        success = False
        try:
            self.log("=== Rozpoczynam wgrywanie firmware ===")
            self.log(f"Firmware v{FIRMWARE_VERSION}")
            self.log(f"Port: {port}")
            self.log(f"Płytka: {BOARD_FQBN}")

            # 1. Znajdź lub zainstaluj arduino-cli
            self.progress(5)
            cli = self._get_arduino_cli()
            if not cli:
                self.log("BŁĄD: Nie można znaleźć arduino-cli")
                self.log("Zainstaluj: brew install arduino-cli")
                return

            # 2. Sprawdź/zainstaluj MiniCore
            self.progress(20)
            if not self._ensure_minicore(cli):
                self.log("BŁĄD: Nie można zainstalować MiniCore")
                return

            # 3. Zapisz firmware do pliku tymczasowego
            self.progress(40)
            sketch_dir = self._write_temp_sketch()
            if not sketch_dir:
                self.log("BŁĄD: Nie można zapisać firmware")
                return

            # 4. Kompiluj
            self.progress(50)
            self.log("Kompilowanie...")
            build_dir = os.path.join(tempfile.gettempdir(), "nixie_build")
            os.makedirs(build_dir, exist_ok=True)

            compile_cmd = [
                cli, "compile",
                "--fqbn", BOARD_FQBN,
                "--build-path", build_dir,
                sketch_dir
            ]
            result = self._run(compile_cmd)
            if result.returncode != 0:
                self.log("BŁĄD KOMPILACJI:")
                self.log(result.stderr[-500:] if result.stderr else "brak szczegółów")
                return

            self.log("Kompilacja OK")
            self.progress(75)

            # 5. Wgraj
            self.log(f"Wgrywanie na port {port}...")
            hex_file = os.path.join(build_dir, "NixieClock.ino.hex")

            upload_cmd = [
                cli, "upload",
                "--fqbn", BOARD_FQBN,
                "--port", port,
                "--input-file", hex_file
            ]
            result = self._run(upload_cmd)
            if result.returncode != 0:
                self.log("BŁĄD WGRYWANIA:")
                self.log(result.stderr[-500:] if result.stderr else "brak szczegółów")
                return

            self.progress(100)
            self.log("=== FIRMWARE WGRANY POMYŚLNIE ===")
            self.log("Zegar uruchomi się za chwilę...")
            success = True

        except Exception as e:
            self.log(f"BŁĄD: {str(e)}")
        finally:
            # Sprzątanie
            try:
                if 'sketch_dir' in locals() and sketch_dir:
                    shutil.rmtree(sketch_dir, ignore_errors=True)
            except:
                pass

            if done_callback:
                done_callback(success)

    # ================================================================
    # ARDUINO-CLI
    # ================================================================
    def _get_arduino_cli(self):
        """Szuka arduino-cli w typowych lokalizacjach"""

        if Flasher.ARDUINO_CLI_PATH:
            return Flasher.ARDUINO_CLI_PATH

        # Sprawdź znane ścieżki
        candidates = [
            "arduino-cli",                              # w PATH
            "/usr/local/bin/arduino-cli",               # Homebrew Intel
            "/opt/homebrew/bin/arduino-cli",            # Homebrew Apple Silicon
            os.path.expanduser("~/bin/arduino-cli"),    # lokalny
        ]

        for path in candidates:
            try:
                result = subprocess.run(
                    [path, "version"],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    self.log(f"arduino-cli: {result.stdout.strip()}")
                    Flasher.ARDUINO_CLI_PATH = path
                    return path
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue

        self.log("Nie znaleziono arduino-cli")
        self.log("Instalacja: brew install arduino-cli")
        return None

    def _ensure_minicore(self, cli):
        """Sprawdza czy MiniCore jest zainstalowany, jeśli nie - instaluje"""

        self.log("Sprawdzam MiniCore board package...")

        # Sprawdź czy już jest
        result = self._run([cli, "board", "listall", "MiniCore"])
        if "MiniCore" in (result.stdout or ""):
            self.log("MiniCore: OK")
            return True

        # Dodaj URL i zainstaluj
        self.log("Instaluję MiniCore (może potrwać ~1 min)...")

        minicore_url = "https://mcudude.github.io/MiniCore/package_MiniCore_index.json"

        # Dodaj URL do konfiguracji
        self._run([cli, "config", "add", "board_manager.additional_urls", minicore_url])

        # Aktualizuj indeks
        self._run([cli, "core", "update-index"])

        # Zainstaluj MiniCore
        result = self._run([cli, "core", "install", "MiniCore:avr"])
        if result.returncode == 0:
            self.log("MiniCore zainstalowany")
            return True

        # Sprawdź czy teraz jest
        result = self._run([cli, "board", "listall", "MiniCore"])
        if "MiniCore" in (result.stdout or ""):
            self.log("MiniCore: OK")
            return True

        self.log("Nie udało się zainstalować MiniCore")
        return False

    def _write_temp_sketch(self):
        """Zapisuje firmware do katalogu tymczasowego"""
        try:
            sketch_dir = os.path.join(tempfile.gettempdir(), "NixieClock")
            os.makedirs(sketch_dir, exist_ok=True)

            sketch_path = os.path.join(sketch_dir, "NixieClock.ino")
            with open(sketch_path, "w", encoding="utf-8") as f:
                f.write(FIRMWARE_SOURCE)

            self.log(f"Firmware zapisany ({len(FIRMWARE_SOURCE)} bajtów)")
            return sketch_dir
        except Exception as e:
            self.log(f"Błąd zapisu: {e}")
            return None

    def _run(self, cmd, timeout=120):
        """Uruchamia komendę i zwraca wynik"""
        try:
            return subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
        except subprocess.TimeoutExpired:
            self.log(f"Timeout: {' '.join(cmd[:3])}")
            result = type('obj', (object,), {'returncode': 1, 'stdout': '', 'stderr': 'Timeout'})()
            return result
        except Exception as e:
            result = type('obj', (object,), {'returncode': 1, 'stdout': '', 'stderr': str(e)})()
            return result

    @staticmethod
    def is_arduino_cli_available():
        """Szybkie sprawdzenie czy arduino-cli jest dostępne"""
        candidates = [
            "arduino-cli",
            "/usr/local/bin/arduino-cli",
            "/opt/homebrew/bin/arduino-cli",
        ]
        for path in candidates:
            try:
                r = subprocess.run([path, "version"], capture_output=True, timeout=3)
                if r.returncode == 0:
                    return True
            except:
                continue
        return False
