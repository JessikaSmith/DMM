import numpy as np
import pandas as pd

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

        # TODO: remove hardcode
        self.male_babies_rate = 0.52
        self.female_babies_rate = 0.48

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

    def calculate_survival_coeffs_1_year(self, data, initial_year, final_year):

        coeffs = []
        for group_idx in range(0, len(self.age_groups) - 1):
            coeff = self.surv_coeff(data, self.age_groups[group_idx], self.age_groups[group_idx + 1],
                                    initial_year, final_year)
            coeffs += [np.power(coeff, 1 / 5)] * 5
        return coeffs

    def get_value_prediction(self, data, group, counter):

        idx = self.fem_data.columns.get_loc(group)
        return data.iloc[counter, idx] * self.coeffs[idx - 8]

    def pred_model_1_year_with_fertility(self, num_years, fertility, type='both'):
        selected = self.pred_dict[type].copy()
        females = self.pred_dict['female'].copy()
        surv_coeffs = self.calculate_survival_coeffs_1_year(selected, INITIAL_YEAR - 5, INITIAL_YEAR)
        fem_surv_coeffs = self.calculate_survival_coeffs_1_year(females, INITIAL_YEAR - 5, INITIAL_YEAR)

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
                    next_females[group_idx] = fertility * self.female_babies_rate * sum(prev_females[19:39]) / 5.0 / 4.0

                else:
                    next_population[group_idx] = \
                        prev_population[group_idx - 1] * surv_coeffs[group_idx - 1]
                    next_females[group_idx] = \
                        prev_females[group_idx - 1] * fem_surv_coeffs[group_idx - 1]

            new_row = pd.DataFrame.from_records([[year] + next_population], columns=['date'] + cols)
            predicted_df = predicted_df.append(new_row)
            prev_population = next_population

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
        print(df)
        grouped_df = pd.DataFrame(columns=['date'] + self.age_groups)

        ages = [str(i) for i in range(101)]
        # TODO: improve this somehow
        for _, row in df.iterrows():
            sums = []
            len_of_group = 0
            sum_of_group = 0.0
            for age in ages:
                if age == '100':
                    sums.append(row[age])
                else:
                    len_of_group += 1
                    if len_of_group <= 5:
                        sum_of_group += row[age]
                    else:
                        sums.append(sum_of_group)
                        len_of_group = 0
                        sum_of_group = 0.0
            print(sums)
            new_row = pd.DataFrame.from_records([[row['date']] + sums], columns=['date'] + self.age_groups)
            grouped_df = grouped_df.append(new_row)
        return grouped_df

    def total_population(self, data, year):
        data = data.query('date == @year')
        print(data)
        total = 0
        for group in self.age_groups:
            total += data[group]

        return total
