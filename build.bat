@echo off
title Building FolderCreator.exe (Obfuscated & Encrypted)
echo.
echo  ============================================
echo   Building FolderCreator.exe (PyArmor Obfuscated)
echo  ============================================
echo.

if not exist ".venv\Scripts\activate.bat" (
    echo  [ERROR] Run setup.bat first.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
taskkill /f /im FolderCreator.exe >nul 2>&1
pip install pyarmor pyinstaller >nul

echo  [1/3] Obfuscating source code with PyArmor...
if exist "build_obf" rmdir /s /q "build_obf"
python -m pyarmor.cli gen -O build_obf -r main.py app/

if not exist "build_obf\main.py" (
    echo  [ERROR] PyArmor obfuscation failed.
    pause
    exit /b 1
)

echo  [2/3] Compiling executable with PyInstaller...
pyinstaller ^
  --noconfirm ^
  --onedir ^
  --windowed ^
  --name "FolderCreator" ^
  --paths "build_obf" ^
  --add-data "config.json;." ^
  --add-data "build_obf\app;app" ^
  --add-data "build_obf\pyarmor_runtime_000000;pyarmor_runtime_000000" ^
  --hidden-import "app" ^
  --hidden-import "app.config" ^
  --hidden-import "app.constants" ^
  --hidden-import "app.models.job" ^
  --hidden-import "app.models.result" ^
  --hidden-import "app.services.crop_service" ^
  --hidden-import "app.services.folder_service" ^
  --hidden-import "app.services.logger_service" ^
  --hidden-import "app.services.notifier" ^
  --hidden-import "app.services.ocr_engine" ^
  --hidden-import "app.services.queue_service" ^
  --hidden-import "app.services.usb_monitor" ^
  --hidden-import "app.services.validator" ^
  --hidden-import "app.services.watch_service" ^
  --hidden-import "app.viewmodels.app_viewmodel" ^
  --hidden-import "app.views.dashboard_tab" ^
  --hidden-import "app.views.history_tab" ^
  --hidden-import "app.views.large_display_window" ^
  --hidden-import "app.views.main_window" ^
  --hidden-import "app.views.settings_tab" ^
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
  build_obf\main.py

echo  [3/3] Setting up distribution folders...
if exist "dist\FolderCreator\" (
    mkdir "dist\FolderCreator\Sticker\Processed" >nul 2>&1
    mkdir "dist\FolderCreator\Sticker\Failed" >nul 2>&1
    mkdir "dist\FolderCreator\Logs" >nul 2>&1
)

echo.
echo  ============================================
echo   Done! Obfuscated Executable: dist\FolderCreator\
echo  ============================================
pause
