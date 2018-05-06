# -*- coding: utf-8 -*-

import googlemaps
from indalsig import settings
from indalsig.domain import Address

# Conexión con la clave de la API e inicialización del cliente
gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)


def get_address_from_coords(lat, lng):
    # Lanzamiento de la consulta a la API
    result = gmaps.reverse_geocode((lat, lng))[0]

    address = Address()

    # Objeto de datos para la tabla "sig_addresses"

    address.lat = str(lat)
    address.lon = str(lng)
    address.formatted_address = result["formatted_address"]

    add_comps = result['address_components']

    # Rellenado de los datos en el Data Entry
    for comp in add_comps:
        if "street_number" in comp["types"]:
            address.street_number = comp["long_name"]
        elif "route" in comp["types"]:
            address.street_name = comp["long_name"]
        elif "postal_code" in comp["types"]:
            address.postcode = int(comp["long_name"])

    return address


def get_address_from_text(address_text):
    # Lanzamiento de la consulta a la API
    result = gmaps.geocode(address_text)[0]

    address = Address()

    # Objeto de datos para la tabla "sig_addresses"

    address.lat = result["geometry"]["location"]["lat"]
    address.lon = result["geometry"]["location"]["lng"]
    address.formatted_address = result["formatted_address"]

    add_comps = result['address_components']

    # Rellenado de los datos en el Data Entry
    for comp in add_comps:
        if "street_number" in comp["types"]:
            address.street_number = comp["long_name"]
        elif "route" in comp["types"]:
            address.street_name = comp["long_name"]
        elif "postal_code" in comp["types"]:
            address.postcode = int(comp["long_name"])

    return address
