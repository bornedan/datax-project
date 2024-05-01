import pandas as pd
import numpy as np
import geopandas as gpd
from shapely import Point
import matplotlib.pyplot as plt
import contextily as ctx

listings = pd.read_csv('C:/Users/filip/OneDrive - Vysoká škola ekonomická v Praze/Plocha/DATA X/listings.csv.gz', compression='gzip', low_memory=False)
listings.rename(columns={'id':'listings_id'},inplace=True)
listings['listings_id'] = listings['listings_id'].astype('int64')
listings['last_scraped'] = pd.to_datetime(listings['last_scraped'])
listings[['listings_id', 'scrape_id']] = listings[['listings_id', 'scrape_id']].astype(str)

text_columns = ['name', 'description','bathrooms','bedrooms','amenities', 'neighborhood_overview','host_neighbourhood', 'neighbourhood', 'neighbourhood_group_cleansed', 'license']
listings[text_columns] = listings[text_columns].fillna('Not provided')
for sloupec in text_columns:
    listings[sloupec] = listings[sloupec].str.lower().str.strip()

num_columns = ['reviews_per_month']
for sloupec in num_columns:
    listings[sloupec] = listings[sloupec].fillna(listings[sloupec].median())    

listings['host_response_rate'] = listings['host_response_rate'].str.replace('%', '').astype(float) / 100
listings['host_acceptance_rate'] = listings['host_acceptance_rate'].str.replace('%', '').astype(float) / 100

listings.rename(columns={'host_response_rate': 'host_response_rate_in_percents',
                         'host_acceptance_rate': 'host_acceptance_rate_in_percents'}, inplace=True)

listings['price'] = listings['price'].str.replace('$', '').str.replace(',', '').astype(str)
listings.rename(columns={'price': 'price_in_dollars'}, inplace=True)
listings['price_in_dollars'] = listings['price_in_dollars'].astype(float)
listings['instant_bookable'] = listings['instant_bookable'].map({'t': True, 'f': False})
listings['room_type'] = listings['room_type'].astype('category')
prvni_kvantil = listings['reviews_per_month'].quantile(0.01)
posledni_kvantil = listings['reviews_per_month'].quantile(0.99)
listings = listings[(listings['reviews_per_month'] >= prvni_kvantil) & (listings['reviews_per_month'] <= posledni_kvantil)]

print(listings.head())
print(listings.dtypes)
print(listings.info)
listings.to_csv('C:/Users/filip/OneDrive - Vysoká škola ekonomická v Praze/Plocha/DATA X/listings_upravene.csv.', index= False)
listings

gdf = gpd.GeoDataFrame(listings, geometry=[Point(xy) for xy in zip(listings.longitude, listings.latitude)])

# Nastavení souřadnicového systému (CRS) na WGS84
gdf.crs = "EPSG:4326"

# Vytvoření grafu
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, marker='o', color='blue', markersize=1)

# Přidání základní mapy
try:
    ctx.add_basemap(ax, crs=gdf.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)
except AttributeError as e:
    print("Při pokusu o načtení základní mapy došlo k chybě. Zkontrolujte dostupnost zdroje mapy nebo použijte alternativní zdroj.")
    # Zde můžeš zkusit alternativní zdroj mapy
    # Například: ctx.providers.OpenStreetMap.Mapnik
    # ctx.add_basemap(ax, crs=gdf.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)

# Zobrazení
plt.show()
