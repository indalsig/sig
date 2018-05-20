# -*- coding: utf-8 -*-

from indalsig.labs.callejero.lab03 import show_ways_with_postcodes
from geopandas import GeoDataFrame
from shapely.geometry import MultiPolygon, Polygon

# Creamos el GeoDataFrame y definimos la columna geométrica y el código postal
postcodes_gdf = GeoDataFrame(columns=['geometry', 'postcode'])


# Del tutorial anterior recuperamos todos los multipolígonos del cálculo
for postcode_data in show_ways_with_postcodes.gf_postcode_poly.values:

    postcode = dict()
    postcode['postcode'] = postcode_data[1]

    # Transformamos los polígonos en multipolígonos e ignoramos lo que no sea convertible a multipolígono
    if isinstance(postcode_data[0], Polygon):
        postcode['geometry'] = MultiPolygon([postcode_data[0]])
    elif isinstance(postcode_data[0], MultiPolygon):
        postcode['geometry'] = MultiPolygon(postcode_data[0])
    else:
        print postcode_data[0]
        continue

    # Añadimos nuestra fila al GeoDataFrame
    postcodes_gdf = postcodes_gdf.append(postcode, ignore_index=True)

# Usando el driver fiona grabamos el Geopanda en formato GeoJSON
postcodes_gdf.to_file('postcodes.json', 'GeoJSON')

