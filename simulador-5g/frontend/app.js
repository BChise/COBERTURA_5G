// ==========================
// MAPA
// ==========================
var map = L.map('map').setView([-12.1, -77.0], 15);

// capa base (OpenStreetMap)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap'
}).addTo(map);

// ==========================
// VARIABLES
// ==========================
let antennas = [];
let gridLayer = L.layerGroup().addTo(map);

// ==========================
// AGREGAR ANTENAS
// ==========================
map.on('click', function(e) {

    let lat = e.latlng.lat;
    let lon = e.latlng.lng;

    // valores actuales de interfaz
    let ptx = parseFloat(
        document.getElementById("ptx").value
    );

    let height = parseFloat(
        document.getElementById("height").value
    );

    // marcador visual
    let marker = L.marker([lat, lon]).addTo(map);

    // guardar antena
    antennas.push({
        lat: lat,
        lon: lon,
        ptx: ptx,
        h: height
    });

    console.log("Antenas:", antennas);
});

// ==========================
// FUNCIÓN COLOR (PRx → COLOR)
// ==========================
function getColor(prx) {

    if (prx > -60) return "red";          // excelente
    if (prx > -70) return "orange";       // muy buena
    if (prx > -80) return "yellow";       // buena
    if (prx > -90) return "green";        // media
    if (prx > -100) return "cyan";        // baja
    if (prx > -110) return "blue";        // muy baja

    return "purple";                      // sin cobertura
}

// ==========================
// SIMULACIÓN
// ==========================
function simular() {

    if (antennas.length === 0) {
        alert("Agrega al menos una antena");
        return;
    }

    // frecuencia seleccionada
    let frequency = parseFloat(
        document.getElementById("frequency").value
    );

    // modelo seleccionado
    let modelo = document.getElementById("modelo").value;

    document.getElementById("loading").style.display = "block";

    fetch("http://127.0.0.1:5000/simulate", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            antennas: antennas,
            frequency: frequency,
            modelo: modelo
        })

    })

    .then(res => res.json())

    .then(data => {

        // limpiar grid anterior
        gridLayer.clearLayers();

        // tamaño de celda (~10m)
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