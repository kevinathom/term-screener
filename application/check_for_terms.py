# -*- coding: utf-8 -*-
"""
purpose: Extract PDF text elements and screen for given terms
@author: kevinat
"""

"""
Build preliminary functions
"""
# Show file/directory selection dialog
import tkinter as tk
from tkinter import filedialog

def open_file_dialog(your_title = "Select a file"):
    # Initialize tkinter
    root = tk.Tk()
    # Hide the main window
    root.withdraw()
    # Show the file dialog and get the selected file path
    file_path = filedialog.askopenfilename(
        title = your_title,
        filetypes = (
            ("Comma-separated values", "*.csv"),
        )
    )
    # Clean up the tkinter instance
    root.destroy()
    return file_path

def open_directory_dialog(your_title = "Select a directory"):
    # Initialize tkinter
    root = tk.Tk()
    # Hide the main window
    root.withdraw()
    # Show the directory dialog and get the selected directory path
    directory_path = filedialog.askdirectory(
        title = your_title,
        mustexist = True
    ) + "/"
    # Clean up the tkinter instance
    root.destroy()
    return directory_path

# Show completion message window
from tkinter import messagebox

def show_completion_message(your_title = "Process Complete", your_message = "The process is complete."):
    # Initialize tkinter
    root = tk.Tk()
    # Hide the main window
    root.withdraw()
    # Show the message
    messagebox.showinfo(your_title, your_message)
    # Clean up the tkinter instance
    root.destroy()

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
import pandas as pd
# Specify file locations
term_set = open_file_dialog(your_title = "Select your terms file")
term_set = pd.read_csv(term_set)
data_dir = open_directory_dialog(your_title = "Select your directory of PDF files")

# Separate include/exclude terms
term_include = term_set[~term_set['Exclude']]
term_exclude = term_set[term_set['Exclude']]
del term_set

# Initialize storage
papers = []
any_match = []
canonicals = term_include['Canonical'].unique().tolist()
canonicals_clean = [can.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_').lower() for can in canonicals]
for can in canonicals_clean:
    globals()[f'{can}'] = []
del can

# Run algorithm on PDF files
from pdfminer.high_level import extract_text # Install pdfminer.six, not pdfminer

for file in list_files(data_dir):
    # List the filename
    papers.append(file[(file.rindex('/') + 1):-4])
    
    # When content metadata are missing
    if extract_text(file)['content'] is None:
        # Fill with Excel NA
        for can in canonicals_clean:
            globals()[f'{can}'].append('#N/A')
        del can
        any_match.append('#N/A')
      
    # When content metadata are present
    else:
        # Extract text content in four variations
        ## All variations remove line breaks, white space, and excluded terms
        ## words_pc retains *p*unctuation and *c*apitalization...
        words_pc = exclude_terms(term_exclude, extract_text(file)['content'].replace("\n", "").replace(" ", ""))
        words_p = exclude_terms(term_exclude, words_pc.lower())
        words_c = exclude_terms(term_exclude, words_pc.translate(str.maketrans('', '', string.punctuation)))
        words_ = exclude_terms(term_exclude, words_pc.translate(str.maketrans('', '', string.punctuation)).lower())
        
        # Check text for term matches
        match_can = []
        for i in list(range(len(canonicals))):
            match_var = []
            # Check each variation, conditional to arguments
            for index, row in term_include[term_include['Canonical'] == canonicals[i]].iterrows():
                if row['MatchPunctuation'] and row['MatchCase']:
                    match_var.append(row['Variation'].replace(" ", "") in words_pc)
                elif row['MatchPunctuation']:
                    match_var.append(row['Variation'].replace(" ", "").lower() in words_p)
                elif row['MatchCase']:
                    match_var.append(row['Variation'].replace(" ", "").translate(str.maketrans('', '', string.punctuation)) in words_c)
                else:
                    match_var.append(row['Variation'].replace(" ", "").translate(str.maketrans('', '', string.punctuation)).lower() in words_)
            # Combine any matches for the canonical term
            globals()[f'{canonicals_clean[i]}'].append(any(match_var))
            match_can.append(any(match_var))
        any_match.append(any(match_can))
        del match_can, i, match_var, index, row
del words_pc, words_p, words_c, words_

# Export results
result = pd.DataFrame({'Paper': papers, 'Any Match': any_match})
for i in list(range(len(canonicals))):
    result[canonicals[i]] = globals()[f'{canonicals_clean[i]}']
del i

from datetime import date
result.to_csv(data_dir + "results_" + str(date.today()) + ".csv", index = None, header = True)

# Confirm completion
show_completion_message(your_message = "Find results in " + data_dir + "results_" + str(date.today()) + ".csv")
