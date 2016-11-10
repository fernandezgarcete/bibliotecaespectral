/**
 * Created by Juanjo on 25/08/2016.
 */

// Cargar el plugin Polygon Manager de Leaflet leaflet.pm.min.js
//$.getScript('https://code.jquery.com/jquery-latest.js');



// Mapas base
var calles = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/{id}/{z}/{x}/{y}?access_token={accessToken}', {
        //attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
        //'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; ' +
        //'<a href="http://mapbox.com">Mapbox</a>',
        id: '256',
        maxZoom: 18,
        accessToken: 'pk.eyJ1IjoibXJqdWFuam8iLCJhIjoiY2lzYXFyZGVwMDAwYTJ1bTZuaGVvYjl0MiJ9.WT1_Np3aSmvenQLTw6UPZw'
    }),
    satelite = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v9/tiles/{id}/{z}/{x}/{y}?access_token={accessToken}', {
        ///attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
        //'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; ' +
        //'<a href="http://mapbox.com">Mapbox</a>',
        id: '256',
        maxZoom: 18,
        accessToken: 'pk.eyJ1IjoibXJqdWFuam8iLCJhIjoiY2lzYXFyZGVwMDAwYTJ1bTZuaGVvYjl0MiJ9.WT1_Np3aSmvenQLTw6UPZw'
    });


var mapasBase = {
    'Calles': calles,
    'Satelite': satelite
};

// Creación del Objeto Mapa
var mimapa = L.map('mapa_punto', {
    center: [-34.58, -58.40],
    zoom: 10,
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

// Agregar un identificador al mapa
var marcador = L.marker([-34.582, -58.41]);
marcador.addTo(mimapa);


var latlng = {lat:marcador.getLatLng().lat, lng:marcador.getLatLng().lng};
marcador.bindPopup('Ingrese Latitud Longitud');



// Tratando con eventos
var popup = L.popup();


marcador.openPopup();




