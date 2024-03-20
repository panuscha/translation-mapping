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

def get_official_languages(country):
    try: 
        page = 'https://en.wikipedia.org/wiki/{country}'.format(country = country)
        infoboxes = read_html(page, index_col=0)[0]

        infoboxes = [i for _, i in infoboxes.iterrows()]

        infobox_dict = {}

        for s in infoboxes :
            if isinstance(s.name, str) and "official" in s.name.lower() and 'language' in s.name.lower():
                words = s.values
                languages = [extract_language(word) for word in words] 
                languages_list = []
                for combined_word in languages:
                    languages_list.extend(extract_words(combined_word))
                infobox_dict['Official language'] = languages_list#[].extend([extract_words(s.values[i]) for i in range(len(s.values)) ])
                break

        print(country)
        if 'Official language' in infobox_dict.keys():
            #print(infobox_dict['Official language'])     
        
            return infobox_dict['Official language']
        
        return []
    except: 
        #print(country + " not found.") 
        return []       
    

geotagged_df = pd.read_excel("geotagged/geotagged_germany_country_update.xlsx")


language_codes = pd.read_excel("geotagged/language_codes.xlsx")
language_codes.index = language_codes.name

df_dict = {}

for country in geotagged_df['geonames_country'].unique():
    country = country.replace(' ', '_')
    official_languages = get_official_languages(country)
    df_dict[country] = []
    for lang in official_languages:
        lang_code = language_codes[language_codes.index == lang.strip()]['alpha3-b'].squeeze()
        if len(lang_code) > 0 : 
            df_dict[country].append(lang_code)
    print(df_dict[country])        
    #official_languages
    
# Find the maximum length among all lists
max_length = max(len(lst) for lst in df_dict.values())

# Pad the shorter lists with None to make them of equal length
padded_data = {key: lst + [None] * (max_length - len(lst)) for key, lst in df_dict.items()}
    
df = pd.DataFrame(padded_data)
df.to_excel('geotagged/countries_official_languages.xlsx')

