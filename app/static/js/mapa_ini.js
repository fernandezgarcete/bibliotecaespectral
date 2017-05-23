/**
 * Created by Juanjo on 25/08/2016.
 */

// Cargar el plugin Polygon Manager de Leaflet leaflet.pm.min.js
//$.getScript($SCRIPT_ROOT+'/static/js/leaflet.pm.min.js');


// Mapas base
var ign = L.tileLayer('https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{y}.png',{
        maxZoom: 18,
        tms: true,
        attribution: 'Argenmap; <a href="http://www.ign.gob.ar">IGN</a>  '
    }),
    calles = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/{id}/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
        '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; ' +
        '<a href="http://mapbox.com">Mapbox</a>',
        id: '256',
        maxZoom: 18,
        accessToken: 'pk.eyJ1IjoibXJqdWFuam8iLCJhIjoiY2lzYXFyZGVwMDAwYTJ1bTZuaGVvYjl0MiJ9.WT1_Np3aSmvenQLTw6UPZw'
    }),
    satelite = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v9/tiles/{id}/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
        '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; ' +
        '<a href="http://mapbox.com">Mapbox</a>',
        id: '256',
        maxZoom: 18,
        accessToken: 'pk.eyJ1IjoibXJqdWFuam8iLCJhIjoiY2lzYXFyZGVwMDAwYTJ1bTZuaGVvYjl0MiJ9.WT1_Np3aSmvenQLTw6UPZw'
    });

var mapasBase = {
    'IGN': ign,
    'OSM Calles': calles,
    'OSM Satelite': satelite
};

// Creación del Objeto Mapa
var mimapa = L.map('mapa_index', {
    center: [-38.15, -65.91],
    zoom: 4,
    layers: [ign]
});

// Creación del Control de Capas Base y Superpuestas
var layerControl = L.control.layers(mapasBase).addTo(mimapa);

mimapa.addControl(layerControl);


// Tratando con eventos
var popup = L.popup();

var capas = agregarCapa($SCRIPT_ROOT+'/consultar/mapa/loc', 'Muestreos');

// Funcion que agrega capas superpuestas
function agregarCapa(url, titulo){
    $.ajax({
        url: url,
        method: 'GET',
        success: function (resp) {
            var loc = L.geoJson(resp, {
                onEachFeature: function (feature, layer){
                    var loc = feature.properties.name;
                    layer.bindPopup(popupConsulta(loc));
                }
            });
            layerControl.addOverlay(loc, titulo);
            mimapa.addLayer(loc);
        }
    });
}

// Armando el Popup que contendrá el botón de consulta
function popupConsulta(loc){
    return '<strong>'+loc+'</strong>'
}


