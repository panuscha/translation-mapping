import pandas as pd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from itertools import compress
from matplotlib.patches import Patch
import pandas as pd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from itertools import compress
from matplotlib.patches import Patch
from matplotlib.legend_handler import HandlerTuple
from matplotlib.collections import PatchCollection

#!/usr/bin/env python
# -*- coding: utf-8 -*-

TOP = 3
MIN_TRANS = 4 

# size of the outer chart
SIZE = 0.2

title_legend = True
            

# Table with number of translations for each country, language and decade
df = pd.read_excel("weights/translations_language_countries.xlsx")

# countries and languages from number_of_colors.py  
languages = ["rus", "est", "arm", "glg", "ukr", "wen", "eng", "lit", "baq", "dut", "slv", "mac", "hrv", "epo", "hun", "ger", "cat", "fre", "slo", "other"]

country = "USSR"
plot_year = '1945'
except_countries = {"Czechoslovakia" : ["slo"], "Belgium" : ["fre", "dut"],  "Switzerland": ["ger", "fre"], "Yugoslavia": ["hrv"]}


my_color_palette = {}
#all_colors = list(colors.CSS4_COLORS.keys())
all_colors =[plt.cm.tab20(i) for i in range(20)]
handles = []

# Save color for each country
for i, language in enumerate(languages):
    my_color_palette[language] = all_colors[i]


# define an object that will be used by the legend
class MulticolorPatch(object):
    def __init__(self, colors):
        self.colors = colors
        
# define a handler for the MulticolorPatch object
class MulticolorPatchHandler(object):
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        width, height = handlebox.width, handlebox.height
        patches = []
        for i, c in enumerate(orig_handle.colors):
            patches.append(plt.Rectangle([width/len(orig_handle.colors) * i - handlebox.xdescent, 
                                          -handlebox.ydescent],
                           width / len(orig_handle.colors),
                           height, 
                           facecolor=c, 
                           edgecolor='none'))

        patch = PatchCollection(patches,match_original=True)

        handlebox.add_artist(patch)
        return patch


# Select only non empty rows that are in the decade and for that country
if not df[(df['map_year'] == int(plot_year)) &  (df['country'] == country)].empty:

    # All non-empty rows
    h = df[(df['map_year'] == int(plot_year)) &  (df['country'] == country)]
    
    # sort values by weights descending
    h = h.sort_values(by = 'weights', ascending = 0)
    
    # if only weights, change to h.weights
    sum_weights = sum(h.weights)
    
    
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
    
    # outher colors, major will always be transparent, minor is displayed as black
    outer_colors = [my_color_palette['eng'] , 'black' ]

    # list of outer weights 
    weights_all = [h_max, sum_weights - h_max ]
    
    # plot
    fig, ax = plt.subplots(figsize = (10,10))
    
    # outer pie
    n = ax.pie(weights_all, radius=1, colors=outer_colors,
    
    # white edges
    wedgeprops=dict(width=SIZE, edgecolor='w'))
    
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
        #language = ['podíl překladů do dalších jazyků', 'poměrné zastoupení dalších jazyků']
        
        # if only weights, change to h.weights
        weights = [w/sum_weights for w in h.weights] 


        if title_legend:
        # inner pie chart
            
            # colors = [['black'], 
            # [my_color_palette['ukr'],my_color_palette['arm'],my_color_palette['lit'], my_color_palette['other']]]
            # categories = ['podíl překladů do dalších jazyků','poměrné zastoupení dalších jazyků']
            # #create dict
            # legend_dict=dict(zip(categories,colors))
            # #create patches
            # patchList = []
            # for cat, col in legend_dict.items():
            #     patchList.append([mpatches.Patch(facecolor=c, label=cat, linestyle='-') for c in col])


            # plt.gca()
            # plt.legend(handles=patchList, labels=categories, ncol=len(categories), fontsize='x-large', 
            #            bbox_to_anchor=(1.1, 1), 
            #             handler_map = {list: HandlerTuple(None)})


            pa1 = Patch(facecolor='black', edgecolor='black')
            pa2 = Patch(facecolor='black', edgecolor='black')
            pa3 = Patch(facecolor='black', edgecolor='black')
            pa4 = Patch(facecolor='black', edgecolor='black')
            #
            pb1 = Patch(facecolor=my_color_palette['ukr'], edgecolor='black')
            pb2 = Patch(facecolor=my_color_palette['arm'], edgecolor='black')
            pb3 = Patch(facecolor=my_color_palette['lit'], edgecolor='black')
            pb4 = Patch(facecolor=my_color_palette['other'], edgecolor='black')

            ax.legend(handles=[pa1, pb1, pa2, pb2, pa3, pb3, pa4, pb4],
                    labels=['', '', '', '', '', '', '                                       ', '                                    '], #'poměr zastoupení dalších jazyků', 'podíl překladů do dalších jazyků'
                    ncol=4, handletextpad=0.6, handlelength=1.1, columnspacing=-0.6,
                    loc='best', fontsize=16)

            
            # #wedges, _ = ax.pie(weights, radius=1-SIZE, colors=inner_colors,
            wedges, _ = ax.pie(weights, radius=1-SIZE, colors=inner_colors, ## for legend
            wedgeprops=dict(edgecolor='w')) #width=size, 
            # ax.legend(wedges, language,
            # title='poměrné zastoupení dalších jazyků',
            # loc="lower left",
            # bbox_to_anchor=(0.5, 0, 0.5, 1))
            #plt.title("{country}_{year}".format(country = country, year = plot_year))
        
        #plt.show()
        #hist = h[['language','weights']].plot(kind = 'bar', figsize=(8, 6), x = 'language', ylim = [0, y_max], color = colors).get_figure()
        #plt.savefig('plots/without title/pie charts minor top 19 languages plain/{country}_{year}.png'.format(country = country, year = plot_year), transparent=True, dpi=600)
        plt.savefig('plots/with title/dummy charts/dummy_chart.svg', transparent=True, dpi=600)
    plt.close()
        #close(hist)
    



