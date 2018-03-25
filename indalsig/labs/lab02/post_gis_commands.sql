-- Commandos para crear las columnas

SELECT AddGeometryColumn('sig_nodes', 'geom', 4326, 'POINT', 2);
SELECT AddGeometryColumn('sig_ways', 'geom', 4326, 'LINESTRING', 2);

-- Crear los puntos a partir de los nodos

UPDATE sig_nodes SET geom = ST_SetSRID(ST_Point(lng, lat), 4326);

-- A partir de los puntos y su secuencia crear las vías

UPDATE sig_ways W
SET
geom = (
      SELECT ST_MakeLine(n.geom ORDER BY wn. seq)
      FROM sig_ways_nodes wn
        JOIN sig_nodes n
        ON wn.node_id = n.id
      WHERE
        wn.way_id = w.id
  	);