# Import libraries
import pandas as pd
import folium
import os

# Load the shape of the zone (GHMC Zones)
# You have to set the directory where you saved it
state_geo = os.path.join('./data/map_data', 'hyderabad_zone.geojson')
geo_data_df = pd.read_json(state_geo)

# Load the prediction value for each state
# circle_prediction = os.path.join('/home/harris/Documents/17.08.2018/documents/courses/4-2/swe/project/heatmaps/data','final_dataset2.csv')#'sample_data.csv')#'final_dataset.csv')
circle_prediction="final_dataset.csv"
circle_data = pd.read_csv(circle_prediction)

list_north = ['Alwal', 'Begumpet', 'Gajula Ramaram', 'Malkajgiri', 'Quthbullapur', 'Secunderabad Division']
list_south = ['Chandrayangutta', 'Charminar', 'Falakunuma', 'Malakpet', 'Rajendra Nagar', 'Santhoshnagar']
list_west = ['Chandanagar', 'Kukatpally', 'Moosapet', 'Ramachandra Puram / Patancheru', 'Serilingampally']
list_east = ['Hayathnagar', 'Kapra', 'LB Nagar', 'Saroornagar', 'Uppal']
list_central = ['Amberpet', 'Goshamahal', 'Jubilee Hills', 'Karwan', 'Khairatabad', 'Mehdipatnam', 'Musheerabad', 'Yousufguda']

def which_zone(circle):
    if  circle in list_north:
        return 'North Zone'
    elif circle in list_south:
        return 'South Zone'
    elif circle in list_east:
        return 'East Zone'
    elif circle in list_west:
        return 'West Zone'
    else:
        return 'Central Zone'
    
def risk_to_num(risk):
    if  risk == 'high':
        return '800'
    elif risk == 'medium':
        return '500'
    else:
        return '200'
    
circle_data['zone'] = circle_data.apply(lambda x: which_zone(x.location), axis = 1)
circle_data['zone_risk'] = circle_data.apply(lambda x: risk_to_num(x.predicted_risk), axis = 1).apply(pd.to_numeric)
zone_data = circle_data.groupby('zone')['zone_risk'].mean().reset_index().head()

print (circle_data['predicted_risk'].dtypes)

# Initialize the map:
m = folium.Map(
    location =[17.3850, 78.4867],
    zoom_start=12
)

# Add the color for the chloropleth:
folium.Choropleth(
    geo_data = state_geo,
    name = 'choropleth',
    data = zone_data,#zone_data,
    columns = ['zone', 'zone_risk'],#'zone_risk'],
    key_on = 'feature.properties.name',
    fill_color = 'BrBG',
    fill_opacity = 0.7,
    line_opacity = 0.2,
    legend_name = 'Predictions'
).add_to(m)

folium.LayerControl().add_to(m)

# Save to html
m.save('static/example.html')
