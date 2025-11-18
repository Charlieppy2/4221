import React, { useState, useEffect } from 'react';
import './App.css';
import DocumentUpload from './components/DocumentUpload';
import ResultDisplay from './components/ResultDisplay';
import MapDisplay from './components/MapDisplay';
import HistoryPanel from './components/HistoryPanel';
import ProgressBar from './components/ProgressBar';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);

  // 從localStorage加載歷史記錄
  useEffect(() => {
    const savedHistory = localStorage.getItem('documentHistory');
    if (savedHistory) {
      try {
        setHistory(JSON.parse(savedHistory));
      } catch (e) {
        console.error('載入歷史記錄失敗:', e);
      }
    }
  }, []);

  // 保存歷史記錄到localStorage
  useEffect(() => {
    if (history.length > 0) {
      localStorage.setItem('documentHistory', JSON.stringify(history));
    }
  }, [history]);

  const handleUpload = async (file) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setProgress(0);

    try {
      // 1. 上傳文件
      setProgress(10);
      const formData = new FormData();
      formData.append('file', file);

      const uploadResponse = await fetch(`${API_BASE_URL}/api/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!uploadResponse.ok) {
        const errorData = await uploadResponse.json().catch(() => ({}));
        throw new Error(errorData.message || '文件上傳失敗');
      }

      const uploadData = await uploadResponse.json();
      const fileId = uploadData.file_id;
      setProgress(30);

      // 2. 識別文檔
      setProgress(50);
      const recognizeResponse = await fetch(`${API_BASE_URL}/api/recognize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ file_id: fileId }),
      });

      if (!recognizeResponse.ok) {
        const errorData = await recognizeResponse.json().catch(() => ({}));
        throw new Error(errorData.message || '文檔識別失敗');
      }

      setProgress(80);
      const recognizeData = await recognizeResponse.json();
      const resultData = recognizeData.data;
      
      // 添加時間戳
      resultData.timestamp = new Date().toISOString();
      resultData.fileId = fileId;
      
      setResult(resultData);
      setProgress(100);

      // 添加到歷史記錄（最多保存10條）
      setHistory(prev => {
        const newHistory = [resultData, ...prev].slice(0, 10);
        return newHistory;
      });

      // 重置進度條
      setTimeout(() => setProgress(0), 1000);
    } catch (err) {
      setError(err.message);
      console.error('錯誤:', err);
      setProgress(0);
    } finally {
      setLoading(false);
    }
  };

  const handleClearHistory = () => {
    setHistory([]);
    localStorage.removeItem('documentHistory');
  };

  const handleLoadFromHistory = (historyItem) => {
    setResult(historyItem);
    setShowHistory(false);
    // 滾動到結果區域
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-3 sm:px-4 py-4 sm:py-8">
        {/* 標題 */}
        <header className="text-center mb-4 sm:mb-8">
          <div className="flex items-center justify-between mb-2">
            <button
              onClick={() => setShowHistory(!showHistory)}
              className="p-2 text-gray-600 hover:text-gray-800 hover:bg-white rounded-lg transition-colors"
              title="歷史記錄"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </button>
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-800 flex-1">
              智能文檔識別系統
            </h1>
            <div className="w-10"></div> {/* 平衡按鈕 */}
          </div>
          <p className="text-sm sm:text-base text-gray-600">
            Smart Document Recognition and Information Extraction System
          </p>
        </header>

        {/* 進度條 */}
        {loading && <ProgressBar progress={progress} />}

        {/* 歷史記錄面板 */}
        {showHistory && (
          <HistoryPanel
            history={history}
            onLoad={handleLoadFromHistory}
            onClose={() => setShowHistory(false)}
            onClear={handleClearHistory}
          />
        )}

        {/* 主要內容 */}
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
            {/* 左側：上傳區域 */}
            <div className="bg-white rounded-lg shadow-lg p-4 sm:p-6 order-2 lg:order-1">
              <h2 className="text-xl sm:text-2xl font-semibold mb-3 sm:mb-4 text-gray-800">
                上傳文檔
              </h2>
              <DocumentUpload
                onUpload={handleUpload}
                loading={loading}
              />
              {error && (
                <div className="mt-4 p-3 sm:p-4 bg-red-100 border border-red-400 text-red-700 rounded text-sm sm:text-base">
                  <div className="flex items-start">
                    <svg className="w-5 h-5 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                    <span>{error}</span>
                  </div>
                </div>
              )}
            </div>

            {/* 右側：結果顯示 */}
            <div className="bg-white rounded-lg shadow-lg p-4 sm:p-6 order-1 lg:order-2">
              <div className="flex items-center justify-between mb-3 sm:mb-4">
                <h2 className="text-xl sm:text-2xl font-semibold text-gray-800">
                  識別結果
                </h2>
                {result && (
                  <button
                    onClick={() => {
                      const dataStr = JSON.stringify(result, null, 2);
                      const dataBlob = new Blob([dataStr], { type: 'application/json' });
                      const url = URL.createObjectURL(dataBlob);
                      const link = document.createElement('a');
                      link.href = url;
                      link.download = `result_${new Date().getTime()}.json`;
                      link.click();
                    }}
                    className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                    title="下載結果"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                  </button>
                )}
              </div>
              {loading ? (
                <div className="flex flex-col items-center justify-center py-8 sm:py-12">
                  <div className="animate-spin rounded-full h-10 w-10 sm:h-12 sm:w-12 border-b-2 border-blue-600"></div>
                  <span className="mt-4 text-sm sm:text-base text-gray-600">處理中...</span>
                  {progress > 0 && (
                    <span className="mt-2 text-xs text-gray-500">{progress}%</span>
                  )}
                </div>
              ) : result ? (
                <ResultDisplay result={result} />
              ) : (
                <div className="text-center py-8 sm:py-12 text-gray-500 text-sm sm:text-base">
                  <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <p>請上傳文檔以開始識別</p>
                </div>
              )}
            </div>
          </div>

          {/* 地圖顯示 */}
          {result && result.extracted_info && result.extracted_info.address && (
            <div className="mt-4 sm:mt-6 bg-white rounded-lg shadow-lg p-4 sm:p-6">
              <h2 className="text-xl sm:text-2xl font-semibold mb-3 sm:mb-4 text-gray-800">
                地址地圖
              </h2>
              <MapDisplay address={result.extracted_info.address} />
            </div>
          )}

          {/* 遮蔽後的圖片顯示 */}
          {result && result.masked_image && (
            <div className="mt-4 sm:mt-6 bg-white rounded-lg shadow-lg p-4 sm:p-6">
              <h2 className="text-xl sm:text-2xl font-semibold mb-3 sm:mb-4 text-gray-800">
                隱私保護版本
              </h2>
              <div className="flex justify-center">
                <img
                  src={`${API_BASE_URL}/api/images/${result.masked_image.split('/').pop()}`}
                  alt="遮蔽後的文檔"
                  className="max-w-full h-auto rounded-lg shadow-md"
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;

