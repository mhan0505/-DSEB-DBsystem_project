# 📖 HƯỚNG DẪN SỬ DỤNG GIT & GITHUB CHO NGƯỜI MỚI

> **Dành cho:** Team members chưa biết Git  
> **Thời gian đọc:** 10 phút  
> **Repo:** https://github.com/mhan0505/-DSEB-DBsystem_project.git

---

## 📋 MỤC LỤC

1. [Cài đặt Git](#1--cài-đặt-git)
2. [Cấu hình lần đầu](#2--cấu-hình-lần-đầu)
3. [Clone repo về máy](#3--clone-repo-về-máy)
4. [Quy trình làm việc hàng ngày](#4--quy-trình-làm-việc-hàng-ngày)
5. [Tạo branch riêng](#5--tạo-branch-riêng-quan-trọng)
6. [Commit và Push code](#6--commit-và-push-code)
7. [Pull code mới từ team](#7--pull-code-mới-từ-team)
8. [Merge và Pull Request](#8--merge-và-pull-request)
9. [Xử lý lỗi thường gặp](#9--xử-lý-lỗi-thường-gặp)
10. [Lệnh Git tóm tắt](#10--bảng-tóm-tắt-lệnh)

---

## 1. 🔧 Cài đặt Git

### Windows:
1. Vào https://git-scm.com/download/win
2. Tải file `.exe` và cài đặt
3. Khi cài, **chọn mặc định** tất cả (cứ Next → Next → Install)
4. Sau khi cài xong, mở **PowerShell** hoặc **Command Prompt**, gõ:

```bash
git --version
```

Nếu thấy `git version 2.x.x` → ✅ Cài thành công!

---

## 2. ⚙️ Cấu hình lần đầu

Mở **PowerShell** (hoặc Terminal), chạy 2 lệnh này (thay tên và email của bạn):

```bash
git config --global user.name "Tên Của Bạn"
git config --global user.email "email_cua_ban@gmail.com"
```

> ⚠️ **Email phải trùng** với email đăng ký GitHub!

Kiểm tra lại:
```bash
git config --global --list
```

---

## 3. 📥 Clone repo về máy

**Clone = tải toàn bộ project từ GitHub về máy tính của bạn.**

### Bước 1: Mở PowerShell, di chuyển đến thư mục muốn lưu project

```bash
cd D:\DSEB
```

> Bạn có thể thay `D:\DSEB` bằng bất kỳ thư mục nào bạn muốn.

### Bước 2: Clone repo

```bash
git clone https://github.com/mhan0505/-DSEB-DBsystem_project.git
```

### Bước 3: Vào thư mục project

```bash
cd -DSEB-DBsystem_project
```

✅ Done! Bạn đã có toàn bộ code trên máy.

---

## 4. 🔄 Quy trình làm việc hàng ngày

```
┌─────────────────────────────────────────────────────┐
│                  QUY TRÌNH LÀM VIỆC                  │
│                                                       │
│   1. git pull              ← Lấy code mới nhất        │
│   2. Viết code / sửa file  ← Làm việc của mình       │
│   3. git add .             ← Chọn files đã sửa       │
│   4. git commit -m "..."   ← Lưu thay đổi            │
│   5. git push              ← Đẩy lên GitHub          │
│                                                       │
│   ⚠️ LUÔN PULL TRƯỚC KHI LÀM VIỆC!                  │
└─────────────────────────────────────────────────────┘
```

### Chi tiết:

```bash
# Bước 1: MỞ ĐẦU NGÀY → Lấy code mới nhất từ team
git pull origin main

# Bước 2: Viết code (sửa files trong VS Code / PyCharm / ...)

# Bước 3: Xem mình đã sửa gì
git status

# Bước 4: Thêm tất cả files đã sửa vào "staging"
git add .

# Bước 5: Lưu lại (commit) với mô tả ngắn
git commit -m "Implement patient_repository get_all method"

# Bước 6: Đẩy lên GitHub
git push origin main
```

---

## 5. 🌿 Tạo Branch riêng (QUAN TRỌNG!)

**Branch = nhánh riêng để mỗi người làm việc không ảnh hưởng nhau.**

> 🎯 **Quy tắc nhóm:** Mỗi người tạo 1 branch riêng, KHÔNG code trực tiếp trên `main`!

### Tạo branch mới:

```bash
# Tạo branch và chuyển sang branch đó
git checkout -b ten-cua-ban

# Ví dụ:
git checkout -b member1-patient
git checkout -b member2-doctor
git checkout -b member3-appointment
git checkout -b member4-invoice
git checkout -b member5-tests
```

### Xem đang ở branch nào:

```bash
git branch
```

Kết quả (dấu * là branch hiện tại):
```
  main
* member1-patient
```

### Chuyển giữa các branch:

```bash
# Chuyển về main
git checkout main

# Chuyển sang branch của mình
git checkout member1-patient
```

### Push branch lên GitHub:

```bash
# Lần đầu push branch mới
git push -u origin member1-patient

# Các lần sau chỉ cần
git push
```

---

## 6. 💾 Commit và Push code

### Commit là gì?
**Commit = "lưu game"** 🎮 Mỗi commit là 1 điểm bạn có thể quay lại.

### Cách viết commit message tốt:

```bash
# ❌ Không tốt:
git commit -m "update"
git commit -m "fix"
git commit -m "abc"

# ✅ Tốt:
git commit -m "Implement get_all method in PatientRepository"
git commit -m "Add TODO SQL for create table Departments"
git commit -m "Fix database connection error in config.py"
git commit -m "Complete test_double_booking test cases"
```

### Quy tắc commit message:
- Viết bằng tiếng Anh (hoặc tiếng Việt không dấu)
- Bắt đầu bằng động từ: `Add`, `Fix`, `Implement`, `Update`, `Remove`
- Ngắn gọn, mô tả rõ đã làm gì

### Ví dụ workflow đầy đủ:

```bash
# Sửa xong file patient_repository.py
git status
# → modified: src/repositories/patient_repository.py

git add src/repositories/patient_repository.py
# Hoặc add tất cả: git add .

git commit -m "Implement CRUD methods in PatientRepository"

git push
```

---

## 7. 📩 Pull code mới từ team

### Khi nào cần pull?
- **Đầu mỗi ngày** trước khi bắt đầu code
- Khi teammate nói "mình đã push code mới"
- Trước khi push code của mình

```bash
# Lấy code mới nhất từ main
git pull origin main
```

### Nếu bị CONFLICT (xung đột):

```
CONFLICT (content): Merge conflict in src/config.py
```

**Đây là khi 2 người sửa cùng 1 file!** Cách xử lý:

1. Mở file bị conflict trong VS Code
2. Bạn sẽ thấy:
```
<<<<<<< HEAD
code_cua_ban
=======
code_cua_teammate
>>>>>>> origin/main
```
3. **Chọn** giữ code nào (hoặc gộp cả 2)
4. Xóa các dòng `<<<<<<`, `=======`, `>>>>>>>`
5. Save file
6. Commit lại:
```bash
git add .
git commit -m "Resolve merge conflict in config.py"
git push
```

> 💡 **Tip:** Để tránh conflict, mỗi người nên làm **file khác nhau**!

---

## 8. 🔀 Merge và Pull Request

### Khi nào merge?
Khi bạn đã code xong phần của mình trên branch riêng và muốn gộp vào `main`.

### Cách 1: Merge trên GitHub (Khuyến nghị cho người mới)

1. Push branch của bạn lên GitHub:
```bash
git push origin member1-patient
```

2. Vào GitHub: https://github.com/mhan0505/-DSEB-DBsystem_project

3. Bạn sẽ thấy nút **"Compare & pull request"** → Click vào

4. Viết mô tả ngắn về những gì bạn đã làm

5. Click **"Create pull request"**

6. Nhờ team lead (hoặc tự mình) click **"Merge pull request"**

### Cách 2: Merge bằng command (nâng cao)

```bash
# Chuyển về main
git checkout main

# Lấy code mới nhất
git pull origin main

# Merge branch của mình vào main
git merge member1-patient

# Push lên
git push origin main
```

---

## 9. 🚨 Xử lý lỗi thường gặp

### Lỗi 1: "fatal: not a git repository"
```
fatal: not a git repository (or any of the parent directories)
```
**Nguyên nhân:** Bạn chưa ở trong thư mục project.  
**Fix:** `cd` vào đúng thư mục:
```bash
cd D:\DSEB\-DSEB-DBsystem_project
```

### Lỗi 2: "failed to push some refs"
```
error: failed to push some refs to '...'
hint: Updates were rejected because the remote contains work that you do not have locally.
```
**Nguyên nhân:** Teammate đã push code mới mà bạn chưa pull.  
**Fix:** Pull trước rồi push lại:
```bash
git pull origin main
# Giải quyết conflict nếu có
git push origin main
```

### Lỗi 3: "Permission denied"
```
remote: Permission to ... denied to ...
```
**Nguyên nhân:** Bạn chưa được thêm vào repo.  
**Fix:** Nhờ owner (mhan0505) vào **Settings → Collaborators → Add people** và nhập GitHub username của bạn.

### Lỗi 4: "Your branch is behind"
```
Your branch is behind 'origin/main' by 3 commits
```
**Fix:**
```bash
git pull origin main
```

### Lỗi 5: Muốn HỦY thay đổi chưa commit
```bash
# Hủy thay đổi trên 1 file (chưa add)
git checkout -- ten_file.py

# Hủy tất cả thay đổi (chưa add)
git checkout -- .

# Đã add rồi, muốn bỏ staging
git reset HEAD ten_file.py

# Đã commit rồi, muốn quay lại commit trước
git reset --soft HEAD~1
```

### Lỗi 6: Đẩy nhầm file nhạy cảm (password, key)
```bash
# Xóa file khỏi git (giữ trên máy)
git rm --cached ten_file_nham
git commit -m "Remove sensitive file"
git push
```
> Sau đó thêm file đó vào `.gitignore`

---

## 10. 📋 Bảng tóm tắt lệnh

| Lệnh | Mô tả | Khi nào dùng |
|-------|--------|-------------|
| `git clone <url>` | Tải repo về máy | Lần đầu tiên |
| `git pull origin main` | Lấy code mới | ⭐ Đầu mỗi ngày |
| `git status` | Xem files đã sửa | Trước khi commit |
| `git add .` | Thêm tất cả files | Trước khi commit |
| `git add <file>` | Thêm 1 file cụ thể | Khi chỉ muốn commit 1 file |
| `git commit -m "..."` | Lưu thay đổi | Sau khi add |
| `git push` | Đẩy lên GitHub | Sau khi commit |
| `git branch` | Xem danh sách branch | Kiểm tra branch |
| `git checkout -b <name>` | Tạo branch mới | Bắt đầu task mới |
| `git checkout <name>` | Chuyển branch | Đổi sang branch khác |
| `git log --oneline -5` | Xem 5 commit gần nhất | Kiểm tra lịch sử |
| `git diff` | Xem chi tiết thay đổi | Debug, review |

---

## 🎯 PHÂN CÔNG & BRANCH CHO TỪNG NGƯỜI

| Thành viên | Branch name | Files phụ trách |
|------------|-------------|-----------------|
| Member 1 | `member1-database` | `database/scripts/01-03` (DDL + Data) |
| Member 2 | `member2-advanced-sql` | `database/scripts/04-08` (Views, Procs, Triggers) |
| Member 3 | `member3-python-core` | `src/models/`, `src/repositories/`, `src/database_connection.py` |
| Member 4 | `member4-services-cli` | `src/services/`, `src/cli/` |
| Member 5 | `member5-tests-docs` | `tests/`, `docs/`, `database/scripts/09` |

### Mỗi người tạo branch:
```bash
git checkout -b member1-database     # Member 1
git checkout -b member2-advanced-sql  # Member 2
git checkout -b member3-python-core   # Member 3
git checkout -b member4-services-cli  # Member 4
git checkout -b member5-tests-docs    # Member 5
```

---

## 💡 TIPS CHO NEWBIE

1. **LUÔN PULL TRƯỚC KHI LÀM VIỆC** → tránh conflict
2. **Commit thường xuyên** → dễ rollback nếu có lỗi
3. **Mỗi commit = 1 việc** → không gộp nhiều thay đổi vào 1 commit
4. **Đọc error message** → Git thường gợi ý cách fix ngay trong lỗi
5. **Không sợ sai** → Git có thể quay lại bất kỳ thời điểm nào
6. **Hỏi team lead** khi không chắc chắn → tốt hơn là làm sai

---

## 🆘 CẦN GIÚP?

- Hỏi team lead
- Google: "git [tên lỗi]"
- Xem video: YouTube search "Git cơ bản tiếng Việt"
- Trang cheat sheet: https://education.github.com/git-cheat-sheet-education.pdf
