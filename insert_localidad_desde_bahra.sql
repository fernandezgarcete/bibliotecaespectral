INSERT INTO "localidad"( nombre, nombre_dpto, nombre_prov, geom)
    (SELECT nombre, nom_depto, nom_prov, the_geom FROM bahra.base
	WHERE nombre LIKE '%SAN ANTONIO OESTE%' AND nom_prov LIKE '%RIO NEGRO%');

INSERT INTO "localidad"( nombre, nombre_dpto, nombre_prov, geom)
    (SELECT nombre, nom_depto, nom_prov, the_geom FROM bahra.base
	WHERE nombre LIKE 'GUALEGUAYCHU' AND nom_prov LIKE '%ENTRE RIOS%');

INSERT INTO "localidad"( nombre, nombre_dpto, nombre_prov, geom)
    (SELECT nombre, nom_depto, nom_prov, the_geom FROM bahra.base
	WHERE nombre LIKE 'SALTO GRANDE' AND nom_prov LIKE '%ENTRE RIOS%');

INSERT INTO "localidad"( nombre, nombre_dpto, nombre_prov, geom)
    (SELECT nombre, nom_depto, nom_prov, the_geom FROM bahra.base
	WHERE nombre LIKE 'PALERMO' AND nom_prov LIKE '%CIUDAD DE BUENOS AIRES%');

INSERT INTO "localidad"( nombre, nombre_dpto, nombre_prov, geom)
    (SELECT nombre, nom_depto, nom_prov, the_geom FROM bahra.base
	WHERE nombre LIKE 'LAS GRUTAS' AND nom_prov LIKE '%RIO NEGRO%');

INSERT INTO "localidad"( nombre, nombre_dpto, nombre_prov, geom)
    (SELECT nombre, nom_depto, nom_prov, the_geom FROM bahra.base
	WHERE nombre LIKE 'PUNTA PIEDRAS' AND nom_prov LIKE '%BUENOS AIRES%');

INSERT INTO "localidad"( nombre, nombre_dpto, nombre_prov, geom)
    (SELECT nombre, nom_depto, nom_prov, the_geom FROM bahra.base
	WHERE nombre LIKE '%HILARIO ASCASUBI%' AND nom_prov LIKE '%BUENOS AIRES%');

INSERT INTO "localidad"( nombre, nombre_dpto, nombre_prov, geom)
    (SELECT nombre, nom_depto, nom_prov, the_geom FROM bahra.base
	WHERE nombre LIKE 'AZUL' AND nom_prov LIKE '%BUENOS AIRES%');

INSERT INTO "localidad"( nombre, nombre_dpto, nombre_prov, geom)
    (SELECT nombre, nom_depto, nom_prov, the_geom FROM bahra.base
	WHERE nombre LIKE '%BELL VILLE%' AND nom_prov LIKE '%CORDOBA%');

INSERT INTO "localidad"( nombre, nombre_dpto, nombre_prov, geom)
    (SELECT nombre, nom_depto, nom_prov, the_geom FROM bahra.base
	WHERE nombre LIKE '%FALDA DEL CARMEN%' AND nom_prov LIKE '%CORDOBA%');

INSERT INTO "localidad"( nombre, nombre_dpto, nombre_prov, geom)
    (SELECT nombre, nom_depto, nom_prov, the_geom FROM bahra.base
	WHERE nombre LIKE '%MONTE BUEY%' AND nom_prov LIKE '%CORDOBA%');

INSERT INTO "localidad"( nombre, nombre_dpto, nombre_prov, geom)
    (SELECT nombre, nom_depto, nom_prov, the_geom FROM bahra.base
	WHERE nombre LIKE '%PEHUAJO%' AND nom_prov LIKE '%BUENOS AIRES%');

INSERT INTO "localidad"( nombre, nombre_dpto, nombre_prov, geom)
    (SELECT nombre, nom_depto, nom_prov, the_geom FROM bahra.base
	WHERE nombre LIKE 'CHAMICAL' AND nom_prov LIKE 'LA RIOJA');

INSERT INTO "localidad"( nombre, nombre_dpto, nombre_prov, geom)
    (SELECT nombre, nom_depto, nom_prov, the_geom FROM bahra.base
	WHERE nombre LIKE 'BALCARCE' AND nom_prov LIKE 'BUENOS AIRES');

INSERT INTO "localidad"( nombre, nombre_dpto, nombre_prov, geom)
    (SELECT nombre, nom_depto, nom_prov, the_geom FROM bahra.base
	WHERE nombre LIKE 'BRAGADO' AND nom_prov LIKE 'BUENOS AIRES');

INSERT INTO "localidad"( nombre, nombre_dpto, nombre_prov, geom)
    (SELECT nombre, nom_depto, nom_prov, the_geom FROM bahra.base
	WHERE nombre LIKE '%BELGRANO%' AND nom_prov LIKE '%CIUDAD DE BUENOS AIRES%');