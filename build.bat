@echo off
title Building FolderCreator.exe
echo.
echo  ============================================
echo   Building FolderCreator.exe (onedir mode)
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
  --hidden-import "paddleocr" ^
  --hidden-import "paddle" ^
  --hidden-import "sklearn" ^
  --hidden-import "skimage" ^
  --hidden-import "scipy" ^
  --hidden-import "cv2" ^
  --hidden-import "PIL" ^
  --hidden-import "customtkinter" ^
  --hidden-import "watchdog.observers.winapi" ^
  --hidden-import "winotify" ^
  --collect-all "paddleocr" ^
  --collect-all "paddle" ^
  --collect-all "customtkinter" ^
  main.py

echo.
echo  ============================================
echo   Done!  Output: dist\FolderCreator\
echo   Copy the entire FolderCreator\ folder.
echo  ============================================
pause
