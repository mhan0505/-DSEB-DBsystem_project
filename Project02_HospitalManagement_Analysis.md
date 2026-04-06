### 1. Phân tích Hệ thống và Yêu cầu (System Analysis and Requirements)

Đây là bước đầu tiên để xác định phạm vi và chức năng của hệ thống.

*   **Mục tiêu:** Số hóa quy trình bệnh viện, chăm sóc bệnh nhân, quản lý lịch hẹn và tối ưu hóa tài chính.

*   **Xác định các thực thể chính:**

    *   Bệnh nhân (Patients)

    *   Bác sĩ (Doctors)

    *   Khoa phòng (Departments)

    *   Lịch hẹn (Appointments)

    *   Hóa đơn tài chính (Invoices)

*   **Xác định chức năng chính (Main Functionalities):**

    *   Quản lý bệnh nhân (Thêm, sửa, xóa, tìm kiếm).

    *   Quản lý bác sĩ (Thêm, sửa thông tin và chuyên khoa).

    *   Quản lý khoa phòng (Định nghĩa và cập nhật).

    *   Đặt lịch hẹn và quản lý lịch khám.

    *   Tạo hóa đơn và theo dõi tài chính.

    *   Báo cáo (Thống kê lượt khám và giao dịch tài chính).


### 2. Thiết kế Cơ sở dữ liệu (Database Design)

Bước này chuyển đổi yêu cầu nghiệp vụ thành mô hình dữ liệu.

*   **Thiết kế mô hình dữ liệu (Data Model Design):**

    *   Vẽ sơ đồ thực thể kết hợp (ER Diagram).

    *   Chuyển đổi sơ đồ ER thành lược đồ cơ sở dữ liệu quan hệ (Relational Database Schema).

    *   Xác định rõ Khóa chính (PK), Khóa ngoại (FK) và các ràng buộc (Constraints).

*   **Xây dựng cấu trúc bảng (Table Structures):**

    Theo yêu cầu dự án, bạn cần tạo các bảng sau:

    1.  **Patients:** `PatientID, PatientName, DateOfBirth, Gender, Address, PhoneNumber`

    2.  **Doctors:** `DoctorID, DoctorName, DepartmentID, Specialty`

    3.  **Departments:** `DepartmentID, DepartmentName`

    4.  **Invoices:** `InvoiceID, PatientID, InvoiceDate, TotalAmount`

    5.  **Appointments:** `AppointmentID, DoctorID, PatientID, AppointmentDate, AppointmentTime`


### 3. Triển khai Cơ sở dữ liệu (Database Implementation)

Sử dụng **MySQL** để hiện thực hóa thiết kế.

*   **Tạo bảng và nhập liệu:**

    *   Viết script SQL tạo bảng theo cấu trúc trên.

    *   Populate (nhập) dữ liệu mẫu: Mỗi bảng từ 5-10 bản ghi đại diện.

    *   Sử dụng MySQL Workbench để sinh sơ đồ database.

*   **Tạo các đối tượng cơ sở dữ liệu nâng cao (Advanced Database Objects):**

    *   **Indexes:** Tạo chỉ mục để tăng tốc độ truy vấn.

    *   **Views:** Tạo view cho các truy vấn thường dùng (ví dụ: lịch hẹn trong ngày).

    *   **Stored Procedures:** Tự động hóa thao tác (quản lý lịch hẹn, tạo hóa đơn).

    *   **User Defined Functions (UDF):** Hàm tùy chỉnh cho tính toán (ví dụ: tính phí).

    *   **Triggers:** Tự động cập nhật dữ liệu liên quan khi có lịch hẹn hoặc hóa đơn mới.


### 4. Phát triển Ứng dụng Python (Python Application Development)

Xây dựng phần mềm tương tác với cơ sở dữ liệu.

*   **Kết nối Database:** Sử dụng `mysql-connector-python` hoặc `SQLAlchemy` để kết nối Python với MySQL.

*   **Quản lý dữ liệu:** Viết script Python để thực hiện CRUD (Thêm, sửa, xóa, đọc) cho bệnh nhân, bác sĩ, lịch hẹn.

*   **Báo cáo:** Phát triển các báo cáo thống kê và tài chính tự động.

*   **Giao diện:** Xây dựng giao diện dòng lệnh (CLI) hoặc giao diện đồ họa (GUI) để người dùng tương tác.


### 5. Bảo mật và Quản trị (Database Security and Administration)

Đảm bảo an toàn và hiệu suất cho hệ thống.

*   **Phân quyền:** Cấu hình vai trò người dùng (user roles), quyền hạn (permissions).

*   **Bảo mật:** Đề xuất và áp dụng các giải pháp bảo mật dữ liệu.

*   **Sao lưu và Phục hồi:** Implement quy trình backup và recovery.

*   **Tối ưu hóa:** Áp dụng các chiến lược tối ưu hiệu suất database.


### 6. Báo cáo và Bàn giao (Deliverables)

Hoàn thiện sản phẩm cuối cùng theo hướng dẫn của trường.

*   **Báo cáo:** Viết báo cáo comprehensive (20-30 trang) bao gồm phân tích, triển khai, kết luận và kiến nghị.

*   **Mã nguồn:** Submit toàn bộ script SQL, code Python đã được document đầy đủ.

*   **Sơ đồ:** Bao gồm các sơ đồ cơ sở dữ liệu.

*   **Kết luận:** Tóm tắt kết quả đạt được và đề xuất hướng phát triển trong tương lai.


Bạn cần tuân thủ đúng trình tự này để đảm bảo hệ thống được xây dựng robust (vững chắc) và đáp ứng đủ yêu cầu của môn học tại NEU-College of Technology.

