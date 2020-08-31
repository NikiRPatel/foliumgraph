import pandas as pd
import folium
import json

df = pd.read_csv("D:/Work/TheDataArt/Road Accident SA/2019_DATA_SA_Crash.csv") 
zipcode_data = df.groupby(['Postcode'], as_index=False).agg({'REPORT_ID': 'count'}).rename(columns={'REPORT_ID':'Count'})
zipcode_data.columns = ['postcode', 'count']
zipcode_data['postcode'] = zipcode_data['postcode'].apply(str)
print(zipcode_data)
zipcode_data.to_csv("Total_accident.csv")
""" 
# Get geo data file path
geo_data_file = "D:/Work/TheDataArt/Road Accident SA/Suburbs_GDA2020.geojson"

# load GeoJSON
with open(geo_data_file, 'r') as jsonFile:
    geo_data = json.load(jsonFile)
    
tmp = geo_data
# remove ZIP codes not in geo data
geozips = []
for i in range(len(tmp['features'])):
    if tmp['features'][i]['properties']['postcode'] in list(zipcode_data['postcode'].unique()):
        geozips.append(tmp['features'][i])
# creating new JSON object
new_json = dict.fromkeys(['type','features'])
new_json['type'] = 'FeatureCollection'
new_json['features'] = geozips
# save uodated JSON object
open("cleaned_geodata.json", "w").write(json.dumps(new_json, sort_keys=True, indent=4, separators=(',', ': ')))
 """

def map_feature_by_zipcode(zipcode_data, col):
    """
    Generates a folium map of SA
    :param zipcode_data: zipcode dataset
    :param col: feature to display
    :return: m
    """

    # read updated geo data
    king_geo = "cleaned_geodata.json"

    # Initialize Folium Map with SA latitude and longitude
    m = folium.Map(location=[138.6007,34.9285], zoom_start=11)

    # Create choropleth map
    m.choropleth(
        geo_data=king_geo,
        name='choropleth',
        data=zipcode_data,
        # col: feature of interest
        columns=['postcode', col],
        key_on='feature.properties.postcode',
        fill_color='OrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Number of Road Crash"
    )
    folium.LayerControl().add_to(m)
    # Save map based on feature of interest
    m.save(col + '.html')

    return m

map_feature_by_zipcode(zipcode_data, 'count')