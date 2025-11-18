# 數據收集指南

## 數據收集要求

### 數據量建議
- 每個類別至少 **100-200張** 圖片
- 總數據量建議 **600-1200張**
- 訓練集：驗證集：測試集 = 7:2:1

### 數據質量要求
- 圖片清晰，分辨率至少 224x224
- 包含各種角度和光照條件
- 包含完整文檔（不要裁剪過多）
- 格式：PNG, JPG, JPEG

## 數據來源

### 1. 自行拍攝（推薦）
- 使用手機或相機拍攝
- 注意隱私保護（不要使用真實敏感信息）
- 可以遮蓋敏感信息後拍攝

### 2. 公開數據集
- [Kaggle Document Classification](https://www.kaggle.com/datasets)
- [GitHub文檔數據集](https://github.com/topics/document-dataset)
- 注意：必須標註數據來源

### 3. 合成數據
- 使用模板生成文檔
- 使用數據增強技術
- 說明生成方法

## 數據組織結構

```
data/
  raw/
    identity_card/
      img_001.jpg
      img_002.jpg
      ...
    utility_bill/
      bill_001.jpg
      bill_002.jpg
      ...
    bank_statement/
      ...
    address_proof/
      ...
    lease_agreement/
      ...
    other/
      ...
```

## 數據標註

### 文檔類型標籤
1. `identity_card` - 身份證
2. `utility_bill` - 水電費單
3. `bank_statement` - 銀行賬單
4. `address_proof` - 地址證明
5. `lease_agreement` - 租約
6. `other` - 其他

### 信息標註（可選）
如果需要訓練信息提取模型，可以標註：
- 地址位置
- 姓名位置
- 日期位置
- 其他關鍵信息位置

## 數據預處理

運行預處理腳本：
```bash
cd model_training
python data_preprocessing.py
```

這將：
1. 創建處理後的數據目錄結構
2. 調整圖片大小
3. 轉換圖片格式
4. （可選）進行數據增強

## 數據增強

可以通過以下方式增強數據：
- 旋轉（±15度）
- 平移
- 縮放
- 亮度調整
- 對比度調整

運行數據增強：
```bash
python data_preprocessing.py
# 在腳本中取消註釋 augment_data() 調用
```

## 注意事項

1. **隱私保護**：不要使用真實的敏感信息
2. **數據多樣性**：確保每個類別有足夠的變化
3. **數據平衡**：盡量保持各類別數據量平衡
4. **標註準確性**：確保標籤正確
5. **數據來源記錄**：記錄所有數據的來源

## 數據收集檢查清單

- [ ] 每個類別至少100張圖片
- [ ] 圖片清晰，分辨率足夠
- [ ] 數據組織結構正確
- [ ] 標籤準確
- [ ] 記錄數據來源
- [ ] 完成數據預處理
- [ ] 檢查數據分布平衡

