import React from 'react';

const ResultDisplay = ({ result }) => {
  const { document_type, confidence, extracted_info, ocr_text } = result;

  const documentTypeNames = {
    identity_card: '身份證',
    utility_bill: '水電費單',
    bank_statement: '銀行賬單',
    address_proof: '地址證明',
    lease_agreement: '租約',
    other: '其他'
  };

  const formatFieldName = (field) => {
    const fieldNames = {
      address: '地址',
      name: '姓名',
      date: '日期',
      phone: '電話',
      amount: '金額',
      id_number: '身份證號碼',
      account_number: '賬戶號碼',
      bill_period: '賬單週期',
      account_balance: '賬戶餘額'
    };
    return fieldNames[field] || field;
  };

  return (
    <div className="space-y-3 sm:space-y-4">
      {/* 文檔類型 */}
      <div className="bg-blue-50 p-3 sm:p-4 rounded-lg">
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center space-y-2 sm:space-y-0">
          <div className="flex items-center space-x-2">
            <span className="font-semibold text-gray-700 text-sm sm:text-base">文檔類型:</span>
            <span className="text-blue-700 font-bold text-sm sm:text-base">
              {documentTypeNames[document_type] || document_type}
            </span>
          </div>
        </div>
        <div className="mt-2 sm:mt-3">
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center space-y-2 sm:space-y-0">
            <span className="text-xs sm:text-sm text-gray-600">置信度:</span>
            <div className="flex items-center space-x-2 flex-1 sm:flex-initial sm:ml-4">
              <div className="flex-1 sm:w-32 bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all"
                  style={{ width: `${confidence * 100}%` }}
                ></div>
              </div>
              <span className="text-xs sm:text-sm font-medium text-gray-700 min-w-[3rem] text-right">
                {(confidence * 100).toFixed(1)}%
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* 提取的信息 */}
      {extracted_info && (
        <div>
          <h3 className="font-semibold text-gray-800 mb-2 sm:mb-3 text-sm sm:text-base">提取的信息:</h3>
          <div className="space-y-2">
            {Object.entries(extracted_info).map(([key, value]) => {
              if (value) {
                return (
                  <div
                    key={key}
                    className="flex flex-col sm:flex-row sm:justify-between p-2 sm:p-3 bg-gray-50 rounded border border-gray-200"
                  >
                    <span className="font-medium text-gray-700 text-xs sm:text-sm mb-1 sm:mb-0">
                      {formatFieldName(key)}:
                    </span>
                    <span className="text-gray-900 text-xs sm:text-sm sm:text-right sm:max-w-xs break-words">
                      {value}
                    </span>
                  </div>
                );
              }
              return null;
            })}
          </div>
        </div>
      )}

      {/* OCR文字 */}
      {ocr_text && (
        <div className="mt-3 sm:mt-4">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-semibold text-gray-800 text-sm sm:text-base">識別文字:</h3>
            <button
              onClick={() => {
                navigator.clipboard.writeText(ocr_text);
                // 可以添加一個toast提示
              }}
              className="text-xs text-blue-600 hover:text-blue-800 flex items-center space-x-1"
              title="複製文字"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              <span>複製</span>
            </button>
          </div>
          <div className="bg-gray-50 p-3 sm:p-4 rounded border border-gray-200 max-h-40 sm:max-h-48 overflow-y-auto">
            <pre className="text-xs sm:text-sm text-gray-700 whitespace-pre-wrap font-sans leading-relaxed">
              {ocr_text}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultDisplay;

