# -*- coding: utf-8 -*-

from indalsig import db
from indalsig.db.dao import PostcodeDAO, WayDAO
from geopandas.geodataframe import GeoDataFrame, GeoSeries
from geoalchemy2.shape import to_shape
import matplotlib.pyplot as plt

session = db.Session()
postcode_dao = PostcodeDAO(session)
way_dao = WayDAO(session)

# Representación de las calles con GeoSeries
# Extraemos todas las calles
ways = []
for way in way_dao.getAll():
    ways.append(to_shape(way.geom))
wgs = GeoSeries(ways)
base = wgs.plot(color="blue")

qfilter = {'ad_type': 'RENT', 'asset_type': 'GARAGE'}
prices = session.execute('SELECT postcode, avg_price FROM inmosig_average_prices WHERE ad_type = :ad_type AND '
                         'asset_type = :asset_type', qfilter)

gdf = GeoDataFrame(columns=['geometry', 'price', 'postcode'])
for price in prices.fetchall():
    postcode = postcode_dao.search_by_postcode(price[0])
    if postcode is not None:
        gdf = gdf.append({'geometry': to_shape(postcode.geom), 'price': float(price[1]), 'postcode': price[0]},
                         ignore_index=True)

gdf.head()
gdf.plot(ax=base, column='price', cmap='OrRd', scheme="quantiles", legend=True)
plt.show()