"""
信息提取器
從OCR結果中提取關鍵信息（地址、姓名、日期等）
"""
import re
from typing import Dict, List, Optional


class InfoExtractor:
    def __init__(self):
        """初始化信息提取器"""
        # 香港地址模式
        self.address_patterns = [
            r'[香港|九龍|新界].*?(?:區|道|街|路|號|大廈|樓|室)',
            r'[A-Za-z].*?(?:Road|Street|Avenue|Lane|Building|Flat|Room)',
        ]
        
        # 日期模式
        self.date_patterns = [
            r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',
            r'\d{1,2}[-/]\d{1,2}[-/]\d{4}',
            r'\d{4}年\d{1,2}月\d{1,2}日',
        ]
        
        # 電話模式
        self.phone_patterns = [
            r'\d{4}\s?\d{4}',  # 香港電話
            r'\+852\s?\d{4}\s?\d{4}',
        ]
        
        # 金額模式
        self.amount_patterns = [
            r'[HK\$|HK\$\s]?\d+[,.]?\d*\.?\d{2}',
            r'\$\d+[,.]?\d*\.?\d{2}',
        ]
    
    def extract(self, ocr_text: str, document_type: str) -> Dict:
        """
        從OCR文本中提取關鍵信息
        
        Args:
            ocr_text: OCR識別的文字
            document_type: 文檔類型
            
        Returns:
            dict: 提取的信息
        """
        extracted = {
            'address': self._extract_address(ocr_text),
            'name': self._extract_name(ocr_text, document_type),
            'date': self._extract_date(ocr_text),
            'phone': self._extract_phone(ocr_text),
            'amount': self._extract_amount(ocr_text),
            'id_number': self._extract_id_number(ocr_text, document_type),
            'account_number': self._extract_account_number(ocr_text, document_type),
        }
        
        # 根據文檔類型提取特定信息
        if document_type == 'identity_card':
            extracted['id_number'] = self._extract_hk_id(ocr_text)
        elif document_type == 'utility_bill':
            extracted['bill_period'] = self._extract_bill_period(ocr_text)
        elif document_type == 'bank_statement':
            extracted['account_balance'] = self._extract_balance(ocr_text)
        
        return extracted
    
    def _extract_address(self, text: str) -> Optional[str]:
        """提取地址"""
        for pattern in self.address_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0]
        return None
    
    def _extract_name(self, text: str, doc_type: str) -> Optional[str]:
        """提取姓名"""
        # 簡單的姓名提取（可以根據實際情況改進）
        # 通常在"姓名"、"Name"等關鍵詞後面
        name_patterns = [
            r'(?:姓名|Name)[:：\s]+([A-Za-z\s]+|[\u4e00-\u9fa5]+)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)',  # 英文全名
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None
    
    def _extract_date(self, text: str) -> Optional[str]:
        """提取日期"""
        for pattern in self.date_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        return None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """提取電話號碼"""
        for pattern in self.phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        return None
    
    def _extract_amount(self, text: str) -> Optional[str]:
        """提取金額"""
        for pattern in self.amount_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[-1]  # 通常最後一個是總金額
        return None
    
    def _extract_id_number(self, text: str, doc_type: str) -> Optional[str]:
        """提取身份證號碼"""
        if doc_type == 'identity_card':
            # 香港身份證格式: 字母+6-7位數字+括號內1位數字或字母
            id_pattern = r'[A-Z]\d{6,7}\([0-9A]\)'
            match = re.search(id_pattern, text)
            if match:
                return match.group(0)
        return None
    
    def _extract_hk_id(self, text: str) -> Optional[str]:
        """提取香港身份證號碼"""
        id_pattern = r'[A-Z]\d{6,7}\([0-9A]\)'
        match = re.search(id_pattern, text)
        return match.group(0) if match else None
    
    def _extract_account_number(self, text: str, doc_type: str) -> Optional[str]:
        """提取賬戶號碼"""
        if doc_type in ['bank_statement', 'utility_bill']:
            # 賬戶號碼通常是長數字
            account_pattern = r'(?:賬戶|Account|A/C)[:：\s]*(\d{8,})'
            match = re.search(account_pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    def _extract_bill_period(self, text: str) -> Optional[str]:
        """提取賬單週期"""
        period_pattern = r'(?:賬單週期|Bill Period|期間)[:：\s]*(\d{4}[-/]\d{1,2}[-/]\d{1,2}\s*至\s*\d{4}[-/]\d{1,2}[-/]\d{1,2})'
        match = re.search(period_pattern, text, re.IGNORECASE)
        return match.group(1) if match else None
    
    def _extract_balance(self, text: str) -> Optional[str]:
        """提取賬戶餘額"""
        balance_pattern = r'(?:餘額|Balance)[:：\s]*([HK\$]?\d+[,.]?\d*\.?\d{2})'
        match = re.search(balance_pattern, text, re.IGNORECASE)
        return match.group(1) if match else None

