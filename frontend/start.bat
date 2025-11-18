@echo off
echo ====================================
echo 啟動前端開發服務器
echo ====================================
echo.

REM 檢查 node_modules 是否存在
if not exist "node_modules" (
    echo 安裝依賴...
    call npm install
)

REM 啟動開發服務器
echo.
echo ====================================
echo 啟動 React 開發服務器...
echo ====================================
echo 前端將在 http://localhost:3000 運行
echo 瀏覽器會自動打開
echo 按 Ctrl+C 停止服務器
echo.
call npm start

pause

