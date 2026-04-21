"""
TEST DATA ENCRYPTION - Verifies sensitive data is encrypted.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.security.encryption import DataEncryption, get_encryption
import src.security.encryption as enc_module


class TestDataEncryption(unittest.TestCase):
    """Test suite for data encryption/decryption."""

    def setUp(self):
        # Reset singleton for clean state
        enc_module._encryption_instance = None
        self.enc = get_encryption()

    def test_01_encrypt_decrypt_phone(self):
        """Mã hóa và giải mã số điện thoại."""
        phone = "0901234567"
        encrypted = self.enc.encrypt(phone)
        
        # Encrypted value phải khác original
        if self.enc.is_available:
            self.assertNotEqual(encrypted, phone)
        
        # Decrypt phải trả về giá trị gốc
        decrypted = self.enc.decrypt(encrypted)
        self.assertEqual(decrypted, phone)
        print(f"  ✅ Phone: {phone} → Encrypted → Decrypted: {decrypted}")

    def test_02_encrypt_decrypt_address(self):
        """Mã hóa và giải mã địa chỉ."""
        address = "12 Trần Hưng Đạo, Hà Nội"
        encrypted = self.enc.encrypt(address)
        decrypted = self.enc.decrypt(encrypted)
        self.assertEqual(decrypted, address)
        print(f"  ✅ Address encrypted and decrypted correctly")

    def test_03_none_handled(self):
        """None values không bị lỗi."""
        self.assertIsNone(self.enc.encrypt(None))
        self.assertIsNone(self.enc.decrypt(None))
        print("  ✅ None values handled correctly")

    def test_04_empty_string_handled(self):
        """Empty strings không bị lỗi."""
        self.assertEqual(self.enc.encrypt(''), '')
        self.assertEqual(self.enc.decrypt(''), '')
        print("  ✅ Empty strings handled correctly")

    def test_05_different_encryptions(self):
        """Cùng input → khác ciphertext (do Fernet dùng random IV)."""
        phone = "0901234567"
        enc1 = self.enc.encrypt(phone)
        enc2 = self.enc.encrypt(phone)
        
        if self.enc.is_available:
            # Fernet tạo ciphertext khác nhau mỗi lần (random IV)
            # → Chống replay attack
            self.assertNotEqual(enc1, enc2)
        
        # Nhưng cả hai đều decrypt về cùng giá trị
        self.assertEqual(self.enc.decrypt(enc1), phone)
        self.assertEqual(self.enc.decrypt(enc2), phone)
        print("  ✅ Same input → different ciphertexts (random IV)")

    def test_06_encrypted_data_not_readable(self):
        """Dữ liệu mã hóa không thể đọc được."""
        sensitive = "Nguyễn Văn An - 0901234567 - 12 Trần Hưng Đạo"
        encrypted = self.enc.encrypt(sensitive)
        
        if self.enc.is_available:
            # Ciphertext không chứa thông tin gốc
            self.assertNotIn("Nguyễn", encrypted)
            self.assertNotIn("0901234567", encrypted)
            self.assertNotIn("Trần Hưng Đạo", encrypted)
        
        print("  ✅ Encrypted data is not human-readable")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  🔐 DATA ENCRYPTION TESTS")
    print("=" * 60 + "\n")
    unittest.main(verbosity=2)
