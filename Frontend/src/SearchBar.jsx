import React, { useState, useEffect, useRef } from 'react';
import { useMap } from 'react-leaflet';
import L from 'leaflet';

function SearchBar({ onSelectLocation }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [searching, setSearching] = useState(false);
  const map = useMap();
  const containerRef = useRef(null);

  // Prevent map clicks when clicking on the search bar
  useEffect(() => {
    if (containerRef.current) {
      L.DomEvent.disableClickPropagation(containerRef.current);
      L.DomEvent.disableScrollPropagation(containerRef.current);
    }
  }, []);

  // Debounced Auto-complete
  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (query.trim().length > 2) {
        performSearch(query);
      } else {
        setResults([]);
      }
    }, 400);

    return () => clearTimeout(delayDebounceFn);
  }, [query]);

  const performSearch = async (searchQuery) => {
    setSearching(true);
    try {
      const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery)}&viewbox=77.40,13.15,77.75,12.80&bounded=1&limit=8`);
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error("Search failed", error);
    } finally {
      setSearching(false);
    }
  };

  const handleSelect = (place) => {
    const lat = parseFloat(place.lat);
    const lon = parseFloat(place.lon);
    
    map.flyTo([lat, lon], 14, { duration: 1.5 });
    
    onSelectLocation({
      latitude: lat,
      longitude: lon,
      display_id: place.name || place.display_name.split(',')[0]
    });
    
    setQuery('');
    setResults([]);
  };

  return (
    <div 
      ref={containerRef}
      style={{
        position: 'absolute', 
        top: '20px', 
        left: '60px', 
        zIndex: 1000,
        width: '320px',
        fontFamily: 'inherit'
      }}
    >
      <style>{`
        @keyframes search-spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
      
      <div style={{
        display: 'flex', 
        alignItems: 'center',
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(8px)',
        boxShadow: '0 4px 16px rgba(0,0,0,0.1)', 
        borderRadius: '24px', 
        overflow: 'hidden',
        border: '1px solid rgba(0,0,0,0.05)',
        padding: '4px 16px',
        transition: 'box-shadow 0.2s ease'
      }}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#666" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input 
          type="text" 
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Search location (e.g. Majestic)..." 
          style={{
            flex: 1, 
            padding: '10px 12px', 
            border: 'none', 
            outline: 'none', 
            background: 'transparent', 
            color: '#111',
            fontSize: '14px',
            fontWeight: '500'
          }}
        />
        {searching && (
          <div style={{
            width: '16px', 
            height: '16px', 
            border: '2px solid rgba(0,0,0,0.1)', 
            borderTopColor: '#1a73e8', 
            borderRadius: '50%', 
            animation: 'search-spin 0.8s linear infinite'
          }} />
        )}
      </div>
      
      {results.length > 0 && (
        <div style={{
          marginTop: '8px',
          background: 'rgba(255, 255, 255, 0.98)',
          backdropFilter: 'blur(12px)',
          borderRadius: '12px',
          boxShadow: '0 8px 24px rgba(0,0,0,0.12)',
          overflow: 'hidden',
          border: '1px solid rgba(0,0,0,0.08)'
        }}>
          {results.map((place, idx) => (
            <div 
              key={idx}
              onClick={() => handleSelect(place)}
              style={{
                padding: '12px 16px',
                borderBottom: idx < results.length - 1 ? '1px solid rgba(0,0,0,0.06)' : 'none',
                cursor: 'pointer',
                transition: 'background 0.2s ease',
                display: 'flex',
                flexDirection: 'column',
                gap: '4px'
              }}
              onMouseEnter={e => e.currentTarget.style.background = 'rgba(26, 115, 232, 0.05)'}
              onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
            >
              <div style={{fontWeight: '600', color: '#111', fontSize: '13px'}}>
                {place.name || place.display_name.split(',')[0]}
              </div>
              <div style={{color: '#666', fontSize: '11px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>
                {place.display_name}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default SearchBar;
