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
        self.set_of_age_groups = ['0-4', '5-9', '10-14', '15-19', '20-24',
                                  '25-29', '30-34', '35-39', '40-44', '45-49',
                                  '50-54', '55-59', '60-64', '65-69', '70-74', '75-79',
                                  '80-84', '85-89', '90-94', '95-99', '100']
        self.fem_fert_groups = ['20-24', '25-29', '30-34', '35-39']
        self.fem_data = self.extract_russia_data(file, fem_sheet)
        self.male_data = self.extract_russia_data(file, male_sheet)
        self.both_data = self.extract_russia_data(file, both_sheet)
        self.pred_dict = {
            'female': self.fem_data,
            'male': self.male_data,
            'both': self.both_data
        }

    def extract_russia_data(self, file_name, sheet_name):

        data = pd.read_excel(file_name, sheetname=sheet_name, skiprows=6, names=self.columns)
        subs = data[(data['area'] == 'Russian Federation') & (data['date'].isin([INITIAL_YEAR-5, INITIAL_YEAR]))]
        return subs

    def fertility_rate(self, year, type='both'):

        people_data = self.pred_dict[type]
        groups = self.fem_fert_groups
        subs = self.fem_data[self.fem_data['date'] == year]
        people_subs = people_data[people_data['date'] == year]
        return people_subs['0-4'].values[0] / subs[groups].sum(axis=1).values[0]

    def fertility_rate_1_year(self, year, type='both'):

        people_data = self.pred_dict[type]
        groups = self.fem_fert_groups
        subs = self.fem_data[self.fem_data['date'] == year]
        people_subs = people_data[people_data['date'] == year]
        return ((people_subs['0-4'].values[0])/5) / subs[groups].sum(axis=1).values[0]

    def surv_coeff(self, group, data):

        idx = data.columns.get_loc(group)
        return data.iloc[1, idx + 1] / data.iloc[0, idx]

    def count_coeffs(self, data):

        coeffs = []
        for group in self.set_of_age_groups[:-1]:
            coeffs += [np.power(self.surv_coeff(group, data), 1/5)]*5
        return coeffs

    def get_value_prediction(self, data, group, counter):

        idx = self.fem_data.columns.get_loc(group)
        return data.iloc[counter, idx]*self.coeffs[idx-8]

    def reshape_dataset(self, data):
        # TODO: implement reshaping
        return True

    def pred_model_5_years(self, num_years, type='both'):
        """simple implementation of model with 5 years step"""

        data = self.pred_dict[type].copy()
        fertility = self.fertility_rate(INITIAL_YEAR, type)
        self.coeffs = []
        for group in self.set_of_age_groups[:-1]:
            self.coeffs.append(self.surv_coeff(group, data))
        counter = 1
        fem = self.fem_data[self.fem_data['date'] == INITIAL_YEAR][self.fem_fert_groups].values.tolist()
        fem = fem[0]
        next = []
        for i in range(INITIAL_YEAR, INITIAL_YEAR+num_years, 5):
            next = [0] * 5 + [i + 5] + [0]
            for group in self.set_of_age_groups[1:]:
                next += [round(self.get_value_prediction(data, group, counter), 3)]
            fem_sum = 0
            # coeff for both sexes are used here
            fem = np.multiply(self.coeffs[3:7], fem).tolist()
            next[6] = round(sum(fem)*fertility, 3)
            df = pd.DataFrame.from_records([tuple(next)], columns=self.columns)
            data = data.append(df)
            counter += 1
        return data

    def pred_model_1_year(self, num_years, type = 'both'):
        """simple implementation of model with 1 year step"""

        data = self.pred_dict[type].copy()
        coeffs = self.count_coeffs(data)
        # TODO: fix fertility
        fertility = self.fertility_rate_1_year(INITIAL_YEAR, type)
        titles = ['date'] + [str(i) for i in range(101)]

        subs = data[data['date'] == INITIAL_YEAR].values[0]
        subs = subs[6:]
        vals = []
        for i in subs:
            vals += [round(i/5, 3)]*5
        vals = vals[0:len(vals) - 4]
        vals[-1] == subs[-1]

        data = pd.DataFrame.from_records([tuple([INITIAL_YEAR]+vals)], columns=titles)
        fm = self.fem_data[self.fem_data['date'] == INITIAL_YEAR][self.fem_fert_groups].values.tolist()[0]
        fem = []
        for i in fm:
            fem += [i/5]*5
        counter = 0
        for i in range(INITIAL_YEAR+1, INITIAL_YEAR + num_years + 1):
            next = [i, 0]
            next += np.multiply(coeffs, data.iloc[counter, 1:-1].tolist()).tolist()
            next = [round(i, 3) for i in next]
            fem = np.multiply(coeffs[19:39], fem).tolist()
            next[1] = round(sum(fem) * fertility, 3)

            df = pd.DataFrame.from_records([tuple(next)], columns=titles)
            data = data.append(df)
            counter += 1
        # reshape data to groups of sums ("0-4" and so on)
        # return self.reshape_dataset(data)
        return(data)

    # bad variant (jic)
    def brute_surv_coeff_1year(data, group):

        idx = data.columns.get_loc(group)
        coef = []
        for i in np.arange(data.iloc[0, idx], data.iloc[1, idx + 1], (data.iloc[1, idx + 1] - data.iloc[0, idx]) / 5):
            print(i)
            coef += [(i + ((data.iloc[1, idx + 1] - data.iloc[0, idx]) / 5)) / i]
        return [np.mean(coef)]