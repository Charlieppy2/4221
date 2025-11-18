"""
模型評估腳本
評估訓練好的模型性能
"""
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


class ModelEvaluator:
    def __init__(self, model_path='../backend/models/document_classifier.h5', 
                 test_data_dir='../data/processed'):
        """
        初始化評估器
        
        Args:
            model_path: 模型文件路徑
            test_data_dir: 測試數據目錄
        """
        self.model_path = model_path
        self.test_data_dir = test_data_dir
        self.model = None
        
        self.class_names = [
            'identity_card',
            'utility_bill',
            'bank_statement',
            'address_proof',
            'lease_agreement',
            'other'
        ]
    
    def load_model(self):
        """加載模型"""
        if os.path.exists(self.model_path):
            self.model = keras.models.load_model(self.model_path)
            print(f"模型已加載: {self.model_path}")
        else:
            raise FileNotFoundError(f"模型文件不存在: {self.model_path}")
    
    def evaluate(self):
        """評估模型"""
        if self.model is None:
            self.load_model()
        
        # 創建測試數據生成器
        test_datagen = ImageDataGenerator(rescale=1./255)
        
        test_generator = test_datagen.flow_from_directory(
            self.test_data_dir,
            target_size=(224, 224),
            batch_size=32,
            class_mode='categorical',
            shuffle=False
        )
        
        # 評估
        print("開始評估...")
        results = self.model.evaluate(test_generator, verbose=1)
        
        print(f"\n測試損失: {results[0]:.4f}")
        print(f"測試準確率: {results[1]:.4f}")
        
        # 預測
        predictions = self.model.predict(test_generator, verbose=1)
        predicted_classes = np.argmax(predictions, axis=1)
        true_classes = test_generator.classes
        
        # 分類報告
        print("\n分類報告:")
        print(classification_report(
            true_classes,
            predicted_classes,
            target_names=self.class_names
        ))
        
        # 混淆矩陣
        cm = confusion_matrix(true_classes, predicted_classes)
        self.plot_confusion_matrix(cm)
        
        return results
    
    def plot_confusion_matrix(self, cm):
        """繪製混淆矩陣"""
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            cm,
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=self.class_names,
            yticklabels=self.class_names
        )
        plt.title('混淆矩陣 (Confusion Matrix)')
        plt.ylabel('真實標籤')
        plt.xlabel('預測標籤')
        plt.tight_layout()
        plt.savefig('../docs/confusion_matrix.png', dpi=300)
        print("混淆矩陣已保存到 docs/confusion_matrix.png")


if __name__ == '__main__':
    evaluator = ModelEvaluator()
    evaluator.evaluate()

