import re

Lines = ['', 'Financial Statements: Standalone', '', 'Standalone Balance Sheet', 'as at March 31, 2023', 'CIN : L93030DL2010PLC198141', '', '(INR million)', '', 'Particulars Note Asat Asat', 'March 31,2023 March 31, 2022', '', 'Assets', 'Non-current assets', 'Property, plant and equipment 3 587 326', 'Right-of-use asset 32 1,339 257', 'Goodwill 4 12,093 12,093', 'Other intangible assets 4 4 799', 'Financial assets', 'Investments 5 88,619 35,356', 'Loans 10 9,580 -', 'Other financial assets 1 18,627 52,150', 'Tax assets (net) 12 963 658', 'Other non-current assets 13 22 0', 'Total non-current assets 131,834 101,639', '', 'Current assets', '', 'Inventories 14 3 -', 'Financial assets', 'Investments 6 38,325 16,008', 'Trade receivables 7 622 1669', 'Cash and cash equivalents 8 1,228 2,941', 'Other bank balances 9 2,755 11,706', 'Loans 10 - 3,750', 'Other financial assets 1 43,995 36,639', 'Other current assets 13 507 655', 'Total current assets 87,435 73,368', 'Total assets 219,269 175,007', '', 'Equity and liabilities', '', 'Equity', '', 'Equity share capital 15(a) 8,364 7643', 'Other equity 15(b) 199,704 160,029', 'Total equity 208,068 167,672', 'Liabilities', '', 'Non-current liabilities', 'Financial liabilities', '', 'Lease liabilities 32 1,261 182', 'Provisions 17 570 520', 'Other non-current liabilities 19 - 2', '', 'Total non-current liabilities 1,831 704', '', '']
listp1 = []
listp2 = []
listp3 = []
list4 = []
date_pattern = r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|' \
               r'\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{2,4}|' \
               r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2})\b'

date_pattern2 = r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|' \
                r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-zA-Z.,-]*[\s-]?\d{1,2}?[,\s-]?[\s]?\d{4}|' \
                r'\d{1,2}[/-]\d{4}|\d{4})\b(?!-?\d{2,4})'

date_pattern3 = r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s*\d{4}\b"

for elements in Lines:


print("List-D1:", listp1)
print("List-D2:", listp2)
print("List-D3:", listp3)
print("List-4:", list4)