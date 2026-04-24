// var map = L.map('map').setView([-12.1, -77.0], 15);

// // capa base (OpenStreetMap)
// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     attribution: '&copy; OpenStreetMap'
// }).addTo(map);


// let antennas = [];

// map.on('click', function(e) {
//     let lat = e.latlng.lat;
//     let lon = e.latlng.lng;

//     let marker = L.marker([lat, lon]).addTo(map);

//     antennas.push({
//         lat: lat,
//         lon: lon,
//         ptx: 30,
//         h: 10
//     });

//     console.log("Antenas:", antennas);
// });


// let heatLayer;

// function simular() {

//     if (antennas.length === 0) {
//         alert("Agrega al menos una antena");
//         return;
//     }

//     document.getElementById("loading").style.display = "block";

//     fetch("http://127.0.0.1:5000/simulate", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json"
//         },
//         body: JSON.stringify({
//             antennas: antennas,
//             frequency: 3.5
//         })
//     })
//     .then(res => res.json())
//     .then(data => {

//         let puntos = data.map(p => {
//             let intensidad = (p.value + 100) / 40;
//             return [p.lat, p.lon, intensidad];
//         });

//         if (heatLayer) {
//             map.removeLayer(heatLayer);
//         }

//         heatLayer = L.heatLayer(puntos, {
//             radius: 25
//         }).addTo(map);

//         document.getElementById("loading").style.display = "none";
//     });
// }


// fetch("http://127.0.0.1:5000/simulate", {
//     method: "POST",
//     headers: {
//         "Content-Type": "application/json"
//     },
//     body: JSON.stringify({
//         antennas: antennas,
//         frequency: 3.5
//     })
// })
// .then(res => res.json())
// .then(data => {

//     let puntos = data.map(p => {
//         let intensidad = (p.value + 100) / 40;
//         intensidad = Math.max(0, Math.min(1, intensidad));
//         return [p.lat, p.lon, intensidad];
//     });

//     if (heatLayer) {
//         map.removeLayer(heatLayer);
//     }

//     heatLayer = L.heatLayer(puntos, {
//     radius: getRadius()
//     }).addTo(map);

//     document.getElementById("loading").style.display = "none";
// })
// .catch(err => {
//     console.error(err);
//     document.getElementById("loading").style.display = "none";
//     alert("Error en la simulación");
// });


// function limpiar() {
//     antennas = [];
//     map.eachLayer(function(layer) {
//         if (layer instanceof L.Marker) {
//             map.removeLayer(layer);
//         }
//     });

//     if (heatLayer) {
//         map.removeLayer(heatLayer);
//     }
// }


// function getRadius() {
//     let zoom = map.getZoom();

//     // Ajuste empírico (puedes afinarlo)
//     return Math.max(10, zoom * 2);
// }

// map.on('zoomend', function () {
//     if (heatLayer) {
//         heatLayer.setOptions({
//             radius: getRadius()
//         });
//     }
// });



var map = L.map('map').setView([-12.1, -77.0], 15);

// capa base (OpenStreetMap)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap'
}).addTo(map);

let antennas = [];
let gridLayer = L.layerGroup().addTo(map);

// ==========================
// AGREGAR ANTENAS
// ==========================
map.on('click', function(e) {
    let lat = e.latlng.lat;
    let lon = e.latlng.lng;

    let marker = L.marker([lat, lon]).addTo(map);

    antennas.push({
        lat: lat,
        lon: lon,
        ptx: 30,
        h: 10
    });

    console.log("Antenas:", antennas);
});

// ==========================
// FUNCIÓN COLOR (PRx → COLOR)
// ==========================
function getColor(prx) {
    if (prx > -70) return "red";        // excelente
    if (prx > -80) return "orange";
    if (prx > -90) return "yellow";
    if (prx > -100) return "green";
    return "blue";                      // mala
}

// ==========================
// SIMULACIÓN
// ==========================
function simular() {

    if (antennas.length === 0) {
        alert("Agrega al menos una antena");
        return;
    }

    document.getElementById("loading").style.display = "block";

    fetch("http://127.0.0.1:5000/simulate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            antennas: antennas,
            frequency: 3.5
        })
    })
    .then(res => res.json())
    .then(data => {

        // limpiar grid anterior
        gridLayer.clearLayers();

        // tamaño de celda (~10m aprox)
        let delta = 0.00009;

        data.forEach(p => {

            let color = getColor(p.value);

            let bounds = [
                [p.lat - delta/2, p.lon - delta/2],
                [p.lat + delta/2, p.lon + delta/2]
            ];

            let rect = L.rectangle(bounds, {
                color: color,
                weight: 0,
                fillOpacity: 0.6
            });

            gridLayer.addLayer(rect);
        });

        document.getElementById("loading").style.display = "none";
    })
    .catch(err => {
        console.error(err);
        document.getElementById("loading").style.display = "none";
        alert("Error en la simulación");
    });
}

// ==========================
// LIMPIAR
// ==========================
function limpiar() {
    antennas = [];

    map.eachLayer(function(layer) {
        if (layer instanceof L.Marker) {
            map.removeLayer(layer);
        }
    });

    gridLayer.clearLayers();
}
