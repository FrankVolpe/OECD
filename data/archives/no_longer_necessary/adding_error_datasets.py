''' See the file o_failed_datasets for information as to why this is necessary
'''

import sys

with open('o_dataset_ids.txt', 'r') as inf:
    datasets = eval(inf.read())

datasets['PRICES_CPI'] = 'Prices: Consumer prices'
datasets['FDI_POS_AGGR'] = 'Benchmark definition, 4th edition (BMD4): Foreign direct investment: positions, main aggregates'
datasets['CHAPTER_C_EAG2014'] = 'Education at a glance: ISCED-97, Access to education, participation and progression (Edition 2014)'
datasets['CHAPTER_A_EAG2014_NEW'] = 'Education at a glance: ISCED-97, Education and learning outputs and outcomes (Edition 2014)'
datasets['CHAPTER_B_EAG2014'] = 'Education at a glance: ISCED-97, Financial and human resources investment in education (Edition 2014)'
datasets['IDD'] = 'Social Expenditure: Income Distribution'
datasets['FIXINCLSA'] = 'Social Expenditure: Taxes and Benefits'
datasets['TAXBEN'] = 'Social Expenditure: Taxes and benefits - indicators'

sys.stdout = open('dataset_ids.txt', 'w')
print(datasets)
