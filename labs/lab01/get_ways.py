# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import overpy
from db.dao import WayDAO, NodeDAO
from db import Session
from domain import Way, WayNode, Node

# Crear session y DAOs
session = Session()

wayDAO = WayDAO(session)
nodeDAO = NodeDAO(session)



# Conectar con la Overpass API para traer todas sus calles y respectivos nodos
api = overpy.Overpass()

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

result = api.query(query)

i = 1
for way in result.ways:

    # Try to get way from database based in osm id
    way_item = wayDAO.search_by_openstreetmap_id(way.id)

    # Create way item if not exists
    if way_item is None:
        way_item = Way()
        way_item.city = 'AL'

    # Merge way object
    way_item.name = way.tags['name']
    way_item.openstreetmap_id = way.id

    node_osm_ids = []
    seq = 0
    for node in way.nodes:

        # Get relationship between node and way from DB
        way_node_item = way_item.search_way_node_by_id_and_seq(node.id, seq)

        # Create if not exists
        if way_node_item is None:
            way_node_item = WayNode()
            way_node_item.way = way_item

        # Merge relationship
        way_node_item.seq = seq

        # Try to get node from DB based in osm id
        if way_node_item.node is None:

            # Search in new reletionships nodes
            node_item = way_item.search_way_node_by_id(node.id)
            # If not try to get it from DB
            if node_item is None:
                node_item = nodeDAO.search_by_openstreetmap_id(node.id)
            # If not exists, create it
            if node_item is None:
                node_item = Node()
            way_node_item.node = node_item
        else:
            node_item = way_node_item.node

        # Merge node with osm data
        node_item.lat = node.lat
        node_item.lng = node.lon
        node_item.openstreetmap_id = node.id

        way_item.way_nodes.append(way_node_item)
        node_osm_ids.append(node.id)
        seq = seq + 1

    # Delete obsolete way-node relationships
    way_item.delete_invalid_relationships(node_osm_ids)

    wayDAO.save(way_item)
    session.commit()
    print(way_item.name + '. Row: ' + str(i) +
          '. Percentage accomplished: ' + str(round(float(i) / len(result.ways) * 100, 3)) + '%')
    i += 1
