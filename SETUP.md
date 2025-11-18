# 快速開始指南

## 項目設置步驟

### 1. 後端設置

```bash
# 進入後端目錄
cd backend

# 創建虛擬環境
python -m venv venv

# 激活虛擬環境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt

# 創建必要的目錄
mkdir uploads results masked_images models
```

### 2. 前端設置

```bash
# 進入前端目錄
cd frontend

# 安裝依賴
npm install

# 創建環境變量文件
copy .env.example .env
# 或 Linux/Mac:
# cp .env.example .env
```

### 3. 數據目錄設置

```bash
# 在項目根目錄
mkdir -p data/raw
mkdir -p data/processed

# 創建類別目錄
mkdir -p data/raw/identity_card
mkdir -p data/raw/utility_bill
mkdir -p data/raw/bank_statement
mkdir -p data/raw/address_proof
mkdir -p data/raw/lease_agreement
mkdir -p data/raw/other
```

### 4. 啟動應用

#### 啟動後端（終端1）
```bash
cd backend
python app.py
```

#### 啟動前端（終端2）
```bash
cd frontend
npm start
```

### 5. 訪問應用

- 前端: http://localhost:3000
- 後端API: http://localhost:5000

## 注意事項

1. **PaddleOCR安裝**：如果安裝失敗，可以嘗試：
   ```bash
   pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
   pip install paddleocr -i https://mirror.baidu.com/pypi/simple
   ```

2. **Google Maps API**：需要申請API Key並配置在 `.env` 文件中

3. **模型訓練**：首次運行需要先訓練模型，參考 `docs/PROJECT_GUIDE.md`

## 下一步

1. 收集數據（參考 `docs/DATA_COLLECTION.md`）
2. 訓練模型（參考 `model_training/train.py`）
3. 測試應用功能
4. 優化和部署

