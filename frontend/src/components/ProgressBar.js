import React from 'react';

const ProgressBar = ({ progress }) => {
  return (
    <div className="fixed top-0 left-0 right-0 z-50">
      <div className="h-1 bg-gray-200">
        <div
          className="h-full bg-gradient-to-r from-blue-500 to-indigo-600 transition-all duration-300 ease-out"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      {progress > 0 && progress < 100 && (
        <div className="bg-blue-600 text-white text-center py-1 text-xs sm:text-sm">
          處理中... {progress}%
        </div>
      )}
    </div>
  );
};

export default ProgressBar;

