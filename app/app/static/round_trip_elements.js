function setStyle(feature) {
    return feature.properties && feature.style;
}


function setPopup(feature, layer) {
    var content = '';
    for (var key in feature.properties) {
        if (feature.properties.hasOwnProperty(key)) {
            content += key + ': ' + feature.properties[key] + '<br>';
        }
    }
    layer.bindPopup(content);
}

var olli = L.realtime({
    url: 'http://127.0.0.1:5000/round_trip_feed',
    crossOrigin: true,
    type: 'json'
}, {
    interval: 100,
    pointToLayer: function (feature, latlng) {
        info.update(feature.properties)
        return L.marker(latlng, {
            'icon': L.icon({
                iconUrl: '../static/images/olli.png',
                iconSize: [24, 20],
                iconAnchor: [12, 19]
            })
        });
    }
}).addTo(map);

var ground_data = L.realtime({
    url: 'http://127.0.0.1:5000/round_trip_ground_feed',
    crossOrigin: true,
    type: 'json'
}, {
    interval: 1000,
    style: setStyle,
    onEachFeature: setPopup,
    pointToLayer: function (feature, latlng) {
        return L.circle(latlng, feature.style.radius ? feature.style.radius : 500, setStyle);
    }
}).addTo(map);

olli.on('update', function(e) {
    map.fitBounds(olli.getBounds(), {maxZoom: 16});
});
