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
taskkill /f /im FolderCreator.exe >nul 2>&1
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

REM Automatically create Sticker, Processed, Failed, and Logs folders inside dist\FolderCreator\
if exist "dist\FolderCreator\" (
    mkdir "dist\FolderCreator\Sticker\Processed" >nul 2>&1
    mkdir "dist\FolderCreator\Sticker\Failed" >nul 2>&1
    mkdir "dist\FolderCreator\Logs" >nul 2>&1
)

echo.
echo  ============================================
echo   Done! Output: dist\FolderCreator\
echo  ============================================
pause
