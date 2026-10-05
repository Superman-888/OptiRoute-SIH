const payload = {
  depot: { latitude: 12.9716, longitude: 77.5946 },
  customers: [
    { node_id: 1, latitude: 12.972, longitude: 77.595, demand: 10, earliest: 0, latest: 1000, service_time: 10 },
    { node_id: 2, latitude: 12.973, longitude: 77.596, demand: 10, earliest: 0, latest: 1000, service_time: 10 }
  ],
  vehicles: [
    { vehicle_id: 1, capacity: 200 }
  ]
};

fetch('https://optiroute-sih-4.onrender.com/optimization', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(payload)
}).then(res => res.json()).then(data => console.log(JSON.stringify(data, null, 2)));
