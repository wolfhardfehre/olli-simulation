var coords = L.control({position: 'bottomright'});

coords.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'coords');
    this.update();
    return this._div;
};

coords.update = function (lat, lon) {
    this._div.innerHTML = lat?
        'Lat: ' + Math.round(lat * 10000) / 10000 +
        '<br>Lon: ' + Math.round(lon * 10000) / 10000 : '';
};

coords.addTo(map);

function onMouseMove(e) {
    coords.update(e.latlng.lat, e.latlng.lng);
}

map.on('mousemove', onMouseMove);
