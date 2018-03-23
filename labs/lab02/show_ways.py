# -*- coding: utf-8 -*-

import psycopg2
import settings

from shapely.wkb import loads
from geopandas import GeoSeries
import matplotlib.pyplot as plt

# Conectamos con la base de datos

conn = psycopg2.connect(user=settings.PG_USER, password=settings.PG_PASSWD, host=settings.PG_HOST,
                        dbname=settings.PG_DBNAME)

# Extraemos todas las vías de la tabla

cur = conn.cursor()
cur.execute("SELECT geom, id, name FROM sig_ways")
rows = cur.fetchall()

# Creamos con la función loads de shapely el objeto geométrico

ways = []
for geom, id, name in rows:
    way = loads(geom, True)
    ways.append(way)

# Construimos un GeoSeries de GeoPandas con todas las vías

gs = GeoSeries(ways)

# Selecionamos color azul para las líneas y ploteamos la serie

gs.plot(color='blue')

plt.show()
