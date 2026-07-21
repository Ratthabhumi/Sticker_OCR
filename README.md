# 💽 Sticker OCR — Disk Sanitization Assistant

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078D6.svg)](https://microsoft.com/windows)
[![Release](https://img.shields.io/badge/Release-v1.0.0-green.svg)](https://github.com/Ratthabhumi/Sticker_OCR/releases/tag/v1.0.0)
[![OCR Engine](https://img.shields.io/badge/OCR-RapidOCR%20(ONNX)-orange.svg)](https://github.com/RapidAI/RapidOCR)

**Disk Sanitization Assistant** คือโปรแกรมช่วยอำนวยความสะดวกสำหรับกระบวนการล้างข้อมูลเครื่องคอมพิวเตอร์โน้ตบุ๊ก (Disk Sanitization) โดยจะเฝ้าดูรูปถ่ายสติ๊กเกอร์เครื่อง และสแกนหา **Serial Number (S/N)** กับ **Device ID (ID No.)** ด้วยระบบ **RapidOCR (ONNX Runtime)** แบบความเร็วสูง เพื่อสร้างโฟลเดอร์ปลายทาง `USB:\<SN>(<ID>)\Picture\` บน Flashdrive / USB External Drive อัตโนมัติทันที

---

## ✨ Features (คุณสมบัติเด่น)

- ⚡ **High-Speed ONNX OCR Engine:** ใช้ RapidOCR สแกนตัวอักษรภาษาอังกฤษและตัวเลขแม่นยำสูง รวดเร็ว ไม่ต้องลง C++ Runtime หรือโปรแกรมเสริม
- 💾 **Smart USB Drive Detection & Manual Select:** สแกนตรวจจับไดร์ฟ USB (เช่น DiskDeleter, Flash Drive, External HDD) อัตโนมัติ พร้อมเมนู Dropdown เลือก Target Drive ด้วยตนเองหากเสียบ USB พร้อมกันหลายตัว
- 🖼️ **Interactive Preview & Fullscreen Zoom:** แสดงตัวอย่างรูปภาพขนาดใหญ่ (`860x540`) พร้อมปุ่ม Zoom ขยายรูปภาพคมชัดระดับ HD และรองรับการแก้ไขข้อมูล Real-time
- 🧹 **Real-Time Input Sanitization:** ดักจับและลบอักขระต้องห้ามของระบบปฏิบัติการ Windows (`\ / : * ? " < > |`) ออกจาก S/N และ ID อัตโนมัติ เพื่อป้องกันระบบสร้างโฟลเดอร์พัง
- 🔒 **File Lock Race Condition Recovery:** มีระบบ Retry Loop เมื่อบันทึกภาพจากโปรแกรมภายนอก (เช่น LINE PC) พร้อมระบบสำรอง Copy-fallback หากไฟล์โดนเปิดค้างไว้
- 🛡️ **Disk Space Protection:** ตรวจเช็คพื้นที่ว่างบน USB ก่อนสร้างโฟลเดอร์เสมอ (ป้องกันปัญหา Flashdrive พื้นที่เต็ม)
- 📊 **CSV Audit Logging:** บันทึกประวัติการทำงานประจำวันเป็นไฟล์ CSV ละเอียดในโฟลเดอร์ `Logs/`
- 🖥️ **Large Display Mode (F11):** โหมดตัวหนังสือยักษ์เต็มหน้าจอสำหรับช่างเทคนิคที่ต้องการมองเห็น S/N และ ID ชัดเจนจากระยะไกล

---

## 📸 Workflow การทำงาน

```mermaid
graph TD
    A[เสียบ USB Flashdrive / External HDD] --> B[วางรูปสติ๊กเกอร์ในโฟลเดอร์ Sticker/]
    B --> C[RapidOCR สแกน S/N และ ID No.]
    C --> D[แสดงหน้าต่าง Preview ให้ตรวจสอบความถูกต้อง]
    D -->|กด Confirm| E[สร้างโฟลเดอร์ USB:\<SN>(<ID>)\Picture\]
    E --> F[ย้ายรูปไปโฟลเดอร์ Sticker/Processed/]
    D -->|กด Skip| G[ย้ายรูปไปโฟลเดอร์ Sticker/Failed/]
```

---

## 🚀 Quick Download & Running (.exe)

ไม่ต้องติดตั้ง Python! ดาวน์โหลดแพ็กเกจสำเร็จรูปไปใช้งานได้ทันที:

1. ดาวน์โหลดไฟล์ **`FolderCreator.zip`** จาก [GitHub Releases v1.0.0](https://github.com/Ratthabhumi/Sticker_OCR/releases/tag/v1.0.0)
2. แตกไฟล์ ZIP ออกมา จะได้โฟลเดอร์ `FolderCreator`
3. ดับเบิลคลิกเปิดใช้งาน **`FolderCreator.exe`** ได้ทันที

---

## ⌨️ Shortcut Keys (คีย์ลัด)

| Key | Action |
|-----|--------|
| **F11** | เปิด / ปิด โหมดตัวหนังสือยักษ์เต็มหน้าจอ (Large Display Mode) |
| **ESC** | ปิดหน้าต่าง Zoom รูปภาพ หรือออกจากโหมดเต็มหน้าจอ |

---

## 🛠️ Developer Setup (สำหรับนักพัฒนา)

### 1. Prerequisite
- Python 3.10 ขึ้นไป
- Windows 10 / 11

### 2. Installation & Run

```powershell
# Clone repository
git clone https://github.com/Ratthabhumi/Sticker_OCR.git
cd Sticker_OCR

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run Application
python main.py
```

### 3. Build Standalone Executable

```powershell
.\build.bat
```

---

## 📁 Project Structure

```
Sticker_OCR/
├── main.py                   # Main Application Entry Point
├── build.bat                 # Automated PyInstaller Executable Builder
├── config.json               # Application Configuration
├── requirements.txt          # Dependencies
├── app/
│   ├── config.py             # Config Manager
│   ├── constants.py          # App Constants & UI Colors
│   ├── models/               # Data Models (Job, OCRResult, FolderResult)
│   ├── services/             # Core Services (OCR Engine, USB Monitor, File Watcher, Validator)
│   ├── viewmodels/           # MVVM ViewModel State & Logic
│   └── views/                # UI Views (Main Window, Dashboard, History, Settings, Zoom Dialog)
├── Sticker/                  # Input Folder for Sticker Images
│   ├── Processed/            # Successfully processed images
│   └── Failed/               # Failed / skipped images
└── Logs/                     # Daily CSV Log files
```

---

## 🔒 Code Protection & Reverse Engineering Note

> [!WARNING]
> **ความปลอดภัยของไฟล์ Executable (.exe):**
> โปรแกรมนี้ถูกคอมไพล์ด้วย **PyInstaller** ซึ่งเป็นการแพ็กรวม Python Bytecode (`.pyc`) เข้ามาไว้ในชุดโปรแกรม ผู้ใช้งานที่มีความรู้ด้านเทคนิคสามารถใช้เครื่องมือประเภท Decompiler (เช่น `pyinstxtractor` + `pycdc`) ถอดรหัสไฟล์ `.pyc` กลับมาเป็น Python Source Code ได้
> 
> หากต้องการป้องกันไม่ให้ผู้อื่นนำซอร์สโค้ดไปพัฒนาต่อหรือคัดลอก Logic โปรแกรม แนะนำให้ใช้โซลูชัน **Code Obfuscation** เช่น:
> - **[PyArmor](https://github.com/dashingsoft/pyarmor):** แปลงโค้ด Python เป็น Native C Extension (`.pyd`) ก่อนนำไปสร้าง `.exe` (ป้องกันการถอดโค้ดได้ 100%)
> - **Cython:** คอมไพล์ไฟล์ `.py` ที่สำคัญให้กลายเป็นไดนามิกลิงก์ไลบรารี C (`.pyd`)

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
