/**
 * Created by Juanjo on 25/08/2016.
 */

// Cargar el plugin Polygon Manager de Leaflet leaflet.pm.min.js
//$.getScript($SCRIPT_ROOT+'/static/js/leaflet.pm.min.js');

// Agrupando capas y Capas de control
var sanpedro = L.marker([-33.68, -59.66]).bindPopup('San Pedro, Buenos Aires'),
    chacabuco = L.marker([-34.64, -60.47]).bindPopup('Chacabuco, Buenos Aires'),
    riestra = L.marker([-35.27, -59.77]).bindPopup('Norberto de la Riestra, Buenos Aires'),
    lujan = L.marker([-34.56, -59.11]).bindPopup('Lujan, Buenos Aires');

var ciudades = L.layerGroup([sanpedro, chacabuco, riestra, lujan]);

// Mapas base
var calles = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/{id}/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
        '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; ' +
        '<a href="http://mapbox.com">Mapbox</a>',
        id: '256',
        maxZoom: 18,
        accessToken: 'pk.eyJ1IjoibXJqdWFuam8iLCJhIjoiY2lzYXFyZGVwMDAwYTJ1bTZuaGVvYjl0MiJ9.WT1_Np3aSmvenQLTw6UPZw'
    }),
    satellite = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v9/tiles/{id}/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
        '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; ' +
        '<a href="http://mapbox.com">Mapbox</a>',
        id: '256',
        maxZoom: 18,
        accessToken: 'pk.eyJ1IjoibXJqdWFuam8iLCJhIjoiY2lzYXFyZGVwMDAwYTJ1bTZuaGVvYjl0MiJ9.WT1_Np3aSmvenQLTw6UPZw'
    });/*,
    mapagris = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
        '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; ' +
        '<a href="http://mapbox.com">Mapbox</a>',
        id: '256',
        maxZoom: 18,
        accessToken: 'pk.eyJ1IjoibXJqdWFuam8iLCJhIjoiY2lzYXFyZGVwMDAwYTJ1bTZuaGVvYjl0MiJ9.WT1_Np3aSmvenQLTw6UPZw'
    });*/

var mapasBase = {
    'Calles': calles,
    //'Gris': mapagris,
    'Satelite': satellite
};

// Creación del Objeto Mapa
var mimapa = L.map('mapid', {
    center: [-34.58, -58.40],
    zoom: 5,
    layers: [calles]
});

// Creación del Control de Capas Base y Superpuestas
var layerControl = L.control.layers(mapasBase).addTo(mimapa);

mimapa.addControl(layerControl);

// Plugin gestor de poligonos leaflet.pm
var options = {
    drawPolygon: true, // agrega boton poligon
    editPolygon: true, // agrega boton de editar
    deleteLayer: true  // agrega boton borrar
};

// agregar controles pm al mapa
//map.pm.addControls(options);

/* Relleno del objeto mapa con un mapa base de Mapbox
L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/{id}/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
                 '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; ' +
                 '<a href="http://mapbox.com">Mapbox</a>',
    id: '256',
    maxZoom: 18,
    accessToken: 'pk.eyJ1IjoibXJqdWFuam8iLCJhIjoiY2lzYXFyZGVwMDAwYTJ1bTZuaGVvYjl0MiJ9.WT1_Np3aSmvenQLTw6UPZw'
}).addTo(map);
*/

// Agregar un identificador al mapa
var marcador = L.marker([-34.582, -58.41]);

// Agregar un círculo
var circulo = L.circle([-34.603, -58.381], 500, {
    color: 'orange',
    fillcolor: '#f03',
    fillOpacity: 0.5
});

// Agregar un polígono
var poligono = L.polygon([
    [-34.559, -58.48],
    [-34.553, -58.46],
    [-34.57, -58.45]
]);

// Agregar comentarios a los indentificadores, circulos y poligonos
marcador.bindPopup("<b>Casa</b><br>Por aca esta el edificio<br>donde vivo.");
circulo.bindPopup("500 mts alrededor del Obelisco,");
poligono.bindPopup("Barrios Coghlan, Belgrano, Colegiales.");

// Agregar un comentario al mapa independiente de un objeto que lo contenga
var popap = L.popup()
    .setLatLng([51.52, -0.09])
    .setContent("Soy un globo independiente.");

// Tratando con eventos
var popup = L.popup();

// Funcion que devuelve la ubicacion geografica en LatLng
function onMapClick(e){
    popup
        .setLatLng(e.latlng)
        .setContent("Ha clickeado el mapa en " + e.latlng.toString())
        .openOn(mimapa);
}

//map.on('click', onMapClick);

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
    var c = "Campa\u00f1as ";
    return '<strong>'+loc+'</strong><br><br>' +
        '<span class="btn btn-info" onclick="consultaCamp(\''+loc+'\')">'+ c +
        '<span class="glyphicon glyphicon-search"></span>' +
        '</span>';
}

// Consultar campañas de la localidad
function consultaCamp(loc){
    $.ajax({
        url: $SCRIPT_ROOT+'/consultar/mapa',
        method: 'POST',
        data: {loc: loc},
        success: function(resp){
            console.log(resp.indexOf("footer"));
            $("#result")[0].innerHTML = "<br>" + resp.substring(resp.indexOf("<p>"), resp.indexOf("footer"));
        }
    });
}

