import pandas as pd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from itertools import compress


TOP = 3
MIN_TRANS = 4 

# all plot years
plot_years = ['1918', '1929', '1945', '1956', '1967','1978', '1989', '2000', '2011' ] 

# Table with number of translations for each country, language and decade
df = pd.read_excel("weights\\translations_language_countries.xlsx")

# all countries and languages
#countries = df.country.unique()
# languages = df.language.unique()

#countries = ["USSR", "Switzerland", "Slovakia", "Italy", "Germany", "Spain", "United Kingdom", "Sweden", "Denmark", "Poland",  "Austria", "Czechoslovakia", "Yugoslavia", "Belgium", "Hungary"]

# countries and languages from number_of_colors.py  
countries =["Italy", "Belgium", "United Kingdom", "Czechoslovakia", "Denmark", "Sweden", "Slovakia", "Spain", "Switzerland", "USSR", "Germany (Soviet)", "East Germany",  "Germany", "Yugoslavia", "Poland", "Austria", "Italy", "Hungary"]
languages = ["rus", "est", "arm", "glg", "ukr", "wen", "eng", "lit", "baq", "dut", "slv", "mac", "hrv", "epo", "hun", "ger", "cat", "fre", "slo", "other"]

except_countries = {"Czechoslovakia" : ["slo"], "Belgium" : ["fre", "dut"],  "Switzerland": ["ger", "fre"], "Yugoslavia": ["hrv"]}


my_color_palette = {}
#all_colors = list(colors.CSS4_COLORS.keys())
all_colors =[plt.cm.tab20(i) for i in range(20)]
handles = []

# Save color for each country
for i, language in enumerate(languages):
    my_color_palette[language] = all_colors[i]

# Iterate through all decades
for plot_year in plot_years: 

    
    # Iterate through countries to plot the bar chart                
    for country in countries: # 

        # Select only non empty rows that are in the decade and for that country
        if not df[(df['map_year'] == int(plot_year)) &  (df['country'] == country)].empty:

            # All non-empty rows
            h = df[(df['map_year'] == int(plot_year)) &  (df['country'] == country)]
            
            # sort values by weights descending
            h = h.sort_values(by = 'weights', ascending = 0)
            
            # if only weights, change to h.weights
            sum_weights = sum(h.weights)
            
            # size of the outer chart
            size = 0.1
            
            # if major language is an exception
            if country in except_countries.keys():
                
                # find weight of that language or sum of languages
                h_max = sum(h[h['language'].isin(except_countries[country])].weights)
                
                # Discard major language
                h = h[~h['language'].isin(except_countries[country])]
            else:
                # major language
                h_max = max(h.weights)
            
                # Discard the most common language (= should be the major language)
                h = h.iloc[1:, :]
           
            # outher colors, major will always be transparent, major is displayed as black
            outer_colors = [my_color_palette['eng'] , 'black' ]

            # list of outer weights 
            weights_all = [h_max, sum_weights - h_max ]
            
            # plot
            fig, ax = plt.subplots(figsize = (10,10))
            
            # outer pie
            n = ax.pie(weights_all, radius=1, colors=outer_colors,
            
            # white edges
            wedgeprops=dict(width=size, edgecolor='w'))
            
            # set major language transparent
            n[0][0].set_alpha(0.0)

            # if there are minor languages translations
            if not(h.empty):
                
                # if there are more then TOP languages translations or any of the language is not in languages list
                if len(h.weights) > TOP or any(l not in languages for l in h.language):
                    
                    # sort values by weights descending
                    h = h.sort_values(by = 'weights', ascending = 0)
                    
                    # weights
                    weights_sorted = list(h.weights)
                    
                    h_lang = h.language.tolist()
                    
                    # index of languages that are in languages
                    ind_top_lang_trans = list(map(lambda i: True if h_lang[i] in languages else False ,range(len(h.language)) ))
                    
                    if sum(ind_top_lang_trans) > TOP:
                        res = [i for i, val in enumerate(ind_top_lang_trans) if val]
                        
                        #ind_under_top = ind_top_lang_trans[res[TOP]:]
                        
                        ind_top_lang_trans[res[TOP]:] = [False for i in range(len(ind_top_lang_trans) - res[TOP])]
                        #ind_top_lang_trans = ind_top_lang_trans[0:TOP]
                        # index of languages that are not in languages or under TOP threshold 
                        ind_not_top_trans = list(map(lambda i: True if h_lang[i] not in languages or i in res[TOP:] else False, range(len(h.language)) ))
                    else:
                        
                        # index of languages that are not in languages
                        ind_not_top_trans = list(map(lambda i: True if h_lang[i] not in languages else False, range(len(h.language)) ))
                    
                    
                    # "other" category languages
                    sum_not_top_lang = sum(list(compress(h.weights.tolist(), ind_not_top_trans))) #map(lambda i: weights_sorted[i], ind_not_top_trans)
                    df2_dict = {'country': country, 'language': "other", 'map_year': plot_year, 'weights': sum_not_top_lang }
                    df2 = pd.DataFrame(data = df2_dict, index = ['0'])
                    
                    #idx = pd.Series(ind_top_lang_trans)
                    
                    # only non-other languages
                    h = h.iloc[ind_top_lang_trans, :]
                    
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
                #ax.legend(wedges, language,
                #    title="languages",
                #    loc="center left",
                #    bbox_to_anchor=(1, 0, 0.5, 1))
                #plt.title("{country}_{year}".format(country = country, year = plot_year))
                
                #plt.show()
                #hist = h[['language','weights']].plot(kind = 'bar', figsize=(8, 6), x = 'language', ylim = [0, y_max], color = colors).get_figure()
                plt.savefig('plots\\pie charts minor top 19 languages plain\\{country}_{year}'.format(country = country, year = plot_year), transparent=True)
            plt.close()
                #close(hist)
      
