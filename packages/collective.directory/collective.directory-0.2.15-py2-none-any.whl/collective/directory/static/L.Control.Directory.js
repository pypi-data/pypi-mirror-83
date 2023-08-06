L.Control.Directory = L.Control.Layers.extend({
    options: {
        collapsed: false,
        position: 'topleft',
        autoZIndex: true
    },
    initialize: function (overlays, directory_title, options) {
        L.setOptions(this, options);

        this._layers = {};
        this._lastZIndex = 0;
        this._handlingClick = false;
        this._directory_title = directory_title;
        this.selectalltext = "Tout sélectionner";
        this.unselectalltext = "Tout désélectionner";
        //this._markers = markers;
        for (i in overlays) {
            this._addLayer(overlays[i], i, true);
        }
    },

    _initLayout: function () {
        var className = 'leaflet-control-layers',
            container = this._container = L.DomUtil.create('div', className);

        //Makes this work on IE10 Touch devices by stopping it from firing a mouseout event when the touch is released
        container.setAttribute('aria-haspopup', true);

        if (!L.Browser.touch) {
            L.DomEvent
                .disableClickPropagation(container)
                .disableScrollPropagation(container);
        } else {
            L.DomEvent.on(container, 'click', L.DomEvent.stopPropagation);
        }

        var form = this._form = L.DomUtil.create('form', className + '-list');

        if (this.options.collapsed) {
            if (!L.Browser.android) {
                L.DomEvent
                    .on(container, 'mouseover', this._expand, this)
                    .on(container, 'mouseout', this._collapse, this);
            }
            var link = this._layersLink = L.DomUtil.create('a', className + '-toggle', container);
            link.href = '#';
            link.title = 'Layers';

            if (L.Browser.touch) {
                L.DomEvent
                    .on(link, 'click', L.DomEvent.stop)
                    .on(link, 'click', this._expand, this);
            }
            else {
                L.DomEvent.on(link, 'focus', this._expand, this);
            }
            //Work around for Firefox android issue https://github.com/Leaflet/Leaflet/issues/2033
            L.DomEvent.on(form, 'click', function () {
                setTimeout(L.bind(this._onInputClick, this), 0);
            }, this);

            this._map.on('click', this._collapse, this);
            // TODO keyboard accessibility
        } else {
            this._expand();
        }

        this._baseLayersList = L.DomUtil.create('div', className + '-base', form);
        this._separator = L.DomUtil.create('div', className + '-separator', form);

        var selectall = this._selectall = L.DomUtil.create('a', 'category-title', form);
        selectall.innerHTML = this.unselectalltext;
        this.isselectall = false;
        L.DomEvent.on(selectall, 'click', this._selectAll, this);
        var h3 = L.DomUtil.create('h3', 'category-title', form);
        h3.innerHTML = this._directory_title;
        h3.setAttribute('rel', className + '-overlays');
        this._overlaysList = h3;
        L.DomEvent.addListener(h3, 'click', this._toggleTitle, this);
        this._overlaysList = L.DomUtil.create('div', className + '-overlays', form);

        mapHeight = parseInt($('#map').css('height'), 10);
        zoomHeight = parseInt($('.leaflet-control-zoom').css('height'), 10);
        formHeight = mapHeight-zoomHeight-80; // 80 is border and padding
        this._overlaysList.style.maxHeight = formHeight+'px';

        container.appendChild(form);
    },

    _selectAll: function() {
        var inputs = this._form.getElementsByTagName('input'),
            input, layer, hasLayer;

        this._handlingClick = true;

        for (var i = 0, len = inputs.length; i < len; i++) {
            input = inputs[i];
            layer = this._layers[input.layerId].layer;
            hasLayer = this._map.hasLayer(layer);

            if (this.isselectall) {
                //markers.addLayers(layer)
                this._map.addLayer(layer);
                input.checked = true;
            }else if (!this.isselectall) {
                //markers.removeLayers(layer);
                this._map.removeLayer(layer);
                input.checked = false;
            }
        }
        if (this.isselectall) {
            this._selectall.innerHTML = this.unselectalltext;
            this.isselectall = false;
        } else if (!this.isselectall) {
            this._selectall.innerHTML = this.selectalltext;
            this.isselectall = true;
        }
        this._handlingClick = false;
    },

    _toggleTitle:  function(e) {
        $('.'+e.currentTarget.getAttribute('rel')).toggle(200);
    }
});

L.control.directory = function (geojsonlayers, directory_title, options) {
    return new L.Control.Directory(geojsonlayers, directory_title, options);
};
