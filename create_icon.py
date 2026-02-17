#!/usr/bin/env python3
"""
Generator ikony dla Nixie Clock Control
Tworzy ikonę w stylu lampy Nixie - ciemne tło, pomarańczowa cyfra z poświatą
Uruchom: python create_icon.py
"""

import os
import struct
import zlib


def create_nixie_icon_png(size):
    """Rysuje ikonę Nixie ręcznie (bez Pillow) jako PNG"""
    import math
    
    # Tworzenie tablicy pikseli RGBA
    pixels = []
    
    cx, cy = size // 2, size // 2
    radius = size // 2 - 2
    
    for y in range(size):
        row = []
        for x in range(size):
            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx*dx + dy*dy)
            
            # Poza okręgiem - przezroczysty
            if dist > radius:
                row.extend([0, 0, 0, 0])
                continue
            
            # Normalizacja do -1..1
            nx = dx / radius
            ny = dy / radius
            
            # === TŁO - ciemny brąz z gradientem ===
            bg_r = int(20 + 10 * (1 - dist / radius))
            bg_g = int(12 + 6 * (1 - dist / radius))
            bg_b = int(8 + 4 * (1 - dist / radius))
            
            # === POŚWIATA - pomarańczowa w centrum ===
            glow = max(0, 1 - (dist / (radius * 0.7)))
            glow_r = int(180 * glow * glow)
            glow_g = int(80 * glow * glow)
            glow_b = int(10 * glow * glow)
            
            # === OBWÓDKA lampy ===
            rim = 1 if (dist > radius - size * 0.04) else 0
            rim_r = int(184 * rim)
            rim_g = int(115 * rim)
            rim_b = int(51 * rim)
            
            # Łączenie warstw
            r = min(255, bg_r + glow_r + rim_r)
            g = min(255, bg_g + glow_g + rim_g)
            b = min(255, bg_b + glow_b + rim_b)
            
            # === CYFRA "N" ===
            # Skalowanie do rozmiaru ikony
            s = size / 128.0
            
            # Prostokąt cyfry: 35-93 x, 28-100 y (dla 128px)
            fx = x / s
            fy = y / s
            
            in_digit = False
            
            if 35 <= fx <= 93 and 28 <= fy <= 100:
                # Lewa pionowa kreska
                if 35 <= fx <= 50:
                    in_digit = True
                # Prawa pionowa kreska
                elif 78 <= fx <= 93:
                    in_digit = True
                # Ukośna kreska N
                elif 50 <= fx <= 78:
                    # Linia z (50,28) do (78,100)
                    expected_y = 28 + (fx - 50) * (100 - 28) / (78 - 50)
                    if abs(fy - expected_y) <= 7:
                        in_digit = True
            
            if in_digit:
                # Pomarańczowa cyfra z poświatą
                digit_r = 255
                digit_g = 160
                digit_b = 30
                alpha = 255
                row.extend([digit_r, digit_g, digit_b, alpha])
            else:
                # Miękka krawędź okręgu
                edge_alpha = 255
                if dist > radius - 2:
                    edge_alpha = int(255 * (radius - dist) / 2)
                row.extend([r, g, b, edge_alpha])
        
        pixels.append(row)
    
    return pixels_to_png(pixels, size)


def pixels_to_png(pixels, size):
    """Konwertuje tablicę pikseli RGBA na bajty PNG"""
    
    def png_chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    
    # PNG signature
    signature = b'\x89PNG\r\n\x1a\n'
    
    # IHDR
    ihdr_data = struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0)
    # Bit depth=8, color type=6 (RGBA), compression=0, filter=0, interlace=0
    ihdr_data = struct.pack('>II', size, size) + bytes([8, 6, 0, 0, 0])
    ihdr = png_chunk(b'IHDR', ihdr_data)
    
    # IDAT
    raw_data = b''
    for row in pixels:
        raw_data += b'\x00'  # filter type None
        raw_data += bytes(row)
    
    compressed = zlib.compress(raw_data, 9)
    idat = png_chunk(b'IDAT', compressed)
    
    # IEND
    iend = png_chunk(b'IEND', b'')
    
    return signature + ihdr + idat + iend


def write_png(filename, size):
    """Zapisuje plik PNG"""
    png_data = create_nixie_icon_png(size)
    with open(filename, 'wb') as f:
        f.write(png_data)
    print(f"  ✓ {filename} ({size}x{size})")


def create_iconset():
    """Tworzy iconset z wymaganymi rozmiarami macOS"""
    
    iconset_dir = "NixieClock.iconset"
    os.makedirs(iconset_dir, exist_ok=True)
    
    print("🎨 Generowanie ikon Nixie...")
    
    # Wymagane rozmiary przez macOS
    sizes = [
        (16, "icon_16x16.png"),
        (32, "icon_16x16@2x.png"),
        (32, "icon_32x32.png"),
        (64, "icon_32x32@2x.png"),
        (128, "icon_128x128.png"),
        (256, "icon_128x128@2x.png"),
        (256, "icon_256x256.png"),
        (512, "icon_256x256@2x.png"),
        (512, "icon_512x512.png"),
        (1024, "icon_512x512@2x.png"),
    ]
    
    for size, filename in sizes:
        write_png(os.path.join(iconset_dir, filename), size)
    
    print("\n🔧 Konwersja do .icns...")
    
    result = os.system(f"iconutil -c icns {iconset_dir} -o NixieClock.icns")
    
    if result == 0:
        print("  ✓ NixieClock.icns gotowy!")
        os.system(f"rm -rf {iconset_dir}")
    else:
        print("  ✗ Błąd iconutil - sprawdź czy masz macOS")
        print("  Iconset zapisany w:", iconset_dir)
    
    return result == 0


if __name__ == "__main__":
    print("=" * 50)
    print("  NIXIE CLOCK - Generator Ikony")
    print("=" * 50)
    
    success = create_iconset()
    
    if success:
        print("\n✅ Ikona NixieClock.icns gotowa!")
        print("   Uruchom teraz: ./build.sh")
    else:
        print("\n⚠️  Sprawdź czy jesteś na macOS")
