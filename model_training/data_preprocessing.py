"""
數據預處理腳本
整理和預處理文檔圖片數據
"""
import os
import shutil
from PIL import Image
import numpy as np


class DataPreprocessor:
    def __init__(self, raw_data_dir='../data/raw', output_dir='../data/processed'):
        """
        初始化數據預處理器
        
        Args:
            raw_data_dir: 原始數據目錄
            output_dir: 輸出目錄
        """
        self.raw_data_dir = raw_data_dir
        self.output_dir = output_dir
        
        # 文檔類型目錄
        self.classes = [
            'identity_card',
            'utility_bill',
            'bank_statement',
            'address_proof',
            'lease_agreement',
            'other'
        ]
    
    def organize_data(self):
        """整理數據到對應的類別文件夾"""
        # 創建輸出目錄結構
        for class_name in self.classes:
            class_dir = os.path.join(self.output_dir, class_name)
            os.makedirs(class_dir, exist_ok=True)
        
        print("數據目錄結構已創建")
        print("請將原始圖片按照類別放入對應的文件夾中")
        print(f"原始數據目錄: {self.raw_data_dir}")
        print(f"處理後數據目錄: {self.output_dir}")
    
    def preprocess_images(self, target_size=(224, 224), format='RGB'):
        """
        預處理圖片
        
        Args:
            target_size: 目標圖片大小
            format: 圖片格式
        """
        for class_name in self.classes:
            class_dir = os.path.join(self.output_dir, class_name)
            if not os.path.exists(class_dir):
                continue
            
            print(f"處理 {class_name} 類別...")
            count = 0
            
            for filename in os.listdir(class_dir):
                if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    continue
                
                filepath = os.path.join(class_dir, filename)
                
                try:
                    # 打開圖片
                    img = Image.open(filepath)
                    
                    # 轉換格式
                    if format and img.mode != format:
                        img = img.convert(format)
                    
                    # 調整大小
                    img = img.resize(target_size, Image.Resampling.LANCZOS)
                    
                    # 保存處理後的圖片
                    img.save(filepath, optimize=True, quality=95)
                    count += 1
                
                except Exception as e:
                    print(f"處理 {filename} 時出錯: {e}")
                    continue
            
            print(f"  {class_name}: 處理了 {count} 張圖片")
    
    def augment_data(self, augment_per_image=3):
        """
        數據增強
        
        Args:
            augment_per_image: 每張圖片生成的增強版本數量
        """
        from tensorflow.keras.preprocessing.image import ImageDataGenerator
        
        datagen = ImageDataGenerator(
            rotation_range=15,
            width_shift_range=0.1,
            height_shift_range=0.1,
            shear_range=0.1,
            zoom_range=0.1,
            horizontal_flip=False,
            fill_mode='nearest'
        )
        
        for class_name in self.classes:
            class_dir = os.path.join(self.output_dir, class_name)
            if not os.path.exists(class_dir):
                continue
            
            print(f"增強 {class_name} 類別...")
            
            for filename in os.listdir(class_dir):
                if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    continue
                
                filepath = os.path.join(class_dir, filename)
                
                try:
                    img = Image.open(filepath)
                    img_array = np.array(img)
                    img_array = np.expand_dims(img_array, axis=0)
                    
                    # 生成增強圖片
                    aug_iter = datagen.flow(img_array, batch_size=1)
                    
                    for i in range(augment_per_image):
                        aug_img = next(aug_iter)[0].astype('uint8')
                        aug_filename = f"aug_{i}_{filename}"
                        aug_filepath = os.path.join(class_dir, aug_filename)
                        
                        Image.fromarray(aug_img).save(aug_filepath)
                
                except Exception as e:
                    print(f"增強 {filename} 時出錯: {e}")
                    continue
            
            print(f"  {class_name}: 數據增強完成")
    
    def check_data_distribution(self):
        """檢查數據分布"""
        print("\n數據分布統計:")
        print("-" * 50)
        
        total = 0
        for class_name in self.classes:
            class_dir = os.path.join(self.output_dir, class_name)
            if os.path.exists(class_dir):
                count = len([f for f in os.listdir(class_dir) 
                           if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
                total += count
                print(f"{class_name:20s}: {count:4d} 張圖片")
        
        print("-" * 50)
        print(f"{'總計':20s}: {total:4d} 張圖片")
        print()


if __name__ == '__main__':
    preprocessor = DataPreprocessor()
    
    # 1. 整理數據目錄
    preprocessor.organize_data()
    
    # 2. 預處理圖片（在放入數據後執行）
    # preprocessor.preprocess_images()
    
    # 3. 數據增強（可選）
    # preprocessor.augment_data(augment_per_image=3)
    
    # 4. 檢查數據分布
    preprocessor.check_data_distribution()

