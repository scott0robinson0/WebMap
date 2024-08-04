import json
import plotly.express as px
import pymongo
from pymongo import ReplaceOne
import http.client
import socket

# Get data from the restcountries API
def request_restcountries():
    conn = http.client.HTTPSConnection('restcountries.com')

    try:
        conn.request('GET', '/v3.1/all')
    except socket.timeout as st:
        return 0
    
    res = conn.getresponse()
    json_bytes = res.read()
    json_string = json_bytes.decode('utf-8')
    json_obj = json.loads(json_string)

    return json_obj

# Load Gapminder data
def load_gapminder():   
    df = px.data.gapminder()
    # Remove data older than 2007
    df.drop(df[df.year < 2007].index, inplace=True)
    df = df.reset_index()
    return df

# Combine gapminder and restcountries.com data
def combineData(rest_countries, gap_minder):
    rows = []

    for rest_country in rest_countries:
        row = {}
        # Add restcountries.com data
        row.update({'Name': rest_country['name']['common']})
        row.update({'ISO': rest_country['cca3']})
        if 'languages' in rest_country: row.update({'Number of Languages Spoken': len(rest_country['languages'])})
        row.update({'Landlocked': rest_country['landlocked']})
        row.update({'Number of Borders': len(rest_country['borders']) if 'borders' in rest_country else 0})
        row.update({'Area': rest_country['area']})
        row.update({'Population': rest_country['population']})
        if 'gini' in rest_country: row.update({'GINI': next(iter(rest_country['gini'].values()))})
        row.update({'Drives on Right': rest_country['car']['side'] == 'right'})

        # Add gapminder data
        if rest_country['cca3'] in gap_minder['iso_alpha'].values:
            gap_country = gap_minder.loc[gap_minder['iso_alpha'] == rest_country['cca3']]
            row.update({'Life Expectancy (2007)': gap_country['lifeExp'].values[0]})
            row.update({'GDP Per Capita (2007)': gap_country['gdpPercap'].values[0]})
        rows.append(row)
    return rows

# Load and combine all data
def load_all():
    rest_countries = request_restcountries()
    df_gapminder = load_gapminder()



    return combineData(rest_countries, df_gapminder)

# Upload country data to MongoDB
def upload():
    countries = load_all()
    # Connect to MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['CountryInfoDatabase']
    collection = db['CountryInfoCollection']

    # Set up bulk write operation
    operations = [
        ReplaceOne({'ISO': country['ISO']}, country, upsert=True) for country in countries
    ]

    # Execute bulk write operation
    collection.bulk_write(operations)

    client.close()

# Download country data from MongoDB
def download():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['CountryInfoDatabase']
    collection = db['CountryInfoCollection']
       
    countries = []
    for country in collection.find():
        countries.append(country)
    client.close() 

    return countries

# Uncomment if using mongodb
# upload()

data = request_restcountries()

import json
with open('test.json', 'w') as file:
    json.dump(data, file)
