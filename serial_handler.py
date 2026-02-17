"""
Serial Handler - obsługa komunikacji z zegarem Nixie
"""

import serial
import serial.tools.list_ports
from typing import List, Optional


class SerialHandler:
    def __init__(self):
        self.connection: Optional[serial.Serial] = None
        self.port: Optional[str] = None
        
    def get_available_ports(self) -> List[str]:
        """
        Pobiera listę dostępnych portów szeregowych
        """
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
        
    def connect(self, port: str, baudrate: int = 9600) -> bool:
        """
        Łączy się z portem szeregowym
        
        Args:
            port: Nazwa portu (np. /dev/cu.usbserial-14210)
            baudrate: Prędkość transmisji (domyślnie 9600)
            
        Returns:
            True jeśli połączenie udane, False w przeciwnym razie
        """
        try:
            self.connection = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=1,
                write_timeout=1
            )
            self.port = port
            return True
        except (serial.SerialException, OSError) as e:
            print(f"Błąd połączenia: {e}")
            self.connection = None
            self.port = None
            return False
            
    def disconnect(self) -> None:
        """
        Rozłącza połączenie z portem szeregowym
        """
        if self.connection and self.connection.is_open:
            self.connection.close()
        self.connection = None
        self.port = None
        
    def is_connected(self) -> bool:
        """
        Sprawdza czy połączenie jest aktywne
        """
        return self.connection is not None and self.connection.is_open
        
    def send_command(self, command: str) -> bool:
        """
        Wysyła komendę do Arduino
        
        Args:
            command: Komenda do wysłania (np. "SET_TIME:14:30:00")
            
        Returns:
            True jeśli wysłanie udane, False w przeciwnym razie
        """
        if not self.is_connected():
            print("Brak połączenia")
            return False
            
        try:
            # Dodaj znak nowej linii na końcu komendy
            message = f"{command}\n"
            self.connection.write(message.encode('utf-8'))
            self.connection.flush()
            return True
        except (serial.SerialException, OSError) as e:
            print(f"Błąd wysyłania: {e}")
            return False
            
    def read_response(self, timeout: float = 1.0) -> Optional[str]:
        """
        Odczytuje odpowiedź z Arduino
        
        Args:
            timeout: Maksymalny czas oczekiwania w sekundach
            
        Returns:
            Odczytana linia lub None jeśli brak danych
        """
        if not self.is_connected():
            return None
            
        try:
            self.connection.timeout = timeout
            line = self.connection.readline()
            if line:
                return line.decode('utf-8').strip()
            return None
        except (serial.SerialException, OSError, UnicodeDecodeError) as e:
            print(f"Błąd odczytu: {e}")
            return None
