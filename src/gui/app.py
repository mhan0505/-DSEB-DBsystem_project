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
        
        self.btn_lookup = ctk.CTkButton(
            self.sidebar_frame, text="📋 Tra cứu dữ liệu", 
            command=self.show_lookup, fg_color="transparent", 
            text_color=("gray10", "gray90"), anchor="w"
        )
        self.btn_lookup.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.btn_patient_crud = ctk.CTkButton(
            self.sidebar_frame, text="👤 Quản lý Bệnh nhân", 
            command=self.show_patient_crud, fg_color="transparent", 
            text_color=("gray10", "gray90"), anchor="w"
        )
        self.btn_patient_crud.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        
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

        # Lấy danh sách từ DB để fill vào dropdown (tránh nhập sai mã)
        try:
            doctors = self.doctor_repo.get_all()
            # DoctorRepository trả về list[dict] do có JOIN
            doc_options = [f"{d['DoctorID']} - {d['DoctorName']}" for d in doctors] if doctors else []
        except Exception:
            doc_options = []

        try:
            patients = self.patient_repo.get_all()
            # PatientRepository trả về list[Patient]
            pat_options = [f"{p.patient_id} - {p.patient_name}" for p in patients] if patients else []
        except Exception:
            pat_options = []

        if not doc_options: doc_options = ["(Không tải được danh sách)"]
        if not pat_options: pat_options = ["(Không tải được danh sách)"]

        # Tự động sinh mã lịch hẹn (Apt ID) tối đa 10 ký tự: A + hhmmss + 3 số ngẫu nhiên
        import random
        auto_apt_id = f"A{datetime.now().strftime('%H%M%S')}{random.randint(100, 999)}"
        
        self.entry_apt_id = self._create_form_row(form_frame, 1, "Mã Lịch Hẹn (Tự động):", "")
        self.entry_apt_id.insert(0, auto_apt_id)
        self.entry_apt_id.configure(state="readonly") # Khóa lại để hệ thống tự quản lý mã

        self.entry_doc_id = self._create_combobox_row(form_frame, 2, "Chọn Bác Sĩ:", doc_options)
        self.entry_pat_id = self._create_combobox_row(form_frame, 3, "Chọn Bệnh Nhân:", pat_options)
        self._create_date_picker_row(form_frame, 4, "Ngày Khám:")
        self._create_time_picker_row(form_frame, 5, "Giờ Khám:")

        btn_submit = ctk.CTkButton(
            form_frame, text="Xác nhận Đặt Lịch", 
            font=ctk.CTkFont(size=16, weight="bold"), height=40,
            command=self._handle_schedule_appointment
        )
        btn_submit.grid(row=6, column=0, columnspan=2, pady=30)

        # --- Hướng dẫn đặt lịch ---
        guide_frame = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color=("gray85", "gray25"))
        guide_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 20))
        
        guide_title = ctk.CTkLabel(guide_frame, text="💡 Hướng dẫn Đặt lịch:", font=ctk.CTkFont(size=16, weight="bold"), text_color="#4DB6AC")
        guide_title.pack(padx=20, pady=(15, 5), anchor="w")
        
        guide_text = (
            "1. Mã Lịch Hẹn: Hệ thống tự động sinh mã duy nhất, bạn không cần nhập tay.\n"
            "2. Bác Sĩ & Bệnh Nhân: Chọn từ danh sách thả xuống để tránh gõ sai mã ID.\n"
            "3. Ngày & Giờ: Được chọn qua các hộp thả xuống để đảm bảo tính hợp lệ tuyệt đối.\n"
            "⚠️ Hệ thống sẽ chặn tự động nếu Bác Sĩ đã có lịch hẹn vào cùng Ngày và Giờ (Double Booking)."
        )
        guide_lbl = ctk.CTkLabel(guide_frame, text=guide_text, justify="left", font=ctk.CTkFont(size=14))
        guide_lbl.pack(padx=20, pady=(0, 15), anchor="w")

    def _create_combobox_row(self, parent, row, label_text, values):
        label = ctk.CTkLabel(parent, text=label_text, font=ctk.CTkFont(size=14, weight="bold"))
        label.grid(row=row, column=0, padx=30, pady=10, sticky="e")
        
        combo = ctk.CTkComboBox(parent, values=values, width=300, height=35)
        combo.grid(row=row, column=1, padx=(0, 30), pady=10, sticky="w")
        if values:
            combo.set(values[0])
        return combo

    def _create_date_picker_row(self, parent, row, label_text):
        label = ctk.CTkLabel(parent, text=label_text, font=ctk.CTkFont(size=14, weight="bold"))
        label.grid(row=row, column=0, padx=30, pady=10, sticky="e")
        
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=1, padx=(0, 30), pady=10, sticky="w")
        
        days = [f"{i:02d}" for i in range(1, 32)]
        months = [f"{i:02d}" for i in range(1, 13)]
        current_year = datetime.now().year
        years = [str(i) for i in range(current_year, current_year + 5)]
        
        self.combo_day = ctk.CTkComboBox(frame, values=days, width=70)
        self.combo_day.pack(side="left", padx=(0, 5))
        self.combo_day.set(datetime.now().strftime("%d"))
        
        lbl_slash1 = ctk.CTkLabel(frame, text="/", font=ctk.CTkFont(size=18))
        lbl_slash1.pack(side="left", padx=5)
        
        self.combo_month = ctk.CTkComboBox(frame, values=months, width=70)
        self.combo_month.pack(side="left", padx=5)
        self.combo_month.set(datetime.now().strftime("%m"))
        
        lbl_slash2 = ctk.CTkLabel(frame, text="/", font=ctk.CTkFont(size=18))
        lbl_slash2.pack(side="left", padx=5)
        
        self.combo_year = ctk.CTkComboBox(frame, values=years, width=90)
        self.combo_year.pack(side="left", padx=(5, 0))
        self.combo_year.set(datetime.now().strftime("%Y"))

    def _create_time_picker_row(self, parent, row, label_text):
        label = ctk.CTkLabel(parent, text=label_text, font=ctk.CTkFont(size=14, weight="bold"))
        label.grid(row=row, column=0, padx=30, pady=10, sticky="e")
        
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=1, padx=(0, 30), pady=10, sticky="w")
        
        hours = [f"{i:02d}" for i in range(7, 20)] # Giờ làm việc 07:00 -> 19:00
        minutes = ["00", "15", "30", "45"] # Chia slot 15 phút
        
        self.combo_hour = ctk.CTkComboBox(frame, values=hours, width=70)
        self.combo_hour.pack(side="left", padx=(0, 5))
        self.combo_hour.set("09")
        
        lbl_colon = ctk.CTkLabel(frame, text=":", font=ctk.CTkFont(size=18, weight="bold"))
        lbl_colon.pack(side="left", padx=5)
        
        self.combo_minute = ctk.CTkComboBox(frame, values=minutes, width=70)
        self.combo_minute.pack(side="left", padx=(5, 0))
        self.combo_minute.set("00")

    def _create_form_row(self, parent, row, label_text, placeholder):
        label = ctk.CTkLabel(parent, text=label_text, font=ctk.CTkFont(size=14, weight="bold"))
        label.grid(row=row, column=0, padx=30, pady=10, sticky="e")
        
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=300, height=35)
        entry.grid(row=row, column=1, padx=(0, 30), pady=10, sticky="w")
        return entry

    def _handle_schedule_appointment(self):
        aid = self.entry_apt_id.get().strip()
        
        # Combo box text có dạng "DR001 - Nguyen Van A" -> cắt lấy ID
        raw_did = self.entry_doc_id.get().strip()
        did = raw_did.split(" - ")[0] if " - " in raw_did else raw_did
        
        raw_pid = self.entry_pat_id.get().strip()
        pid = raw_pid.split(" - ")[0] if " - " in raw_pid else raw_pid
        
        date_str = f"{self.combo_year.get()}-{self.combo_month.get()}-{self.combo_day.get()}"
        time_str = f"{self.combo_hour.get()}:{self.combo_minute.get()}:00"

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

    def show_lookup(self):
        self._clear_main_frame()
        self.btn_dashboard.configure(fg_color="transparent")
        if hasattr(self, 'btn_appointments'):
            self.btn_appointments.configure(fg_color="transparent")
        self.btn_lookup.configure(fg_color=("gray75", "gray25"))

        title = ctk.CTkLabel(self.main_frame, text="📋 Tra Cứu Thông Tin (Demo RBAC)", font=ctk.CTkFont(size=28, weight="bold"))
        title.grid(row=0, column=0, sticky="nw", pady=(0, 20))

        ctrl_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        ctrl_frame.grid(row=1, column=0, sticky="ew")

        ctk.CTkLabel(ctrl_frame, text="Chọn loại dữ liệu:").pack(side="left", padx=(0, 10))
        
        self.lookup_type = ctk.CTkComboBox(ctrl_frame, values=["Thông tin Bệnh nhân", "Lịch hẹn (Tất cả)", "Lịch Bác sĩ (Bận/Rảnh)", "Báo cáo Doanh thu"], width=200)
        self.lookup_type.pack(side="left", padx=10)
        
        btn_view = ctk.CTkButton(ctrl_frame, text="Xem Dữ Liệu", command=self._fetch_lookup_data)
        btn_view.pack(side="left", padx=10)

        self.lookup_textbox = ctk.CTkTextbox(self.main_frame, width=800, height=450, font=ctk.CTkFont(family="Consolas", size=13))
        self.lookup_textbox.grid(row=2, column=0, sticky="nsew", pady=20)
        self.lookup_textbox.insert("end", "💡 Hãy chọn một mục và bấm 'Xem Dữ Liệu'.\nLưu ý: Bạn chỉ có thể xem được dữ liệu nếu Tài khoản có quyền (RBAC).")

    def _fetch_lookup_data(self):
        self.lookup_textbox.delete("0.0", "end")
        selected = self.lookup_type.get()
        
        try:
            if selected == "Thông tin Bệnh nhân":
                patients = self.patient_repo.get_all()
                if not patients:
                    self.lookup_textbox.insert("end", "Không có dữ liệu bệnh nhân.")
                    return
                
                output = f"{'ID':<10} | {'Tên Bệnh Nhân':<25} | {'Điện Thoại (Đã Giải Mã)':<15} | {'Địa Chỉ (Đã Giải Mã)'}\n"
                output += "-"*90 + "\n"
                for p in patients:
                    output += f"{p.patient_id:<10} | {p.patient_name:<25} | {p.phone_number or 'N/A':<15} | {p.address or 'N/A'}\n"
                
                self.lookup_textbox.insert("end", output)

            elif selected == "Lịch hẹn (Tất cả)":
                appts = self.appt_repo.get_all()
                if not appts:
                    self.lookup_textbox.insert("end", "Không có dữ liệu lịch hẹn.")
                    return
                
                output = f"{'Apt ID':<10} | {'Bác Sĩ':<25} | {'Bệnh Nhân':<20} | {'Ngày Khám':<12} | {'Giờ Khám'}\n"
                output += "-"*90 + "\n"
                for a in appts:
                    output += f"{a['AppointmentID']:<10} | {a['DoctorName']:<25} | {a['PatientName']:<20} | {str(a['AppointmentDate']):<12} | {str(a['AppointmentTime'])}\n"
                
                self.lookup_textbox.insert("end", output)

            elif selected == "Lịch Bác sĩ (Bận/Rảnh)":
                query = """
                    SELECT d.DoctorID, d.DoctorName, a.AppointmentDate, a.AppointmentTime, a.AppointmentID
                    FROM Doctors d
                    LEFT JOIN Appointments a ON d.DoctorID = a.DoctorID AND a.AppointmentDate >= CURDATE()
                    ORDER BY d.DoctorID, a.AppointmentDate, a.AppointmentTime
                """
                results = self.db.execute_query(query)
                
                output = f"{'Bác Sĩ':<25} | {'Trạng Thái':<12} | {'Ngày Khám':<12} | {'Giờ Khám':<10} | {'Mã Lịch'}\n"
                output += "-"*80 + "\n"
                for r in results:
                    doc_info = f"{r['DoctorID']} - {r['DoctorName']}"
                    if r['AppointmentID']:
                        output += f"{doc_info:<25} | {'🔴 Đã Kín':<12} | {str(r['AppointmentDate']):<12} | {str(r['AppointmentTime']):<10} | {r['AppointmentID']}\n"
                    else:
                        output += f"{doc_info:<25} | {'🟢 Rảnh':<12} | {'---':<12} | {'---':<10} | {'---'}\n"
                
                self.lookup_textbox.insert("end", output)

            elif selected == "Báo cáo Doanh thu":
                from src.repositories.invoice_repository import InvoiceRepository
                inv_repo = InvoiceRepository()
                
                total_rev = inv_repo.get_total_revenue()
                invoices = inv_repo.get_all()
                
                output = f"💰 TỔNG DOANH THU TOÀN HỆ THỐNG: {total_rev:,.0f} VND\n\n"
                output += f"CHI TIẾT CÁC HÓA ĐƠN ({len(invoices)} giao dịch):\n"
                output += "-"*85 + "\n"
                output += f"{'Mã Hóa Đơn':<15} | {'Tên Bệnh Nhân':<25} | {'Ngày Thu':<15} | {'Số Tiền'}\n"
                output += "-"*85 + "\n"
                
                for i in invoices:
                    output += f"{i['InvoiceID']:<15} | {i['PatientName']:<25} | {str(i['InvoiceDate']):<15} | {i['TotalAmount']:,.0f} VND\n"
                    
                self.lookup_textbox.insert("end", output)

        except Exception as e:
            err_msg = str(e)
            if "denied" in err_msg.lower() or "1142" in err_msg:
                self.lookup_textbox.insert("end", f"❌ LỖI PHÂN QUYỀN (RBAC):\n\nTài khoản '{self.current_user_role}' KHÔNG ĐƯỢC PHÉP truy cập bảng này.\n\nChi tiết lỗi từ MySQL:\n{err_msg}")
            else:
                self.lookup_textbox.insert("end", f"🚨 LỖI HỆ THỐNG:\n\n{err_msg}")

    # =========================================================
    # PATIENT CRUD
    # =========================================================
    def show_patient_crud(self):
        self._clear_main_frame()
        self.btn_dashboard.configure(fg_color="transparent")
        if hasattr(self, 'btn_appointments'): self.btn_appointments.configure(fg_color="transparent")
        if hasattr(self, 'btn_lookup'): self.btn_lookup.configure(fg_color="transparent")
        if hasattr(self, 'btn_patient_crud'): self.btn_patient_crud.configure(fg_color=("gray75", "gray25"))

        title = ctk.CTkLabel(self.main_frame, text="👤 Quản lý Bệnh nhân (CRUD)", font=ctk.CTkFont(size=28, weight="bold"))
        title.grid(row=0, column=0, sticky="nw", pady=(0, 20))

        # --- Top: Search ---
        search_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        self.entry_search = ctk.CTkEntry(search_frame, placeholder_text="Nhập Tên hoặc Mã Bệnh Nhân", width=300)
        self.entry_search.pack(side="left", padx=(0, 10))
        
        btn_search = ctk.CTkButton(search_frame, text="🔍 Tìm kiếm", command=self._handle_search_patient)
        btn_search.pack(side="left")

        # --- Middle: Result ---
        self.crud_textbox = ctk.CTkTextbox(self.main_frame, height=180, font=ctk.CTkFont(family="Consolas", size=13))
        self.crud_textbox.grid(row=2, column=0, sticky="nsew", pady=(0, 20))
        self.crud_textbox.insert("end", "Nhập mã hoặc tên và bấm Tìm kiếm...")

        # --- Bottom: Form ---
        form_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        form_frame.grid(row=3, column=0, sticky="nsew")

        self.entry_p_id = self._create_form_row(form_frame, 0, "Mã BN:", "VD: P001")
        self.entry_p_name = self._create_form_row(form_frame, 1, "Tên BN:", "VD: Nguyen Van A")
        self.entry_p_dob = self._create_form_row(form_frame, 2, "Ngày sinh:", "YYYY-MM-DD")
        self.entry_p_gender = self._create_form_row(form_frame, 3, "Giới tính:", "M / F / O")
        self.entry_p_address = self._create_form_row(form_frame, 4, "Địa chỉ:", "")
        self.entry_p_phone = self._create_form_row(form_frame, 5, "Điện thoại:", "")

        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

        ctk.CTkButton(btn_frame, text="Thêm Mới", command=self._handle_create_patient, fg_color="#2E7D32", hover_color="#1B5E20").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Cập Nhật", command=self._handle_update_patient, fg_color="#1565C0", hover_color="#0D47A1").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Xóa", command=self._handle_delete_patient, fg_color="#C62828", hover_color="#B71C1C").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Làm Mới", command=self._handle_clear_patient_form, fg_color="#757575", hover_color="#424242").pack(side="left", padx=10)

    def _handle_clear_patient_form(self):
        # Xóa tìm kiếm và kết quả
        self.entry_search.delete(0, 'end')
        self.crud_textbox.delete("0.0", "end")
        self.crud_textbox.insert("end", "Nhập mã hoặc tên và bấm Tìm kiếm...")
        
        # Xóa Form
        self.entry_p_id.delete(0, 'end')
        self.entry_p_name.delete(0, 'end')
        self.entry_p_dob.delete(0, 'end')
        self.entry_p_gender.delete(0, 'end')
        self.entry_p_address.delete(0, 'end')
        self.entry_p_phone.delete(0, 'end')

    def _get_patient_from_form(self):
        from src.models.patient import Patient
        from datetime import date
        pid = self.entry_p_id.get().strip()
        name = self.entry_p_name.get().strip()
        dob_str = self.entry_p_dob.get().strip()
        gender = self.entry_p_gender.get().strip().upper()
        address = self.entry_p_address.get().strip()
        phone = self.entry_p_phone.get().strip()

        if not all([pid, name, dob_str, gender]):
            raise ValueError("ID, Name, Date of Birth và Gender là bắt buộc!")
            
        dob = date.fromisoformat(dob_str)
        return Patient(pid, name, dob, gender, address, phone)

    def _handle_search_patient(self):
        self.crud_textbox.delete("0.0", "end")
        search_kw = self.entry_search.get().strip()
        if not search_kw:
            self.crud_textbox.insert("end", "Vui lòng nhập từ khóa.")
            return
            
        try:
            results = []
            if search_kw.upper().startswith('P'):
                p = self.patient_repo.get_by_id(search_kw)
                if p: results.append(p)
            else:
                results = self.patient_repo.search_by_name(search_kw)

            if not results:
                self.crud_textbox.insert("end", "❌ Không tìm thấy bệnh nhân nào.")
                return
                
            output = f"🔍 Tìm thấy {len(results)} kết quả:\n"
            output += "-"*80 + "\n"
            for p in results:
                output += f"ID: {p.patient_id:<10} | Tên: {p.patient_name:<20} | DOB: {p.date_of_birth} | Giới: {p.gender} | SĐT: {p.phone_number}\n"
                
                # Auto fill form if exact 1 match
                if len(results) == 1:
                    self._fill_patient_form(p)
                    
            self.crud_textbox.insert("end", output)
        except Exception as e:
            self.crud_textbox.insert("end", f"Lỗi: {str(e)}")

    def _fill_patient_form(self, p):
        self.entry_p_id.delete(0, 'end'); self.entry_p_id.insert(0, p.patient_id)
        self.entry_p_name.delete(0, 'end'); self.entry_p_name.insert(0, p.patient_name)
        self.entry_p_dob.delete(0, 'end'); self.entry_p_dob.insert(0, str(p.date_of_birth))
        self.entry_p_gender.delete(0, 'end'); self.entry_p_gender.insert(0, p.gender or '')
        self.entry_p_address.delete(0, 'end'); self.entry_p_address.insert(0, p.address or '')
        self.entry_p_phone.delete(0, 'end'); self.entry_p_phone.insert(0, p.phone_number or '')

    def _handle_create_patient(self):
        try:
            p = self._get_patient_from_form()
            self.patient_repo.create(p)
            messagebox.showinfo("Thành công", "Đã thêm mới bệnh nhân thành công!")
            self._handle_search_patient()
        except Exception as e:
            from src.security.input_validator import InputValidator
            messagebox.showerror("Lỗi", InputValidator.sanitize_error_message(e))

    def _handle_update_patient(self):
        try:
            p = self._get_patient_from_form()
            self.patient_repo.update(p)
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin bệnh nhân!")
            self._handle_search_patient()
        except Exception as e:
            from src.security.input_validator import InputValidator
            messagebox.showerror("Lỗi", InputValidator.sanitize_error_message(e))

    def _handle_delete_patient(self):
        pid = self.entry_p_id.get().strip()
        if not pid:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã BN cần xóa!")
            return
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa Bệnh nhân {pid}?"):
            try:
                self.patient_repo.delete(pid)
                messagebox.showinfo("Thành công", "Đã xóa bệnh nhân!")
                self.crud_textbox.delete("0.0", "end")
            except Exception as e:
                from src.security.input_validator import InputValidator
                messagebox.showerror("Lỗi", InputValidator.sanitize_error_message(e))

if __name__ == "__main__":
    app = HospitalGUI()
    app.mainloop()
