from indalsig import db
from indalsig.db.dao import PostcodeDAO
from geopandas.geodataframe import GeoDataFrame
from geoalchemy2.shape import to_shape
import matplotlib.pyplot as plt

session = db.Session()
postcode_dao = PostcodeDAO(session)

qfilter = {'ad_type': 'SELL', 'asset_type': 'GARAGE'}
prices = session.execute('SELECT postcode, avg_price FROM inmosig_average_prices WHERE ad_type = :ad_type AND '
                         'asset_type = :asset_type', qfilter)

gdf = GeoDataFrame(columns=['geometry', 'price'])
for price in prices.fetchall():
    postcode = postcode_dao.search_by_postcode(price[0])
    if postcode is not None:
        gdf = gdf.append({'geometry': to_shape(postcode.geom), 'price': float(price[1])}, ignore_index=True)

gdf.head()
gdf.plot(column='price', cmap='OrRd', scheme="quantiles", legend=True)
plt.show()