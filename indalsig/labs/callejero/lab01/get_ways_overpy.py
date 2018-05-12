# -*- coding: utf-8 -*-

import overpy


# Conectar con la Overpass API para traer todas sus calles y respectivos nodos
api = overpy.Overpass()

# Query para seleccionar las calles de la ciudad.
query = """

// Seleccionar Almería

area[name="Almería"][admin_level="8"]->.almeria;

// Combinar todas las calles con nombre y leer sus nodos
(
way(area.almeria)[highway][name];
node(w);
);

out;
"""

# Ejecutar la query a través de la API
result = api.query(query)

# Explorar resultados.
for way in result.ways:
    print("Name: %s" % way.tags.get("name", "n/a"))
    print("  Highway: %s" % way.tags.get("highway", "n/a"))
    print("  Nodes:")
    for node in way.nodes:
        print("    Lat: %f, Lon: %f" % (node.lat, node.lon))
