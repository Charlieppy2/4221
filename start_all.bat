@echo off
echo ====================================
echo 啟動完整應用
echo ====================================
echo.
echo 這將啟動兩個服務器：
echo 1. 後端服務器 (端口 5000)
echo 2. 前端服務器 (端口 3000)
echo.
echo 請確保：
echo - Python 已安裝
echo - Node.js 已安裝
echo.
pause

REM 啟動後端（在新窗口）
echo 啟動後端服務器...
start "後端服務器" cmd /k "cd backend && start.bat"

REM 等待幾秒讓後端啟動
timeout /t 3 /nobreak >nul

REM 啟動前端（在新窗口）
echo 啟動前端服務器...
start "前端服務器" cmd /k "cd frontend && start.bat"

echo.
echo ====================================
echo 兩個服務器已啟動！
echo ====================================
echo.
echo 後端: http://localhost:5000
echo 前端: http://localhost:3000
echo.
echo 瀏覽器應該會自動打開前端頁面
echo 如果沒有，請手動訪問 http://localhost:3000
echo.
echo 關閉服務器：關閉對應的命令窗口
echo.
pause

