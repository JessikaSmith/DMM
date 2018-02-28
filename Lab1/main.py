import pandas as pd
import numpy as np

def extract_russia_data(file_name, sheet_name):
    columns = ['index', 'variant', 'area', 'notes', 'code', 'date',
               '0-4', '5-9', '10-14', '15-19', '20-24',
               '25-29', '30-34', '35-39', '40-44', '45-49',
               '50-54', '55-59', '60-64', '65-69', '70-74', '75-79',
               '80-84', '85-89', '90-94', '95-99', '100']

    data = pd.read_excel(file_name, sheetname=sheet_name, skiprows=6, names=columns)

    subs = data[(data['area'] == 'Russian Federation') & (data['date'].isin([2000, 2005]))]

    return subs


def surv_coeff(data, group):
    idx = data.columns.get_loc(group)

    return data.iloc[1, idx + 1] / data.iloc[0, idx]


def fertility_rate(both, fem, year):
    groups = ['20-24', '25-29', '30-34', '35-39']

    subs = fem[fem['date'] == year]
    both_subs = both[both['date'] == year]
    return both_subs['0-4'].values[0] / subs[groups].sum(axis=1).values[0]


def get_fm_ratio(ml, fem, year):
    group = '0-4'
    return ml.loc[ml['date']==year, group].values[0] / fem.loc[fem['date']==year, group].values[0]


def brute_1year_surv_coeff(data, group):
    idx = data.columns.get_loc(group)
    coef = []
    for i in np.arange(data.iloc[0, idx],data.iloc[1, idx + 1],(data.iloc[1, idx + 1]-data.iloc[0, idx])/5):
        print(i)
        coef += [(i+((data.iloc[1, idx + 1]-data.iloc[0, idx])/5))/i]
    return [np.mean(coef)]

name = 'age_data.xls'
fem_sheet = 'f; 1950-2005, estimates'
male_sheet = 'm; 1950-2005, estimates'
both_sheet = 'both; 1950-2005, estimates'

groups = ['0-4', '5-9', '10-14', '15-19', '20-24',
          '25-29', '30-34', '35-39', '40-44', '45-49',
          '50-54', '55-59', '60-64', '65-69', '70-74', '75-79',
          '80-84', '85-89', '90-94', '95-99']

fem = extract_russia_data(name, fem_sheet)
male = extract_russia_data(name, male_sheet)
both = extract_russia_data(name, both_sheet)
surv = []
for group in groups:
    surv.append(surv_coeff(fem, group))
print(surv)

surv_fem_1year = []
for group in ['90-94', '95-99']:
    surv_fem_1year += brute_1year_surv_coeff(fem, group)

print(surv_fem_1year)

#print(fertility_rate(both, fem, 2000))
print(get_fm_ratio(male, fem, 2000))


