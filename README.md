# Disk Sanitization Assistant

Automates folder creation for the laptop disk sanitization workflow.

## Requirements

- Windows 10 / 11
- Python 3.12+
- USB drive (FAT32 / exFAT / NTFS removable)

## Installation

```powershell
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

> **Note:** PaddleOCR downloads model weights (~100 MB) on first run.
> Ensure internet access for the initial launch.

## Running

```powershell
python main.py
```

## Workflow

1. Insert USB drive — app detects it automatically.
2. Drop sticker photo into `Sticker/` folder.
3. App runs OCR → shows preview dialog.
4. Edit S/N or ID if OCR was wrong, then click **Confirm**.
5. App creates `USB:\<SN>(<ID>)\Picture\` folder.
6. Image moves to `Sticker/Processed/`.
7. Windows notification confirms success.

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| F11 | Large Display Mode (fullscreen SN/ID for easy retyping) |
| ESC | Exit Large Display Mode |

## Folder Structure

```
Sticker_OCR/
├── main.py
├── config.json
├── requirements.txt
├── app/
│   ├── config.py
│   ├── constants.py
│   ├── models/
│   ├── services/
│   ├── viewmodels/
│   └── views/
├── Sticker/
│   ├── Processed/
│   └── Failed/
└── Logs/
```

## S/N and ID Format

| Field | Pattern | Example |
|-------|---------|---------|
| S/N   | `[A-Z0-9]{8}` | `PF3NL004` |
| ID No.| `\d{2}S-[A-Z]\d{3}` | `22S-A460` |
| Folder| `SN(ID)` | `PF3NL004(22S-A460)` |

## Retry Failed Images

Click **Retry Failed** on the Dashboard to move all images from
`Sticker/Failed/` back to `Sticker/` for reprocessing.

## Building the .exe

```powershell
pip install pyinstaller

pyinstaller `
  --noconfirm `
  --onefile `
  --windowed `
  --name "FolderCreator" `
  --add-data "config.json;." `
  --hidden-import paddleocr `
  --hidden-import paddle `
  --collect-all paddleocr `
  --collect-all paddle `
  main.py
```

The output `.exe` will be in the `dist/` folder.
Copy `config.json` next to `FolderCreator.exe` before distributing.

## Logging

Daily CSV logs are written to `Logs/log_YYYY-MM-DD.csv`:

```
Time,SN,ID,Folder,USB,Status,Error
15:30:01,PF3NL004,22S-A460,PF3NL004(22S-A460),E:\,Success,
15:31:05,PF3NL005,22S-A461,PF3NL005(22S-A461),E:\,Duplicate,
```
