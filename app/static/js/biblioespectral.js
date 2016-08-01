/**
 * Created by Juanjo on 12 abr 2016.
 */

// Navegacion Boostrap
function navegador(item){
    $(item).addClass("active");
}

// Date-picker
function pickerdate(item) {
    $(item).datepicker({
        startDate: '01-01-2005',
        endDate: 'today',
        todayBtn: true,
        orientation: 'bottom auto',
        format: 'dd-mm-yyyy',
        language: 'es',
        todayHighlight: true
    });
}

// Validacion de formularios
function validaciones(item){
    // Evita los caracteres invalidos
    $(item).keydown(function(e){
        var accepted = [8,9,13,46,48,49,50,51,52,53,54,55,56,57,58,189]; // numeros, guion, borrar, enter
        if ($.inArray(e.keyCode, accepted) == -1){
            e.preventDefault();
        }
    });
}


// Filtro para combos selectores
function tipocobertura(){
    var elem = document.getElementById('tipo_cobertura');
    var valor = elem.options[elem.selectedIndex].value;
    var agro = [[0,''],[8,'ALFALFA'], [4,'MAIZ'], [5,'SOJA'], [16,'SORGO'], [10,'TRIGO'], [6, 'GIRASOL'], [7, 'AGROPIRO'],
                [9, 'CEBOLLA'], [11, 'ZANAHORIA'], [12, 'BARBECHO'], [13, 'CEBADA'], [14, 'RASTROJO'], [15, 'SUELO'],
                [17, 'CEBOLLA MORADA']];
    var agua = [[0,''],[3,'LAGO'], [2,'RIO'], [1,'MAR']];
    var cali = [[0,''],[18,'CALIBRACION']];
    var lab = [[0,''],[19,'LABORATORIO']];

    $('#cobertura').find('option').remove().end();

    if (valor == 0){
        for ( i = 0; i < agro.length; i++) {
            $('#cobertura').find('option').end().append('<option value="' + agro[i][0] + '">' + agro[i][1] + '</option>');
        }
        for ( i = 1; i < agua.length; i++) {
            $('#cobertura').find('option').end().append('<option value="' + agua[i][0] + '">' + agua[i][1] + '</option>');
        }
        for ( i = 1; i < cali.length; i++) {
            $('#cobertura').find('option').end().append('<option value="' + cali[i][0] + '">' + cali[i][1] + '</option>');
        }
         for ( i=1; i < lab.length; i++){
            $('#cobertura').find('option').end().append('<option value="'+lab[i][0]+'">'+lab[i][1]+'</option>');
        }
    }
    if (valor == 2) {
        for (i = 0; i < agro.length; i++) {
            $('#cobertura').find('option').end().append('<option value="' + agro[i][0] + '">' + agro[i][1] + '</option>');
        }
    }
    if (valor == 1) {
        for (i = 0; i < agua.length; i++) {
            $('#cobertura').find('option').end().append('<option value="' + agua[i][0] + '">' + agua[i][1] + '</option>');
        }
    }
    if (valor == 3) {
        for (i = 0; i < cali.length; i++) {
            $('#cobertura').find('option').end().append('<option value="' + cali[i][0] + '">' + cali[i][1] + '</option>');
        }
    }
    if (valor == 4) {
        for (i=0; i < lab.length; i++){
            $('#cobertura').find('option').end().append('<option value="'+lab[i][0]+'">'+lab[i][1]+'</option>');
        }
    }

    elem.options[elem.selectedIndex].value = valor;

    return elem.options[elem.selectedIndex].value = valor;
}
// Llamado que crea y amplia una tabla de datos, instancia el grafico de tortas, pasa el dato y lo dibuja.
function dibujarGrafico(){
    // Crear la tabla de datos
    var data = new google.visualization.DataTable();
    data.addColumn('number', 'X');
    data.addColumn('number', 'Cebolla');
    data.addColumn('number', 'Trigo');

    data.addRows([
        [0,3,5], [1,5,3], [2,4,8], [3,6,2], [4,3,7],
        [5,1,2], [6,2,2], [7,2,5], [8,3,1], [9,2,5],
        [10,1,1],[11,1,2],[12,2,5],[13,5,4],[14,2,6],
        [15,3,1],[16,5,7],[17,3,6],[18,8,3],[19,6,7],
        [20,5,2],[21,4,6],[22,6,8],[23,2,1],[24,5,2]
    ]);

    // Conf optiones del grafico
    var options = {hAxis:{title: 'Longitud de onda', format:'decimal'},
                    vAxis:{title: 'Cantidades'},
                    colors:['#e2431e','#43459d'],
                    pointSize:5,
                    pointShape:'square',
                    curveType: 'function',
                    legend: { position: 'bottom' }
    };

    // Instanciar y dibujar el grafico, pasando algunas opciones
    var grafico = new google.visualization.LineChart(document.getElementById('grafico_linea'));

    grafico.draw(data, options);
}

// Configurar a llamado a ejecucion cuando la API de visualizacion de Google esta cargada



// Funcion de post.html
function translate(sourceLang, destLang, sourceId, destId, loadingId){
    $(destId).hide();
    $(loadingId).show();
    $.post('/translate', {
        text: $(sourceId).text(),
        sourceLang: sourceLang,
        destLang: destLang
    }).done(function(translated){
        $(destId).text(translated['text']);
        $(loadingId).hide();
        $(destId).show();
    }).fail(function(){
        $(destId).text('{{gettext("Error: No se puede conectar al servidor.")}}');
        $(loadingId).hide();
        $(destId).show();
    });
}
