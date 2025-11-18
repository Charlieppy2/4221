# 快速啟動指南 🚀

## 第一步：設置後端

### 1. 打開終端/命令提示符，進入後端目錄
```bash
cd backend
```

### 2. 創建虛擬環境（如果還沒有）
```bash
python -m venv venv
```

### 3. 激活虛擬環境

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. 安裝依賴
```bash
pip install -r requirements.txt
```

### 5. 創建必要的文件夾
```bash
# Windows
mkdir uploads results masked_images models

# Mac/Linux
mkdir -p uploads results masked_images models
```

### 6. 啟動後端服務器
```bash
python app.py
```

✅ **成功的話會看到：**
```
 * Running on http://0.0.0.0:5000
```

**保持這個終端窗口打開！**

---

## 第二步：設置前端

### 1. 打開**另一個**終端窗口，進入前端目錄
```bash
cd frontend
```

### 2. 安裝依賴（第一次運行需要）
```bash
npm install
```

### 3. 啟動前端開發服務器
```bash
npm start
```

✅ **成功的話會：**
- 自動打開瀏覽器
- 顯示 `http://localhost:3000`
- 看到應用界面

---

## 第三步：查看應用

### 在瀏覽器中訪問：
🌐 **http://localhost:3000**

### 你應該看到：
- ✅ 智能文檔識別系統的標題
- ✅ 上傳文檔區域
- ✅ 識別結果區域

---

## 測試應用

### 1. 上傳一張圖片
- 點擊「點擊上傳」按鈕
- 或拖放圖片到上傳區域
- 選擇一張文檔圖片（PNG、JPG、JPEG）

### 2. 等待識別
- 會顯示進度條
- 處理完成後顯示結果

---

## 常見問題

### ❌ 問題1: 後端啟動失敗

**錯誤：ModuleNotFoundError**

**解決方法：**
```bash
# 確保虛擬環境已激活
# 重新安裝依賴
pip install -r requirements.txt
```

### ❌ 問題2: 前端啟動失敗

**錯誤：npm不是內部或外部命令**

**解決方法：**
1. 安裝 Node.js: https://nodejs.org/
2. 重新打開終端
3. 再次運行 `npm install`

### ❌ 問題3: 端口被占用

**錯誤：Port 3000 is already in use**

**解決方法：**
- 關閉其他使用3000端口的程序
- 或修改端口（在 `package.json` 中）

### ❌ 問題4: 後端連接失敗

**錯誤：無法連接到後端**

**解決方法：**
1. 確保後端正在運行（終端1）
2. 檢查後端是否在 `http://localhost:5000` 運行
3. 在瀏覽器訪問 `http://localhost:5000` 測試

---

## 快速檢查清單

- [ ] 後端虛擬環境已創建並激活
- [ ] 後端依賴已安裝
- [ ] 後端文件夾已創建（uploads, results等）
- [ ] 後端服務器正在運行（終端1）
- [ ] 前端依賴已安裝（npm install）
- [ ] 前端服務器正在運行（終端2）
- [ ] 瀏覽器已打開 http://localhost:3000

---

## 需要幫助？

如果遇到問題，檢查：
1. 兩個終端窗口是否都在運行
2. 端口是否被占用
3. 依賴是否正確安裝
4. 查看終端的錯誤信息

