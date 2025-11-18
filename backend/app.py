"""
Flask後端應用
處理文檔上傳、識別和信息提取
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename
from utils.ocr_processor import OCRProcessor
from utils.info_extractor import InfoExtractor
from utils.document_classifier import DocumentClassifier
from utils.privacy_masker import PrivacyMasker

app = Flask(__name__)
CORS(app)  # 允許跨域請求

# 配置
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# 確保上傳目錄存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('results', exist_ok=True)

# 初始化處理器
ocr_processor = OCRProcessor()
info_extractor = InfoExtractor()
document_classifier = DocumentClassifier()
privacy_masker = PrivacyMasker()


def allowed_file(filename):
    """檢查文件擴展名是否允許"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """健康檢查"""
    return jsonify({
        'status': 'success',
        'message': 'Document Recognition API is running'
    })


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """處理文檔上傳"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        # 生成唯一文件名
        file_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        saved_filename = f"{file_id}.{file_ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
        
        # 保存文件
        file.save(filepath)
        
        return jsonify({
            'status': 'success',
            'file_id': file_id,
            'filename': saved_filename
        })
    
    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/api/recognize', methods=['POST'])
def recognize_document():
    """識別文檔並提取信息"""
    try:
        data = request.json
        file_id = data.get('file_id')
        
        if not file_id:
            return jsonify({'error': 'file_id is required'}), 400
        
        # 查找文件
        filepath = None
        for ext in ['png', 'jpg', 'jpeg', 'pdf']:
            potential_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}.{ext}")
            if os.path.exists(potential_path):
                filepath = potential_path
                break
        
        if not filepath:
            return jsonify({'error': 'File not found'}), 404
        
        # 1. 文檔分類
        doc_type, confidence = document_classifier.classify(filepath)
        
        # 2. OCR識別
        ocr_result = ocr_processor.process(filepath)
        
        # 3. 信息提取
        extracted_info = info_extractor.extract(ocr_result, doc_type)
        
        # 4. 隱私遮蔽
        masked_image_path = privacy_masker.mask_info(filepath, extracted_info)
        
        # 保存結果
        result_id = str(uuid.uuid4())
        result_data = {
            'result_id': result_id,
            'file_id': file_id,
            'document_type': doc_type,
            'confidence': float(confidence),
            'ocr_text': ocr_result,
            'extracted_info': extracted_info,
            'masked_image': masked_image_path
        }
        
        return jsonify({
            'status': 'success',
            'data': result_data
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/results/<result_id>', methods=['GET'])
def get_result(result_id):
    """獲取識別結果"""
    # 這裡可以從數據庫讀取結果
    # 暫時返回示例數據
    return jsonify({
        'status': 'success',
        'message': 'Result retrieval not implemented yet'
    })


@app.route('/api/images/<filename>')
def uploaded_file(filename):
    """提供上傳的圖片"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

