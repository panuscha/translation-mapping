import pandas as pd
import plotly.graph_objects as go
from ast import literal_eval

minyear = 1917
maxyear = 2019
df = pd.read_csv('geotagged.csv') #pd.read_csv('preprocessed_data/clean_all_simplified.csv')
df = df[(df.year>minyear-1) & (df.year<maxyear+1)]
df = df[~df.geonames_country.isna()]
df = df[['language','year','geonames_country']].copy()
df['geonames_country'] = df.geonames_country.apply(literal_eval)

df_country_codes = pd.read_csv('https://gist.githubusercontent.com/tadast/8827699/raw/f5cac3d42d16b78348610fc4ec301e9234f82821/countries_codes_and_coordinates.csv')
country_codes_dict = dict(zip(df_country_codes.Country, df_country_codes['Alpha-3 code'].str.replace('"','').str.strip()))
country_codes_dict['Czechia'] ='CZE'
country_codes_dict['Iran'] ='IRN'
country_codes_dict['Kosovo'] ='SRB'
country_codes_dict['Moldova'] ='MDA'
country_codes_dict['North Korea'] ='PRK'
country_codes_dict['North Macedonia'] ='MKD'
country_codes_dict['Syria'] ='SYR'

df['weight'] = df.apply(lambda x: 1/len(x.geonames_country), axis=1)
df = df.explode('geonames_country')
df = df.reset_index(drop=True)
df = df[['geonames_country','weight']].groupby('geonames_country').sum()
df = df.set_index(df.index.map(country_codes_dict))

# follows one off map

fig = go.Figure()
fig.add_trace(go.Choropleth(
    locations=df.index,
    z= df.weight,
    colorscale='speed',
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickangle=-90,
    colorbar_tickvals=[500,df.max().max()-500],
    colorbar_ticktext=['méně překladů','více překladů'],
    zmin=0,
    zmax = df.max().max()
))
fig.update_layout(
    title_text = f'Letopočet: {minyear} - {maxyear}',
    title_x=0.2,    # europe only
    title_y=0.95,   # europe only
    # title_x=0.55,    # world only
    # title_y=0.20,   # world only
    coloraxis_colorbar_x=0.9,
    font_color='black',
    font_size=14,
    paper_bgcolor='rgba(255,255,255,1)',
    plot_bgcolor='rgba(255,255,255,1)',
    xaxis=dict(
        linecolor='black'
        ),
    yaxis=dict(
        linecolor='black',
        showgrid=True,
        gridcolor='rgba(0,0,0,0.2)'
        ),
    margin={"r":5,"t":0,"l":0,"b":0}
)
fig.update_geos(
    showcountries=True,
    resolution=50,
    showocean=True, 
    oceancolor="LightBlue",
    showlakes=True,
    lakecolor="LightBlue",
    showrivers=True,
    rivercolor='LightBlue'
)
# fig.update_geos(   # full earth
#     projection_type='robinson',
#     lataxis_range=[0,0],
#     lonaxis_range=[0,0],
# )
fig.update_geos(    # europe only
    projection_type='robinson',
    lataxis_range=[35,70],
    lonaxis_range=[-20,40],
)
fig.show()
fig.write_image(f'casestudies/maps/fig_europe.png', width=1080, height=650) # world width = 1280


print('done')