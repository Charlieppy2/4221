"""
測試後端API的腳本
"""
import requests
import os
from pathlib import Path

API_BASE_URL = "http://localhost:5000"

def test_backend_health():
    """測試後端健康狀態"""
    print("=" * 50)
    print("測試 1: 後端健康檢查")
    print("=" * 50)
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"狀態碼: {response.status_code}")
        print(f"響應: {response.json()}")
        print("[OK] 後端運行正常\n")
        return True
    except Exception as e:
        print(f"[ERROR] 後端連接失敗: {e}\n")
        return False

def test_upload_and_recognize(image_path):
    """測試上傳和識別功能"""
    print("=" * 50)
    print("測試 2: 文件上傳和識別")
    print("=" * 50)
    
    if not os.path.exists(image_path):
        print(f"[ERROR] 圖片文件不存在: {image_path}")
        print("提示: 請提供一張測試圖片的路徑")
        return False
    
    try:
        # 1. 上傳文件
        print(f"上傳文件: {image_path}")
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            response = requests.post(f"{API_BASE_URL}/api/upload", files=files)
        
        if response.status_code != 200:
            print(f"[ERROR] 上傳失敗: {response.status_code}")
            print(f"錯誤: {response.text}")
            return False
        
        upload_data = response.json()
        file_id = upload_data.get('file_id')
        print(f"[OK] 上傳成功, File ID: {file_id}")
        
        # 2. 識別文檔
        print("\n開始識別文檔...")
        response = requests.post(
            f"{API_BASE_URL}/api/recognize",
            json={'file_id': file_id},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code != 200:
            print(f"[ERROR] 識別失敗: {response.status_code}")
            print(f"錯誤: {response.text}")
            return False
        
        result = response.json()
        data = result.get('data', {})
        
        print("\n[OK] 識別成功!")
        print("\n識別結果:")
        print(f"  文檔類型: {data.get('document_type', 'N/A')}")
        print(f"  置信度: {data.get('confidence', 0) * 100:.1f}%")
        
        if data.get('extracted_info'):
            print("\n提取的信息:")
            for key, value in data['extracted_info'].items():
                if value:
                    print(f"  {key}: {value}")
        
        if data.get('ocr_text'):
            print(f"\nOCR文字 (前100字符):")
            print(f"  {data['ocr_text'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "=" * 50)
    print("智能文檔識別系統 - API 測試")
    print("=" * 50 + "\n")
    
    # 測試1: 健康檢查
    if not test_backend_health():
        print("[ERROR] 後端未運行，請先啟動後端服務器")
        print("啟動命令: cd backend && python app.py")
        return
    
    # 測試2: 上傳和識別
    # 檢查是否有測試圖片
    test_images = [
        "test_image.jpg",
        "test_image.png",
        "backend/uploads/test.jpg",
        "test.jpg"
    ]
    
    image_path = None
    for path in test_images:
        if os.path.exists(path):
            image_path = path
            break
    
    if image_path:
        test_upload_and_recognize(image_path)
    else:
        print("\n" + "=" * 50)
        print("提示: 沒有找到測試圖片")
        print("=" * 50)
        print("你可以:")
        print("1. 將一張圖片放到項目根目錄，命名為 test_image.jpg")
        print("2. 或使用瀏覽器打開 frontend/test.html 進行測試")
        print("3. 或手動指定圖片路徑:")
        print("   python test_api.py <圖片路徑>")
    
    print("\n" + "=" * 50)
    print("測試完成")
    print("=" * 50)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # 如果提供了圖片路徑作為參數
        test_backend_health()
        test_upload_and_recognize(sys.argv[1])
    else:
        main()

