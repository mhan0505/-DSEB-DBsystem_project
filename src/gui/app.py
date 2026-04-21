import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

import customtkinter as ctk
import tkinter.messagebox as messagebox
from datetime import datetime

from src.database_connection import DatabaseConnection
from src.services.appointment_service import AppointmentService
from src.repositories.patient_repository import PatientRepository
from src.repositories.doctor_repository import DoctorRepository
from src.repositories.appointment_repository import AppointmentRepository

# =========================================================
# THEME CONFIGURATION
# =========================================================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class HospitalGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("🏥 Hospital Management System Pro")
        self.geometry("1100x700")
        self.minsize(900, 600)

        # configure grid layout (1x2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.current_user_role = None
        
        # Show Login Screen First
        self.show_login_screen()

    def show_login_screen(self):
        """Màn hình Đăng nhập để chọn Quyền (Role)"""
        # Clear everything
        for widget in self.winfo_children():
            widget.destroy()
            
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        login_frame = ctk.CTkFrame(self, width=400, corner_radius=15)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(login_frame, text="ĐĂNG NHẬP HỆ THỐNG", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=(40, 10))
        
        subtitle = ctk.CTkLabel(login_frame, text="Trình diễn tính năng Phân Quyền (RBAC)", text_color="gray")
        subtitle.pack(pady=(0, 30))

        # Preset Roles Dropdown
        role_label = ctk.CTkLabel(login_frame, text="Chọn Vai trò (Auto-fill credentials):", anchor="w")
        role_label.pack(padx=40, pady=(0, 5), anchor="w")
        
        self.roles_data = {
            "Quản trị viên (Admin)": ("admin_hospital", "Admin@Hospital2024!"),
            "Bác sĩ (Doctor)": ("doctor_user", "Doctor@Hospital2024!"),
            "Lễ tân (Receptionist)": ("receptionist", "Reception@Hospital2024!"),
            "Kế toán (Accountant)": ("accountant", "Account@Hospital2024!"),
            "Khách (Read-Only)": ("readonly_user", "ReadOnly@Hospital2024!")
        }
        
        self.role_combobox = ctk.CTkComboBox(
            login_frame, values=list(self.roles_data.keys()), width=300,
            command=self._autofill_credentials
        )
        self.role_combobox.pack(padx=40, pady=(0, 20))

        # Username Input
        self.entry_user = ctk.CTkEntry(login_frame, placeholder_text="Database Username", width=300)
        self.entry_user.pack(padx=40, pady=10)

        # Password Input
        self.entry_pass = ctk.CTkEntry(login_frame, placeholder_text="Database Password", show="*", width=300)
        self.entry_pass.pack(padx=40, pady=10)
        
        # Auto-fill for the default selected role
        self._autofill_credentials(self.role_combobox.get())

        # Login Button
        btn_login = ctk.CTkButton(
            login_frame, text="ĐĂNG NHẬP", font=ctk.CTkFont(weight="bold"), 
            width=300, height=40, command=self._handle_login
        )
        btn_login.pack(padx=40, pady=(30, 40))

    def _autofill_credentials(self, choice):
        """Tự động điền tài khoản DB khi chọn Role từ dropdown"""
        user, pwd = self.roles_data.get(choice, ("", ""))
        self.entry_user.delete(0, 'end')
        self.entry_user.insert(0, user)
        self.entry_pass.delete(0, 'end')
        self.entry_pass.insert(0, pwd)

    def _handle_login(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        
        try:
            # Init Database with dynamic credentials
            self.db = DatabaseConnection()
            self.db.connect(user=user, password=pwd)
            
            # Setup Services with the new connection
            self.patient_repo = PatientRepository()
            self.doctor_repo = DoctorRepository()
            self.appt_repo = AppointmentRepository()
            self.appt_service = AppointmentService()
            
            self.current_user_role = user
            messagebox.showinfo("Đăng nhập thành công", f"Đã kết nối Database với quyền: {user}")
            
            # Khởi tạo giao diện chính
            self._init_main_interface()
            
        except Exception as e:
            messagebox.showerror("Đăng nhập thất bại", f"Tài khoản hoặc mật khẩu không đúng.\n(Lỗi DB: {str(e)})")

    def _init_main_interface(self):
        """Build the main app layout after login"""
        for widget in self.winfo_children():
            widget.destroy()
            
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self._create_sidebar()
        self._create_main_area()
        self.show_dashboard()

    def _create_sidebar(self):
        """Tạo thanh điều hướng bên trái (Sidebar)"""
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        # Logo / Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="DATCOM Lab", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 5))
        
        # Hiển thị Role đang đăng nhập
        role_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text=f"Quyền: {self.current_user_role}", 
            text_color="green",
            font=ctk.CTkFont(size=12, slant="italic")
        )
        role_label.grid(row=1, column=0, padx=20, pady=(0, 30))

        # Buttons
        self.btn_dashboard = ctk.CTkButton(
            self.sidebar_frame, text="📊 Dashboard", 
            command=self.show_dashboard, fg_color="transparent", 
            text_color=("gray10", "gray90"), anchor="w"
        )
        self.btn_dashboard.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.btn_appointments = ctk.CTkButton(
            self.sidebar_frame, text="📅 Đặt lịch khám", 
            command=self.show_appointments, fg_color="transparent", 
            text_color=("gray10", "gray90"), anchor="w"
        )
        self.btn_appointments.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        # Ẩn nút "Đặt lịch khám" nếu là Kế toán hoặc Khách
        if self.current_user_role in ['accountant', 'readonly_user']:
            self.btn_appointments.grid_remove()

        # Logout Button
        self.btn_logout = ctk.CTkButton(
            self.sidebar_frame, text="🚪 Đăng xuất", 
            command=self.logout, fg_color="#C62828", hover_color="#B71C1C"
        )
        self.btn_logout.grid(row=8, column=0, padx=20, pady=20, sticky="ew")

    def logout(self):
        """Ngắt kết nối và quay lại màn hình Login"""
        if hasattr(self, 'db'):
            self.db.disconnect()
        self.show_login_screen()

    def _create_main_area(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

    def _clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self._clear_main_frame()
        self.btn_dashboard.configure(fg_color=("gray75", "gray25"))
        if hasattr(self, 'btn_appointments'):
            self.btn_appointments.configure(fg_color="transparent")

        title = ctk.CTkLabel(self.main_frame, text="📊 Tổng quan Hệ thống", font=ctk.CTkFont(size=28, weight="bold"))
        title.grid(row=0, column=0, sticky="nw", pady=(0, 20))

        # Lấy dữ liệu thực tế. Xử lý lỗi nếu không có quyền SELECT (ví dụ: Kế toán không được xem Doctors)
        try:
            total_patients = self.patient_repo.count()
        except Exception:
            total_patients = "N/A"
            
        try:
            total_doctors = len(self.doctor_repo.get_all())
        except Exception:
            total_doctors = "N/A"
            
        try:
            total_appts = len(self.appt_repo.get_all())
        except Exception:
            total_appts = "N/A"

        cards_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        cards_frame.grid(row=1, column=0, sticky="ew")
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self._create_stat_card(cards_frame, 0, "Tổng Bệnh Nhân", str(total_patients), "👤")
        self._create_stat_card(cards_frame, 1, "Tổng Bác Sĩ", str(total_doctors), "👨‍⚕️")
        self._create_stat_card(cards_frame, 2, "Lịch Hẹn (All)", str(total_appts), "📅")

        # Security Status Panel
        sec_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        sec_frame.grid(row=2, column=0, sticky="nsew", pady=30)
        
        sec_title = ctk.CTkLabel(sec_frame, text="🔒 Tình trạng Bảo mật", font=ctk.CTkFont(size=20, weight="bold"))
        sec_title.pack(padx=20, pady=(20, 10), anchor="w")

        sec_text = (
            f"👤 Đang đăng nhập: {self.current_user_role}\n\n"
            "✅ AES-256 Encryption: Đang hoạt động\n"
            "✅ SQL Injection Prevention: Bật (Input Validator)\n"
            "✅ 3NF Normalization: CSDL đạt chuẩn\n"
            "✅ RBAC & Audit Log: Đang giám sát hệ thống"
        )
        sec_lbl = ctk.CTkLabel(sec_frame, text=sec_text, justify="left", font=ctk.CTkFont(size=14))
        sec_lbl.pack(padx=20, pady=(0, 20), anchor="w")

    def _create_stat_card(self, parent, col, title, value, icon):
        card = ctk.CTkFrame(parent, corner_radius=15)
        card.grid(row=0, column=col, padx=10, sticky="ew")
        
        lbl_icon = ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=40))
        lbl_icon.pack(pady=(20, 5))
        
        # Nếu là N/A (không có quyền xem), tô màu đỏ cảnh báo
        color = "#FF5252" if value == "N/A" else ("gray10", "gray90")
        lbl_value = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=36, weight="bold"), text_color=color)
        lbl_value.pack()
        
        lbl_title = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14), text_color="gray")
        lbl_title.pack(pady=(0, 20))

    def show_appointments(self):
        self._clear_main_frame()
        self.btn_appointments.configure(fg_color=("gray75", "gray25"))
        self.btn_dashboard.configure(fg_color="transparent")

        title = ctk.CTkLabel(self.main_frame, text="📅 Đặt Lịch Khám Mới", font=ctk.CTkFont(size=28, weight="bold"))
        title.grid(row=0, column=0, sticky="nw", pady=(0, 20))

        form_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        form_frame.grid(row=1, column=0, sticky="nsew")
        form_frame.grid_columnconfigure(1, weight=1)

        instruction = ctk.CTkLabel(
            form_frame, 
            text="Hệ thống tự động kiểm tra chống Trùng lịch (Double Booking) và SQL Injection.", 
            text_color="gray", font=ctk.CTkFont(slant="italic")
        )
        instruction.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.entry_apt_id = self._create_form_row(form_frame, 1, "Mã Lịch Hẹn (Apt ID):", "VD: APT001")
        self.entry_doc_id = self._create_form_row(form_frame, 2, "Mã Bác Sĩ (Doc ID):", "VD: DR001")
        self.entry_pat_id = self._create_form_row(form_frame, 3, "Mã Bệnh Nhân (Pat ID):", "VD: P001")
        self.entry_date = self._create_form_row(form_frame, 4, "Ngày (YYYY-MM-DD):", datetime.now().strftime("%Y-%m-%d"))
        self.entry_time = self._create_form_row(form_frame, 5, "Giờ (HH:MM:SS):", "09:00:00")

        btn_submit = ctk.CTkButton(
            form_frame, text="Xác nhận Đặt Lịch", 
            font=ctk.CTkFont(size=16, weight="bold"), height=40,
            command=self._handle_schedule_appointment
        )
        btn_submit.grid(row=6, column=0, columnspan=2, pady=30)

    def _create_form_row(self, parent, row, label_text, placeholder):
        label = ctk.CTkLabel(parent, text=label_text, font=ctk.CTkFont(size=14, weight="bold"))
        label.grid(row=row, column=0, padx=30, pady=10, sticky="e")
        
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=300, height=35)
        entry.grid(row=row, column=1, padx=(0, 30), pady=10, sticky="w")
        return entry

    def _handle_schedule_appointment(self):
        aid = self.entry_apt_id.get().strip()
        did = self.entry_doc_id.get().strip()
        pid = self.entry_pat_id.get().strip()
        date_str = self.entry_date.get().strip()
        time_str = self.entry_time.get().strip()

        if not all([aid, did, pid, date_str, time_str]):
            messagebox.showwarning("Lỗi Nhập Liệu", "Vui lòng điền đầy đủ các trường!")
            return

        try:
            from datetime import date, time
            appt_date = date.fromisoformat(date_str)
            parts = time_str.split(':')
            appt_time = time(int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) > 2 else 0)
            
            result = self.appt_service.schedule_appointment(aid, did, pid, appt_date, appt_time)
            
            if result['status'] == 'SUCCESS':
                messagebox.showinfo("Thành Công", f"✅ {result['message']}")
                self.entry_apt_id.delete(0, 'end')
            else:
                messagebox.showerror("Lỗi Nghiệp Vụ", f"❌ {result['message']}\n\n(Bị chặn bởi Business Logic)")
                
        except ValueError as e:
            messagebox.showerror("Lỗi Validation", f"⚠️ Input không hợp lệ:\n{e}\n\n(Bị chặn bởi Input Validator)")
        except Exception as e:
            from src.security.input_validator import InputValidator
            safe_msg = InputValidator.sanitize_error_message(e)
            messagebox.showerror("Lỗi Hệ Thống", f"🚨 {safe_msg}")

if __name__ == "__main__":
    app = HospitalGUI()
    app.mainloop()
