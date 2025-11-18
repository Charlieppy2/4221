"""
文檔分類模型訓練腳本
使用TensorFlow/Keras訓練文檔分類模型
"""
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2, EfficientNetB0
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt


class DocumentClassifierTrainer:
    def __init__(self, data_dir='../data/processed', img_size=(224, 224), batch_size=32):
        """
        初始化訓練器
        
        Args:
            data_dir: 數據目錄
            img_size: 圖片大小
            batch_size: 批次大小
        """
        self.data_dir = data_dir
        self.img_size = img_size
        self.batch_size = batch_size
        self.num_classes = 6  # 6種文檔類型
        
        # 類別標籤
        self.class_names = [
            'identity_card',
            'utility_bill',
            'bank_statement',
            'address_proof',
            'lease_agreement',
            'other'
        ]
    
    def create_data_generators(self):
        """創建數據生成器"""
        # 數據增強
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=15,
            width_shift_range=0.1,
            height_shift_range=0.1,
            shear_range=0.1,
            zoom_range=0.1,
            horizontal_flip=False,  # 文檔通常不應該翻轉
            fill_mode='nearest',
            validation_split=0.2  # 20%作為驗證集
        )
        
        # 訓練數據生成器
        train_generator = train_datagen.flow_from_directory(
            self.data_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='training',
            shuffle=True
        )
        
        # 驗證數據生成器
        validation_generator = train_datagen.flow_from_directory(
            self.data_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='validation',
            shuffle=False
        )
        
        return train_generator, validation_generator
    
    def build_model(self, base_model_name='mobilenetv2'):
        """
        構建模型
        
        Args:
            base_model_name: 基礎模型名稱 ('mobilenetv2' 或 'efficientnet')
        """
        # 選擇基礎模型
        if base_model_name == 'mobilenetv2':
            base_model = MobileNetV2(
                input_shape=(*self.img_size, 3),
                include_top=False,
                weights='imagenet'
            )
        elif base_model_name == 'efficientnet':
            base_model = EfficientNetB0(
                input_shape=(*self.img_size, 3),
                include_top=False,
                weights='imagenet'
            )
        else:
            raise ValueError(f"不支持的模型: {base_model_name}")
        
        # 凍結基礎模型（可選，用於遷移學習）
        base_model.trainable = False
        
        # 構建完整模型
        model = keras.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dropout(0.2),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        # 編譯模型
        model.compile(
            optimizer=Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train(self, epochs=50, base_model='mobilenetv2'):
        """
        訓練模型
        
        Args:
            epochs: 訓練輪數
            base_model: 基礎模型名稱
        """
        print("準備數據生成器...")
        train_gen, val_gen = self.create_data_generators()
        
        print(f"訓練樣本數: {train_gen.samples}")
        print(f"驗證樣本數: {val_gen.samples}")
        
        print("構建模型...")
        model = self.build_model(base_model)
        model.summary()
        
        # 回調函數
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True
            ),
            keras.callbacks.ModelCheckpoint(
                '../backend/models/document_classifier.h5',
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7
            )
        ]
        
        print("開始訓練...")
        history = model.fit(
            train_gen,
            epochs=epochs,
            validation_data=val_gen,
            callbacks=callbacks,
            verbose=1
        )
        
        # 保存最終模型
        model.save('../backend/models/document_classifier_final.h5')
        
        # 繪製訓練曲線
        self.plot_training_history(history)
        
        return model, history
    
    def plot_training_history(self, history):
        """繪製訓練歷史"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # 準確率
        ax1.plot(history.history['accuracy'], label='Training Accuracy')
        ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        
        # 損失
        ax2.plot(history.history['loss'], label='Training Loss')
        ax2.plot(history.history['val_loss'], label='Validation Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig('../docs/training_history.png')
        print("訓練曲線已保存到 docs/training_history.png")


if __name__ == '__main__':
    # 設置GPU（如果可用）
    physical_devices = tf.config.list_physical_devices('GPU')
    if len(physical_devices) > 0:
        print(f"使用GPU: {physical_devices[0]}")
        tf.config.experimental.set_memory_growth(physical_devices[0], True)
    else:
        print("使用CPU")
    
    # 創建訓練器
    trainer = DocumentClassifierTrainer(
        data_dir='../data/processed',
        img_size=(224, 224),
        batch_size=32
    )
    
    # 開始訓練
    model, history = trainer.train(
        epochs=50,
        base_model='mobilenetv2'  # 或 'efficientnet'
    )
    
    print("訓練完成！")

