# -*- coding: utf-8 -*-

import show_postcode_average_prices_fns as fns
import folium
import pandas as pd
import numpy as np


mapa = folium.Map(location=[36.83, -2.45], zoom_start=13)

prices_gd = {}
for ad_type in ['RENT', 'SELL']:

    gdf_rent_garages = fns.get_average_prices(ad_type, 'LOCAL')

    prices_gd[ad_type] = gdf_rent_garages

    geoPath = gdf_rent_garages.to_json()
    data1 = gdf_rent_garages

    mapa.choropleth(geo_data=geoPath,
                    data=data1,
                    columns=['postcode', 'price'],
                    key_on='feature.properties.postcode',
                    name=ad_type,
                    fill_color='YlOrBr',
                    legend_name=ad_type)

prices = pd.merge(left=prices_gd['RENT'][['geometry', 'postcode', 'price']],
                  right=prices_gd['SELL'][['postcode', 'price']],
                  on='postcode')


prices['calc_yield'] = prices['price_x'] / prices['price_y'] * 12 * 100

prices = prices[~(np.abs(prices.calc_yield - prices.calc_yield.mean()) > (3*prices.calc_yield.std()))]

print prices.head(50)

mapa.choropleth(geo_data=prices.to_json(),
                data=prices,
                columns=['postcode', 'calc_yield'],
                key_on='feature.properties.postcode',
                name='Yield',
                fill_color='YlOrBr',
                legend_name='Yield')

folium.LayerControl().add_to(mapa)

mapa.save(outfile='local_garage.html')
