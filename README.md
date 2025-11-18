# 智能文档识别與信息提取系統
## Smart Document Recognition and Information Extraction System

### 項目簡介
這是一個基於深度學習的智能文檔識別系統，能夠識別香港常見文檔類型（身份證、水電費單、銀行賬單等），並自動提取關鍵信息（地址、姓名、日期等），同時提供地圖顯示和隱私保護功能。

### 技術棧
- **前端**: React + Tailwind CSS
- **後端**: Flask + Python
- **深度學習**: TensorFlow/Keras
- **OCR**: PaddleOCR
- **地圖**: Google Maps API

### 項目結構
```
.
├── backend/                 # 後端應用
│   ├── app.py              # Flask主應用
│   ├── models/             # 模型文件
│   ├── utils/              # 工具函數
│   └── requirements.txt    # Python依賴
├── frontend/               # 前端應用
│   ├── src/
│   ├── public/
│   └── package.json
├── model_training/         # 模型訓練
│   ├── train.py           # 訓練腳本
│   ├── data_preprocessing.py
│   └── evaluate.py
├── data/                   # 數據集
│   ├── raw/               # 原始數據
│   ├── processed/         # 處理後數據
│   └── labels/            # 標籤文件
├── docs/                   # 文檔
└── README.md
```

### 安裝與運行

#### 後端設置
```bash
cd backend
pip install -r requirements.txt
python app.py
```

#### 前端設置
```bash
cd frontend
npm install
npm start
```

### 功能特性
- ✅ 文檔類型識別（6種類型）
- ✅ OCR文字識別
- ✅ 關鍵信息提取
- ✅ 地圖地址顯示
- ✅ 隱私信息遮蔽
- ✅ 信息審核與編輯

### 開發團隊
4人小組項目

### 參考資料
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [TensorFlow](https://www.tensorflow.org/)
- [Google Maps API](https://developers.google.com/maps)

