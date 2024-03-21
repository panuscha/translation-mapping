import pandas as pd
from pandas.io.html import read_html
import html5lib
import re


def extract_language(s):
    # Extracting language before square brackets or parentheses
    match = re.match(r'([^\[\(]+)(?:\[|\()', s)
    if match:
        return match.group(1).strip()
    else:
        # If no square brackets or parentheses are found, return the whole string
        return s.strip()
    
def extract_words(s):
    words = re.findall('[A-Z][^A-Z]*', s)    
    return words

def get_official_languages(country_wiki):
    try: 
        page = 'https://en.wikipedia.org/wiki/{country}'.format(country = country_wiki)
        infoboxes = read_html(page, index_col=0)
        found = False
        for i in range(len(infoboxes)):
            infobox = infoboxes[i]
            infobox = [i for _, i in infobox.iterrows()]

            infobox_dict = {}

            for s in infobox :
                if isinstance(s.name, str) and "official" in s.name.lower() and 'language' in s.name.lower():
                    words = s.values
                    languages = [extract_language(word) for word in words] 
                    languages_list = []
                    for combined_word in languages:
                        languages_list.extend(extract_words(combined_word))
                    infobox_dict['Official language'] = languages_list#[].extend([extract_words(s.values[i]) for i in range(len(s.values)) ])
                    found = True
                    break
            if found:
                break    

        if 'Official language' in infobox_dict.keys():
            #print(infobox_dict['Official language'])     
        
            return infobox_dict['Official language']
        
        return []
    except: 
        #print(country + " not found.") 
        return []       
    


countries_info = pd.read_excel('geotagged/countries_codes.xlsx')
countries_info.index = countries_info['Country']


language_codes = pd.read_excel("geotagged/language_codes.xlsx")
language_codes.index = language_codes.name

df_dict = {}
countries_info['Official_language']  = [() for i in range(len(countries_info))]

for country in countries_info['Country'].unique():
    country_wiki = country.replace(' ', '_')
    print(country_wiki)
    official_languages = get_official_languages(country_wiki)
    df_dict[country] = []
    for lang in official_languages:
        lang_code = language_codes[language_codes.index == lang.strip()]['alpha3-b'].squeeze()
        if len(lang_code) > 0 : 
            df_dict[country].append(lang_code)
        else:
            lang_code = language_codes[language_codes.index == lang.strip()[:-1]]['alpha3-b'].squeeze() 
            if len(lang_code) > 0 : 
                df_dict[country].append(lang_code)   

    countries_info.at[country, 'Official_language'] = ",".join(df_dict[country])
    print(df_dict[country])        
    #official_languages
   

countries_info.to_excel("geotagged/countries_info_new.xlsx")
    
# Find the maximum length among all lists
max_length = max(len(lst) for lst in df_dict.values())

# Pad the shorter lists with None to make them of equal length
padded_data = {key: lst + [None] * (max_length - len(lst)) for key, lst in df_dict.items()}
    
df = pd.DataFrame(padded_data)
df.to_excel('geotagged/countries_official_languages.xlsx')

