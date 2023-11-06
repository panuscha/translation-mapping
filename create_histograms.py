import pandas as pd
import math

plot_years = ['1978', '1989', '2000', '2011'] # '1918', '1929', '1945', '1956', '1967', 

df = pd.read_excel("C:\\Users\\Panuskova\\Nextcloud\\translation-mapping\\weights\\translations_language_countries.xlsx")

countries = df.country.unique()

for plot_year in plot_years:     
    for country in countries:
        if not df[(df['map_year'] == int(plot_year)) &  (df['country'] == country)].empty:
            h = df[(df['map_year'] == int(plot_year)) &  (df['country'] == country)]
            hist = h[['language','weights']].plot(kind = 'bar', figsize=(8, 6), x = 'language').get_figure()
            hist.savefig('C:\\Users\\Panuskova\\Nextcloud\\translation-mapping\\plots\\histograms\\{country}_{year}.png'.format(country = country, year = plot_year))
