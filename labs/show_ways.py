import psycopg2
import settings

from shapely.wkb import loads
from geopandas import GeoSeries
import matplotlib.pyplot as plt

conn = psycopg2.connect(user=settings.PG_USER, password=settings.PG_PASSWD, host=settings.PG_HOST,
                        dbname=settings.PG_DBNAME)

cur = conn.cursor()
cur.execute("SELECT geom, id, name FROM sig_ways")
rows = cur.fetchall()

ways = []
for geom, id, name in rows:
    way = loads(geom, True)
    ways.append(way)
    # print str(way) + ' ' + str(id) + ' ' + name

gs = GeoSeries(ways)

print gs

gs.plot(color='blue')

plt.show()