# term-screener
Screen a set of documents for given terms.

## Capabilities
Given a directory of PDF files encoded with text metadata and a complete terms input table, *check_for_terms.py* will search each PDF for submitted terms and variations. The script will output, in CSV format, a matrix identifying which of the documents contain which of the submitted terms.

## Instructions
1. Following the format of `terms_template.csv`, list all terms and variations to find. Column descriptions:
   - Canonical - The shared name you want to use for a given term or set of term variations; The results report by unique Canonical
   - Variation - A specific instance of a term that the tool should match; Any Variation of a single Canonical will flag the Canonical as present
   - Exclude - True will remove the term from text before searching; False will search for the term
   - MatchPunctuation - True will match based on punctuation; False will ignore punctuation
   - MatchCase - True will match based on case/capitalization; False will ignore case/capitalization
1. Place all PDF files to search within one directory. Files can be in subdirectories.
1. Run `check_for_terms.exe` on Windows or `check_for_terms.py` using Python.
   1. When prompted, select your CSV file of terms to find.
   1. When prompted, select a directory containing all PDF files to search. The script will search this directory and its subdirectories.
   1. You will be prompted when the process completes.
1. Find results in your directory of PDFs, filename `results_*YYYY-MM-DD*.csv`.

## Aspirations
- Add error-handling for missing/unexpected values in the terms input table.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
