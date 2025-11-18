import React, { useEffect, useRef } from 'react';

const MapDisplay = ({ address }) => {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);

  useEffect(() => {
    if (!address || !mapRef.current) return;

    // 初始化地圖
    const initMap = async () => {
      try {
        // 注意：需要設置 Google Maps API Key
        const loader = new window.google.maps.places.PlacesService(
          new window.google.maps.Map(mapRef.current)
        );

        const geocoder = new window.google.maps.Geocoder();
        
        geocoder.geocode({ address: address }, (results, status) => {
          if (status === 'OK' && results[0]) {
            const location = results[0].geometry.location;
            
            const map = new window.google.maps.Map(mapRef.current, {
              center: location,
              zoom: 15,
            });

            new window.google.maps.Marker({
              position: location,
              map: map,
              title: address,
            });

            mapInstanceRef.current = map;
          } else {
            console.error('Geocoding failed:', status);
            // 如果地理編碼失敗，顯示錯誤信息
            mapRef.current.innerHTML = `
              <div class="p-4 text-center text-gray-600">
                <p>無法找到地址: ${address}</p>
                <p class="text-sm mt-2">請檢查地址是否正確</p>
              </div>
            `;
          }
        });
      } catch (error) {
        console.error('地圖初始化錯誤:', error);
        mapRef.current.innerHTML = `
          <div class="p-4 text-center text-gray-600">
            <p>地圖加載失敗</p>
            <p class="text-sm mt-2">請檢查 Google Maps API 配置</p>
          </div>
        `;
      }
    };

    // 檢查 Google Maps API 是否已加載
    if (window.google && window.google.maps) {
      initMap();
    } else {
      // 如果未加載，顯示提示
      mapRef.current.innerHTML = `
        <div class="p-4 text-center text-gray-600">
          <p>正在加載地圖...</p>
          <p class="text-sm mt-2">請確保已配置 Google Maps API Key</p>
        </div>
      `;
    }
  }, [address]);

  return (
    <div>
      <div className="mb-2">
        <span className="text-gray-700 font-medium">地址: </span>
        <span className="text-gray-900">{address}</span>
      </div>
      <div
        ref={mapRef}
        className="w-full h-64 sm:h-80 md:h-96 rounded-lg border border-gray-300"
        style={{ minHeight: '250px' }}
      ></div>
      <p className="text-xs text-gray-500 mt-2">
        提示: 需要配置 Google Maps API Key 才能顯示地圖
      </p>
    </div>
  );
};

export default MapDisplay;

