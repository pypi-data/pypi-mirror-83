directory_title = $('#directory_title').data('directory_title');
var markers = new L.MarkerClusterGroup();

var categories = {},
    categories_meta = {},
    overlayMaps = {},
    markers_category = {},
    leaflet_meta = {};

for(var index in data_categories) {
    category_title = data_categories[index]['title'];
    categories[category_title] = new L.layerGroup().addTo(map);
}

for(var index in categories) {
    markers_category[index] = [];
    overlayMaps[index] = categories[index];
}

for(var index in data_categories) {
    category_title = data_categories[index]['title'];
    var icon_url = data_categories[index]['img_url']
    for (var m in data_categories[index]['markers']){
        objmark = data_categories[index]['markers'][m];
        latlon =  new L.LatLng(
            objmark['geom']['coordinates'][1],
            objmark['geom']['coordinates'][0]
        );
        var CustomIcon = L.Icon.Default.extend({
        options: {
                iconUrl: icon_url
            }
        });
        var customIcon = new CustomIcon();
        var marker = L.marker(latlon, {icon: customIcon, title: objmark['title']});
        marker.bindPopup(
            '<a href="'+objmark['url']+'" target="_blank">'+
            '<h3>'+objmark['title']+'</h3>'+
            '</a>'+
            '<p>'+objmark['description']+'</p>');
        marker.on('mouseover', function (e) {
            this.openPopup();
        });
        markers.addLayer(marker);
        markers_category[category_title].push(marker);

    }
}


var control = L.control.directory(overlayMaps, directory_title);
/*var control = L.control.layers(null, overlayMaps, {
        collapsed: false,
        position: 'topleft'
    }
);*/

control.addTo(map);
map.addLayer(markers);

for (var row in control._layers) {
    leaflet_meta[L.Util.stamp(control._layers[row].layer)] = control._layers[row].name;
}

map.on('overlayadd', function (a) {
    var category_index = leaflet_meta[L.Util.stamp(a.layer)];
    markers.addLayers(markers_category[category_index]);
});
map.on('overlayremove', function (a) {
    var category_index = leaflet_meta[L.Util.stamp(a.layer)];
    markers.removeLayers(markers_category[category_index]);
});
