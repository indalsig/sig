# -*- coding: utf-8 -*-

from indalsig.labs.callejero.lab03 import show_ways_with_postcodes
from indalsig.domain import Postcode
from indalsig import db
from indalsig.db.dao import PostcodeDAO
from geoalchemy2.shape import from_shape
from shapely.geometry import MultiPolygon, Polygon

# Creamos una sesión de base de datos
session = db.Session()

# Creamos una instancia de DAO de los códigos postales
postcode_dao = PostcodeDAO(session)

# Del tutorial anterior recuperamos todos los multipolígonos del cálculo
for postcode_data in show_ways_with_postcodes.gf_postcode_poly.values:

    # Buscamos a ver si existe el código postal en la BBDD
    postcode = postcode_dao.search_by_postcode(postcode_data[1])

    if postcode is None:
        # Si no existe el código postal lo creamos
        postcode = Postcode()
        postcode.postcode = postcode_data[1]

    # Dependiendo de la clase de objeto que encontremos tenemos que convertirlo de una manera o de otra
    # Utilizaremos geoalchemy2.shape.from_shape para integrar sqlalchemy y shapely
    if isinstance(postcode_data[0], Polygon):
        postcode.geom = from_shape(MultiPolygon([postcode_data[0]]), 4326)
    elif isinstance(postcode_data[0], MultiPolygon):
        postcode.geom = from_shape(MultiPolygon(postcode_data[0]), 4326)
    else:
        print postcode_data[0]

    # Salvamos o actualizamos el código postal
    postcode_dao.save(postcode)

session.commit()

