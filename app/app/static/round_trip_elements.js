function setStyle(feature) {
    return feature.properties && feature.style;
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
    interval: 100,
    style: setStyle,
    pointToLayer: function (feature, latlng) {
        return L.circle(latlng, feature.style.radius ? feature.style.radius : 500, setStyle);
    }
}).addTo(map);

olli.on('update', function(e) {
    map.fitBounds(olli.getBounds(), {maxZoom: 16});
});
