# 項目開發指南

## 項目概述
智能文檔識別與信息提取系統 - 一個基於深度學習的文檔識別和信息提取應用

## 開發步驟

### 第一階段：環境設置（Week 1）

#### 1. 後端環境設置
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

#### 2. 前端環境設置
```bash
cd frontend
npm install
```

#### 3. 創建必要的目錄
```bash
mkdir -p backend/uploads
mkdir -p backend/results
mkdir -p backend/masked_images
mkdir -p backend/models
mkdir -p data/raw
mkdir -p data/processed
```

### 第二階段：數據收集（Week 1-2）

#### 數據收集建議
1. **身份證**：收集至少100-200張樣本（注意隱私，使用合成數據或公開數據集）
2. **水電費單**：收集CLP、HKE等公司的賬單樣本
3. **銀行賬單**：收集不同銀行的賬單樣本
4. **地址證明**：收集各種地址證明文件
5. **租約**：收集租約文件樣本
6. **其他**：其他常見文檔

#### 數據組織
將數據按照以下結構組織：
```
data/
  raw/
    identity_card/
      img1.jpg
      img2.jpg
      ...
    utility_bill/
      ...
  processed/
    (將由預處理腳本生成)
```

#### 運行數據預處理
```bash
cd model_training
python data_preprocessing.py
```

### 第三階段：模型訓練（Week 3-4）

#### 訓練模型
```bash
cd model_training
python train.py
```

#### 評估模型
```bash
python evaluate.py
```

### 第四階段：後端開發（Week 5-6）

#### 啟動後端服務
```bash
cd backend
python app.py
```

後端將在 http://localhost:5000 運行

#### API端點
- `GET /` - 健康檢查
- `POST /api/upload` - 上傳文件
- `POST /api/recognize` - 識別文檔
- `GET /api/results/<result_id>` - 獲取結果
- `GET /api/images/<filename>` - 獲取圖片

### 第五階段：前端開發（Week 7-8）

#### 啟動前端開發服務器
```bash
cd frontend
npm start
```

前端將在 http://localhost:3000 運行

#### 配置環境變量
創建 `frontend/.env` 文件：
```
REACT_APP_API_URL=http://localhost:5000
```

### 第六階段：整合與測試（Week 9）

1. 測試完整流程
2. 修復bug
3. 優化性能
4. 實現本地運行功能（加分項）

### 第七階段：交付準備（Week 10）

1. 錄製演示視頻
2. 撰寫報告
3. 準備交付文件

## 注意事項

### 數據來源標註
所有使用的數據必須標註來源，包括：
- 自行拍攝的數據
- 公開數據集（提供鏈接）
- 合成數據（說明生成方法）

### 模型部署
- 確保模型文件可以正常加載
- 測試API響應時間
- 優化模型大小（考慮使用TensorFlow Lite）

### 隱私保護
- 實現信息遮蔽功能
- 不存儲敏感信息
- 遵守數據保護法規

## 常見問題

### Q: PaddleOCR安裝失敗？
A: 嘗試使用conda環境或參考PaddleOCR官方文檔

### Q: 模型訓練時間太長？
A: 可以使用Google Colab的免費GPU，或減少數據量進行測試

### Q: 前端無法連接後端？
A: 檢查CORS設置和API URL配置

## 參考資源

- [TensorFlow文檔](https://www.tensorflow.org/)
- [PaddleOCR文檔](https://github.com/PaddlePaddle/PaddleOCR)
- [React文檔](https://react.dev/)
- [Flask文檔](https://flask.palletsprojects.com/)

