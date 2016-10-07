/**
 * Created by Juanjo on 25/08/2016.
 */
$.getScript($SCRIPT_ROOT+'/static/js/biblioespectral.js');
// Mapa busqueda de Localidades

// This example adds a search box to a map, using the Google Place Autocomplete
// feature. People can enter geographical searches. The search box will return a
// pick list containing a mix of places and predicted search terms.


var localidad = {lat: 0, lng: 0, name: ''};

function EnviarControl(controlDiv, map, markers){
    var controlUI = document.createElement('div');
    controlUI.style.backgroundColor = '#fff';
    controlUI.style.border = '2px solid #fff';
    controlUI.style.borderRadius = '3px';
    controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
    controlUI.style.cursor = 'pointer';
    controlUI.style.marginBottom = '22px';
    controlUI.style.textAlign = 'center';
    controlUI.title = 'Enviar la localidad encontrada';
    controlDiv.appendChild(controlUI);

    var controlText = document.createElement('div');
    controlText.style.color = 'rgb(66,139,202)';
    controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
    controlText.style.fontSize = '16px';
    controlText.style.lineHeight = '38px';
    controlText.style.paddingLeft = '5px';
    controlText.style.paddingRight = '5px';
    controlText.innerHTML = 'Enviar <i class="glyphicon glyphicon-send"></i>';
    controlUI.appendChild(controlText);

    controlUI.addEventListener('click', function(){
        if(localidad.lat == 0 && localidad.lng == 0){
            errorMensaje(0,'err',"Ingrese una Localidad antes de enviar",$('#mensaje')[0]);
            return;
        }
        $.ajax({
            url: $SCRIPT_ROOT + '/cargar/localidad',
            method: 'POST',
            data: localidad
        }).done(function(resp){
            if(resp.hasOwnProperty('info')){
                infoMensaje(1,'info', resp.info + '. Localidad: ' + resp.loc, $('#mensaje')[0]);
            }
            if(resp.hasOwnProperty('error')){
                var m = '. Asegurarse que sea una localidad dentro de Argentina';
                errorMensaje(1,'err', resp.error + m, $('#mensaje')[0]);
            }
        });
    });
}


function initAutocomplete() {
  var map = new google.maps.Map(document.getElementById('mapa_loc'), {
    center: {lat: -34.58, lng: -58.40},
    zoom: 5,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });

  // Create the search box and link it to the UI element.
  var input = document.getElementById('pac-input');
  var searchBox = new google.maps.places.SearchBox(input);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  // Bias the SearchBox results towards current map's viewport.
  map.addListener('bounds_changed', function() {
    searchBox.setBounds(map.getBounds());
  });

  var markers = [];
  // [START region_getplaces]
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener('places_changed', function() {
    var places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }

    // Clear out the old markers.
    markers.forEach(function(marker) {
      marker.setMap(null);
    });
    markers = [];

    // For each place, get the icon, name and location.
    var bounds = new google.maps.LatLngBounds();
    places.forEach(function(place) {
      var icon = {
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25)
      };

      // Create a marker for each place.
      markers.push(new google.maps.Marker({
        map: map,
        icon: icon,
        title: place.name,
        position: place.geometry.location
      }));

        localidad.lat = markers[0].getPosition().lat();
        localidad.lng = markers[0].getPosition().lng();
        localidad.name = markers[0].getTitle();

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
  });
  // [END region_getplaces]

    var div = document.createElement('div');
    var enviarControl = new EnviarControl(div, map, markers);

    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(div);
}



