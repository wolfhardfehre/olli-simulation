function setStyle(feature) {
    info.update(feature.properties);
    return feature.properties && feature.style;
}

var geojsonMarkerOptions = {
    radius: 18,
    fillColor: "#ff7800",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
};

var realtime = L.realtime({
    url: 'http://127.0.0.1:5000/animation_feed',
    crossOrigin: true,
    type: 'json'
}, {
    interval: 100,
    pointToLayer: function (feature, latlng) {
        return L.marker(latlng, {
            'icon': L.icon({
                iconUrl: '../static/images/olli.png',
                iconSize: [24, 20],
                iconAnchor: [12, 19]
            })
        });
    }
}).addTo(map);

realtime.on('update', function(e) {
    map.fitBounds(realtime.getBounds(), {maxZoom: 18});
});
