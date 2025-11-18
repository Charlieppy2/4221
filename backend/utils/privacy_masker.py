"""
隱私信息遮蔽器
遮蔽圖片中的敏感信息
"""
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os


class PrivacyMasker:
    def __init__(self):
        """初始化隱私遮蔽器"""
        self.output_dir = 'masked_images'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def mask_info(self, image_path, extracted_info):
        """
        遮蔽圖片中的敏感信息
        
        Args:
            image_path: 原始圖片路徑
            extracted_info: 提取的信息字典
            
        Returns:
            str: 遮蔽後的圖片路徑
        """
        try:
            # 讀取圖片
            img = cv2.imread(image_path)
            if img is None:
                return image_path  # 如果讀取失敗，返回原圖
            
            # 需要遮蔽的字段
            sensitive_fields = [
                'name',
                'id_number',
                'phone',
                'account_number'
            ]
            
            # 這裡應該使用OCR的框位置信息來精確遮蔽
            # 目前使用簡單的矩形遮蔽作為示例
            masked_img = img.copy()
            
            # 在圖片上添加遮蔽矩形（示例位置，實際應該根據OCR結果定位）
            height, width = masked_img.shape[:2]
            
            # 遮蔽區域（這些位置需要根據實際OCR結果調整）
            mask_regions = [
                (int(width * 0.1), int(height * 0.2), int(width * 0.4), int(height * 0.1)),  # 姓名區域
                (int(width * 0.1), int(height * 0.4), int(width * 0.4), int(height * 0.1)),  # ID區域
            ]
            
            for x, y, w, h in mask_regions:
                # 使用黑色矩形遮蔽
                cv2.rectangle(masked_img, (x, y), (x + w, y + h), (0, 0, 0), -1)
                # 或者使用模糊效果
                # roi = masked_img[y:y+h, x:x+w]
                # blurred = cv2.GaussianBlur(roi, (51, 51), 0)
                # masked_img[y:y+h, x:x+w] = blurred
            
            # 保存遮蔽後的圖片
            filename = os.path.basename(image_path)
            output_path = os.path.join(self.output_dir, f"masked_{filename}")
            cv2.imwrite(output_path, masked_img)
            
            return output_path
        
        except Exception as e:
            print(f"遮蔽處理錯誤: {e}")
            return image_path  # 如果處理失敗，返回原圖
    
    def mask_with_boxes(self, image_path, ocr_boxes, sensitive_texts):
        """
        根據OCR框位置精確遮蔽敏感信息
        
        Args:
            image_path: 圖片路徑
            ocr_boxes: OCR識別的文本框列表
            sensitive_texts: 需要遮蔽的文字列表
            
        Returns:
            str: 遮蔽後的圖片路徑
        """
        try:
            img = cv2.imread(image_path)
            if img is None:
                return image_path
            
            masked_img = img.copy()
            
            # 遍歷OCR結果，找到敏感信息並遮蔽
            for box_info in ocr_boxes:
                text = box_info.get('text', '')
                box = box_info.get('box', [])
                
                # 檢查是否包含敏感信息
                if any(sensitive in text for sensitive in sensitive_texts):
                    if len(box) == 4:
                        # 將框轉換為整數座標
                        pts = np.array(box, dtype=np.int32)
                        
                        # 使用多邊形遮蔽
                        cv2.fillPoly(masked_img, [pts], (0, 0, 0))
            
            # 保存遮蔽後的圖片
            filename = os.path.basename(image_path)
            output_path = os.path.join(self.output_dir, f"masked_{filename}")
            cv2.imwrite(output_path, masked_img)
            
            return output_path
        
        except Exception as e:
            print(f"精確遮蔽處理錯誤: {e}")
            return image_path

