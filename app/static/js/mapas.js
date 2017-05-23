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
var ign = L.tileLayer('https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{y}.png', {
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
/*,
 mapagris = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}', {
 attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
 '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; ' +
 '<a href="http://mapbox.com">Mapbox</a>',
 id: '256',
 maxZoom: 18,
 accessToken: 'pk.eyJ1IjoibXJqdWFuam8iLCJhIjoiY2lzYXFyZGVwMDAwYTJ1bTZuaGVvYjl0MiJ9.WT1_Np3aSmvenQLTw6UPZw'
 });*/

var mapasBase = {
    'IGN': ign,
    'OSM Calles': calles,
    //'Gris': mapagris,
    'OSM Satelite': satelite
};

// Creaci�n del Objeto Mapa

var mimapa = L.map('mapid', {
    center: [-38.15, -65.91],
    zoom: 4,
    layers: [ign]
});

// Creaci�n del Control de Capas Base y Superpuestas
var layerControl = L.control.layers(mapasBase).addTo(mimapa);

mimapa.addControl(layerControl);

// Plugin gestor de poligonos leaflet.pm
var options = {
    drawPolygon: true, // agrega boton poligon
    editPolygon: true, // agrega boton de editar
    deleteLayer: true  // agrega boton borrar
};

function redibujar(){
     mimapa = L.map('mapid', {
        center: [-38.15, -65.91],
        zoom: 4,
        layers: [ign]
    });
    mimapa.removeControl(layerControl);
    layerControl.addTo(mimapa);
    mimapa.addControl(layerControl);
    checkLayer('OSM Calles');
    checkLayer('IGN');
}

function checkLayer(label){
    var labels = document.querySelectorAll('.leaflet-control-layers-base label span');
    for(var i= 0, l=labels.length; i<l; i++){
        if(labels[i].textContent.trim(' ') == label){
            labels[i].parentNode
                .getElementsByClassName('leaflet-control-layers-selector')[0]
                .click();
            return true;
        }
    }
    return false;
}
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

// Agregar un c�rculo
var circulo = L.circle([-34.603, -58.381], 500, {
    color: 'orange',
    fillcolor: '#f03',
    fillOpacity: 0.5
});

// Agregar un pol�gono
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
function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("Ha clickeado el mapa en " + e.latlng.toString())
        .openOn(mimapa);
}

//map.on('click', onMapClick);


var muestreos;

// Funcion que agrega capas superpuestas
function agregarCapa(url, titulo) {
    var fuente = $('#fuente').val();
    var tp = $('#tipo_cobertura').val();
    var data = {};
    if (fuente) {
        data['fuente'] = fuente;
        data['tp'] = tp;
    }
    if (muestreos) {
        layerControl.removeLayer(muestreos);
        mimapa.removeLayer(muestreos);
    }
    $.ajax({
        url: url,
        method: 'GET',
        data: data,
        success: function (resp) {
            muestreos = L.geoJson(resp, {
                onEachFeature: function (feature, layer) {
                    var loc = feature.properties.name;
                    layer.bindPopup(popupConsulta(loc));
                }
            });
            muestreos.id = 'muestreos';
            layerControl.addOverlay(muestreos, titulo);
            mimapa.addLayer(muestreos);
        }
    });
}

// Armando el Popup que contendr� el bot�n de consulta
function popupConsulta(loc) {
    var c = "Campa\u00f1as ";
    return '<strong>' + loc + '</strong><br><br>' +
        '<span id="lupa" class="btn btn-info" onclick="consultaCamp(\'' + loc + '\',\'#loading\',\'#lupa\')">' + c +
        '<span class="glyphicon glyphicon-search"></span>' +
        '</span><img id="loading" style="display: none" src="/static/img/loading.gif">';
}

// Consultar campa�as de la localidad
function consultaCamp(loc, loading, btn) {
    $(btn).hide();
    $(loading).show();
    $.ajax({
        url: $SCRIPT_ROOT + '/consultar/mapa',
        method: 'POST',
        data: {loc: loc, csrf_token: $csrf_token}
    }).done(function (resp) {
        $("#result")[0].innerHTML = "<br>" + resp;
        window.location.href = '#result';
        $(btn).show();
        $(loading).hide();
    }).fail(function (resp) {
        console.log(resp)
    });
}

