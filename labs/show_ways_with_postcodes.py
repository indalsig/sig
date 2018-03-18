import psycopg2
import settings

from shapely.wkb import loads

from geopandas import GeoDataFrame, GeoSeries
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

import seaborn as sns
from labs import alpha_shape

conn = psycopg2.connect(user=settings.PG_USER, password=settings.PG_PASSWD,
                        host=settings.PG_HOST,
                        dbname=settings.PG_DBNAME)

cur = conn.cursor()
cur.execute("""SELECT geom, id, name FROM sig_ways w""")
rows = cur.fetchall()

ways = []
for geom, id, name in rows:
    way = loads(geom, True)
    ways.append(way)
    # print str(way) + ' ' + str(id) + ' ' + name

gs = GeoSeries(ways)


post_code_filter = []

cur.execute("""SELECT geom, id, postcode FROM sig_nodes n WHERE postcode IS NOT NULL AND postcode != 0""")
rows = cur.fetchall()
gf_data = {'geometry': [], 'postcode': []}

for geom, id, postcode in rows:
    node = loads(geom, True)
    gf_data['geometry'].append(node)
    gf_data['postcode'].append(postcode)

gf = GeoDataFrame(gf_data)
if len(post_code_filter) > 0:
    gf = gf.loc[gf.postcode.isin(post_code_filter)]

postcodes_arr = gf.postcode.unique()
postcodes_arr.sort()
gf_postcode_poly = GeoDataFrame(columns=['geometry', 'postcode'])
for postcode in postcodes_arr:

    points = []
    for point in gf.loc[gf.postcode == postcode].geometry:
        points.append(point)

    alpha_geometry, edge_points = alpha_shape.alpha_shape(points, 1000)
    gf_postcode_poly = gf_postcode_poly.append({'geometry': alpha_geometry, 'postcode': postcode}, ignore_index=True)

print gf_postcode_poly.head()

colors = sns.hls_palette(len(postcodes_arr))
colormap = ListedColormap(colors)
base = gs.plot(color='blue')

gf.plot(ax=base, marker="*", column="postcode", cmap=colormap, categorical=True)

gf_postcode_poly.plot(ax=base, column="postcode", cmap=colormap, categorical=True, legend=True, alpha=0.4)

plt.show()
