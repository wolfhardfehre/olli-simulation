var map = new L.Map('map');
var layersControl = new L.Control.Layers();
map.addControl(layersControl);

var baseConfig = [
    {"mapid":"mapbox.dark","name":"Mapbox Dark"},
	{"mapid":"mapbox.comic","name":"Mapbox Comic"},
	{"mapid":"mapbox.pencil","name":"Mapbox Pencil"},
	{"mapid":"mapbox.outdoors","name":"Mapbox Outdoors"},
	{"mapid":"mapbox.streets-satellite","name":"Mapbox Streets Satellite"}
];

for (var i=0; i<baseConfig.length; i++) {
    var attr = 'Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"http://mapbox.com\">Mapbox</a>';
    var tokens = token;
    var mapconf = baseConfig[i];
    mapconf.layer = new L.TileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}',
            {maxZoom:22, attribution:attr, id:mapconf.mapid, accessToken:tokens});
    layersControl.addBaseLayer(mapconf.layer, mapconf.name);
}
map.addLayer(baseConfig[0].layer);

var coords = L.control({position: 'bottomright'});
coords.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'coords');
    this.update();
    return this._div;
};
coords.update = function (lat, lon) {
    this._div.innerHTML = lat? 'Lat: ' + Math.round(lat * 10000) / 10000 +
                           '<br>Lon: ' + Math.round(lon * 10000) / 10000 : '';
};
coords.addTo(map);

function onMouseMove(e) {
    coords.update(e.latlng.lat, e.latlng.lng);
}
map.on('mousemove', onMouseMove);
var info = L.control({position: 'bottomleft'});
info.onAdd = function (map) {
	this._div = L.DomUtil.create('div', 'info');
	this.update();
	return this._div;
};

info.update = function (props) {
    var coll = '';
    for (var key in props) {
        if (props.hasOwnProperty(key)) {
            coll += key.toUpperCase() + ': ' + props[key] + '<br>';
        }
    }
	this._div.innerHTML = '<h4>Information</h4>' + (
        props ?
            '<sup>' + coll + '</sup>'
        : 'Hover over an element' );
};
info.addTo(map);

function setStyle(feature) {
    return feature.properties && feature.style;
}

function onEachFeature(feature, layer) {
	layer.on({
		mouseover: highlight,
		mouseout: resetHighlighting,
		click: zoomToFeature
	});
}

function highlight(e) {
	var layer = e.target;
	if (layer.feature.highlight) layer.setStyle(layer.feature.highlight)
	if (!L.Browser.ie && !L.Browser.opera) layer.bringToFront();
	info.update(layer.feature.properties);
}

function resetHighlighting(e) {
	elements.resetStyle(e.target);
	info.update();
}

function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
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

var overlayConfig = [
    {"mapid": elements, "name": "points"},
];

for (var i=0; i<overlayConfig.length; i++) {
    var overlay = overlayConfig[i];
    layersControl.addOverlay(overlay.mapid, overlay.name);
}