import pandas as pd
import numpy as np


path = "/Users/lantyynka/University/Masters/FIS/DAB/2 Semestr/3 Data-X/listings 2.csv"
listings = pd.read_csv(path)
# pd.set_option("display.max_rows", None)
# pd.set_option("display.max_columns", None)

listings.head()
listings.describe()
listings.info()
listings.isnull().sum()
listings.duplicated().sum()
listings.columns
listings.description
columns_to_drop = ['listing_url', 'scrape_id', 'last_scraped', 'name', 'description', 'picture_url', 
                   'host_url', 'host_name', 'host_location', 'host_thumbnail_url', 'host_picture_url', 
                   'host_neighbourhood', 'neighbourhood', 'neighbourhood_group_cleansed', 'property_type', 
                   'bathrooms', 'bedrooms', 'amenities', 'calendar_updated', 'calendar_last_scraped', 
                   'number_of_reviews', 'number_of_reviews_ltm', 'number_of_reviews_l30d', 'first_review', 
                   'last_review', 'license', 'calculated_host_listings_count', 
                   'calculated_host_listings_count_entire_homes', 'calculated_host_listings_count_private_rooms', 
                   'calculated_host_listings_count_shared_rooms']

listings = listings.drop(columns=columns_to_drop)

import matplotlib.pyplot as plt

numeric_columns = listings.select_dtypes(include=['float64', 'int64'])
categorical_columns = listings.select_dtypes(include=['object'])

# vizualizace - numerické
for column in numeric_columns.columns:
    plt.figure(figsize=(8, 6))
    sns.histplot(listings[column], kde=True)
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()

# vizualizace - kategoriální
for column in categorical_columns.columns:
    plt.figure(figsize=(8, 6))
    sns.countplot(listings[column])
    plt.title(f'Count Plot of {column}')
    plt.xlabel(column)
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.show()

null_columns = listings.columns[listings.isnull().any()]
null_columns
#text
text_col = ["neighborhood_overview",
            "host_about"]
listings[text_col] = listings[text_col].fillna("Not provided")
listings[text_col].isnull().sum()
for col in text_col:
    listings[col] = listings[col].str.lower().str.strip()
#listings.bathrooms_text, ...
listings.nunique()
#bool - dát na bool nebo int 1/0 ?
bool_col = ["host_is_superhost",
            "host_has_profile_pic",
            "host_identity_verified",
            "has_availability",
            "instant_bookable"]
listings[bool_col].nunique()
listings[bool_col].head()
bool_mapping = {"t": True, "f": False}
listings[bool_col] = listings[bool_col].replace(bool_mapping)
listings[bool_col] = listings[bool_col].fillna(False)
listings[bool_col].info()

# odstranění znaků
listings['host_response_rate_in_percents'] = listings['host_response_rate'].str.replace('%', '').astype(float) / 100
listings['host_acceptance_rate_in_percents'] = listings['host_acceptance_rate'].str.replace('%', '').astype(float) / 100
listings.drop(columns=["host_response_rate",
                       "host_acceptance_rate"])

listings['price_dollars'] = listings['price'].str.replace('$', '').str.replace(',', '').astype(float)
listings.drop("price", axis=1, inplace=True)

#chcem vůbec nechávat bathrooms_text? - případně musíme sjednotit
listings['bathrooms_text'] = listings['bathrooms_text'].str.split().str[0]
listings['bathrooms_text'].unique()

# listings.neighbourhood / listings.neighbourhood_cleansed - smažeme neighbourhood, nebo porovnáme, jestli mají nižší cenu, když mají divně napsanou lokaci?

#host_verification - rozdělit na True/False (1/0) sloupců podle Email, Phone, ...
listings["verificated_email"] = listings["host_verifications"].str.contains("email").astype(int)
listings["verificated_phone"] = listings["host_verifications"].str.contains("phone").astype(int)
listings["verificated_work_email"] = listings["host_verifications"].str.contains("work_email").astype(int)
listings.drop("host_verifications", axis=1, inplace=True)

#korelace
import seaborn as sns

numeric_columns = listings.select_dtypes(include=[np.number])
corr = numeric_columns.corr()
sns.heatmap(corr, 
            xticklabels=corr.columns,
            yticklabels=corr.columns, annot=True,
            linewidth=.5)