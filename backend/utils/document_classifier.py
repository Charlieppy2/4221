"""
文檔分類器
使用訓練好的模型對文檔進行分類
"""
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras


class DocumentClassifier:
    def __init__(self, model_path='models/document_classifier.h5'):
        """
        初始化文檔分類器
        
        Args:
            model_path: 模型文件路徑
        """
        self.model_path = model_path
        self.model = None
        self.img_size = (224, 224)
        
        # 文檔類型標籤
        self.class_labels = [
            'identity_card',      # 身份證
            'utility_bill',       # 水電費單
            'bank_statement',     # 銀行賬單
            'address_proof',      # 地址證明
            'lease_agreement',    # 租約
            'other'               # 其他
        ]
        
        # 嘗試加載模型
        self._load_model()
    
    def _load_model(self):
        """加載訓練好的模型"""
        try:
            if os.path.exists(self.model_path):
                self.model = keras.models.load_model(self.model_path)
                print(f"模型已加載: {self.model_path}")
            else:
                print(f"模型文件不存在: {self.model_path}")
                print("將使用隨機分類結果（僅用於測試）")
        except Exception as e:
            print(f"模型加載失敗: {e}")
            print("將使用隨機分類結果（僅用於測試）")
    
    def classify(self, image_path):
        """
        對文檔進行分類
        
        Args:
            image_path: 圖片路徑
            
        Returns:
            tuple: (文檔類型, 置信度)
        """
        if self.model is None:
            # 如果模型未加載，返回隨機結果（僅用於測試）
            import random
            doc_type = random.choice(self.class_labels)
            confidence = random.uniform(0.7, 0.95)
            return doc_type, confidence
        
        try:
            # 預處理圖片
            img = self._preprocess_image(image_path)
            
            # 預測
            predictions = self.model.predict(img, verbose=0)
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            
            # 獲取類別名稱
            doc_type = self.class_labels[predicted_class_idx]
            
            return doc_type, confidence
        
        except Exception as e:
            print(f"分類錯誤: {e}")
            # 返回默認值
            return 'other', 0.5
    
    def _preprocess_image(self, image_path):
        """
        預處理圖片
        
        Args:
            image_path: 圖片路徑
            
        Returns:
            numpy array: 預處理後的圖片數組
        """
        # 讀取圖片
        img = Image.open(image_path)
        
        # 轉換為RGB（如果是RGBA或其他格式）
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 調整大小
        img = img.resize(self.img_size)
        
        # 轉換為數組並歸一化
        img_array = np.array(img) / 255.0
        
        # 添加批次維度
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array

