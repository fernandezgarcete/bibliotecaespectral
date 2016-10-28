/**
 * Created by Juanjo on 12 abr 2016.
 */

// Navegacion Boostrap
function navegador(item){
    $(item).addClass("active");
}

// Validacion de formularios
function validaciones(item){
    // Evita los caracteres invalidos
    $(item).keydown(function(e){
        var accepted = [8,9,13,46,48,49,50,51,52,53,54,55,56,57,58,96,97,98,99,100,101,102,103,104,105,110,189]; // numeros, guion, borrar, enter
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
    var modal = document.createElement('div');
    modal.id = nombre + id;
    modal.classList.add('modal');
    modal.classList.add('fade');
    modal.role = 'dialog';
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
    crearModal(id, 'nueva-cob', 'Nueva Cobertura', 'Cargar los datos de la nueva cobertura', 'Guardar', 'btn-primary');

    var body = $('#nueva-cob'+id+' .modal-body')[0];

    var f = $.ajax({url:$SCRIPT_ROOT+'/editar/nueva_cobertura', success: function(res){
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
                        $.ajax({url:$SCRIPT_ROOT+'/cargar/actualizarcob', method:'GET',
                            data:{id:$('#campania').val(), idtp:$('#tipo_cobertura').val()}, success: function(resp) {
                                cober.innerHTML = resp;
                            }
                        });
                    }
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
function pickerdate(item) {
    $(item).datepicker({
        startDate: '01-01-2009',
        startView: 1,
        endDate: 'today',
        todayBtn: true,
        orientation: 'bottom auto',
        format: 'dd-mm-yyyy',
        language: 'es',
        todayHighlight: true
    });
}

function pickerdate_pub(item) {
    $(item).datepicker({
        startDate: '01-01-2009',
        startView: 1,
        todayBtn: true,
        orientation: 'bottom auto',
        format: 'dd-mm-yyyy',
        language: 'es',
        todayHighlight: true
    });
}

function tipocobertura(){
    var cober = document.getElementById('ecobertura_nueva');
    if (cober == null){
        cober = document.getElementById('cobertura');
    }
    $.ajax({url:$SCRIPT_ROOT+'/cargar/actualizarcob', method:'GET',
        data:{id:$('#campania').val(), idtp:$('#tipo_cobertura').val()}, success: function(resp) {
            cober.innerHTML = resp;
        }
    });
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
            $('#id').val(camps[i].id);
            $('#ncampania').val(camps[i].nombre);
            $('#nproyecto').val(camps[i].id_pro);
            $('#nlocalidad').val(camps[i].id_loc);
            $('#nfecha').val(camps[i].fecha);
            $('#nresponsable').val(camps[i].resp);
            $('#nobjetivo').val(camps[i].obj);
            $('#nfecha_pub').val(camps[i].fecha_pub);
            $('.form-control').prop('disabled',true);
            $('.col-xs-1').css('display','block');
            limpiaResponsables();
        }
    }
}

// Rellena formulario Muestra
function rellenar_mues(nombre){
    for(var i=0; i<mues.length; i++){
        if(mues[i].nombre == nombre){
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
}

// Limpiar Formulario Tipo de Cobertura
function limpiar_tp(){
    $('#id').val(0);
    $('#nombre').val('');
    $('.form-control').prop('disabled',false);
    $('.col-xs-1').css('display','none');
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
}

// Limpia Formulario de Muestra
function limpiar_mues() {
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
}

// Limpia Formulario de Patron
function limpiar_camp() {
    $('#id').val(0);
    $('#nproyecto').val(0);
    $('#nlocalidad').val(0);
    $('#nfecha').val('');
    $('#nresponsable').val('');
    $('#nobjetivo').val('');
    $('#nfecha_pub').val('');
    contador(document.getElementById('nobjetivo'), '#bdesc', 300);
    $('.form-control').prop('disabled', false);
    $('.col-xs-1').css('display', 'none');
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
