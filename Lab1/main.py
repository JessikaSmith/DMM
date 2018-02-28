import pandas as pd


def extract_russia_data(file_name, sheet_name):
    columns = ['index', 'variant', 'area', 'notes', 'code', 'date',
               '0-4', '5-9', '10-14', '15-19', '20-24',
               '25-29', '30-34', '35-39', '40-44', '45-49',
               '50-54', '55-59', '60-64', '65-69', '70-74', '75-79',
               '80-84', '85-89', '90-94', '95-99', '100']

    data = pd.read_excel(file_name, sheetname=sheet_name, skiprows=6, names=columns)

    subs = data[data['area'] == 'Russian Federation']
    subs = subs[subs['date'].isin([2000, 2005])]

    return subs


def surv_coeff(data, group):
    idx = data.columns.get_loc(group)

    return data.iloc[1, idx + 1] / data.iloc[0, idx]


def fertility_rate(both, fem, year):
    groups = ['20-24', '25-29', '30-34', '35-39']

    subs = fem[fem['date'] == year]
    both_subs = both[both['date'] == year]
    print(both_subs['0-4'].values[0] / subs[groups].sum(axis=1).values[0])


name = 'age_data.xls'
fem_sheet = 'f; 1950-2005, estimates'
both_sheet = 'both; 1950-2005, estimates'

groups = ['0-4', '5-9', '10-14', '15-19', '20-24',
          '25-29', '30-34', '35-39', '40-44', '45-49',
          '50-54', '55-59', '60-64', '65-69', '70-74', '75-79',
          '80-84', '85-89', '90-94', '95-99']

fem = extract_russia_data(name, fem_sheet)
both = extract_russia_data(name, both_sheet)
surv = []
for group in groups:
    surv.append(surv_coeff(fem, group))

print(surv)
fertility_rate(both, fem, 2000)
