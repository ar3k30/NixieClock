# Zegar Nixie Z5700M — Panel Sterowania

Aplikacja desktopowa macOS do sterowania zegarem z lampami Nixie Z5700M opartym na mikrokontrolerze ATMega328P.

![macOS](https://img.shields.io/badge/macOS-11.0+-black?logo=apple)
![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![PyQt6](https://img.shields.io/badge/PyQt6-6.6+-green)
![Arduino](https://img.shields.io/badge/Arduino-ATMega328P-teal?logo=arduino)

---

## ✨ Funkcje

- **Ustawianie czasu** — synchronizacja RTC DS3231 z poziomu aplikacji
- **Regulacja jasności** — płynna kontrola jasności lamp (0–100%)
- **Automatyczne ściemnianie** — nocna redukcja jasności w zadanym przedziale godzinowym
- **Harmonogram wyłączania** — automatyczne wygaszanie i włączanie zegara
- **Wgrywanie firmware** — wbudowany kod Arduino, wgrywany jednym przyciskiem bez Arduino IDE
- **Dwa motywy** — MODERN i VINTAGE, przełączane w locie
- **Log komunikacji** — podgląd wszystkich komend wysyłanych do zegara

---

## 🏗️ Architektura projektu

Projekt podzielony na moduły — każdy element można edytować niezależnie.

```
NixieClock/
├── main_unified.py       # Główna aplikacja, logika, składanie UI
├── serial_handler.py     # Komunikacja przez port szeregowy
├── firmware.py           # Kod Arduino wbudowany jako string
├── flasher.py            # Silnik kompilacji i wgrywania firmware
│
├── config.py             # Wymiary i kolory — motyw MODERN
├── styles.py             # Style CSS — motyw MODERN
├── widgets.py            # Sekcje UI — motyw MODERN
│
├── config_vintage.py     # Wymiary i kolory — motyw VINTAGE
├── styles_vintage.py     # Style CSS — motyw VINTAGE
├── widgets_vintage.py    # Sekcje UI — motyw VINTAGE
│
├── create_icon.py        # Generator ikony .icns
├── NixieClock.spec       # Konfiguracja PyInstaller
└── build.sh              # Skrypt budowania aplikacji .app
```

### Zasada modyfikacji

Chcesz zmienić **rozmiar okna lub pola**? → `config.py` / `config_vintage.py`  
Chcesz zmienić **kolory lub styl**? → `styles.py` / `styles_vintage.py`  
Chcesz zmienić **układ sekcji**? → `widgets.py` / `widgets_vintage.py`  
Chcesz zmienić **firmware**? → `firmware.py`

---

## 🔧 Wymagania

### Aplikacja (Python)
- macOS 11.0+
- Python 3.9+
- PyQt6, pyserial

### Wgrywanie firmware (opcjonalne)
```bash
brew install arduino-cli
```

### Sprzęt
- Zegar Nixie Z5700M z ATMega328P (TQFP)
- Kabel USB
- RTC DS3231

---

## 🚀 Instalacja i uruchomienie

### Ze źródeł

```bash
git clone https://github.com/twoj-nick/nixie-clock-control
cd nixie-clock-control

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python3 main_unified.py
```

### Budowanie aplikacji macOS (.app)

```bash
source venv/bin/activate
chmod +x build.sh
./build.sh
```

Gotowa aplikacja: `dist/Zegar Nixie Z5700M.app`

> **Pierwsze uruchomienie:** kliknij prawym → Otwórz → Otwórz  
> lub: System Settings → Privacy & Security → Open Anyway

---

## 📡 Protokół komunikacji

Komunikacja przez port szeregowy, 9600 baud:

| Komenda | Opis | Przykład |
|---------|------|---------|
| `SET_TIME:HH:MM:SS` | Ustawia czas | `SET_TIME:14:30:00` |
| `SET_BRIGHTNESS:N` | Jasność 0–100% | `SET_BRIGHTNESS:75` |
| `SET_DIM:HH:MM,HH:MM,N` | Ściemnianie nocne | `SET_DIM:22:00,08:00,20` |
| `DIM_DISABLE` | Wyłącza ściemnianie | — |
| `SET_SCHEDULE:HH:MM,HH:MM` | Harmonogram wyłączania | `SET_SCHEDULE:23:00,07:00` |
| `SCHEDULE_DISABLE` | Wyłącza harmonogram | — |
| `GET_STATUS` | Zwraca aktualny stan | — |

---

## 💾 Mapa pamięci EEPROM

| Adres | Zmienna | Opis |
|-------|---------|------|
| 0–1 | `timeON` | Jasność (10–4000 µs) |
| 2–3 | `separator` | Tryb separatora (0–4) |
| 4 | `dimEnabled` | Ściemnianie wł/wył |
| 5–8 | `dimStart/End` | Godziny ściemniania |
| 9 | `dimBrightness` | Jasność nocna |
| 10 | `schedEnabled` | Harmonogram wł/wył |
| 11–14 | `schedOff/On` | Godziny harmonogramu |

---

## 🛠️ Sterowanie ręczne (przyciski)

| Kombinacja | Akcja |
|------------|-------|
| MIDDLE | Zmiana trybu separatora (0–4) |
| MIDDLE + LEFT | Godzina +1 |
| MIDDLE + RIGHT | Minuta +1 |
| LEFT + RIGHT | Zmiana jasności |

---

## 📦 requirements.txt

```
PyQt6>=6.6.0
pyserial>=3.5
pyinstaller>=6.0
```

---

## 📄 Licencja

MIT License

---

*Projekt zbudowany dla lamp Nixie Z5730M i ATMega328P w obudowie TQFP.*
