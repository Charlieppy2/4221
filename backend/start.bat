@echo off
echo ====================================
echo 啟動後端服務器
echo ====================================
echo.

REM 檢查虛擬環境是否存在
if not exist "venv" (
    echo 創建虛擬環境...
    python -m venv venv
)

REM 激活虛擬環境
echo 激活虛擬環境...
call venv\Scripts\activate.bat

REM 創建必要的目錄
echo 創建必要的目錄...
if not exist "uploads" mkdir uploads
if not exist "results" mkdir results
if not exist "masked_images" mkdir masked_images
if not exist "models" mkdir models

REM 檢查依賴是否已安裝
echo 檢查依賴...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo 安裝依賴...
    pip install -r requirements.txt
)

REM 啟動服務器
echo.
echo ====================================
echo 啟動 Flask 服務器...
echo ====================================
echo 後端將在 http://localhost:5000 運行
echo 按 Ctrl+C 停止服務器
echo.
python app.py

pause

