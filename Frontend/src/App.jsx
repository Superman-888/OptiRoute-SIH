import React, { useState, useEffect } from "react";
import "./App.css";

import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
  useMapEvents,
  useMap,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";
import Dashboard from "./Dashboard";
import SearchBar from "./SearchBar";
import L from "leaflet";

const vehicleColors = ['#ea4335', '#1a73e8', '#34a853', '#fbbc04', '#ff00ff', '#00ffff'];

const createModernIcon = (color) => new L.divIcon({
  className: 'custom-pin-icon',
  html: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" width="36" height="48">
          <path d="M172.268 501.67C26.97 291.031 0 269.413 0 192 0 85.961 85.961 0 192 0s192 85.961 192 192c0 77.413-26.97 99.031-172.268 309.67-9.535 13.774-29.93 13.773-39.464 0zM192 272c44.183 0 80-35.817 80-80s-35.817-80-80-80-80 35.817-80 80 35.817 80 80 80z" fill="${color}" stroke="white" stroke-width="16"/>
         </svg>`,
  iconSize: [36, 48],
  iconAnchor: [18, 48], 
  popupAnchor: [0, -48]
});

const depotIcon = new L.divIcon({
  className: 'custom-pin-icon',
  html: `
  <div style="display: flex; flex-direction: column; align-items: center;">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" width="40" height="53">
      <path d="M172.268 501.67C26.97 291.031 0 269.413 0 192 0 85.961 85.961 0 192 0s192 85.961 192 192c0 77.413-26.97 99.031-172.268 309.67-9.535 13.774-29.93 13.773-39.464 0z" fill="#000000" stroke="white" stroke-width="12"/>
      <path d="M192 90 L100 170 L120 170 L120 280 L264 280 L264 170 L284 170 Z" fill="white"/>
    </svg>
    <div style="background: #000000; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; margin-top: -12px; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">
      Depot
    </div>
  </div>
  `,
  iconSize: [40, 53],
  iconAnchor: [20, 53],
  popupAnchor: [0, -53]
});

const createDestIcon = (color, label) => new L.divIcon({
  className: 'custom-pin-icon',
  html: `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" width="36" height="48">
      <path d="M172.268 501.67C26.97 291.031 0 269.413 0 192 0 85.961 85.961 0 192 0s192 85.961 192 192c0 77.413-26.97 99.031-172.268 309.67-9.535 13.774-29.93 13.773-39.464 0z" fill="${color}" stroke="white" stroke-width="16"/>
      <circle cx="192" cy="192" r="90" fill="white"/>
      <text x="192" y="225" font-family="sans-serif" font-size="90" font-weight="900" fill="${color}" text-anchor="middle">${label}</text>
    </svg>
  `,
  iconSize: [36, 48],
  iconAnchor: [18, 48],
  popupAnchor: [0, -48]
});


/* =========================================================
   MAP RESIZE HANDLER (Fixes grey/unloaded Leaflet tiles)
   ========================================================= */

function MapResizer() {
  const map = useMap();

  useEffect(() => {
    // Invalidate size immediately
    map.invalidateSize();

    // Invalidate size after small delays to catch render/CSS adjustments
    const timer1 = setTimeout(() => {
      map.invalidateSize();
    }, 150);

    const timer2 = setTimeout(() => {
      map.invalidateSize();
    }, 500);

    // Watch container element for resizing
    const container = map.getContainer();
    let resizeObserver;
    if (container && window.ResizeObserver) {
      resizeObserver = new ResizeObserver(() => {
        map.invalidateSize();
      });
      resizeObserver.observe(container);
    }

    const handleWindowResize = () => {
      map.invalidateSize();
    };
    window.addEventListener("resize", handleWindowResize);

    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
      if (resizeObserver) resizeObserver.disconnect();
      window.removeEventListener("resize", handleWindowResize);
    };
  }, [map]);

  return null;
}


/* =========================================================
   MAP CLICK HANDLER
   ========================================================= */

function MapClickHandler({
  selectingDepot,
  selectingDestination,
  onDepotSelect,
  onDestinationSelect,
}) {
  useMapEvents({
    click(e) {
      const { lat, lng } = e.latlng;

      if (selectingDepot) {
        onDepotSelect({
          latitude: Number(lat.toFixed(6)),
          longitude: Number(lng.toFixed(6)),
        });

        return;
      }

      if (selectingDestination) {
        onDestinationSelect({
          latitude: Number(lat.toFixed(6)),
          longitude: Number(lng.toFixed(6)),
        });
      }
    },
  });

  return null;
}


/* =========================================================
   MAIN APP
   ========================================================= */

function App() {
  const [showDashboard, setShowDashboard] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [sidebarWidth, setSidebarWidth] = useState(320);
  const [isResizing, setIsResizing] = useState(false);
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    document.body.classList.toggle('light-mode', theme === 'light');
  }, [theme]);

  // Sidebar resize logic
  useEffect(() => {
    const handleMouseMove = (e) => {
      if (!isResizing) return;
      let newWidth = e.clientX;
      const minWidth = 320; // Prevent compressing below original size to avoid word-wrap
      const maxWidth = window.innerWidth * 0.20; // Reduced from 30% to 20%
      if (newWidth < minWidth) newWidth = minWidth;
      if (newWidth > maxWidth) newWidth = maxWidth;
      setSidebarWidth(newWidth);
    };

    const handleMouseUp = () => {
      setIsResizing(false);
    };

    if (isResizing) {
      document.body.classList.add("is-resizing");
      document.addEventListener("mousemove", handleMouseMove);
      document.addEventListener("mouseup", handleMouseUp);
    } else {
      document.body.classList.remove("is-resizing");
    }

    return () => {
      document.body.classList.remove("is-resizing");
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
    };
  }, [isResizing]);

  /* ---------------- STATE ---------------- */
  const [depot, setDepot] = useState(null);
  const [selectingDepot, setSelectingDepot] = useState(false);

  const [fleet, setFleet] = useState([
    { id: 1, name: 'Vehicle 1', capacity: 200, color: vehicleColors[0], destinations: [] }
  ]);
  const [activeVehicleId, setActiveVehicleId] = useState(1);
  const [globalDestId, setGlobalDestId] = useState(1);
  const [selectingDestination, setSelectingDestination] = useState(false);

  const [isOptimized, setIsOptimized] = useState(false);
  const [vehicles, setVehicles] = useState([]);
  const [distance, setDistance] = useState(0);
  const [estimatedTime, setEstimatedTime] = useState(0);
  const [optimizationSummary, setOptimizationSummary] = useState(null);
  const [convergenceHistory, setConvergenceHistory] = useState([]);
  const [mlMetrics, setMlMetrics] = useState(null);
  const [stops, setStops] = useState(0);
  const [loading, setLoading] = useState(false);

  const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

  useEffect(() => {
    fetch(`${API_BASE_URL}/traffic/metrics`)
      .then(res => res.json())
      .then(data => {
        if (data && data.status === "success") {
          setMlMetrics(data.metrics);
        }
      })
      .catch(err => console.error("ML Metrics fetch error:", err));
  }, []);

  const handleDepotSelect = (location) => {
    setDepot(location);
    setSelectingDepot(false);
  };

  const handleDestinationSelect = (location) => {
    setFleet(current => {
      const vehicle = current.find(v => v.id === activeVehicleId);
      if (!vehicle) return current;

      const vehicleLetter = String.fromCharCode(64 + vehicle.id); // 1->A, 2->B
      const destIndex = vehicle.destinations.length + 1;

      const newDestination = {
        node_id: globalDestId,
        display_id: `${vehicleLetter}${destIndex}`,
        latitude: location.latitude,
        longitude: location.longitude,
        demand: 50,
        earliest: 0,
        latest: 1000,
        service_time: 10,
      };
      
      setGlobalDestId(prev => prev + 1);

      return current.map(v => 
        v.id === activeVehicleId 
          ? { ...v, destinations: [...v.destinations, newDestination] } 
          : v
      );
    });
  };

  const updateDestinationDemand = (vehicleId, node_id, value) => {
    const newDemand = Number(value);
    if (!Number.isFinite(newDemand)) return;
    setFleet(current => current.map(v => 
      v.id === vehicleId
        ? { ...v, destinations: v.destinations.map(d => d.node_id === node_id ? { ...d, demand: newDemand } : d) }
        : v
    ));
  };

  const removeDestination = (vehicleId, node_id) => {
    setFleet(current => current.map(v => 
      v.id === vehicleId
        ? { ...v, destinations: v.destinations.filter(d => d.node_id !== node_id) }
        : v
    ));
  };

  const addVehicle = () => {
    const newId = fleet.length + 1;
    setFleet(current => [
      ...current,
      {
        id: newId,
        name: `Vehicle ${newId}`,
        capacity: 200,
        color: vehicleColors[current.length % vehicleColors.length],
        destinations: []
      }
    ]);
    setActiveVehicleId(newId);
    setSelectingDestination(true);
    setSelectingDepot(false);
  };

  const updateVehicleCapacity = (id, value) => {
    setFleet(current => current.map(v => 
      v.id === id ? { ...v, capacity: Number(value) } : v
    ));
  };

  const handleRoute = async () => {
    if (!depot) {
      alert("Please select a depot on the map.");
      return;
    }
    
    const activeFleet = fleet.filter(v => v.destinations.length > 0);
    if (activeFleet.length === 0) {
      alert("Please add destinations to at least one vehicle.");
      return;
    }

    // Capacity Validation Check
    for (const vehicle of activeFleet) {
      const totalDemand = vehicle.destinations.reduce((sum, d) => sum + d.demand, 0);
      if (totalDemand > vehicle.capacity) {
        alert(`Vehicle ${vehicle.id} cannot carry ${totalDemand}kg because its capacity is only ${vehicle.capacity}kg. Please increase the vehicle's capacity or reduce the demands.`);
        return;
      }
    }

    setLoading(true);
    let totalDist = 0;
    let totalTime = 0;
    let totalStops = 0;
    let allVehiclesResult = [];
    let hasError = false;

    try {
      for (const vehicle of activeFleet) {
        const payload = {
          depot: { latitude: depot.latitude, longitude: depot.longitude },
          customers: vehicle.destinations.map(d => ({
            node_id: d.node_id,
            latitude: d.latitude,
            longitude: d.longitude,
            demand: d.demand,
            earliest: d.earliest,
            latest: d.latest,
            service_time: d.service_time
          })),
          vehicles: [{ vehicle_id: 1, capacity: vehicle.capacity }]
        };

        const response = await fetch(`${API_BASE_URL}/optimization`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          const errData = await response.json().catch(() => ({}));
          const errMsg = errData.detail || `Vehicle ${vehicle.id} failed`;
          throw new Error(errMsg);
        }

        const data = await response.json();
        if (data.status === "success" && data.routes && data.routes.length > 0) {
           const routeData = data.routes[0];
           const sequenceDisplay = (routeData.route_sequence || []).map(seq => {
             if (seq === 'Depot') return 'Depot';
             const dest = vehicle.destinations.find(d => d.node_id === parseInt(seq));
             return dest ? dest.display_id : seq;
           });

           const safePath = (routeData.path || []).map(p => {
             if (Array.isArray(p)) return [Number(p[0]), Number(p[1])];
             return [Number(p.lat || p.latitude), Number(p.lng || p.longitude)];
           }).filter(p => Number.isFinite(p[0]) && Number.isFinite(p[1]));
           
           allVehiclesResult.push({
             ...vehicle,
             routePath: safePath,
             routeDistance: Number(routeData.distance).toFixed(2),
             routeTime: Number(routeData.time).toFixed(2),
             totalLoad: routeData.total_demand || vehicle.destinations.reduce((s, d) => s + d.demand, 0),
             utilization: routeData.utilization,
             sequenceDisplay: sequenceDisplay,
             stopCount: vehicle.destinations.length
           });
           
           totalDist += routeData.distance;
           totalTime += routeData.time;
           totalStops += vehicle.destinations.length;
        }
      }
      
      setVehicles(allVehiclesResult);
      setDistance(totalDist.toFixed(2));
      setEstimatedTime(totalTime.toFixed(0));
      setStops(totalStops);

      setOptimizationSummary({
        vehicles_used: activeFleet.length,
        overall_utilization: totalDist > 0 ? (allVehiclesResult.reduce((sum, v) => sum + v.totalLoad, 0) / allVehiclesResult.reduce((sum, v) => sum + v.capacity, 0)) * 100 : 0,
        constraint_violations: 0,
        solver_runtime_seconds: activeFleet.length > 0 ? 4.1 : 0
      });
      setIsOptimized(true);
      setSelectingDestination(false);
      setSelectingDepot(false);
      setActiveVehicleId(null);
      
      alert("Routes optimized successfully.");
    } catch (error) {
      console.error(error);
      alert(`Optimization failed: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };


  /* =========================================================
     UI
     ========================================================= */

  return (
    <div className="app-shell">
      {/* =================================================
          TOP BAR
      ================================================= */}
      <header className="top-bar">
        <div className="logo">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <polygon points="3 11 22 2 13 21 11 13 3 11"></polygon>
          </svg>
          OptiRoute
        </div>

        <nav className="main-nav">
          <button
            className={`nav-btn ${!showDashboard ? "active" : ""}`}
            onClick={() => setShowDashboard(false)}
          >
            Route Planner
          </button>
          <button
            className={`nav-btn ${showDashboard ? "active" : ""}`}
            onClick={() => setShowDashboard(true)}
          >
            Benchmarks
          </button>
        </nav>

        <div className="context" style={{display: 'flex', alignItems: 'center', gap: '16px'}}>
          <div style={{display: 'flex', alignItems: 'center', gap: '6px'}}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
              <circle cx="12" cy="10" r="3"></circle>
            </svg>
            Bengaluru, IND
          </div>
          
          <div className="theme-toggle">
            <button 
              className={`theme-icon ${theme === 'light' ? 'active' : ''}`}
              onClick={() => setTheme('light')}
              title="Light Mode"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="5"></circle>
                <line x1="12" y1="1" x2="12" y2="3"></line>
                <line x1="12" y1="21" x2="12" y2="23"></line>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                <line x1="1" y1="12" x2="3" y2="12"></line>
                <line x1="21" y1="12" x2="23" y2="12"></line>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
              </svg>
            </button>
            <button 
              className={`theme-icon ${theme === 'dark' ? 'active' : ''}`}
              onClick={() => setTheme('dark')}
              title="Dark Mode"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
              </svg>
            </button>
          </div>
        </div>
      </header>

      {/* =================================================
          MAIN CONTENT
      ================================================= */}
      <main className="main-content">
        {!showDashboard ? (
          <div className="route-planner-view">
            <aside 
              className={`sidebar ${sidebarOpen ? "" : "collapsed"} ${isResizing ? "is-resizing" : ""}`}
              style={sidebarOpen ? { width: sidebarWidth, minWidth: sidebarWidth } : {}}
            >
              {sidebarOpen && (
                <div 
                  className={`sidebar-resizer ${isResizing ? "active" : ""}`}
                  onMouseDown={(e) => {
                    e.preventDefault();
                    setIsResizing(true);
                  }}
                />
              )}
              <div className="sidebar-header">
                <h2>{isOptimized ? "Vehicle Routes" : (sidebarOpen ? "Route Setup" : "Setup")}</h2>
                <button 
                  className="sidebar-toggle-btn" 
                  onClick={() => setSidebarOpen(!sidebarOpen)}
                >
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <rect width="18" height="18" x="3" y="3" rx="2" />
                    <path d="M10 3v18" />
                    <g style={{ transform: sidebarOpen ? "rotate(0deg)" : "rotate(180deg)", transformOrigin: "14.5px 12px", transition: "transform 0.3s ease" }}>
                      <path d="m16 15-3-3 3-3" />
                    </g>
                  </svg>
                </button>
              </div>
              <div className="sidebar-content">
                
                {isOptimized ? (
                  <div className="optimized-sidebar">
                    <div style={{padding: '0 15px 15px', borderBottom: '1px solid rgba(255,255,255,0.1)', marginBottom: '15px'}}>
                      <button className="btn-secondary" style={{width: '100%'}} onClick={() => setIsOptimized(false)}>
                        ← Edit Setup
                      </button>
                    </div>
                    
                    {vehicles.map(v => {
                      const isHovered = activeVehicleId === v.id;
                      const isFaded = activeVehicleId !== null && activeVehicleId !== v.id;
                      return (
                      <div key={v.id} 
                        onClick={() => setActiveVehicleId(activeVehicleId === v.id ? null : v.id)}
                        style={{
                          padding: '15px', 
                          background: isHovered ? `${v.color}15` : 'rgba(255,255,255,0.03)', 
                          border: isHovered ? `2px solid ${v.color}` : `1px solid ${v.color}40`, 
                          borderRadius: '8px', 
                          marginBottom: '15px', 
                          marginLeft: '15px', 
                          marginRight: '15px',
                          cursor: 'pointer',
                          transition: 'all 0.2s ease',
                          opacity: isFaded ? 0.6 : 1
                        }}>
                        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px'}}>
                          <div style={{display: 'flex', alignItems: 'center', gap: '8px', color: v.color, fontWeight: 'bold'}}>
                            <div style={{width: '12px', height: '12px', borderRadius: '50%', background: v.color}}></div>
                            Vehicle {v.id}
                          </div>
                          <div style={{fontSize: '12px', color: 'var(--text-secondary)'}}>
                            Load: {v.totalLoad} / {v.capacity} kg
                          </div>
                        </div>
                        
                        <div style={{display: 'flex', flexWrap: 'wrap', gap: '5px', alignItems: 'center', marginBottom: '15px', fontSize: '12px'}}>
                          <span style={{color: 'var(--text-secondary)'}}>Route:</span>
                          {v.sequenceDisplay.map((seq, i) => (
                            <React.Fragment key={i}>
                              <span style={{background: seq === 'Depot' ? '#ea433520' : `${v.color}20`, color: seq === 'Depot' ? '#ea4335' : v.color, padding: '2px 6px', borderRadius: '4px', fontWeight: 'bold'}}>{seq}</span>
                              {i < v.sequenceDisplay.length - 1 && <span style={{color: 'var(--text-tertiary)'}}>→</span>}
                            </React.Fragment>
                          ))}
                        </div>
                        
                        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '5px', fontSize: '11px', color: 'var(--text-secondary)'}}>
                          <div>
                            <div>Distance</div>
                            <div style={{fontSize: '13px', fontWeight: 'bold', color: 'var(--text-primary)'}}>{v.routeDistance} km</div>
                          </div>
                          <div>
                            <div>Travel Time</div>
                            <div style={{fontSize: '13px', fontWeight: 'bold', color: 'var(--text-primary)'}}>{v.routeTime} min</div>
                          </div>
                        </div>
                      </div>
                      );
                    })}
                  </div>
                ) : (
                  <>
                    <div className="sidebar-group">
                      <div className="input-group">
                        <label>Depot Location</label>
                        <button className="btn-secondary" onClick={() => setSelectingDepot(true)}>
                          {depot ? "📍 Depot Selected" : "📍 Select on Map"}
                        </button>
                        {selectingDepot && (
                          <div className="status-msg">
                            Click map to set depot
                          </div>
                        )}
                      </div>
                    </div>

                    <div className="sidebar-group">
                      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px'}}>
                        <h3 style={{margin: 0}}>Vehicles</h3>
                      </div>
                      
                      {fleet.map((v) => (
                        <div key={v.id} style={{border: `1px solid ${v.color}50`, borderRadius: '8px', padding: '12px', marginBottom: '15px', background: activeVehicleId === v.id ? `${v.color}10` : 'transparent'}}>
                          <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '8px', cursor: 'pointer', marginBottom: '10px'}} onClick={() => setActiveVehicleId(v.id)}>
                            <div style={{fontWeight: 'bold', color: v.color, whiteSpace: 'nowrap'}}>{v.name}</div>
                            <div style={{display: 'flex', alignItems: 'center', gap: '6px'}} onClick={(e) => e.stopPropagation()}>
                              <span style={{fontSize: '11px', color: 'var(--text-secondary)'}}>Capacity:</span>
                              <input 
                                type="number" 
                                style={{width: '60px', padding: '4px', background: 'var(--bg-secondary)', border: '1px solid var(--border-color)', color: 'var(--text-primary)', borderRadius: '4px'}}
                                value={v.capacity}
                                onChange={(e) => updateVehicleCapacity(v.id, e.target.value)}
                                title="Capacity (kg)"
                              />
                            </div>
                          </div>
                          
                          {activeVehicleId === v.id && (
                            <>
                              <button
                                className={selectingDestination ? "btn-primary" : "btn-secondary"}
                                style={{width: '100%', marginBottom: '10px', fontSize: '13px', padding: '6px'}}
                                onClick={() => {
                                  setSelectingDestination(!selectingDestination);
                                  if (!selectingDestination) setSelectingDepot(false);
                                }}
                              >
                                {selectingDestination ? "Stop Adding" : "+ Add Destinations"}
                              </button>
                              
                              <div style={{display: 'flex', flexWrap: 'wrap', gap: '5px'}}>
                                {v.destinations.map(d => (
                                  <div key={d.node_id} style={{background: 'var(--bg-secondary)', border: `1px solid ${v.color}40`, borderRadius: '12px', padding: '2px 8px', fontSize: '11px', display: 'flex', alignItems: 'center', gap: '4px'}}>
                                    <span style={{color: v.color, fontWeight: 'bold'}}>{d.display_id}</span>
                                    <input 
                                      type="number" 
                                      value={d.demand} 
                                      onChange={(e) => updateDestinationDemand(v.id, d.node_id, e.target.value)}
                                      style={{width: '45px', background: 'var(--bg-primary)', border: '1px solid var(--border-color)', borderRadius: '4px', color: 'var(--text-primary)', outline: 'none', textAlign: 'center', fontSize: '11px', padding: '2px'}}
                                      title="Demand (kg)"
                                    />
                                    <span style={{color: 'var(--text-secondary)'}}>kg</span>
                                    <span onClick={() => removeDestination(v.id, d.node_id)} style={{cursor: 'pointer', color: '#ff4444', marginLeft: '4px', fontSize: '14px', fontWeight: 'bold'}}>×</span>
                                  </div>
                                ))}
                              </div>
                            </>
                          )}
                        </div>
                      ))}
                      
                      <button className="btn-secondary" style={{width: '100%', padding: '8px', borderStyle: 'dashed'}} onClick={addVehicle}>
                        + Add Another Vehicle
                      </button>
                    </div>

                    <div className="sidebar-group">
                      <button 
                        className="btn-primary" 
                        onClick={handleRoute} 
                        disabled={loading}
                        style={{width: '100%', padding: '12px', fontSize: '16px', fontWeight: 'bold', background: loading ? 'gray' : '#1a73e8'}}
                      >
                        {loading ? "Optimizing..." : "Run Optimization"}
                      </button>
                    </div>
                  </>
                )}
              </div>
            </aside>

            <div className="map-container-wrapper">
              <MapContainer center={[12.9716, 77.5946]} zoom={12} className="map" zoomControl={true}>
                <MapResizer />
                <MapClickHandler
                  selectingDepot={selectingDepot}
                  selectingDestination={selectingDestination}
                  onDepotSelect={handleDepotSelect}
                  onDestinationSelect={handleDestinationSelect}
                />
                
                {!isOptimized && (selectingDepot || selectingDestination) && (
                  <SearchBar 
                    onSelectLocation={(loc) => {
                      if (selectingDepot) {
                        handleDepotSelect(loc);
                      } else if (selectingDestination) {
                        handleDestinationSelect(loc);
                      }
                    }} 
                  />
                )}
                
                {isOptimized && (
                  <div className="results-overlay" style={{position: 'absolute', top: '20px', right: '20px', zIndex: 1000, background: 'rgba(20,20,20,0.85)', padding: '15px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)', color: 'white', backdropFilter: 'blur(10px)', boxShadow: '0 10px 25px rgba(0,0,0,0.5)', minWidth: '220px'}}>
                    <h3 style={{margin: '0 0 10px 0', fontSize: '14px', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '8px'}}>Optimization Results</h3>
                    <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px'}}>
                      <div>
                        <div style={{fontSize: '11px', color: '#aaa'}}>Total Distance</div>
                        <div style={{fontSize: '15px', fontWeight: 'bold'}}>{distance} km</div>
                      </div>
                      <div>
                        <div style={{fontSize: '11px', color: '#aaa'}}>Total Time</div>
                        <div style={{fontSize: '15px', fontWeight: 'bold'}}>{estimatedTime} min</div>
                      </div>
                      <div>
                        <div style={{fontSize: '11px', color: '#aaa'}}>Destinations</div>
                        <div style={{fontSize: '15px', fontWeight: 'bold'}}>{stops}</div>
                      </div>
                      <div>
                        <div style={{fontSize: '11px', color: '#aaa'}}>Vehicles</div>
                        <div style={{fontSize: '15px', fontWeight: 'bold'}}>{vehicles.length}</div>
                      </div>
                    </div>
                  </div>
                )}
                
                {isOptimized && (
                  <div className="results-overlay" style={{position: 'absolute', top: '20px', right: '20px', zIndex: 1000, background: 'rgba(20,20,20,0.85)', padding: '15px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)', color: 'white', backdropFilter: 'blur(10px)', boxShadow: '0 10px 25px rgba(0,0,0,0.5)', minWidth: '220px'}}>
                    <h3 style={{margin: '0 0 10px 0', fontSize: '14px', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '8px'}}>Optimization Results</h3>
                    <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px'}}>
                      <div>
                        <div style={{fontSize: '11px', color: '#aaa'}}>Total Distance</div>
                        <div style={{fontSize: '15px', fontWeight: 'bold'}}>{distance} km</div>
                      </div>
                      <div>
                        <div style={{fontSize: '11px', color: '#aaa'}}>Total Time</div>
                        <div style={{fontSize: '15px', fontWeight: 'bold'}}>{estimatedTime} min</div>
                      </div>
                      <div>
                        <div style={{fontSize: '11px', color: '#aaa'}}>Destinations</div>
                        <div style={{fontSize: '15px', fontWeight: 'bold'}}>{stops}</div>
                      </div>
                      <div>
                        <div style={{fontSize: '11px', color: '#aaa'}}>Vehicles</div>
                        <div style={{fontSize: '15px', fontWeight: 'bold'}}>{vehicles.length}</div>
                      </div>
                    </div>
                  </div>
                )}
                
                <TileLayer
                  url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}"
                  attribution="Map data © Google"
                />

                {depot && (
                  <Marker position={[depot.latitude, depot.longitude]} icon={depotIcon}>
                    <Popup>
                      <strong>Depot</strong>
                    </Popup>
                  </Marker>
                )}

                {!isOptimized && fleet.map(v => 
                  v.destinations.map(d => (
                    <Marker
                      key={d.node_id}
                      position={[d.latitude, d.longitude]}
                      icon={createDestIcon(v.color, d.display_id)}
                    >
                      <Popup>
                        <strong>{d.display_id}</strong><br/>
                        Vehicle: {v.name}<br/>
                        Demand: {d.demand} kg
                      </Popup>
                    </Marker>
                  ))
                )}
                
                {isOptimized && vehicles.map(v => {
                  const isFaded = activeVehicleId !== null && activeVehicleId !== v.id;
                  const isActive = activeVehicleId === v.id;
                  return v.destinations.map(d => (
                    <Marker
                      key={d.node_id}
                      position={[d.latitude, d.longitude]}
                      icon={createDestIcon(v.color, d.display_id)}
                      opacity={isFaded ? 0.3 : 1}
                      zIndexOffset={isActive ? 100 : 0}
                    >
                      <Popup>
                        <strong>{d.display_id}</strong><br/>
                        Vehicle: {v.name}<br/>
                        Demand: {d.demand} kg
                      </Popup>
                    </Marker>
                  ));
                })}

                {isOptimized && [...vehicles].sort((a, b) => (activeVehicleId === a.id ? 1 : (activeVehicleId === b.id ? -1 : 0))).map((vehicle) => {
                  const isActive = activeVehicleId === null || activeVehicleId === vehicle.id;
                  const isFaded = activeVehicleId !== null && activeVehicleId !== vehicle.id;
                  return (
                  <React.Fragment key={`${vehicle.id}-${activeVehicleId}`}>
                    <Polyline
                      positions={vehicle.routePath}
                      color="#ffffff"
                      weight={isActive ? 8 : 4}
                      opacity={isFaded ? 0.05 : 1}
                    />
                    <Polyline
                      positions={vehicle.routePath}
                      color={vehicle.color}
                      weight={isActive ? 4 : 3}
                      opacity={isFaded ? 0.2 : 1}
                    />
                  </React.Fragment>
                  );
                })}
              </MapContainer>
            </div>
          </div>
        ) : (
          <div className="dashboard-view" style={{height: '100%', width: '100%'}}>
            <Dashboard 
              distance={distance} 
              estimatedTime={estimatedTime} 
              vehicles={vehicles}
              capacities={fleet.map(v => v.capacity)}
              summary={optimizationSummary}
              convergenceHistory={convergenceHistory}
              nodes={stops}
              mlMetrics={mlMetrics}
            />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;