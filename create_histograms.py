import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# all plot years
plot_years = ['1918', '1929', '1945', '1956', '1967','1978', '1989', '2000', '2011' ] 

# Table with number of translations for each country, language and decade
df = pd.read_excel("C:\\Users\\Panuskova\\Nextcloud\\translation-mapping\\weights\\translations_language_countries.xlsx")

# all countries and languages
countries = df.country.unique()
languages = df.language.unique()

my_color_palette = {}
all_colors = list(mcolors.CSS4_COLORS.keys())

# Save color for each country
for i, language in enumerate(languages):
    my_color_palette[language] = all_colors[i]

# Do not include these countries for setting the limit
forbidden_countries = set(['Czech Republic', 'Czechoslovakia', 'Taiwan'])

# Iterate through all decades
for plot_year in plot_years: 

    # set y lim max to 0
    y_max = 0    

    # Iterate through countries to find the y max limit
    for country in countries:

        # Select only non empty rows that are in the decade and for that country
        if not df[(df['map_year'] == int(plot_year)) &  (df['country'] == country)].empty:

            # All non-empty rows
            h = df[(df['map_year'] == int(plot_year)) &  (df['country'] == country)]
            
            # if only weights, change to h.weights
            sum_weights = sum(h.weights)

            # Discard the most common language (= should be the major language)
            h = h[h.weights != max(h.weights)]

            # if 
            h_c = set(h.country)
            if not(h.empty) and not(forbidden_countries.intersection(h_c)):
                
                # if only weights, change to h.weights
                weights = [w/sum_weights for w in h.weights] 
                if y_max < max(weights):
                    y_max = max(weights)

    # Iterate through countries to plot the bar chart                
    for country in countries:

        # Select only non empty rows that are in the decade and for that country
        if not df[(df['map_year'] == int(plot_year)) &  (df['country'] == country)].empty:

            # All non-empty rows
            h = df[(df['map_year'] == int(plot_year)) &  (df['country'] == country)]
            
            # if only weights, change to h.weights
            sum_weights = sum(h.weights)

            # Discard the most common language (= should be the major language)
            h = h[h.weights != max(h.weights)]

            if not(h.empty):

                # get all colors for languages 
                colors = [my_color_palette[language] for language in h.language  ]

                # get all languages 
                language = h.language
                
                # if only weights, change to h.weights
                weights = [w/sum_weights for w in h.weights] 

                # create figure
                fig, ax = plt.subplots()

                # set y max lim
                plt.ylim([0, y_max])

                # plot the bar chart
                ax.bar(language, weights, label = language, color = colors)
                ax.legend()
                #hist = h[['language','weights']].plot(kind = 'bar', figsize=(8, 6), x = 'language', ylim = [0, y_max], color = colors).get_figure()
                plt.savefig('C:\\Users\\Panuskova\\Nextcloud\\translation-mapping\\plots\\histograms only second major percentage\\{country}_{year}.png'.format(country = country, year = plot_year))
                plt.close()
                #close(hist)
      
