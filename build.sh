#!/bin/bash
# ==============================================
# NIXIE CLOCK - Skrypt budowania aplikacji macOS
# Uruchom: chmod +x build.sh && ./build.sh
# ==============================================

set -e
echo ""
echo "================================================"
echo "   NIXIE CLOCK - Budowanie aplikacji macOS"
echo "================================================"
echo ""

# Sprawdź czy wszystkie pliki są na miejscu
REQUIRED=(
    "main_unified.py"
    "serial_handler.py"
    "firmware.py"
    "flasher.py"
    "config.py"
    "styles.py"
    "widgets.py"
    "config_vintage.py"
    "styles_vintage.py"
    "widgets_vintage.py"
)

echo "Sprawdzam pliki..."
MISSING=0
for f in "${REQUIRED[@]}"; do
    if [ ! -f "$f" ]; then
        echo "  ✗ Brak: $f"
        MISSING=1
    else
        echo "  ✓ $f"
    fi
done

if [ $MISSING -eq 1 ]; then
    echo ""
    echo "❌ Brakuje plików. Pobierz wszystkie pliki z aplikacji."
    exit 1
fi

echo ""

# Aktywuj venv
if [[ "$VIRTUAL_ENV" == "" ]]; then
    if [ -d "venv" ]; then
        echo "Aktywuję venv..."
        source venv/bin/activate
    else
        echo "Tworzę venv..."
        python3 -m venv venv
        source venv/bin/activate
    fi
fi

echo "✓ Python: $(python3 --version)"
echo ""

# Zainstaluj zależności
echo "📦 Instalacja zależności..."
pip install pyserial PyQt6 pyinstaller --quiet
echo "✓ Zależności OK"
echo ""

# Generuj ikonę
echo "🎨 Generowanie ikony..."
python3 create_icon.py
echo ""

# Wyczyść poprzedni build
echo "🧹 Czyszczenie..."
rm -rf build dist __pycache__
echo "✓ OK"
echo ""

# Build
echo "🔨 Budowanie .app..."
echo "   (może potrwać 2-3 minuty)"
echo ""
pyinstaller NixieClock.spec --noconfirm

echo ""
APP_PATH="dist/Zegar Nixie Z5700M.app"

if [ -d "$APP_PATH" ]; then
    SIZE=$(du -sh "$APP_PATH" | cut -f1)
    echo "================================================"
    echo "✅ SUKCES!"
    echo "   Rozmiar: $SIZE"
    echo "   Lokalizacja: $APP_PATH"
    echo "================================================"
    echo ""
    echo "INSTALACJA:"
    echo ""
    echo "  Opcja 1 - przeciągnij do Applications:"
    echo "   cp -r \"dist/Zegar Nixie Z5700M.app\" /Applications/"
    echo ""
    echo "  Opcja 2 - otwórz teraz:"
    echo "   open \"dist/Zegar Nixie Z5700M.app\""
    echo ""
    echo "⚠️  Pierwsze uruchomienie (nieznany developer):"
    echo "   Kliknij prawym → Otwórz → Otwórz"
    echo "   LUB: System Settings → Privacy → Open Anyway"
    echo ""

    read -p "Otworzyć folder dist/? [t/N] " -n 1 -r; echo
    if [[ $REPLY =~ ^[Tt]$ ]]; then open dist/; fi

    read -p "Zainstalować w /Applications/? [t/N] " -n 1 -r; echo
    if [[ $REPLY =~ ^[Tt]$ ]]; then
        cp -r "$APP_PATH" /Applications/
        echo "✅ Zainstalowano! Szukaj w Launchpadzie."
    fi
else
    echo "❌ Build nie powiódł się. Sprawdź błędy powyżej."
    exit 1
fi
