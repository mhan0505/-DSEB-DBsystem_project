import os
import sys

# Đảm bảo Python nhận diện đúng thư mục root của project
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.gui.app import HospitalGUI

if __name__ == "__main__":
    print("Khởi động Hospital Management System GUI...")
    app = HospitalGUI()
    app.mainloop()
