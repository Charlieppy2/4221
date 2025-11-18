"""
OCR處理器
使用PaddleOCR進行文字識別
"""
import os
try:
    from paddleocr import PaddleOCR
    PADDLEOCR_AVAILABLE = True
except ImportError:
    PADDLEOCR_AVAILABLE = False
    print("警告: PaddleOCR 未安裝，OCR功能將不可用")
    print("安裝方法: pip install paddleocr")

import cv2
import numpy as np


class OCRProcessor:
    def __init__(self):
        """初始化OCR處理器"""
        # 初始化PaddleOCR，支持中英文
        # use_angle_cls=True 使用角度分類器
        # lang='ch' 支持中文
        self.ocr = None
        if PADDLEOCR_AVAILABLE:
            try:
                # 新版本 PaddleOCR 參數
                self.ocr = PaddleOCR(
                    use_angle_cls=True,
                    lang='ch'
                    # use_gpu 參數在新版本中已移除，自動檢測
                )
            except Exception as e:
                print(f"OCR初始化失敗: {e}")
                self.ocr = None
        else:
            print("PaddleOCR 未安裝，使用模擬模式")
    
    def process(self, image_path):
        """
        處理圖片並提取文字
        
        Args:
            image_path: 圖片路徑
            
        Returns:
            str: 識別出的文字
        """
        if self.ocr is None:
            # 模擬模式：返回示例文字
            return "【模擬模式】PaddleOCR 未安裝，無法進行真實OCR識別。\n請安裝: pip install paddleocr\n\n示例識別文字：\n這是一個示例文檔\n地址：香港九龍\n姓名：張三\n日期：2025-12-11"
        
        try:
            # 執行OCR
            result = self.ocr.ocr(image_path, cls=True)
            
            # 提取文字
            text_lines = []
            if result and result[0]:
                for line in result[0]:
                    if line and len(line) >= 2:
                        text = line[1][0]  # 文字內容
                        confidence = line[1][1]  # 置信度
                        if confidence > 0.5:  # 只保留置信度高的結果
                            text_lines.append(text)
            
            return '\n'.join(text_lines) if text_lines else "未識別到文字"
        
        except Exception as e:
            print(f"OCR處理錯誤: {e}")
            return f"OCR處理失敗: {str(e)}"
    
    def process_with_boxes(self, image_path):
        """
        處理圖片並返回帶位置信息的文字
        
        Returns:
            list: 包含文字和位置的列表
        """
        if self.ocr is None:
            return []
        
        try:
            result = self.ocr.ocr(image_path, cls=True)
            
            boxes = []
            if result and result[0]:
                for line in result[0]:
                    if line and len(line) >= 2:
                        box = line[0]  # 位置信息
                        text = line[1][0]  # 文字
                        confidence = line[1][1]  # 置信度
                        
                        boxes.append({
                            'box': box,
                            'text': text,
                            'confidence': float(confidence)
                        })
            
            return boxes
        
        except Exception as e:
            print(f"OCR處理錯誤: {e}")
            return []

