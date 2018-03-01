import pandas as pd
import numpy as np

INITIAL_YEAR = 2005

class PredictionModel():

    def __init__(self, file, fem_sheet, male_sheet, both_sheet):

        self.columns = ['index', 'variant', 'area', 'notes', 'code', 'date',
                   '0-4', '5-9', '10-14', '15-19', '20-24',
                   '25-29', '30-34', '35-39', '40-44', '45-49',
                   '50-54', '55-59', '60-64', '65-69', '70-74', '75-79',
                   '80-84', '85-89', '90-94', '95-99', '100']
        self.fem_data = self.extract_russia_data(file, fem_sheet)
        self.male_data = self.extract_russia_data(file, male_sheet)
        self.both_data = self.extract_russia_data(file, both_sheet)
        self.pred_dict = {
            'female':self.fem_data,
            'male': self.male_data,
            'both':self.both_data
        }


    def extract_russia_data(self, file_name, sheet_name):

        data = pd.read_excel(file_name, sheetname=sheet_name, skiprows=6, names=self.columns)
        subs = data[(data['area'] == 'Russian Federation') & (data['date'].isin([INITIAL_YEAR-5, INITIAL_YEAR]))]
        return subs



    def fertility_rate(self, year):

        #check
        groups = self.columns[10:14]
        print(groups)
        subs = self.fem_data[self.fem_data['date'] == year]
        both_subs = self.both_data[self.both_data['date'] == year]
        return both_subs['0-4'].values[0] / subs[groups].sum(axis=1).values[0]



    def surv_coeff(self, group):

        idx = self.both_data.columns.get_loc(group)
        return self.both_data.iloc[1, idx + 1] / self.both_data.iloc[0, idx]



    def get_value_prediction(self, data, group, counter):

        idx = self.fem_data.columns.get_loc(group)

        return data.iloc[counter, idx]*self.coeffs[idx-7]


    # TODO: fix this
    def brute_1year_surv_coeff(data, group):
        idx = data.columns.get_loc(group)
        coef = []
        for i in np.arange(data.iloc[0, idx], data.iloc[1, idx + 1], (data.iloc[1, idx + 1] - data.iloc[0, idx]) / 5):
            print(i)
            coef += [(i + ((data.iloc[1, idx + 1] - data.iloc[0, idx]) / 5)) / i]
        return [np.mean(coef)]



    def pred_model_5_years(self, num_years, type = 'both'):
        """simple implementation of model with 5 years step"""

        data = self.pred_dict['both'].copy()
        fertility = self.fertility_rate(INITIAL_YEAR)
        self.coeffs = []
        print(self.columns[6:26])
        for group in self.columns[6:26]:
            self.coeffs.append(self.surv_coeff(group))
        counter = 1
        next = []
        fem = self.fem_data[self.fem_data['date'] == INITIAL_YEAR][self.columns[10:14]].values.tolist()
        fem = fem[0]
        for i in range(INITIAL_YEAR, INITIAL_YEAR+num_years,5):
            next = [0] * 5 + [i + 5] + [0]
            for group in self.columns[7:27]:
                next += [self.get_value_prediction(data, group, counter)]
            fem_sum = 0
            fem = np.multiply(self.coeffs[3:7], fem).tolist()
            next[6] = sum(fem)*fertility
            df = pd.DataFrame.from_records([tuple(next)], columns=self.columns)
            data = data.append(df)
            counter += 1
        return next

