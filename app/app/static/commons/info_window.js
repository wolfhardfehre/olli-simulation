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
            coll += key + ': ' + props[key] + '<br>';
        }
    }
	this._div.innerHTML = '<h4>Information</h4>' + ('<sup>' + coll + '</sup>');
};
info.addTo(map);