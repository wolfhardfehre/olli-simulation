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