from indalsig.labs.lab03 import show_ways_with_postcodes
from indalsig.domain import Postcode
from indalsig import db
from indalsig.db.dao import PostcodeDAO
from geoalchemy2.shape import from_shape
from shapely.geometry import MultiPolygon, Polygon

session = db.Session()
postcode_dao = PostcodeDAO(session)

for postcode_data in show_ways_with_postcodes.gf_postcode_poly.values:

    postcode = postcode_dao.search_by_postcode(postcode_data[1])

    if postcode is None:
        postcode = Postcode()
        postcode.postcode = postcode_data[1]

    if isinstance(postcode_data[0], Polygon):
        postcode.geom = from_shape(MultiPolygon([postcode_data[0]]), 4326)
    elif isinstance(postcode_data[0], MultiPolygon):
        postcode.geom = from_shape(MultiPolygon(postcode_data[0]), 4326)
    else:
        print postcode_data[0]

    postcode_dao.save(postcode)

session.commit()

