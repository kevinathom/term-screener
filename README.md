# term-screener
Screen a set of documents for given terms.

## Capabilities
Given a set of PDF files encoded with text metadata and a complete terms input table, *check_for_terms.py* will search each PDF for submitted terms and variations. The script will output, in CSV format, a matrix identifying which of the documents contain which of the submitted terms.

## Instructions
1. Identify a directory containing all PDF files to search. The script will search subdirectories.
2. Update *check_for_terms.py*, line 21, to reflect the path for the above directory.
3. Following the format of *terms_template.csv*, list all terms and variations to find. Name this file *terms.csv* and place the file in the base directory Column descriptions:
  - Canonical
  - Variation
  - Exclude
  - MatchPunctuation
  - MatchCase
4. Run *check_for_terms.py*.
5. Find results in the provided directory, filename *results_*YYYY-MM-DD*.csv*

## Aspirations
- Add error-handling for missing/unexpected values in the terms input table.
- Add prompt for filepath/filename.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
