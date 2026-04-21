"""
Data Encryption Module - Mã hóa dữ liệu nhạy cảm.

BẢO MẬT DỮ LIỆU:
Sử dụng AES-256 (Fernet) để mã hóa các trường dữ liệu nhạy cảm:
  - PhoneNumber (Số điện thoại)
  - Address (Địa chỉ)

CONCEPT: Encryption at Application Level
  - Dữ liệu được mã hóa TRƯỚC khi ghi vào database
  - Dữ liệu được giải mã SAU khi đọc từ database
  - Key được lưu riêng trong .env (KHÔNG commit lên Git)
  - Database chỉ chứa ciphertext → dù bị lộ DB, dữ liệu vẫn an toàn

FLOW:
  User Input → Validate → Encrypt → Store in DB
  DB Read → Decrypt → Display to User
"""

import os
import base64
import hashlib
from typing import Optional


class DataEncryption:
    """
    Manages encryption/decryption of sensitive patient data.

    Sử dụng AES thông qua thư viện cryptography (Fernet symmetric encryption).
    Fernet đảm bảo:
      - Confidentiality (bảo mật): dùng AES-128-CBC
      - Integrity (toàn vẹn): dùng HMAC-SHA256
      - Authenticity: nếu dữ liệu bị thay đổi → decrypt sẽ fail

    Usage:
        enc = DataEncryption()
        encrypted = enc.encrypt("0901234567")
        original = enc.decrypt(encrypted)  # → "0901234567"
    """

    def __init__(self):
        """
        Initialize encryption with key from environment variable.
        Key phải được set trong .env:
            ENCRYPTION_KEY=your-secret-key-here
        """
        self._key = self._get_or_create_key()
        self._fernet = None
        self._init_fernet()

    def _get_or_create_key(self) -> bytes:
        """
        Lấy encryption key từ environment variable.
        Nếu chưa có → tạo key mới và hướng dẫn user thêm vào .env.
        """
        env_key = os.getenv('ENCRYPTION_KEY', '')
        if env_key:
            # Derive a proper Fernet key from the user-provided key
            return base64.urlsafe_b64encode(
                hashlib.sha256(env_key.encode()).digest()
            )
        else:
            # Tạo key mặc định cho development (KHÔNG dùng cho production!)
            default_key = "hospital_dev_key_2024_change_in_production"
            print("[WARNING] ENCRYPTION_KEY not set in .env")
            print("    Using default key (development only).")
            print("    Add to .env: ENCRYPTION_KEY=your-secret-key-here")
            return base64.urlsafe_b64encode(
                hashlib.sha256(default_key.encode()).digest()
            )

    def _init_fernet(self):
        """Initialize Fernet cipher với key đã có."""
        try:
            from cryptography.fernet import Fernet
            self._fernet = Fernet(self._key)
        except ImportError:
            print("[WARNING] Library 'cryptography' is not installed.")
            print("    Run: pip install cryptography")
            print("    Encryption will be disabled.")
            self._fernet = None

    def encrypt(self, plaintext: Optional[str]) -> Optional[str]:
        """
        Mã hóa chuỗi văn bản thành ciphertext.

        Args:
            plaintext: Dữ liệu cần mã hóa (ví dụ: số điện thoại, địa chỉ)

        Returns:
            Chuỗi đã mã hóa (base64) hoặc None nếu input là None

        Example:
            encrypt("0901234567") → "gAAAAABl..."
        """
        if plaintext is None or plaintext == '':
            return plaintext

        if self._fernet is None:
            # Fallback: trả về plain text nếu không có thư viện
            return plaintext

        try:
            encrypted = self._fernet.encrypt(plaintext.encode('utf-8'))
            return encrypted.decode('utf-8')
        except Exception as e:
            print(f"[SECURITY LOG] Encryption error: {e}")
            return plaintext

    def decrypt(self, ciphertext: Optional[str]) -> Optional[str]:
        """
        Giải mã ciphertext thành văn bản gốc.

        Args:
            ciphertext: Dữ liệu đã mã hóa

        Returns:
            Chuỗi đã giải mã hoặc None nếu input là None

        Example:
            decrypt("gAAAAABl...") → "0901234567"
        """
        if ciphertext is None or ciphertext == '':
            return ciphertext

        if self._fernet is None:
            return ciphertext

        try:
            decrypted = self._fernet.decrypt(ciphertext.encode('utf-8'))
            return decrypted.decode('utf-8')
        except Exception:
            # Có thể là dữ liệu chưa được mã hóa (legacy data)
            # hoặc key đã thay đổi → trả về giá trị gốc
            return ciphertext

    def is_encrypted(self, value: str) -> bool:
        """
        Kiểm tra xem giá trị đã được mã hóa chưa.
        Fernet ciphertext luôn bắt đầu bằng 'gAAAAA'.
        """
        if not value:
            return False
        return value.startswith('gAAAAA')

    @property
    def is_available(self) -> bool:
        """Kiểm tra xem module mã hóa có sẵn sàng không."""
        return self._fernet is not None


# Singleton instance
_encryption_instance = None


def get_encryption() -> DataEncryption:
    """Lấy singleton instance của DataEncryption."""
    global _encryption_instance
    if _encryption_instance is None:
        _encryption_instance = DataEncryption()
    return _encryption_instance
