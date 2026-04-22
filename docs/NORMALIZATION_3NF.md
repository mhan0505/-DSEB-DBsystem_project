# PHÂN TÍCH CHUẨN HÓA - HOSPITAL MANAGEMENT SYSTEM

> **Kết luận:** Cơ sở dữ liệu Hospital Management System **ĐẠT CHUẨN 3NF** (Third Normal Form)

---

## 1. DẠNG CHUẨN 1 (1NF - First Normal Form)

**Điều kiện:** Mỗi cột chỉ chứa giá trị nguyên tử (atomic), không có nhóm lặp.

| Bảng | Cột | Atomic? | Giải thích |
|------|-----|---------|------------|
| Departments | DepartmentID | ✅ | VARCHAR(10), giá trị đơn |
| Departments | DepartmentName | ✅ | VARCHAR(50), giá trị đơn |
| Patients | PatientID | ✅ | VARCHAR(10), giá trị đơn |
| Patients | PatientName | ✅ | VARCHAR(100), tên đầy đủ (không tách họ/tên) |
| Patients | DateOfBirth | ✅ | DATE, giá trị đơn |
| Patients | Gender | ✅ | VARCHAR(1), chỉ M/F/O |
| Patients | Address | ✅ | VARCHAR(500), địa chỉ đầy đủ (lưu dạng mã hóa) |
| Patients | PhoneNumber | ✅ | VARCHAR(500), một số điện thoại (lưu dạng mã hóa) |
| Doctors | DoctorID | ✅ | VARCHAR(10), giá trị đơn |
| Doctors | DoctorName | ✅ | VARCHAR(100), giá trị đơn |
| Doctors | DepartmentID | ✅ | VARCHAR(10), FK đến 1 department |
| Doctors | Specialty | ✅ | VARCHAR(50), giá trị đơn |
| Appointments | AppointmentID | ✅ | VARCHAR(10), giá trị đơn |
| Appointments | DoctorID | ✅ | VARCHAR(10), FK đến 1 doctor |
| Appointments | PatientID | ✅ | VARCHAR(10), FK đến 1 patient |
| Appointments | AppointmentDate | ✅ | DATE, giá trị đơn |
| Appointments | AppointmentTime | ✅ | TIME, giá trị đơn |
| Invoices | InvoiceID | ✅ | VARCHAR(10), giá trị đơn |
| Invoices | PatientID | ✅ | VARCHAR(10), FK đến 1 patient |
| Invoices | InvoiceDate | ✅ | DATE, giá trị đơn |
| Invoices | TotalAmount | ✅ | DECIMAL(10,2), giá trị đơn |

**✅ Kết luận 1NF:**
- Tất cả các cột đều chứa giá trị nguyên tử
- Mỗi bảng có Primary Key xác định duy nhất từng hàng
- Không có nhóm lặp (repeating groups)
- → **ĐẠT CHUẨN 1NF**

---

## 2. DẠNG CHUẨN 2 (2NF - Second Normal Form)

**Điều kiện:** Đạt 1NF + Không có phụ thuộc hàm bộ phận (partial dependency) vào khóa chính.

> **Lưu ý:** 2NF chỉ áp dụng khi khóa chính là **khóa tổ hợp** (composite key).
> Tất cả 5 bảng trong hệ thống đều có **khóa chính đơn** (single-column PK),
> nên **tự động đạt 2NF**.

| Bảng | Primary Key | Loại PK | Phụ thuộc bộ phận? |
|------|------------|---------|-------------------|
| Departments | DepartmentID | Đơn | Không thể có (PK đơn) |
| Patients | PatientID | Đơn | Không thể có (PK đơn) |
| Doctors | DoctorID | Đơn | Không thể có (PK đơn) |
| Appointments | AppointmentID | Đơn | Không thể có (PK đơn) |
| Invoices | InvoiceID | Đơn | Không thể có (PK đơn) |

**Phân tích chi tiết bảng Doctors (có FK):**
```
Doctors(DoctorID, DoctorName, DepartmentID, Specialty)
         PK

FD (Phụ thuộc hàm):
  DoctorID → DoctorName       ✅ Phụ thuộc đầy đủ vào PK
  DoctorID → DepartmentID     ✅ Phụ thuộc đầy đủ vào PK
  DoctorID → Specialty         ✅ Phụ thuộc đầy đủ vào PK
```

**Phân tích chi tiết bảng Appointments (có 2 FK):**
```
Appointments(AppointmentID, DoctorID, PatientID, AppointmentDate, AppointmentTime)
               PK

FD:
  AppointmentID → DoctorID          ✅ Phụ thuộc đầy đủ vào PK
  AppointmentID → PatientID         ✅ Phụ thuộc đầy đủ vào PK
  AppointmentID → AppointmentDate   ✅ Phụ thuộc đầy đủ vào PK
  AppointmentID → AppointmentTime   ✅ Phụ thuộc đầy đủ vào PK

Lưu ý: (DoctorID, AppointmentDate, AppointmentTime) là UNIQUE INDEX
        nhưng KHÔNG phải Primary Key → không ảnh hưởng 2NF
```

**✅ Kết luận 2NF:** Tất cả PK đều là đơn → **ĐẠT CHUẨN 2NF**

---

## 3. DẠNG CHUẨN 3 (3NF - Third Normal Form)

**Điều kiện:** Đạt 2NF + Không có phụ thuộc hàm bắc cầu (transitive dependency).
> Phụ thuộc bắc cầu: A → B → C (A là PK, B không phải PK, C phụ thuộc vào B thay vì A)

### Bảng Departments
```
Departments(DepartmentID, DepartmentName)
              PK

FD: DepartmentID → DepartmentName
Kiểm tra: DepartmentName phụ thuộc trực tiếp vào PK ✅
Không có thuộc tính trung gian → Không có phụ thuộc bắc cầu ✅
```

### Bảng Patients
```
Patients(PatientID, PatientName, DateOfBirth, Gender, Address, PhoneNumber)
           PK

FD:
  PatientID → PatientName    (trực tiếp vào PK) ✅
  PatientID → DateOfBirth    (trực tiếp vào PK) ✅
  PatientID → Gender         (trực tiếp vào PK) ✅
  PatientID → Address        (trực tiếp vào PK) ✅
  PatientID → PhoneNumber    (trực tiếp vào PK) ✅

Kiểm tra bắc cầu:
  - Gender KHÔNG xác định các thuộc tính khác ✅
  - Address KHÔNG xác định các thuộc tính khác ✅
  - Không tồn tại: PatientID → X → Y (với X không phải PK) ✅
```

### Bảng Doctors
```
Doctors(DoctorID, DoctorName, DepartmentID, Specialty)
          PK                      FK

FD:
  DoctorID → DoctorName       (trực tiếp) ✅
  DoctorID → DepartmentID     (trực tiếp) ✅
  DoctorID → Specialty         (trực tiếp) ✅

Kiểm tra bắc cầu tiềm năng:
  DoctorID → DepartmentID → DepartmentName ?
  
  ⚠️ DepartmentName KHÔNG nằm trong bảng Doctors!
  DepartmentName nằm ở bảng Departments (tham chiếu qua FK).
  → Đây chính là cách chuẩn hóa đúng: tách thông tin khoa ra bảng riêng.
  → KHÔNG có phụ thuộc bắc cầu ✅
```

### Bảng Appointments
```
Appointments(AppointmentID, DoctorID, PatientID, AppointmentDate, AppointmentTime)
                PK              FK        FK

FD:
  AppointmentID → DoctorID          (trực tiếp) ✅
  AppointmentID → PatientID         (trực tiếp) ✅
  AppointmentID → AppointmentDate   (trực tiếp) ✅
  AppointmentID → AppointmentTime   (trực tiếp) ✅

Kiểm tra bắc cầu:
  - DoctorID → DoctorName? DoctorName KHÔNG nằm trong bảng này ✅
  - PatientID → PatientName? PatientName KHÔNG nằm trong bảng này ✅
  - Bảng CHỈ chứa ID tham chiếu, không lưu trùng dữ liệu ✅
```

### Bảng Invoices
```
Invoices(InvoiceID, PatientID, InvoiceDate, TotalAmount)
           PK          FK

FD:
  InvoiceID → PatientID      (trực tiếp) ✅
  InvoiceID → InvoiceDate    (trực tiếp) ✅
  InvoiceID → TotalAmount    (trực tiếp) ✅

Kiểm tra bắc cầu:
  - PatientID → PatientName? PatientName KHÔNG nằm trong bảng này ✅
  - Không có thuộc tính non-key phụ thuộc vào thuộc tính non-key khác ✅
```

**✅ Kết luận 3NF:** Không có phụ thuộc bắc cầu → **ĐẠT CHUẨN 3NF**

---

## 4. TỔNG KẾT

```
                        ┌─────────────┐
                   ┌───→│ Departments │
                   │    │ (PK: DeptID)│
                   │    └─────────────┘
                   │ FK
            ┌──────┴──────┐
            │   Doctors   │
            │ (PK: DocID) │
            └──────┬──────┘
                   │ FK
  ┌────────────┐   │    ┌──────────────┐
  │  Patients  │───┼───→│ Appointments │
  │(PK: PatID) │   │    │  (PK: AptID) │
  └──────┬─────┘        └──────────────┘
         │ FK
    ┌────┴─────┐
    │ Invoices │
    │(PK:InvID)│
    └──────────┘
```

| Chuẩn | Điều kiện | Đạt? | Lý do |
|-------|-----------|------|-------|
| **1NF** | Giá trị nguyên tử, có PK | ✅ | Tất cả cột đều atomic, mỗi bảng có PK |
| **2NF** | Không phụ thuộc bộ phận | ✅ | Tất cả PK đều đơn (single-column) |
| **3NF** | Không phụ thuộc bắc cầu | ✅ | Dữ liệu được tách đúng qua FK, không lưu trùng |

> **Thiết kế cơ sở dữ liệu Hospital Management System đạt chuẩn 3NF.**
> Mỗi thuộc tính non-key phụ thuộc trực tiếp và đầy đủ vào khóa chính,
> thông tin liên quan được tách sang bảng riêng và liên kết qua Foreign Key.
