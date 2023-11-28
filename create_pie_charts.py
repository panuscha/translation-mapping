import pandas as pd
import math
import matplotlib.pyplot as plt


TOP = 3
MIN_TRANS = 4 

# all plot years
plot_years = ['1918', '1929', '1945', '1956', '1967','1978', '1989', '2000', '2011' ] 

# Table with number of translations for each country, language and decade
df = pd.read_excel("D:\\Panuskova\\Nextcloud\\translation-mapping\\translation-mapping\\weights\\translations_language_countries.xlsx")

# all countries and languages
#countries = df.country.unique()
# languages = df.language.unique()

#countries = ["USSR", "Switzerland", "Slovakia", "Italy", "Germany", "Spain", "United Kingdom", "Sweden", "Denmark", "Poland",  "Austria", "Czechoslovakia", "Yugoslavia", "Belgium", "Hungary"]
countries =["Italy", "Belgium", "United Kingdom", "Czechoslovakia", "Denmark", "Sweden", "Slovakia", "Spain", "Switzerland", "USSR", "Germany (Soviet)", "East Germany",  "Germany", "Yugoslavia", "Poland", "Austria", "Italy", "Hungary"]
languages = ["rus", "est", "arm", "glg", "ukr", "wen", "eng", "lit", "baq", "dut", "slv", "mac", "hrv", "epo", "hun", "ger", "cat", "fre", "slo", "other"]


my_color_palette = {}
#all_colors = list(colors.CSS4_COLORS.keys())
all_colors =[plt.cm.tab20(i) for i in range(20)]

# Save color for each country
for i, language in enumerate(languages):
    my_color_palette[language] = all_colors[i]

# Iterate through all decades
for plot_year in plot_years: 

    # Iterate through countries to plot the bar chart                
    for country in countries:

        # Select only non empty rows that are in the decade and for that country
        if not df[(df['map_year'] == int(plot_year)) &  (df['country'] == country)].empty:

            # All non-empty rows
            h = df[(df['map_year'] == int(plot_year)) &  (df['country'] == country)]
            
            # if only weights, change to h.weights
            sum_weights = sum(h.weights)
            
            # size of the outer chart
            size = 0.1
        
            # major language
            h_max = max(h.weights)
            
            # index of major language
            id = h.index[h.weights == h_max]
            
            # outher colors, major will always be transparent, major is displayed as black
            outer_colors = [my_color_palette['eng'] , 'black' ]

            # list of outer weights 
            weights_all = [h_max, sum(h.weights) - h_max ]
            
            # plot
            fig, ax = plt.subplots()
            
            # outer pie
            n = ax.pie(weights_all, radius=1, colors=outer_colors,
            
            # white edges
            wedgeprops=dict(width=size, edgecolor='w'))
            
            # set major language transparent
            n[0][0].set_alpha(0.0)

            # Discard the most common language (= should be the major language)
            h = h[h.weights != h_max]

            # if there are minor languages translations
            if not(h.empty):
                
                # if there are more then TOP languages translations or any of the languages has equal or less then MIN_TRANS translations
                if len(h.weights) > TOP or any(i <= MIN_TRANS for i in h.weights):
                    
                    # sort values by weights descending
                    h = h.sort_values(by = 'weights', ascending = 0)
                    
                    # weights
                    weights_sorted = list(h.weights)
                    
                    # index of first weight that is equal or less then MIN_TRANS
                    ind_min_trans = list(map(lambda i: i <= MIN_TRANS, weights_sorted)).index(True)
                    
                    # index of languages that wil  fall into "other" category
                    ind = min([TOP, ind_min_trans])
                    
                    # "other" category languages
                    df2_dict = {'country': country, 'language': "other", 'map_year': plot_year, 'weights': sum(weights_sorted[ind:]) }
                    df2 = pd.DataFrame(data = df2_dict, index = ['0'])
                    
                    # only non-other languages
                    h = h.head(ind)
                    
                    # combine two DataFrames
                    h = pd.concat([h, df2], ignore_index = True)
                    
                # get all colors for languages 
                inner_colors = [my_color_palette[l] for l in h.language  ]

                # get all languages 
                language = h.language
                
                # if only weights, change to h.weights
                weights = [w/sum_weights for w in h.weights] 

                # inner pie chart
                wedges, _ = ax.pie(weights, radius=1-size, colors=inner_colors,
                wedgeprops=dict(edgecolor='w')) #width=size, 
                ax.legend(wedges, language,
                    title="languages",
                    loc="center left",
                    bbox_to_anchor=(1, 0, 0.5, 1))
                plt.title("{country}_{year}".format(country = country, year = plot_year))
                
                #plt.show()
                #hist = h[['language','weights']].plot(kind = 'bar', figsize=(8, 6), x = 'language', ylim = [0, y_max], color = colors).get_figure()
                plt.savefig('D:\\Panuskova\\Nextcloud\\translation-mapping\\translation-mapping\\plots\\histograms minor percentage pie charts\\{country}_{year}'.format(country = country, year = plot_year))
                plt.close()
                #close(hist)
      
