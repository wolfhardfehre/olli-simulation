function setStyle(feature) {
    return feature.properties && feature.style;
}

var elements = L.geoJson(points, {
    style: setStyle,
    onEachFeature: onEachFeature,
    pointToLayer: function (feature, latlng) {
        return L.circle(latlng, feature.style.radius, setStyle);
    }
});

elements.addTo(map);

var all = new L.featureGroup([elements]);
map.fitBounds(all.getBounds());

layersControl.addOverlay(elements, "Overlay");
