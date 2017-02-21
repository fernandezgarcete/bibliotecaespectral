/**
 * Created by Juanjo on 12 abr 2016.
 */

// Navegacion Boostrap
function navegador(item){
    $(item).addClass("active");
}

// Validacion de formularios
function campo_numerico(item){
    // Evita los caracteres invalidos
    $(item).keydown(function(e){
        var accepted = [8,9,13,46,48,49,50,51,52,53,54,55,56,57,58,96,97,98,99,100,101,102,103,104,105,109,110,189,190]; // numeros, guion, borrar, enter
        if ($.inArray(e.keyCode, accepted) == -1){
            e.preventDefault();
        }
    });
}

// Habilitar Edicion
function habilitar(item, boton){
    if($(boton+' i')[0].classList.contains('glyphicon-pencil')){
        $(boton+' i')[0].classList.remove('glyphicon-pencil');
        $(boton+' i')[0].classList.add('glyphicon-check');
        $(item)[0].disabled = false;
        if (($(item)[0].id).indexOf('fech') !== -1 && ($(item)[0].id).indexOf('fecha_hora') === -1){
            pickerdate_pub(item);
        }
        return
    }
    if($(boton+' i')[0].classList.contains('glyphicon-check')){
        $(boton+' i')[0].classList.remove('glyphicon-check');
        $(boton+' i')[0].classList.add('glyphicon-pencil');
        $(item)[0].disabled = true;
    }
}

// Item a consultar
function item_consulta(item){
    $(item).hide();
    if ($(item)[0].id === $('#p')[0].id){
        $('#fp').show();
    }
    if ($(item)[0].id === $('#l')[0].id){
        $('#fl').show();
    }
    if ($(item)[0].id === $('#f')[0].id){
        $('#ff').show();
    }
    if ($(item)[0].id === $('#t')[0].id){
        $('#ft').show();
    }
    if ($(item)[0].id === $('#c')[0].id){
        $('#fc').show();
    }
    if ($(item)[0].id === $('#to')[0].id){
        $('#to').show();
        $('#p').show();
        $('#l').show();
        $('#f').show();
        $('#t').show();
        $('#c').show();
        $('#fp').hide();
        $('#fl').hide();
        $('#ft').hide();
        $('#fc').hide();
        $('#ff').hide();
        $('#proyecto')[0].value = 0;
        $('#localidad')[0].value = 0;
        $('#tipo_cobertura')[0].value = 0;
        $('#fecha_inicio')[0].value = '';
        $('#fecha_fin')[0].value = '';
        $('#cobertura')[0].value = 0;
    }
}


// Evita caracteres especiales
function escapeRegExp(str) {
    return str.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
}

// Reemplaza todas las ocurrencias de un caracter
function replaceAll(str, find, replace) {
  return str.replace(new RegExp(escapeRegExp(find), 'g'), replace);
}

function limpiaResponsables(){
    var r = document.getElementById('nresponsable').value;
    var r1 = replaceAll(r,'"','');
    var r2 = replaceAll(r1,'{','');
    var r4 = replaceAll(r2,'&#34;','');
    document.getElementById('nresponsable').value = replaceAll(r4,'}','');
}

// Crear Mensaje de Error Generico
function errorMensaje(id, nombre, mens, parent){
    var alerta = document.createElement('div');
    alerta.id = nombre + id;
    alerta.classList.add('alert');
    alerta.classList.add('alert-danger');
    alerta.classList.add('alert-dismissible');
    alerta.role = 'alert';
    parent.appendChild(alerta);

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.classList.add('close');
    btn.setAttribute('data-dismissible','alert');
    btn.setAttribute('aria-label','Cerrar');
    alerta.appendChild(btn);

    var sp = document.createElement('span');
    sp.setAttribute('aria-hidden','true');
    sp.classList.add('glyphicon');
    sp.classList.add('glyphicon-remove');
    sp.classList.add('btn');
    btn.addEventListener('click', function(){alerta.remove();});
    btn.appendChild(sp);

    var tit = document.createElement('strong');
    tit.appendChild(document.createTextNode('Error: '));
    alerta.appendChild(tit);

    alerta.appendChild(document.createTextNode(mens));
}

// Crear Mensaje de Info Generico
function infoMensaje(id, nombre, mens, parent){
    var alerta = document.createElement('div');
    alerta.id = nombre + id;
    alerta.classList.add('alert');
    alerta.classList.add('alert-info');
    alerta.classList.add('alert-dismissible');
    alerta.role = 'alert';
    parent.appendChild(alerta);

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.classList.add('close');
    btn.setAttribute('data-dismissible','alert');
    btn.setAttribute('aria-label','Cerrar');
    alerta.appendChild(btn);

    var sp = document.createElement('span');
    sp.setAttribute('aria-hidden','true');
    sp.classList.add('glyphicon');
    sp.classList.add('glyphicon-remove');
    sp.classList.add('btn');
    btn.addEventListener('click', function(){alerta.remove();});
    btn.appendChild(sp);

    var tit = document.createElement('strong');
    tit.appendChild(document.createTextNode('Info: '));
    alerta.appendChild(tit);

    alerta.appendChild(document.createTextNode(mens));
}

// Crear Modal Generico
function crearModal(id, nombre, tit, mensaje, okBtnText, btnclass){
    mensaje = mensaje || '';
    okBtnText = okBtnText || '';
    btnclass = btnclass || '';
    var modal = document.createElement('div');
    modal.id = nombre + id;
    modal.classList.add('modal');
    modal.classList.add('fade');
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('tab-index','-1');
    modal.setAttribute('aria-labelledby','modal-title');
    document.body.appendChild(modal);

    var dialog = document.createElement('div');
    dialog.classList.add('modal-dialog');
    dialog.role = 'document';
    modal.appendChild(dialog);

    var content = document.createElement('div');
    content.classList.add('modal-content');
    dialog.appendChild(content);

    var header = document.createElement('div');
    header.classList.add('modal-header');
    content.appendChild(header);

    var close = document.createElement('button');
    close.type = 'button';
    close.classList.add('close');
    close.setAttribute('data-dismiss','modal');
    close.setAttribute('aria-label','Close');
    close.classList.add('glyphicon');
    close.classList.add('glyphicon-remove');
    close.classList.add('btn');
    header.appendChild(close);

    var title = document.createElement('h4');
    title.classList.add('modal-title');
    title.id = 'modal-title';
    title.appendChild(document.createTextNode(tit));
    header.appendChild(title);

    var body = document.createElement('div');
    body.classList.add('modal-body');
    content.appendChild(body);

    var mens = document.createElement('p');
        mens.appendChild(document.createTextNode(mensaje));
        body.appendChild(mens);

    if(okBtnText != '' || btnclass != ''){
        var footer = document.createElement('div');
        footer.classList.add('modal-footer');
        content.appendChild(footer);

        var cancel = document.createElement('button');
        cancel.type = 'button';
        cancel.classList.add('btn');
        cancel.classList.add('btn-default');
        cancel.setAttribute('data-dismiss','modal');
        cancel.appendChild(document.createTextNode('Cancelar'));
        footer.appendChild(cancel);

        var ok = document.createElement('a');
        ok.classList.add('btn');
        ok.classList.add(btnclass);
        ok.classList.add('btn-ok');
        ok.appendChild(document.createTextNode(okBtnText));
        footer.appendChild(ok);
    }
}

function cargarCoberturas(){
    // Cantidad de elementos a crear
    var cob = document.getElementById('cobertura');
    var cant = cob.length;
    // lugar donde agragaremos los items
    var container = document.getElementById('container');

    if(cob.value > 0){
        // Limpiar contenido previo
        while (container.hasChildNodes()){
            container.removeChild(container.lastChild);
        }
        // Agregar Coberturas existentes
        for (var i=0; i< cant; i++){
            var nombre = document.getElementById('cobertura')[i].text;
            agregarCobertura(nombre);
        }
    }
}

// Agregar Nueva Cobertura
function agregarCobertura(nombre){
    // lugar donde se agragaran los items
    var container = document.getElementById('container');
    // Nro de item actual
    var j = container.childElementCount;

    if($('select[name=tipo_cobertura]').val() == 0){
        var mens = 'Antes de agregar una Cobertura elija un Tipo de Cobertura';
        errorMensaje(j,'err',mens,container);
        return;
    }

    // Crear el nuevo nodo
    var div_col = document.createElement('div');
    div_col.id = 'col'+j;
    // agregamos al contenedor
    div_col.classList.add('col-md-6');
    div_col.classList.add('col-sm-8');
    container.appendChild(div_col);

    var div = document.createElement('div');
    div.id = 'thumb'+j;
    div.classList.add('thumbnail');
    div_col.appendChild(div);

    var cap = document.createElement('div');
    cap.id = 'cap'+j;
    cap.classList.add('caption');
    div.appendChild(cap);

    // Boton eliminar
    crearModalBorrar(j,'Borrar Cobertura','Desear borrar esta cobertura de la lista?');
    var a = document.createElement('span');
    a.id = 'a'+j;
    a.classList.add('glyphicon');
    a.classList.add('glyphicon-remove');
    a.classList.add('btn');
    a.style = 'float:right;';
    a.setAttribute('data-toggle','modal');
    a.setAttribute('data-target','#confirm-delete'+j);
    a.addEventListener('click', function(){
        var modal = document.getElementById('confirm-delete'+j);
        $('#confirm-delete'+j).on('show.bs.modal', function(e){
            $(this).find('.btn-ok').on('click', function(){
                var modal = this.parentNode.parentNode.parentNode.parentNode;
                var child = document.getElementById('col'+j);
                $('#'+modal.id).modal('hide');
                $('#'+modal.id).on('hidden.bs.modal', function(e){$('#confirm-delete'+j).remove();});
                if(document.getElementById('container').hasChildNodes()){
                    document.getElementById('container').removeChild(child);
                }
            });
        });
    });
    cap.appendChild(a);

    // Título
    var h = document.createElement('h3');
    h.id = 'cob'+j;
    cap.appendChild(h);

    // Nombre de cobertura
    if (nombre){
        h.appendChild(document.createTextNode(nombre));
    } else {
        var cob = document.getElementById('ecobertura_nueva').cloneNode(true);
        cob.disabled = false;
        cob.style = 'display:block';
        cob.id = 'cob'+j;
        cob.addEventListener('change', function(){
            var val = this.options[this.selectedIndex].text;
            if(val === 'Nueva..'){
                crearModalNuevaCobertura(j);
                $('#nueva-cob'+j).modal('show');
            } else {
                var parent = this.parentElement;
                parent.removeChild(this);
                parent.appendChild(document.createTextNode(val));
            }
        });
        h.appendChild(cob);
    }

    // Nodo para el boton agregar punto
    var p = document.createElement('p');
    cap.appendChild(p);

    // Boton agregar punto
    var b = document.createElement('span');
    b.id = 'b'+j;
    b.classList.add('btn');
    b.classList.add('btn-default');
    b.addEventListener('click', function(){
        // Crear nuevo Punto
        var nodo = this;
        crearPunto(nodo);
    });
    p.appendChild(b);
    b.appendChild(document.createTextNode('Agregar Punto'));
}

// Creacion del Punto con sus elementos
function crearPunto(nodo){
    // Nodo de la Cobertura donde se inserta el punto
    var caption = nodo.parentElement.parentElement;
    var p = nodo.parentElement;
    caption.removeChild(p);
    // Nro del punto
    var puntos = caption.childElementCount - 1;

    // Crear punto
    var punto = document.createElement('div');
    punto.id = caption.id+'p'+puntos;

    // Boton eliminar punto
    var elim = document.createElement('span');
    elim.classList.add('glyphicon');
    elim.classList.add('glyphicon-remove');
    elim.classList.add('btn');
    elim.addEventListener('click', function(){
        var child = this.parentElement;
        caption.removeChild(child);
    });
    var tit = document.createElement('h3');
    tit.innerHTML = 'Punto '+puntos+' ';
    punto.appendChild(elim);
    punto.appendChild(tit);

    // Formulario que contendra los archivos
    var f = document.createElement('form');
    f.id = 'fp'+puntos;
    $.ajax({url:$SCRIPT_ROOT+'/editar/punto', method:'GET'}).done(function(resp){
        f.innerHTML = resp;
    });
    punto.appendChild(f);

    caption.appendChild(punto);
    caption.appendChild(p);
}

// Crear Modal para Borrar
function crearModalBorrar(id, tit, mensaje){
    crearModal(id,'confirm-delete', tit, mensaje, 'Eliminar', 'btn-danger');
}

// Crear Modal Nueva Cobertura
function crearModalNuevaCobertura(id){
    crearModal(id, 'nueva-cob', 'Nueva Cobertura', 'Cargar los valores de la nueva cobertura', 'Guardar', 'btn-primary');

    var body = $('#nueva-cob'+id+' .modal-body')[0];

    $.ajax({url:$SCRIPT_ROOT+'/editar/nueva_cobertura', success: function(res){
        body.innerHTML = res;
        $('#ncaltura')[0].addEventListener('keydown', function(e){
            var accepted = [8,9,13,46,48,49,50,51,52,53,54,55,56,57,58,189]; // numeros, guion, borrar, enter
            if ($.inArray(e.keyCode, accepted) == -1){
                e.preventDefault();
            }
        });
        $('#nueva-cob'+id+' .btn-ok')[0].addEventListener('click', function(){
            var valores = {};
            $.each($('#nc_form').serializeArray(), function(i,field){
                valores[field.name] = field.value;
            });
            valores['ncid_tipocobertura'] = $('select[name=tipo_cobertura]').val();
            $.ajax({method:'POST', url:$SCRIPT_ROOT+'/editar/nueva_cobertura', data:valores})
                .done(function(res){
                    if(res["cob"] === "error"){
                        errorMensaje(id,'err',res["error"],$('#nueva-cob'+id)[0]);
                    }
                    if(res["cob"] !== "error"){
                        infoMensaje(id, 'info', res["cob"],$('#nueva-cob'+id)[0]);
                        setTimeout(function() {$('#nueva-cob'+id).modal('hide');}, 2500);
                        var cober = document.getElementById('ecobertura_nueva');
                        $.ajax({url:$SCRIPT_ROOT+'/cargar/actualizarcobloc', method:'GET',
                            data:{id:$('#campania').val(), idtp:$('#tipo_cobertura').val()}, success: function(resp) {
                                cober.innerHTML = resp;
                            }
                        });
                    }
                })
                .fail(function(){

                });
        });
    }});

    $('#nueva-cob'+id).on('hidden.bs.modal', function(e){$('#nueva-cob'+id).remove(); $('#col'+id).remove();});
}

// Guardar Campaña
function guardarCamp(){
    var con = document.getElementById("container");
    var txt = '';
    if(con.children.length > 0){
        for (var k=0; k < con.children.length; k++){
            txt += document.getElementById("cob"+k).textContent;
            if (k < con.children.length-1){
                txt += ",";
            }
        }
    }
    $("#cobertura").val(txt);
}

// Date-picker
function picker_carga(item) {
    var today = new Date();
    var dd = today.getDate()+7;
    var mm = today.getMonth()+1; // Enero es 0!
    var yyyy = today.getFullYear();
    if(dd<10){dd = '0'+dd;}
    if(mm<10){mm = '0'+mm;}
    today = yyyy+'-'+mm+'-'+dd;
    $(item).datepicker({
        startDate: '2009-01-01',
        endDate: today,
        todayBtn: true,
        orientation: 'bottom auto',
        format: 'yyyy-mm-dd',
        language: 'es',
        todayHighlight: true
    });
}

// Date-picker
function pickerdate(item) {
    $(item).datepicker({
        startDate: '01-01-2009',
        startView: 1,
        endDate: 'today',
        todayBtn: true,
        orientation: 'bottom auto',
        format: 'yyyy-mm-dd',
        language: 'es',
        todayHighlight: true
    });
}

function piker_hora(item){
    $(item).datetimepicker({
        minDate: '2009-01-01',
        maxDate: moment(),
        format: 'YYYY-MM-DD HH:mm:ss',
        locale: 'es'
    });
}

function pickerdate_pub(item) {
    $(item).datepicker({
        startDate: '01-01-2009',
        startView: 1,
        todayBtn: true,
        orientation: 'bottom auto',
        format: 'yyyy-mm-dd',
        language: 'es',
        todayHighlight: true
    });
}

// Actualiza la Cobertura al cambiar el Tipo de Cobertura
function tipocobertura(tp){
    var cober = document.getElementById('ecobertura_nueva');
    var loc = document.getElementById('localidad');
    if (cober == null){
        cober = document.getElementById('cobertura');
    }
    var idtp = $('#tipo_cobertura').val();
    if($.type(idtp) === "array"){ idtp = tp }
    $.ajax({url:$SCRIPT_ROOT+'/cargar/actualizarcobloc', method:'GET',
        data:{id:$('#campania').val(), idtp:idtp}, success: function(resp) {
            var resps = resp.trim('\t').split('\n');
            cober.innerHTML = resps[0];
            loc.innerHTML = resps[1];
        }
    });
}

// Actualiza el Tipo de Cobertura al cambiar la Fuente de Datos
function fuente_datos(){
    var tp = document.getElementById('tipo_cobertura');
    $.ajax({url:$SCRIPT_ROOT+'/cargar/actualizartp', method:'GET',
        data:{idfd:$('#fuente').val()}
    }).done(function(resp){
        tp.innerHTML = resp;
        var n3 = $('#n3_tp');
        n3.empty();
        var tps = '';
        $('#tipo_cobertura > option').each(function() {
            if (this.value > 0) {
                tps += '<label class="flat-butt btn-info btn" onclick="bN4(event,' + this.value + ')">' +
                    '<input type="radio" id="b_' + this.text + '" >' + this.text +
                    '</label>';
            }
        });
        n3.append($.parseHTML(tps));
        // Muestra los items de niveles 3
        $('#n3').css('display', 'block');
    });
}

// Llamado que crea y amplia una tabla de valores, instancia el grafico de tortas, pasa el dato y lo dibuja.
function dibujarGrafico(){
    // Crear la tabla de valores
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

// Contador de caracteres para Areas de Texto
function contador(field, counter, limit){
    if (field.value.length > limit){
        field.value = field.value.substring(0, limit);
        return false;
    } else {
        $(counter).text(limit - field.value.length);
    }
}

Object.size = function(obj){
    var size = 0, key;
    for(key in obj){
        if(obj.hasOwnProperty(key)) size++;
    }
    return size;
};

// Rellena formulario de Metodología
function rellenar_metod(nombre){
    for(var i=0; i<metods.length; i++){
        if(metods[i].nombre == nombre){
            $('#id').val(metods[i].id);
            $('#nombre').val(metods[i].nombre);
            $('#descripcion').val(metods[i].descripcion);
            $('#medicion').val(metods[i].medicion);
            $('#cenit').val(metods[i].cenit);
            $('#azimut').val(metods[i].azimut);
            contador(document.getElementById('descripcion'),'#bdesc',600);
            contador(document.getElementById('medicion'),'#bmed',600);
            $('.form-control').prop('disabled',true);
            $('.col-xs-1').css('display','block');
        }
    }
}

// Rellena formulario de Proyecto
function rellenar_proyecto(nombre){
    for(var i=0; i<proyectos.length; i++){
        if(proyectos[i].nombre == nombre){
            $('#id').val(proyectos[i].id);
            $('#nombre').val(proyectos[i].nombre);
            $('#descripcion').val(proyectos[i].descripcion);
            $('#responsables').val(proyectos[i].responsables);
            $('#status').val(proyectos[i].status);
            document.getElementById('status').checked = proyectos[i].status;
            contador(document.getElementById('descripcion'),'#bdesc',600);
            $('.form-control').prop('disabled',true);
            $('.col-xs-1').css('display','block');
        }
    }
}

// Rellena formulario de Proyecto
function rellenar_cob(nombre){
    for(var i=0; i<coberturas.length; i++){
        if(coberturas[i].nombre == nombre){
            $('#id').val(coberturas[i].id);
            $('#nombre').val(coberturas[i].nombre);
            $('#tipo_cobertura').val(coberturas[i].id_tp);
            $('#altura').val(coberturas[i].altura);
            $('#fenologia').val(coberturas[i].fenologia);
            $('#observaciones').val(coberturas[i].observaciones);
            contador(document.getElementById('fenologia'),'#bdesc',140);
            contador(document.getElementById('observaciones'),'#bobse',140);
            $('.form-control').prop('disabled',true);
            $('.col-xs-1').css('display','block');
        }
    }
}

// Rellena formulario de Radiometro
function rellenar_rad(nombre){
    for(var i=0; i<radiometros.length; i++){
        if(radiometros[i].nombre == nombre){
            $('#id').val(radiometros[i].id);
            $('#codigo').val(radiometros[i].codigo);
            $('#nombre').val(radiometros[i].nombre);
            $('#marca').val(radiometros[i].marca);
            $('#modelo').val(radiometros[i].modelo);
            $('#nro_serie').val(radiometros[i].nro_serie);
            $('#rango_espectral').val(radiometros[i].rango_espectral);
            $('#resolucion_espectral').val(radiometros[i].resolucion);
            $('#ancho_banda').val(radiometros[i].ancho_banda);
            $('#tiempo_escaneo').val(radiometros[i].tiempo_escaneo);
            $('#reproducibilidad').val(radiometros[i].reproducibilidad);
            $('#exactitud').val(radiometros[i].exactitud);
            $('#detector_vnir').val(radiometros[i].detector_vnir);
            $('#detector_swir1').val(radiometros[i].detector_swir1);
            $('#detector_swir2').val(radiometros[i].detector_swir2);
            $('#noise_vnir').val(radiometros[i].noise_vnir);
            $('#noise_swir1').val(radiometros[i].noise_swir1);
            $('#noise_swir2').val(radiometros[i].noise_swir2);
            $('#largo_fibra').val(radiometros[i].largo_fibra);
            $('#fov').val(radiometros[i].fov);
            $('#fov_cosenoidal').val(radiometros[i].fov_cosenoidal);
            $('#accesorio').val(radiometros[i].accesorio);
            contador(document.getElementById('accesorio'),'#bdesc',340);
            $('.form-control').prop('disabled',true);
            $('.col-xs-1').css('display','block');
        }
    }
}

// Rellena formulario de Tipo de Cobertura
function rellenar_tp(nombre){
    for(var i=0;i<tps.length;i++){
        if(tps[i].nombre == nombre){
            $('#id').val(tps[i].id);
            $('#nombre').val(tps[i].nombre);
            $('#id_fuente').val(tps[i].id_fuente);
            $('.form-control').prop('disabled',true);
            $('.col-xs-1').css('display','block');
        }
    }
}

// Rellena formulario Patron
function rellenar_pat(nombre){
    for(var i=0; i<patrones.length; i++){
        if(patrones[i].nombre == nombre){
            $('#id').val(patrones[i].id);
            $('#codigo').val(patrones[i].codigo);
            $('#nombre').val(patrones[i].nombre);
            $('#marca').val(patrones[i].marca);
            $('#modelo').val(patrones[i].modelo);
            $('#nro_serie').val(patrones[i].nro_serie);
            $('#accesorio').val(patrones[i].accesorio);
            contador(document.getElementById('accesorio'),'#bdesc',340);
            $('.form-control').prop('disabled',true);
            $('.col-xs-1').css('display','block');
        }
    }
}

// Rellena formulario Fotometro
function rellenar_fot(nombre){
    for(var i=0; i<fotometros.length; i++){
        if(fotometros[i].nombre == nombre){
            $('#id').val(fotometros[i].id);
            $('#codigo').val(fotometros[i].codigo);
            $('#nombre').val(fotometros[i].nombre);
            $('#marca').val(fotometros[i].marca);
            $('#modelo').val(fotometros[i].modelo);
            $('#nro_serie').val(fotometros[i].nro_serie);
            $('#accesorio').val(fotometros[i].accesorio);
            contador(document.getElementById('accesorio'),'#bdesc',340);
            $('.form-control').prop('disabled',true);
            $('.col-xs-1').css('display','block');
        }
    }
}

// Rellena formulario Camara
function rellenar_cam(nombre){
    for(var i=0; i<camaras.length; i++){
        if(camaras[i].nombre == nombre){
            $('#id').val(camaras[i].id);
            $('#codigo').val(camaras[i].codigo);
            $('#nombre').val(camaras[i].nombre);
            $('#marca').val(camaras[i].marca);
            $('#modelo').val(camaras[i].modelo);
            $('#nro_serie').val(camaras[i].nro_serie);
            $('#accesorio').val(camaras[i].accesorio);
            contador(document.getElementById('accesorio'),'#bdesc',340);
            $('.form-control').prop('disabled',true);
            $('.col-xs-1').css('display','block');
        }
    }
}

// Rellena formulario Campania
function rellenar_camp(nombre){
    for(var i=0; i<camps.length; i++){
        if(camps[i].nombre == nombre){
            $('.form-control').prop('disabled',false);
            $('#id').val(camps[i].id);
            $('#ncampania').val(camps[i].nombre);
            $('#nproyecto').val(camps[i].id_pro);
            $('#nlocalidad').val(camps[i].id_loc);
            $('#nfecha').val(camps[i].fecha);
            $('#nresponsable').val(camps[i].resp);
            $('#nobjetivo').val(camps[i].obj);
            $('#teledeteccion').val(camps[i].tele);
            $('#especialidad').val(camps[i].espe);
            $('#nfecha_pub').val(camps[i].fecha_pub);
            contador(document.getElementById('nobjetivo'),'#bdesc',300);
            contador(document.getElementById('teledeteccion'),'#btele',600);
            contador(document.getElementById('especialidad'),'#bespe',600);
            limpiaResponsables();
            $('.form-control').prop('disabled',true);
            $('.col-xs-1').css('display','block');
        }
    }
}

// Rellena formulario Muestra
function rellenar_mues(nombre){
    var nom = $('#nom');
    //nom.empty();
    for(var i=0; i<mues.length; i++){
        if(mues[i].nombre == nombre){
            //nom.append(document.createTextNode(mues[i].nombre));
            $('#nombre').val(mues[i].nombre);
            $('#id').val(mues[i].id);
            $('#metodologia').val(mues[i].id_met);
            $('#radiometro').val(mues[i].id_rad);
            $('#espectralon').val(mues[i].id_pat);
            $('#fotometro').val(mues[i].id_fot);
            $('#gps').val(mues[i].id_gps);
            $('#camara').val(mues[i].id_cam);
            $('#tipo_cobertura').val(mues[i].id_tp);
            $('#cobertura').val(mues[i].id_cob);
            $('.form-control').prop('disabled',true);
            $('.col-xs-1').css('display','block');
        }
    }
}

// Rellena formulario Muestra
function rellenar_punto(nombre){
    var nom = $('#nom');
    nom.empty();
    for(var i=0; i<puntos.length; i++){
        if(puntos[i].nombre == nombre){
            nom.append(document.createTextNode(puntos[i].nombre));
            $('#nombre').val(puntos[i].nombre);
            $('#id').val(puntos[i].id);
            $('#fecha_hora').val(puntos[i].fecha+' '+puntos[i].hora);
            $('#altura').val(puntos[i].altura);
            $('#presion').val(puntos[i].presion);
            $('#temp').val(puntos[i].temp);
            $('#nubosidad').val(puntos[i].nubosidad);
            $('#dir_viento').val(puntos[i].dir_viento);
            $('#vel_viento').val(puntos[i].vel_viento);
            $('#estado').val(puntos[i].estado);
            $('#cant_tomas').val(puntos[i].cant_tomas);
            $('#oleaje').val(puntos[i].oleaje);
            $('#muestra').val(puntos[i].id_muestra);
            $('#obs').val(puntos[i].obs);
            contador(document.getElementById('obs'),'#bdesc',240);
            $('.form-control').prop('disabled',true);
            $('.col-xs-1').css('display','block');
            cargar_latlng(puntos[i].geom);
        }
    }
}

function cargar_latlng(geom){
    var latlng = new L.LatLng(geom.lat, geom.lng);
    $('#lat_long').val(latlng);
    $('#lat').val(geom.lat);
    $('#lng').val(geom.lng);
    marcador.setLatLng(latlng);
    marcador.bindPopup('Lat: '+latlng.lat+', Long: '+latlng.lng);
    mimapa.setView(latlng, 14);
    mimapa.addLayer(satelite);
}

// Rellena formulario GPS
function rellenar_gps(nombre){
    for(var i=0; i<gpses.length; i++){
        if(gpses[i].nombre == nombre){
            $('#id').val(gpses[i].id);
            $('#codigo').val(gpses[i].codigo);
            $('#nombre').val(gpses[i].nombre);
            $('#marca').val(gpses[i].marca);
            $('#modelo').val(gpses[i].modelo);
            $('#nro_serie').val(gpses[i].nro_serie);
            $('#accesorio').val(gpses[i].accesorio);
            contador(document.getElementById('accesorio'),'#bdesc',340);
            $('.form-control').prop('disabled',true);
            $('.col-xs-1').css('display','block');
        }
    }
}

// Eliminar item de Entidades
function btn_eliminar_item(id, lista_entidad, titulo, mensaje, url){
    var boton = document.getElementById(id);
    boton.addEventListener('click', function(){
        var nom = this.id.substr(5);
        var data;
        for(var i=0;i<lista_entidad.length;i++){
            if(lista_entidad[i].nombre == nom){
                data = lista_entidad[i];
                data.csrf_token = $('#csrf_token').val();
                data.del = true;
            }
        }
        crearModalBorrar(data.id, titulo, mensaje+data.nombre+'"?');

        $('#confirm-delete'+data.id).on('show.bs.modal', function(e){
            var modal = $(this);
            $(this).find('.btn-ok').on('click', function(){
                modal.modal('hide');
                modal.on('hidden.bs.modal', function(e){modal.remove();});
                window.location.replace($SCRIPT_ROOT+ url +data.id);
            });
        }).modal('show');
    });
}

// Limpia Formulario de Metodologia
function limpiar_metod(){
    $('#id').val(0);
    $('#nombre').val('');
    $('#descripcion').val('');
    $('#medicion').val('');
    $('#cenit').val(0.0);
    $('#azimut').val(0.0);
    contador(document.getElementById('descripcion'),'#bdesc',600);
    contador(document.getElementById('medicion'),'#bmed',600);
    $('.form-control').prop('disabled',false);
    $('.col-xs-1').css('display','none');
    location.href = "#metod_form";
}

// Limpia Formulario de Metodologia
function limpiar_proyecto(){
    $('#id').val(0);
    $('#nombre').val('');
    $('#descripcion').val('');
    $('#responsables').val('');
    $('#status').val(false);
    document.getElementById('status').checked = false;
    contador(document.getElementById('descripcion'),'#bdesc',600);
    $('.form-control').prop('disabled',false);
    $('.col-xs-1').css('display','none');
    location.href = "#proyecto_form";
}

// Limpia Formulario de Metodologia
function limpiar_cob(){
    $('#id').val(0);
    $('#nombre').val('');
    $('#tipo_cobertura').val(0);
    $('#altura').val(0);
    $('#fenologia').val('');
    $('#observaciones').val('');
    contador(document.getElementById('fenologia'),'#bdesc',140);
    contador(document.getElementById('observaciones'),'#bobse',140);
    $('.form-control').prop('disabled',false);
    $('.col-xs-1').css('display','none');
    location.href = "#cobertura_form";
}

// Limpia Formulario de Radiometro
function limpiar_rad() {
    $('#id').val(0);
    $('#codigo').val('');
    $('#nombre').val('');
    $('#marca').val('');
    $('#modelo').val('');
    $('#nro_serie').val('');
    $('#rango_espectral').val('');
    $('#resolucion_espectral').val('');
    $('#ancho_banda').val('');
    $('#tiempo_escaneo').val(0);
    $('#reproducibilidad').val(0);
    $('#exactitud').val(0);
    $('#detector_vnir').val('');
    $('#detector_swir1').val('');
    $('#detector_swir2').val('');
    $('#noise_vnir').val('');
    $('#noise_swir1').val('');
    $('#noise_swir2').val('');
    $('#largo_fibra').val(0);
    $('#fov').val(0);
    $('#fov_cosenoidal').val('');
    $('#accesorio').val('');
    contador(document.getElementById('accesorio'), '#bdesc', 340);
    $('.form-control').prop('disabled', false);
    $('.col-xs-1').css('display', 'none');
    location.href = "#rad_form";
}

// Limpiar Formulario Tipo de Cobertura
function limpiar_tp(){
    $('#id').val(0);
    $('#nombre').val('');
    $('#id_fuente').val(0);
    $('.form-control').prop('disabled',false);
    $('.col-xs-1').css('display','none');
    location.href = "#tp_form";
}

// Limpia Formulario de Patron
function limpiar_pat() {
    $('#id').val(0);
    $('#codigo').val('');
    $('#nombre').val('');
    $('#marca').val('');
    $('#modelo').val('');
    $('#nro_serie').val('');
    $('#accesorio').val('');
    contador(document.getElementById('accesorio'), '#bdesc', 340);
    $('.form-control').prop('disabled', false);
    $('.col-xs-1').css('display', 'none');
    location.href = "#patron_form";
}

// Limpia Formulario de Muestra
function limpiar_mues() {
    //$('#nom').empty();
    $('#nombre').val('');
    $('#id').val(0);
    $('#metodologia').val(0);
    $('#radiometro').val(0);
    $('#espectralon').val(0);
    $('#fotometro').val(0);
    $('#gps').val(0);
    $('#camara').val(0);
    $('#tipo_cobertura').val(0);
    $('#cobertura').val(0);
    $('.form-control').prop('disabled', false);
    $('.col-xs-1').css('display', 'none');
    location.href = "#form_muestra";
}

// Limpia Formulario de Muestra
function limpiar_punto() {
    $('#lat').val('');
    $('#lng').val('');
    $('#nom').empty();
    $('#nombre').val('');
    $('#id').val(0);
    $('#fecha_hora').val('');
    $('#altura').val(0);
    $('#presion').val(0);
    $('#temp').val(0);
    $('#nubosidad').val(0);
    $('#dir_viento').val('');
    $('#vel_viento').val(0);
    $('#estado').val('');
    $('#cant_tomas').val(0);
    $('#oleaje').val('');
    $('#muestra').val('');
    $('#geom').val('');
    $('#obs').val('');
    $('.form-control').prop('disabled', false);
    $('.col-xs-1').css('display', 'none');
    marcador_punto();
    location.href = "#form_punto";
}

// Limpia Formulario de Patron
function limpiar_camp() {
    $('#id').val(0);
    $('#nproyecto').val(0);
    $('#nlocalidad').val(0);
    $('#nfecha').val('');
    $('#nresponsable').val('');
    $('#nobjetivo').val('');
    $('#teledeteccion').val('');
    $('#especialidad').val('');
    $('#nfecha_pub').val('');
    contador(document.getElementById('nobjetivo'), '#bdesc', 300);
    contador(document.getElementById('teledeteccion'), '#btele', 600);
    contador(document.getElementById('especialidad'), '#bespe', 600);
    $('.form-control').prop('disabled', false);
    $('.col-xs-1').css('display', 'none');
    location.href = "#n_camp";
}

// Limpia Formulario de Fotometro
function limpiar_fot() {
    $('#id').val(0);
    $('#codigo').val('');
    $('#nombre').val('');
    $('#marca').val('');
    $('#modelo').val('');
    $('#nro_serie').val('');
    $('#accesorio').val('');
    contador(document.getElementById('accesorio'), '#bdesc', 340);
    $('.form-control').prop('disabled', false);
    $('.col-xs-1').css('display', 'none');
    location.href = "#fotometro_form";
}

// Limpia Formulario de Camara
function limpiar_cam() {
    $('#id').val(0);
    $('#codigo').val('');
    $('#nombre').val('');
    $('#marca').val('');
    $('#modelo').val('');
    $('#nro_serie').val('');
    $('#accesorio').val('');
    contador(document.getElementById('accesorio'), '#bdesc', 340);
    $('.form-control').prop('disabled', false);
    $('.col-xs-1').css('display', 'none');
    location.href = "#camara_form";
}

// Limpia Formulario de Camara
function limpiar_gps() {
    $('#id').val(0);
    $('#codigo').val('');
    $('#nombre').val('');
    $('#marca').val('');
    $('#modelo').val('');
    $('#nro_serie').val('');
    $('#accesorio').val('');
    contador(document.getElementById('accesorio'), '#bdesc', 340);
    $('.form-control').prop('disabled', false);
    $('.col-xs-1').css('display', 'none');
    location.href = "#gps_form";
}

// Configurar llamado a ejecucion cuando la API de visualizacion de Google esta cargada


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

// Funcion listar todas las descargas
function listar_descargas(lista){
    var parent = document.getElementById('resultado');
    var panel = document.createElement('div');
    panel.classList.add('panel');
    panel.classList.add('panel-default');

    var head = document.createElement('div');
    head.classList.add('panel-heading');
    head.appendChild(document.createTextNode('Descargas'));

    var tabla = document.createElement('table');
    tabla.classList.add('table');

    var thead = document.createElement('thead');
    var tr = document.createElement('tr');
    var th1 = document.createElement('th');
    th1.appendChild(document.createTextNode('CONAE'));
    var th2 = document.createElement('th');
    th2.appendChild(document.createTextNode('OTROS'));
    var th3 = document.createElement('th');
    th3.appendChild(document.createTextNode('Total'));
    tr.appendChild(th1);
    tr.appendChild(th2);
    tr.appendChild(th3);
    thead.appendChild(tr);
    tabla.appendChild(thead);

    var tbody = document.createElement('tbody');
    for(var i=0;i<lista.length;i++){
        var trb = document.createElement('tr');
        var td = document.createElement('td');
        td.appendChild(document.createTextNode(lista[i].nombre+' '+lista[i].inst+' '+lista[i].fecha+' '+lista[i].archivo+' '+lista[i].tamanio));
        trb.appendChild(td);
        tbody.appendChild(trb);
    }
    tabla.appendChild(tbody);
    panel.appendChild(tabla);
    parent.appendChild(panel);
}


function modal_punto(){
    crearModal(0,'modal-latlng','Cargar Coordenadas Lat-Long','','Ok','btn-primary');

    // Cargar el CSS del mapa
    //loadjscssfile('/static/css/map.css','css');
    // Traer el HTML del servidor
    $.ajax({url:$SCRIPT_ROOT+'/punto/mapa', success: function(res){
        var body = $('.modal-body')[0];
        var div = document.createElement('div');
        div.id = 'cont';
        body.appendChild(div);
        div.innerHTML = res;
        $('.btn-ok')[0].addEventListener('click', function(){
            marcador_punto();
            $('.btn-default').click();
        });
        $('#lng').keydown(function(e){
            if(e.keyCode == 13){$('.btn-ok').click()}
        });
        campo_numerico('#lat');
        campo_numerico('#lng');
    }});
    // Cargar el JS del mapa
    //loadjscssfile('/static/js/mapa_punto.js','js');
    // Ejecutar el JS cargado
    //$.getScript('/static/js/mapa_punto.js');

}

function marcador_punto(){
    var lat = $('#lat').val();
    var lng = $('#lng').val();
    var m = $('#modal-latlng0');
    if(lat == '' || lng == ''){
        lat = -34.58;
        lng = -58.40;
        if (m.hasClass('in')) {
            errorMensaje(0,'err','Ingrese los valores de Latitud y Longitud',m);
            return
        }
    }
    try {
        var latlng = new L.LatLng(lat,lng);
    }
    catch(err) {
        if(m.hasClass('in')){
            errorMensaje(0,'err','Invalido. Igrese valores en formato numerico: -99.999',$('#mensj')[0]);
        }
        return
    }
    marcador.setLatLng(latlng);
    if(m.hasClass('in')){
        marcador.bindPopup('Lat: '+latlng.lat+', Long: '+latlng.lng);
        mimapa.setView(latlng, 14);
        mimapa.addLayer(satelite);
        marcador.openPopup();
        $('#lat_long').val(latlng);
    }else{
        marcador.bindPopup('Ingrese Latitud Longitud');
        mimapa.setView(latlng, 10);
        marcador.openPopup();
    }
}

// Carga un Archivo CSS o JS externo
function loadjscssfile(filename, filetype){
    if (filetype=="js"){ //if filename is a external JavaScript file
        var fileref=document.createElement('script');
        fileref.setAttribute("type","text/javascript");
        fileref.setAttribute("src", filename);
        return true;
    }
    else if (filetype=="css"){ //if filename is an external CSS file
        var fileref=document.createElement("link");
        fileref.setAttribute("rel", "stylesheet");
        fileref.setAttribute("type", "text/css");
        fileref.setAttribute("href", filename);
        return true;
    }
    if (typeof fileref!="undefined"){
        document.getElementsByTagName("head")[0].appendChild(fileref);
        return false;
    }
}

// Modal de Logueo
function modal_login(criterios){
    crearModal(-1, 'modal-login', 'Ingresar', '');
    var body = $('#modal-login-1 .modal-body')[0];

    $.ajax({url: $SCRIPT_ROOT+'/loginform'})
    .done(function(res) {
        body.innerHTML = res;
    });
}

function abrir_login(criterios){
    $('#modal-login-1').modal('show');
    if(!$.isEmptyObject(criterios)){
        var form = $('#loginform');
        var action = form.attr('action');
        action += '/consultar?args=' + JSON.stringify(criterios);
        form.attr('action', action);
    }
}

// Realizar el login
function logueo(){
    $('#loginform').submit(function(event){
        event.preventDefault();
        var $form = $(this);
        $('#logueando').show();
        $form.hide();
        var data = {'username':$form.find('input[name="username"]').val(),
                'password':$form.find('input[name="password"]').val(),
                'csrf_token':$form.find('input[name="csrf_token"]').val()
            },
            url = $form.attr('action');
        $.post(url,data).done(function(){
            window.location = $SCRIPT_ROOT;
        });
    });
}

// Descargar url
function descargar(url){
    window.location.href = url;
}

// seleccionar items de checkboxes para manipular
function marcar(id){
    var item = document.getElementById(id);
    $(item).prop("checked", !$(item).prop("checked"));
    var key = $(item).prop("class").split("_")[1];
    cont(key);
}

// contar checkboxes seleccionados
function cont(key){
    var cant = $(".check_"+key+":checked").length;
    $("#cont_"+key).text(" "+cant);
}

// manipular items a descargar o eliminar
function manipular(key, accion, c, m, p){
    var items = $(".check_"+key+":checked");
    var lista = [];
    if (items.length > 0 ){
        $(items).each(function(){lista.push(this.id)});
    } else {
        $("#alert0").modal("show");
        return;
    }
    var data = JSON.stringify({lista: lista, c: c, m: m, p: p, k: key, ax: accion});
    if (accion == "elim"){
        $('#confirm-delete1').on('show.bs.modal', function(e){
            var modal = $(this);
            $(this).find('.btn-ok').on('click', function(){
                modal.modal('hide');
                modal.on('hidden.bs.modal', function(e){modal.remove();});
                // Accion especifica del boton
                manipular_archivos(data);
            });
            // Mensaje para Rellenar el Body del Modal
            var msg = "<p>Est&aacute; seguro de eliminar?</p>";
            if(lista.length > 1){
                msg += "<ul>";
                lista.forEach(function(item){
                    msg += "<li>"+item+"</li>";
                });
                msg += "</ul>";
            } else {
                msg += "<p>"+lista[0]+"</p>";
            }
            msg += "<br><p>Cantidad de archivos: <strong>"+lista.length+"</strong></p>";
            $(this).find('.modal-body').empty().append(msg);
        }).modal('show');
    } else {
        manipular_archivos(data);
    }
}

// Accion especifica de la manipulacion de archivos
function manipular_archivos(data){
    progress("start");
    $.ajax({url:"/archivos/manipular?args="+encodeURIComponent(data)})
        .done(function(resp, status, xhr){
            if (resp.accion === "eliminado"){
                // realiza un F5 de la pag
                location.reload(true);
            } else {
                var URL = window.URL || window.webkitURL;
                if (resp.file) {
                    // usa el atributo a[download] de HTML5 para especificar nombre de archivo
                    var downloadURL = resp.file;
                    var a = document.createElement("a");
                    // Safari aun no lo soporta
                    if (typeof a.download === 'undefined'){
                        // Descargar
                        window.location = downloadURL;
                    } else {
                        // Descargar
                        a.id = "eliminame";
                        a.href = resp.file;
                        document.body.appendChild(a);
                        a.click();
                        eliminar_archivo(resp);
                    }
                } else {
                    console.log("no se pudo descargar");
                }
                setTimeout(function(){URL.revokeObjectURL(downloadURL);}, 100); // Limpiar
            }
        }).fail(function (resp) {
            console.log(resp);
        });
}

// Eliminar el archivo temporal
function eliminar_archivo(resp){
    var split1 = resp.file.split('/');
    progress("stop");
    $('#eliminame').remove();
    if(split1.length == 3){
        var dir = split1[1].split('%5C');
        if (dir.length > 0){
            var data = JSON.stringify({
                lista: [split1[split1.length-1]],
                c: dir[dir.length-4],
                m: dir[dir.length-3],
                p: dir[dir.length-2],
                k: dir[dir.length-1],
                ax: 'elim'});
            $.ajax({url:"/archivos/eliminar?args="+encodeURIComponent(data)})
                .done(function(resp){
                    if (resp.accion !== "eliminado") {
                        console.log(resp);
                    }
                }).fail(function (resp) {
                    console.log(resp);
                });
        }
    }
}

// llama a la url /progress para iterar
function progress(status){
    var bar = $(".progress-bar");
    if (status == 'start'){
        $('#progress99').modal('show');
    } else if (status == 'stop'){
        $('#progress99').modal('hide');
    }
    var source = new EventSource("/progress/" + status);
    source.onmessage = function(ev){
        bar.css("width", ev.data + "%").attr("aria-valuenow", ev.data);
    }

}

// Crea el elemento div que aloja el progress bar
function makeProgressBar(){
    crearModal('99', 'progress');
    var content = $('#progress99 .modal-content');
    content.empty();
    var divp = document.createElement("div");
    divp.classList.add("progress");
    divp.style = "width: 50%; margin: 50px; position: absolute; z-index: 1000;";
    var div = document.createElement("div");
    div.classList.add("progress-bar");
    div.classList.add("progress-bar-striped");
    div.classList.add("active");
    div.setAttribute("role", "progressbar");
    div.setAttribute("aria-valuenow", "0");
    div.setAttribute("aria-valuemin", "0");
    div.setAttribute("aria-valuemax", "100");
    div.style = "width: 0%";
    divp.appendChild(div);
    content.append(divp);
}


// Back-to-Top click function
function to_top(e){
    e.preventDefault();
    var duration = 300;
    jQuery('html, body').animate({scrollTop: 0}, duration);
    return false;
}

jQuery(document).ready(function () {
    var offset = 250;
    var duration = 300;
    jQuery(window).scroll(function(){
        if (jQuery(this).scrollTop() > offset){
            jQuery('.back-to-top').fadeIn(duration);
        } else {
            jQuery('.back-to-top').fadeOut(duration);
        }
    });
});

// Consultar todos
function todos(){
    $('#fuente').val(0);
    $('#tipo_cobertura').val(0);
    $('#cobertura').val(0);
    $('#localidad').val(0);
    $('#fecha_inicio').val('');
    $('#fecha_fin').val('');
    $('#consultarform').submit();
}
