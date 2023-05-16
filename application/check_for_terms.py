# -*- coding: utf-8 -*-
"""
###
Extract PDF text elements and screen for given terms
###

@author: kevinat
"""

"""
Specify file locations

Note:
    tika 1.23.1 fails in Windows 10
    consider installing older version:
        pip install tika==1.23
"""
from datetime import date
import pandas as pd

data_dir = "C:\\Users\\kevinat\\Documents\\GitHub\\term-screener\\data\\"
term_set = pd.read_csv(data_dir + "terms.csv")


"""
Build preliminary functions
"""
# List relevant paths and files
import os

def list_files(filepath = os.getcwd(), filetype = '.pdf'):
    # Specify input path with forward slash (/) or escaped back slash (\\)
    paths = []
    for root, dirs, files in os.walk(filepath):
        # Loop each directory and file within filepath
        for file in files:
            if file.lower().endswith(filetype.lower()):
                # Find PDFs and get their location/name
                paths.append(os.path.join(root, file))
    return(paths)

# Remove terms and flagged variations from text
import string

def exclude_terms(terms_df, text):
    # terms_df must be a pandas dataframe with columns:
    ## 'Variation' = terms to exclude
    ## 'MatchPunctuation' = logical flag where True means punctuation must match
    ## 'MatchCase' = logical flag where True means case must match
    # text must be a single character string
    for index, row in terms_df.iterrows():
        text = text.replace(row['Variation'].replace(" ", ""), '')
        if not row['MatchPunctuation']:
            text = text.replace(row['Variation'].replace(" ", "").translate(str.maketrans('', '', string.punctuation)), '')
        if not row['MatchCase']:
            text = text.replace(row['Variation'].replace(" ", "").lower(), '')
        if not row['MatchPunctuation'] and not row['MatchCase']:
            text = text.replace(row['Variation'].replace(" ", "").translate(str.maketrans('', '', string.punctuation)).lower(), '')
    return(text)


"""
Run procedure
"""
# Separate include/exclude terms
term_include = term_set[~term_set['Exclude']]
term_exclude = term_set[term_set['Exclude']]
del term_set

# Initialize storage
papers = []
canonicals = term_include['Canonical'].unique().tolist()
canonicals_clean = [can.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_').lower() for can in canonicals]
for can in canonicals_clean:
    globals()[f'{can}'] = []
del can

# Run algorithm on PDF files
import tika
tika.initVM()
from tika import parser

for file in list_files(data_dir):
    # List the filename
    papers.append(file[(file.rindex('\\') + 1):-4])
    
    # When content metadata are missing
    if parser.from_file(file)['content'] is None:
        # Fill with Excel NA
        for can in canonicals_clean:
            globals()[f'{can}'].append('#N/A')
        del can
      
    # When content metadata are present
    else:
        # Extract text content in four variations
        ## All variations remove line breaks, white space, and excluded terms
        ## words_pc retains *p*unctuation and *c*apitalization...
        words_pc = exclude_terms(term_exclude, parser.from_file(file)['content'].replace("\n", "").replace(" ", ""))
        words_p = exclude_terms(term_exclude, words_pc.lower())
        words_c = exclude_terms(term_exclude, words_pc.translate(str.maketrans('', '', string.punctuation)))
        words_ = exclude_terms(term_exclude, words_pc.translate(str.maketrans('', '', string.punctuation)).lower())
        
        # Check text for term matches
        for i in list(range(len(canonicals))):
            match = []
            # Check each variation, conditional to arguments
            for index, row in term_include[term_include['Canonical'] == canonicals[i]].iterrows():
                if row['MatchPunctuation'] and row['MatchCase']:
                    match.append(row['Variation'].replace(" ", "") in words_pc)
                elif row['MatchPunctuation']:
                    match.append(row['Variation'].replace(" ", "").lower() in words_p)
                elif row['MatchCase']:
                    match.append(row['Variation'].replace(" ", "").translate(str.maketrans('', '', string.punctuation)) in words_c)
                else:
                    match.append(row['Variation'].replace(" ", "").translate(str.maketrans('', '', string.punctuation)).lower() in words_)
            # Combine any matches for the canonical term
            globals()[f'{canonicals_clean[i]}'].append(any(match))
        del i, match, index, row

# ID where any database appears
any_database = []
for i in range(len(papers)):
    # Condition for missing/present content data
    # TO DO: treat terms dynamically
    if any([type(PitchBook[i]) == str, type(WRDS[i]) == str, type(AdSpender[i]) == str, type(Amadeus[i]) == str, type(Osiris[i]) == str, type(Bureau_van_Dijk[i]) == str, type(LexisNexis[i]) == str, type(Nexis_Uni[i]) == str, type(Data_Axle[i]) == str, type(BCIQ[i]) == str, type(Automotive_News_Data_Center[i]) == str, type(IndustriusCFO[i]) == str, type(SBRnet[i]) == str, type(Mergent[i]) == str, type(Hoovers[i]) == str, type(CB_Insights[i]) == str, type(Real_Capital_Analytics[i]) == str, type(REIS[i]) == str, type(Foundation_Directory[i]) == str, type(Preqin[i]) == str, type(Moodys[i]) == str, type(SimplyAnalytics[i]) == str, type(Global_Financial_Data[i]) == str, type(SRDS[i]) == str, type(UN_Comtrade[i]) == str, type(Bests[i]) == str, type(WARC[i]) == str, type(Bizcomps[i]) == str]):
        any_database.append('#N/A')
    else:
        any_database.append(any([PitchBook[i], WRDS[i], AdSpender[i], Amadeus[i], Osiris[i], Bureau_van_Dijk[i], LexisNexis[i], Nexis_Uni[i], Data_Axle[i], BCIQ[i], Automotive_News_Data_Center[i], IndustriusCFO[i], SBRnet[i], Mergent[i], Hoovers[i], CB_Insights[i], Real_Capital_Analytics[i], REIS[i], Foundation_Directory[i], Preqin[i], Moodys[i], SimplyAnalytics[i], Global_Financial_Data[i], SRDS[i], UN_Comtrade[i], Bests[i], WARC[i], Bizcomps[i]]))

# Export results
#from pandas import DataFrame

# TO DO: generate list dynamically
result = {'Paper': papers,
          'Any_Database': any_database,
          'PitchBook': PitchBook,
          'WRDS': WRDS,
          'AdSpender': AdSpender,
          'Amadeus': Amadeus,
          'Osiris': Osiris,
          'Bureau_van_Dijk': Bureau_van_Dijk,
          'LexisNexis': LexisNexis,
          'Nexis_Uni': Nexis_Uni,
          'Data_Axle': Data_Axle,
          'BCIQ': BCIQ,
          'Automotive_News_Data_Center': Automotive_News_Data_Center,
          'IndustriusCFO': IndustriusCFO,
          'SBRnet': SBRnet,
          'Mergent': Mergent,
          'Hoovers': Hoovers,
          'CB_Insights': CB_Insights,
          'Real_Capital_Analytics': Real_Capital_Analytics,
          'REIS': REIS,
          'Foundation_Directory': Foundation_Directory,
          'Preqin': Preqin,
          'Moodys': Moodys,
          'SimplyAnalytics': SimplyAnalytics,
          'Global_Financial_Data': Global_Financial_Data,
          'SRDS': SRDS,
          'UN_Comtrade': UN_Comtrade,
          'Bests': Bests,
          'WARC': WARC,
          'Bizcomps': Bizcomps}
# TO DO: generate columns dynamically
result = pd.DataFrame(result, columns = ['Paper', 'Any_Database', 'PitchBook', 'WRDS', 'AdSpender', 'Amadeus', 'Osiris', 'Bureau_van_Dijk', 'LexisNexis', 'Nexis_Uni', 'Data_Axle', 'BCIQ', 'Automotive_News_Data_Center', 'IndustriusCFO', 'SBRnet', 'Mergent', 'Hoovers', 'CB_Insights', 'Real_Capital_Analytics', 'REIS', 'Foundation_Directory', 'Preqin', 'Moodys', 'SimplyAnalytics', 'Global_Financial_Data', 'SRDS', 'UN_Comtrade', 'Bests', 'WARC', 'Bizcomps'])

result.to_csv(data_dir + "results_" + str(date.today()) + ".csv", index = None, header = True)