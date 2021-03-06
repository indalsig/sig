# -*- coding: utf-8 -*-

import googlemaps
import psycopg2
import pprint
from indalsig import settings


# Conexión con la clave de la API e inicialización del cliente
gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)

# Conexión con la base de datos
conn = psycopg2.connect(user=settings.PG_USER, password=settings.PG_PASSWD, host=settings.PG_HOST,
                        dbname=settings.PG_DBNAME)

cur = conn.cursor()

# Obtención de todos los nodos donde no haya aun un código postal.
# Se ha cogido un nodo referencia en el centro del mapa y se han
# empezado a calcular los CP a partir de la distancia al mismo
cur.execute("""
            SELECT n.id node_id, n.lng, n.lat 
            FROM
                sig_nodes n
                LEFT JOIN sig_addresses a
                ON n.address_id = a.id
                JOIN sig_nodes nc
                ON nc.id = 437 
            WHERE
                a.id IS NULL
            ORDER BY ST_Distance(n.geom, nc.geom) 
            """)

rows = cur.fetchall()

for node_id, lng, lat in rows:
    # Lanzamiento de la consulta a la API
    result = gmaps.reverse_geocode((lat, lng))[0]

    # Objeto de datos para la tabla "sig_addresses"
    address = {"id": "",
               "lat": str(lat),
               "lon": str(lng),
               "formatted_address": result["formatted_address"],
               "street_name": "",
               "street_number": "",
               "postcode": 0,
               "node_id": str(node_id)
               }

    pprint.pprint(result)

    add_comps = result['address_components']

    # Rellenado de los datos en el Data Entry
    for comp in add_comps:
        if "street_number" in comp["types"]:
            address["street_number"] = comp["long_name"]
        elif "route" in comp["types"]:
            address["street_name"] = comp["long_name"]
        elif "postal_code" in comp["types"]:
            address["postcode"] = int(comp["long_name"])

    pprint.pprint(address)


    # Insercción en la BBDD
    cur.execute("""
                INSERT INTO sig_addresses
                (lat, lon, formatted_address, street_name, street_number, postcode)
                VALUES
                (%(lat)s, %(lon)s, %(formatted_address)s, %(street_name)s, %(street_number)s, %(postcode)s)
                RETURNING ID""", address)

    address["id"] = cur.fetchone()[0]

    cur.execute("""
                UPDATE sig_nodes
                SET address_id = %(id)s
                WHERE id = %(node_id)s""", address)

    conn.commit()
    pprint.pprint(address)
