@echo off
title Building FolderCreator.exe
echo.
echo  ============================================
echo   Building FolderCreator.exe
echo  ============================================
echo.

if not exist ".venv\Scripts\activate.bat" (
    echo  [ERROR] Run setup.bat first.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
pip install pyinstaller >nul

pyinstaller ^
  --noconfirm ^
  --onedir ^
  --windowed ^
  --name "FolderCreator" ^
  --add-data "config.json;." ^
  --hidden-import "rapidocr_onnxruntime" ^
  --hidden-import "onnxruntime" ^
  --hidden-import "cv2" ^
  --hidden-import "PIL" ^
  --hidden-import "customtkinter" ^
  --hidden-import "watchdog.observers.winapi" ^
  --hidden-import "winotify" ^
  --collect-all "rapidocr_onnxruntime" ^
  --collect-all "onnxruntime" ^
  --collect-all "customtkinter" ^
  main.py

echo.
echo  ============================================
echo   Done! Output: dist\FolderCreator\
echo  ============================================
pause
