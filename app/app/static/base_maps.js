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
            {maxZoom:18, attribution:attr, id:mapconf.mapid, accessToken:tokens});
    layersControl.addBaseLayer(mapconf.layer, mapconf.name);
}
map.addLayer(baseConfig[0].layer);
