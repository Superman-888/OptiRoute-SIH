import re

with open('src/App.jsx', 'r') as f:
    content = f.read()

# 1. Icons
icons_new = """const vehicleColors = ['#ea4335', '#1a73e8', '#34a853', '#fbbc04', '#ff00ff', '#00ffff'];

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
      <path d="M172.268 501.67C26.97 291.031 0 269.413 0 192 0 85.961 85.961 0 192 0s192 85.961 192 192c0 77.413-26.97 99.031-172.268 309.67-9.535 13.774-29.93 13.773-39.464 0z" fill="#ea4335" stroke="white" stroke-width="12"/>
      <path d="M192 90 L100 170 L120 170 L120 280 L264 280 L264 170 L284 170 Z" fill="white"/>
    </svg>
    <div style="background: #ea4335; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; margin-top: -12px; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">
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
"""

content = re.sub(
    r"const createModernIcon =.*?const destinationIcon = createModernIcon\('#ea4335'\); // Premium Red for Destinations",
    icons_new,
    content,
    flags=re.DOTALL
)

# 2. State & Logic Replace
state_new = """  /* ---------------- STATE ---------------- */
  const [depot, setDepot] = useState(null);
  const [selectingDepot, setSelectingDepot] = useState(false);

  const [fleet, setFleet] = useState([
    { id: 1, name: 'Vehicle 1', capacity: 100, color: vehicleColors[0], destinations: [] }
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

  useEffect(() => {
    fetch("http://127.0.0.1:8000/traffic/metrics")
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
    const newDestination = {
      node_id: globalDestId,
      display_id: `D${globalDestId}`,
      latitude: location.latitude,
      longitude: location.longitude,
      demand: 50,
      earliest: 0,
      latest: 1000,
      service_time: 10,
    };
    setGlobalDestId(prev => prev + 1);

    setFleet(current => current.map(v => 
      v.id === activeVehicleId 
        ? { ...v, destinations: [...v.destinations, newDestination] } 
        : v
    ));
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
    setFleet(current => [
      ...current,
      {
        id: current.length + 1,
        name: `Vehicle ${current.length + 1}`,
        capacity: 100,
        color: vehicleColors[current.length % vehicleColors.length],
        destinations: []
      }
    ]);
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

        const response = await fetch("http://127.0.0.1:8000/optimization", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          throw new Error(`Vehicle ${vehicle.id} failed`);
        }

        const data = await response.json();
        if (data.status === "success" && data.routes && data.routes.length > 0) {
           const routeData = data.routes[0];
           const sequenceDisplay = routeData.sequence.map(seq => {
             if (seq === 'Depot') return 'Depot';
             const dest = vehicle.destinations.find(d => d.node_id === parseInt(seq));
             return dest ? dest.display_id : seq;
           });
           
           allVehiclesResult.push({
             ...vehicle,
             routePath: routeData.path.map(p => [p.lat || p.latitude, p.lng || p.longitude]),
             routeDistance: routeData.distance,
             routeTime: routeData.travel_time,
             utilization: routeData.utilization,
             sequenceDisplay: sequenceDisplay,
             totalLoad: routeData.load,
             stopCount: vehicle.destinations.length
           });
           
           totalDist += routeData.distance;
           totalTime += routeData.travel_time;
           totalStops += vehicle.destinations.length;
        }
      }
      
      setVehicles(allVehiclesResult);
      setDistance(totalDist.toFixed(2));
      setEstimatedTime(totalTime.toFixed(0));
      setStops(totalStops);
      setIsOptimized(true);
      setSelectingDestination(false);
      setSelectingDepot(false);
      
      alert("Routes optimized successfully.");
    } catch (error) {
      console.error(error);
      alert("Optimization failed.");
    } finally {
      setLoading(false);
    }
  };
"""

content = re.sub(
    r"  /\* ---------------- DEPOT ---------------- \*/.*?  /\* =========================================================\n     UI\n     ========================================================= \*/",
    state_new + "\n\n  /* =========================================================\n     UI\n     ========================================================= */",
    content,
    flags=re.DOTALL
)

# 3. UI Replace
ui_new = """      <main className="main-content">
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
                    
                    {vehicles.map(v => (
                      <div key={v.id} style={{padding: '15px', background: 'rgba(255,255,255,0.03)', border: `1px solid ${v.color}40`, borderRadius: '8px', marginBottom: '15px', marginLeft: '15px', marginRight: '15px'}}>
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
                        
                        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', fontSize: '12px', color: 'var(--text-secondary)'}}>
                          <div>
                            <div>Distance</div>
                            <div style={{fontSize: '16px', fontWeight: 'bold', color: 'var(--text-primary)'}}>{v.routeDistance} km</div>
                          </div>
                          <div>
                            <div>Travel Time</div>
                            <div style={{fontSize: '16px', fontWeight: 'bold', color: 'var(--text-primary)'}}>{v.routeTime} min</div>
                          </div>
                        </div>
                      </div>
                    ))}
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
                          <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer', marginBottom: '10px'}} onClick={() => setActiveVehicleId(v.id)}>
                            <div style={{fontWeight: 'bold', color: v.color}}>{v.name}</div>
                            <input 
                              type="number" 
                              style={{width: '60px', padding: '4px', background: 'var(--bg-secondary)', border: '1px solid var(--border-color)', color: 'var(--text-primary)', borderRadius: '4px'}}
                              value={v.capacity}
                              onChange={(e) => updateVehicleCapacity(v.id, e.target.value)}
                              title="Capacity (kg)"
                              onClick={(e) => e.stopPropagation()}
                            />
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
                                {selectingDestination ? "Stop Adding" : `+ Add Destinations to ${v.name}`}
                              </button>
                              
                              <div style={{display: 'flex', flexWrap: 'wrap', gap: '5px'}}>
                                {v.destinations.map(d => (
                                  <div key={d.node_id} style={{background: 'var(--bg-secondary)', border: `1px solid ${v.color}40`, borderRadius: '12px', padding: '2px 8px', fontSize: '11px', display: 'flex', alignItems: 'center', gap: '4px'}}>
                                    <span style={{color: v.color, fontWeight: 'bold'}}>{d.display_id}</span>
                                    <span>({d.demand}kg)</span>
                                    <span onClick={() => removeDestination(v.id, d.node_id)} style={{cursor: 'pointer', color: '#ff4444'}}>×</span>
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
                
                {isOptimized && vehicles.map(v => 
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

                {isOptimized && vehicles.map((vehicle) => (
                  <React.Fragment key={vehicle.id}>
                    <Polyline
                      positions={vehicle.routePath}
                      color="#ffffff"
                      weight={8}
                      opacity={1}
                    />
                    <Polyline
                      positions={vehicle.routePath}
                      color={vehicle.color}
                      weight={4}
                      opacity={1}
                    />
                  </React.Fragment>
                ))}
              </MapContainer>
            </div>
          </div>
        ) : ("""

content = re.sub(
    r"      <main className=\"main-content\">\n        {!showDashboard \? \(\n          <div className=\"route-planner-view\">.*?<Polyline\n                      positions=\{vehicle\.routePath\}\n                      color=\"#1a73e8\"\n                      weight=\{4\}\n                      opacity=\{1\}\n                    />\n                  </React\.Fragment>\n                \)\)}\n              </MapContainer>\n            </div>\n          </div>\n        \) : \(",
    ui_new,
    content,
    flags=re.DOTALL
)

with open('src/App.jsx', 'w') as f:
    f.write(content)
