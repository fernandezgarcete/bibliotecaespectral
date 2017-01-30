/**
 * Created by Juanjo on 19/01/2017.
 */

function detalle_punto(){
    // Cargar la API de visualizaci�n y el n�cleo del paquete Chart
    google.charts.load('current', {'packages':['corechart'], 'language': 'es'});

// Configurar una ejecuci�n de la respuesta cuando la API de Visualizaci�n de Google est� cargada
    google.charts.setOnLoadCallback(dibujarGrafico);

// Respuesta que crea y expande una tabla de valores, inicializa un gr�fico, pasa los valores y los dibuja
    function dibujarGrafico(){
        // Datos para el conjunto de puntos
        var dt_data = new google.visualization.arrayToDataTable(datos.dt);
        var muestra = $('#m_nombre').children().text();

        // Configura las opciones del gr�fico
        var options = {title:'Reflectancia Promedio - '+ muestra +'\n' + $('#c_nombre').children().text(),
            //'Campa�a ' + $('#c_nombre').children().text(),
            hAxis: {title:'Longitud de Onda (nn)'},
            vAxis: {title:'Cantidades'},
            curveType: 'none',
            legend: {position: 'right'}
        };
        // Grafico comparativo de puntos
        var dt_chart = new google.visualization.AreaChart(document.getElementById('div_dt'));
        // Esperar que se termine de dibujar para llamar al m�todo getImageURI()
        google.visualization.events.addListener(dt_chart, 'ready', function(){

            // Exporta el gr�fico en un formato de imagen
            document.getElementById('btn_guardar').outerHTML = '<a href="' + dt_chart.getImageURI() +
                '" download="reflectancia-'+muestra+'.png">' +
                '<button style="float:right;" type="button" class="btn btn-info">Guardar</button></a>';
        });
        dt_chart.draw(dt_data, options);

        // Para cada punto
        for(var key in datos){
            var k = key.split(' ')[1];
            if(datos.hasOwnProperty(key) && k !== undefined){
                // Crea la tabla de valores
                var data = new google.visualization.DataTable();
                data.addColumn('number', 'Longitud de Onda');
                data.addColumn('number', 'P '+ k);
                data.addRows(datos[key]);

                // Inicializa y dibuja nuestro gr�fico, pasando algunas opciones.
                var chart = new google.visualization.LineChart(document.getElementById('div_'+k));

                // Esperar que se termine de dibujar para llamar al m�todo getImageURI()
                google.visualization.events.addListener(chart, 'ready', function(){

                    // Exporta el gr�fico en un formato de imagen
                    //document.getElementById('btn_guardar').outerHTML = '<a href="' + chart.getImageURI() +
                    //    '" download="reflectancia.png">' +
                    //    '<button style="float:right;" type="button" class="btn btn-info">Guardar</button></a>';
                });

                // Crea el gr�fico
                chart.draw(data);
            }
        }
    }
}

function detalle_muestra(){
// Cargar la API de visualizaci�n y el n�cleo del paquete Chart
    google.charts.load('current', {'packages':['corechart'], 'language': 'es'});

// Configurar una ejecuci�n de la respuesta cuando la API de Visualizaci�n de Google est� cargada
    google.charts.setOnLoadCallback(dibujarGrafico);

// Respuesta que crea y expande una tabla de valores, inicializa un gr�fico, pasa los valores y los dibuja
    function dibujarGrafico(){
        // Datos para el conjunto de muestras
        var dt_data = new google.visualization.arrayToDataTable(datos.dt);

        // Configura las opciones del gr�fico
        var options = {title:'Reflectancia Promedio de las Muestras',
            hAxis: {title:'Longitud de Onda (nn)'},
            vAxis: {title:'Cantidades'},
            curveType: 'none',
            legend: {position: 'right'}
        };
        // Grafico comparativo de puntos
        var dt_chart = new google.visualization.LineChart(document.getElementById('div_dt'));
        // Esperar que se termine de dibujar para llamar al m�todo getImageURI()
        //google.visualization.events.addListener(dt_chart, 'ready', function(){
        //
        //    // Exporta el gr�fico en un formato de imagen
        //    document.getElementById('btn_guardar').outerHTML = '<a href="' + dt_chart.getImageURI() +
        //        '" download="reflectancia_muestras.png">' +
        //        '<button style="float:right;" type="button" class="btn btn-info">Guardar</button></a>';
        //});
        dt_chart.draw(dt_data, options);

    }
}
