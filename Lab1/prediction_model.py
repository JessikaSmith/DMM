import pandas as pd
import numpy as np

INITIAL_YEAR = 2005

fem_pred_sheet = 'f; 2010-50, medium-fertility'
male_pred_sheet = 'm; 2010-50, medium-fertility'
both_pred_sheet = 'both; 2010-50, medium-fertility'


class PredictionModel:

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
        self.fem_pred_data = self.extract_russia_data(file, fem_pred_sheet, 2)
        self.male_pred_data = self.extract_russia_data(file, male_pred_sheet, 2)
        self.both_pred_data = self.extract_russia_data(file, both_pred_sheet, 2)
        self.given_pred = {
            'female': self.fem_pred_data,
            'male': self.male_pred_data,
            'both': self.both_pred_data
        }

    def extract_russia_data(self, file_name, sheet_name, type=1):

        data = pd.read_excel(file_name, sheetname=sheet_name, skiprows=6, names=self.columns)
        if type == 1:
            subs = data[(data['area'] == 'Russian Federation') & (data['date'].isin([INITIAL_YEAR - 5, INITIAL_YEAR]))]
        else:
            subs = data[(data['area'] == 'Russian Federation')]
        return subs

    def extract_given_prediction(self, type='both'):

        return self.given_pred[type]

    def fertility_rate(self, year, type='both'):

        people_data = self.pred_dict[type]
        groups = self.fem_fert_groups
        subs = self.fem_data[self.fem_data['date'] == year]
        people_subs = people_data[people_data['date'] == year]
        return people_subs['0-4'].values[0] / subs[groups].sum(axis=1).values[0]

    # TODO: count fertility coeff (make it more sensible) and look at different scenarios (when the population will be stable)
    def fertility_rate_1_year(self, year, type='both'):

        people_data = self.pred_dict[type]
        groups = self.fem_fert_groups
        subs = self.fem_data[self.fem_data['date'] == year]
        people_subs = people_data[people_data['date'] == year]
        return ((people_subs['0-4'].values[0]) / 5) / subs[groups].sum(axis=1).values[0]

    def surv_coeff(self, group, data):

        idx = data.columns.get_loc(group)
        return data.iloc[1, idx + 1] / data.iloc[0, idx]

    def count_coeffs(self, data):

        coeffs = []
        for group in self.set_of_age_groups[:-1]:
            coeffs += [np.power(self.surv_coeff(group, data), 1 / 5)] * 5
        return coeffs

    def get_value_prediction(self, data, group, counter):

        idx = self.fem_data.columns.get_loc(group)
        return data.iloc[counter, idx] * self.coeffs[idx - 8]

    def pred_model_1_year(self, num_years, type='both'):
        """simple implementation of model with 1 year step"""

        data = self.pred_dict[type].copy()
        coeffs = self.count_coeffs(data)
        fertility = self.fertility_rate_1_year(INITIAL_YEAR, type)
        titles = ['date'] + [str(i) for i in range(101)]

        subs = data[data['date'] == INITIAL_YEAR].values[0]
        # TODO: refactor this
        subs = subs[6:]
        vals = []
        for i in subs:
            vals += [round(i / 5, 3)] * 5
        vals = vals[0:len(vals) - 4]
        vals[-1] == subs[-1]

        new_df = data[6:].copy()

        data = pd.DataFrame.from_records([tuple([INITIAL_YEAR] + vals)], columns=titles)
        fm = self.fem_data[self.fem_data['date'] == INITIAL_YEAR][self.fem_fert_groups].values.tolist()[0]
        fem = []
        for i in fm:
            fem += [i / 5] * 5
        counter = 0
        for i in range(INITIAL_YEAR + 1, INITIAL_YEAR + num_years + 1):
            next = [i, 0]
            next += np.multiply(coeffs, data.iloc[counter, 1:-1].tolist()).tolist()
            next = [round(i, 3) for i in next]
            fem = np.multiply(coeffs[19:39], fem).tolist()
            next[1] = round(sum(fem) * fertility, 3)

            new_next = []
            for t in range(1, len(next) - 5, 5):
                val = 0
                for j in range(5):
                    val += next[t + j]
                new_next += [val]
            df = pd.DataFrame.from_records([tuple([i] + new_next + [next[-1]])],
                                           columns=['date'] + self.set_of_age_groups)
            new_df = new_df.append(df)

            df = pd.DataFrame.from_records([tuple(next)], columns=titles)
            data = data.append(df)

            counter += 1

        return (new_df)

    # bad variant (jic)
    def brute_surv_coeff_1year(data, group):

        idx = data.columns.get_loc(group)
        coef = []
        for i in np.arange(data.iloc[0, idx], data.iloc[1, idx + 1], (data.iloc[1, idx + 1] - data.iloc[0, idx]) / 5):
            print(i)
            coef += [(i + ((data.iloc[1, idx + 1] - data.iloc[0, idx]) / 5)) / i]
        return [np.mean(coef)]
