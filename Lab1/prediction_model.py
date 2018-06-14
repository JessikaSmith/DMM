import numpy as np
import pandas as pd

INITIAL_YEAR = 2005

INITIAL_GIVEN_YEAR = 1950
FINAL_GIVEN_YEAR = 2000

fem_pred_sheet = 'f; 2010-50, medium-fertility'
male_pred_sheet = 'm; 2010-50, medium-fertility'
both_pred_sheet = 'both; 2010-50, medium-fertility'


class PredictionModel:
    def __init__(self, file, fem_sheet, male_sheet, both_sheet, babies_fraction=1.0):

        self.columns = ['index', 'variant', 'area', 'notes', 'code', 'date',
                        '0-4', '5-9', '10-14', '15-19', '20-24',
                        '25-29', '30-34', '35-39', '40-44', '45-49',
                        '50-54', '55-59', '60-64', '65-69', '70-74', '75-79',
                        '80-84', '85-89', '90-94', '95-99', '100']
        self.age_groups = ['0-4', '5-9', '10-14', '15-19', '20-24',
                           '25-29', '30-34', '35-39', '40-44', '45-49',
                           '50-54', '55-59', '60-64', '65-69', '70-74', '75-79',
                           '80-84', '85-89', '90-94', '95-99', '100']
        self.fem_fert_groups = ['20-24', '25-29', '30-34', '35-39']

        self.pred_dict = {
            'female': self.extract_russia_data(file, fem_sheet),
            'male': self.extract_russia_data(file, male_sheet),
            'both': self.extract_russia_data(file, both_sheet)
        }

        self.given_pred = {
            'female': self.extract_russia_data(file, fem_pred_sheet),
            'male': self.extract_russia_data(file, male_pred_sheet),
            'both': self.extract_russia_data(file, both_pred_sheet)
        }

        self.babies_fraction = babies_fraction
        self.calc_babies_fraction(self.babies_fraction)

    def calc_babies_fraction(self, babies_fraction):
        self.male_babies_rate = babies_fraction
        self.female_babies_rate = 1 - self.male_babies_rate

    def extract_russia_data(self, file_name, sheet_name):

        data = pd.read_excel(file_name, sheetname=sheet_name, skiprows=6, names=self.columns)
        russia_only = data.query('area == "Russian Federation"')

        return russia_only

    def extract_given_prediction(self, type='both'):

        return self.given_pred[type]

    # TODO: count fertility coeff (make it more sensible) and look at different scenarios (when the population will be stable)
    def fertility_rate_1_year(self, year, type='both'):

        population = self.pred_dict[type].query('date == @year')
        females = self.pred_dict['female'].query('date == @year')

        babies_group = '0-4'
        return ((population[babies_group].values[0]) / 5) / females[self.fem_fert_groups].sum(axis=1).values[0]

    def surv_coeff(self, population, age_from, age_to, initial_year, final_year):

        population_from = population.query('date == @initial_year')[age_from].values[0]
        population_to = population.query('date == @final_year')[age_to].values[0]

        return population_to / population_from

    def calculate_survival_coeffs_1_year(self, data, initial_year, final_year,
                                         x1=None, x14=None, x18=None, x28=None, x41=None, secret_num=1):

        coeffs = []
        for group_idx in range(0, len(self.age_groups) - secret_num):
            coeff = self.surv_coeff(data, self.age_groups[group_idx], self.age_groups[group_idx + 1],
                                    initial_year, final_year)
            coeffs += [np.power(coeff, 1 / 5)] * 5
        if x1 is not None:
            coeffs[0] = x1
            coeffs[13] = x14
            coeffs[17] = x18
            coeffs[27] = x28
            coeffs[40] = x41
        return coeffs

    def get_value_prediction(self, data, group, counter):

        idx = self.fem_data.columns.get_loc(group)
        return data.iloc[counter, idx] * self.coeffs[idx - 8]

    def pred_model_1_year_with_fertility(self, num_years, fertility, type='both', babies_fraction=1.0, x1=None,
                                         x14=None, x18=None, x28=None, x41=None):
        self.calc_babies_fraction(babies_fraction)

        selected = self.pred_dict[type].copy()
        females = self.pred_dict['female'].copy()
        surv_coeffs = self.calculate_survival_coeffs_1_year(selected, INITIAL_YEAR - 5, INITIAL_YEAR,
                                                            x1=x1, x14=x14, x18=x18, x28=x28, x41=x41)
        fem_surv_coeffs = self.calculate_survival_coeffs_1_year(females, INITIAL_YEAR - 5, INITIAL_YEAR,
                                                                x1=x1, x14=x14, x18=x18, x28=x28, x41=x41)

        population = selected.query('date == @INITIAL_YEAR')[self.age_groups]
        females = females.query('date == @INITIAL_YEAR')[self.age_groups]

        graduated_groups = []
        graduated_fem_groups = []

        for group in population:
            if group == '100':
                graduated_groups += [round(population[group].values[0] / 5, 3)]
                graduated_fem_groups += [round(females[group].values[0] / 5, 3)]
            else:
                graduated_groups += [round(population[group].values[0] / 5, 3)] * 5
                graduated_fem_groups += [round(females[group].values[0] / 5, 3)] * 5

        prev_population = graduated_groups
        prev_females = graduated_fem_groups

        cols = [str(i) for i in range(len(graduated_groups))]
        predicted_df = pd.DataFrame.from_records([[INITIAL_YEAR] + graduated_groups], columns=['date'] + cols)

        for year in range(INITIAL_YEAR + 1, INITIAL_YEAR + num_years):
            next_population = [0] * len(graduated_groups)
            next_females = [0] * len(graduated_fem_groups)
            for group_idx in range(0, len(graduated_groups)):
                if group_idx == 0:
                    # calculate amount of new babies
                    next_population[group_idx] = fertility * sum(prev_females[19:39]) / 5.0 / 4.0
                    next_females[group_idx] = self.female_babies_rate * next_population[group_idx]
                else:
                    next_population[group_idx] = \
                        prev_population[group_idx - 1] * surv_coeffs[group_idx - 1]
                    next_females[group_idx] = \
                        prev_females[group_idx - 1] * fem_surv_coeffs[group_idx - 1]

            new_row = pd.DataFrame.from_records([[year] + next_population], columns=['date'] + cols)
            predicted_df = predicted_df.append(new_row)
            prev_population = next_population
            prev_females = next_females

        return self.group_by_default_age_groups(predicted_df)

    def pred_model_1_year(self, num_years, type='both'):
        fertility = self.fertility_rate_1_year(INITIAL_YEAR, type)

        return self.pred_model_1_year_with_fertility(num_years, fertility, type)

    def pred_model_with_total_fertility(self, num_years, type='both'):
        females = self.pred_dict['female'].copy()
        females = females.query('date == @INITIAL_YEAR')[self.age_groups]
        s = 0.0
        for group in self.fem_fert_groups:
            fem_amount = females[group]
            s += 361.271 / fem_amount
        fertility = s * 5
        return self.pred_model_1_year_with_fertility(num_years, fertility.item(), type)

    def group_by_default_age_groups(self, df):
        grouped_df = pd.DataFrame(columns=['date'] + self.age_groups)

        ages = [str(i) for i in range(101)]
        # TODO: improve this somehow
        for _, row in df.iterrows():
            sums = []
            len_of_group = 0
            sum_of_group = 0.0
            for age in ages:
                if age == '100':
                    sums.append(sum_of_group)
                    sums.append(row[age])
                else:
                    len_of_group += 1
                    if len_of_group <= 5:
                        sum_of_group += row[age]
                    else:
                        sums.append(sum_of_group)
                        len_of_group = 1
                        sum_of_group = row[age]
            new_row = pd.DataFrame.from_records([[row['date']] + sums], columns=['date'] + self.age_groups)
            grouped_df = grouped_df.append(new_row)
        return grouped_df

    def total_population(self, data, year):
        data = data.query('date == @year')
        total = 0
        for group in self.age_groups:
            total += data[group].values
        return list(total)

    def surv_coeffs_from_data(self, secret_num=1):
        coeffs = list()
        for year in range(INITIAL_GIVEN_YEAR + 5, FINAL_GIVEN_YEAR + 1, 5):
            coeffs.append(self.calculate_survival_coeffs_1_year(self.pred_dict['both'].copy(), year - 5, year,
                                                                secret_num=secret_num))
        return coeffs

    def babies_fraction_from_data(self):
        male_proc = []
        fem_proc = []
        for year in range(INITIAL_GIVEN_YEAR, FINAL_GIVEN_YEAR + 1, 5):
            male_proc.append(self.pred_dict['male'].query('date == @year')["0-4"].values[0] / \
                             self.pred_dict['both'].query('date == @year')["0-4"].values[0])
            fem_proc.append(1 - male_proc[-1])
        return male_proc

    def fertility_full(self):
        fert = list()
        for year in range(INITIAL_GIVEN_YEAR, FINAL_GIVEN_YEAR + 1, 5):
            fert.append(self.fertility_from_data(year))

        return fert

    def fertility_from_data(self, year):
        all_fems = sum(self.pred_dict['female'].query('date == @year')[self.fem_fert_groups].values[0])
        next_year = year + 5
        babies = self.pred_dict['both'].query('date == @next_year')["0-4"].values[0]

        return babies * 4.0 / all_fems

    def get_params_variability(self):
        fertility = {}
        ratio = {}
        coeffs = self.surv_coeffs_from_data(secret_num=5)
        x1 = []
        x14 = []
        x18 = []
        x28 = []
        x41 = []
        for i in coeffs:
            x1.append(i[0])
            x14.append(i[13])
            x18.append(i[17])
            x28.append(i[27])
            x41.append(i[40])

        x1 = {"min": min(x1), "max": max(x1)}
        x14 = {"min": min(x14), "max": max(x14)}
        x18 = {"min": min(x18), "max": max(x18)}
        x28 = {"min": min(x28), "max": max(x28)}
        x41 = {"min": min(x41), "max": max(x41)}

        fertility["min"] = min(self.fertility_full())
        fertility["max"] = max(self.fertility_full())
        ratio["min"] = min(self.babies_fraction_from_data())
        ratio["max"] = max(self.babies_fraction_from_data())

        return fertility, ratio, x1, x14, x18, x28, x41
