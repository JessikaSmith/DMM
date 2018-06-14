import numpy as np
from SALib.analyze import sobol
from SALib.sample.saltelli import sample

from Lab3 import vis
from Lab1.prediction_model import PredictionModel

INITIAL_YEAR = 2005
name = '../Lab1/age_data.xls'
fem_sheet = 'f; 1950-2005, estimates'
male_sheet = 'm; 1950-2005, estimates'
both_sheet = 'both; 1950-2005, estimates'


def sensitivity(fertility, ratio, x1, x14, x18, x28, x41):
    model = init_model()
    problem = {
        'num_vars': 7,
        'names': ['fertility', 'babies_fraction', 'x1', 'x14', 'x18', 'x28', 'x41'],
        'bounds': [[fertility["min"], fertility["max"]],
                   [ratio['min'], ratio['max']],
                   [x1['min'], x1['max']],
                   [x14['min'], x14['max']],
                   [x18['min'], x18['max']],
                   [x28['min'], x28['max']],
                   [x41['min'], x41['max']]]
    }

    print(problem['bounds'])

    params = sample(problem, 50)
    years = [2015, 2025, 2055, 2070, 2105]

    for year in years:
        print("YEAR: ", year)
        population = eval(model, params, year)
        population = population.flatten()
        si = sobol.analyze(problem, population, print_to_console=False)
        vis.sensitivity_analysis(si, problem['names'], year)


def init_model():
    model = PredictionModel(name, fem_sheet, male_sheet, both_sheet)
    return model


def eval(model, param_values, year):
    predict_pop = list()
    for params in param_values:
        # print("params: ", params)
        fertility, babies_fraction, x1, x14, x18, x28, x41 = params
        predicted = model.pred_model_1_year_with_fertility(year - INITIAL_YEAR + 1, fertility,
                                                           babies_fraction=babies_fraction,
                                                           x1=x1, x14=x14, x18=x18, x28=x28, x41=x41)
        total_pop = model.total_population(predicted, year)
        # print("predicted total population:", total_pop)
        predict_pop.append(total_pop)

    return np.array(predict_pop)


# sensitivity()
model = PredictionModel(name, fem_sheet, male_sheet, both_sheet)
fertility, ratio, x1, x14, x18, x28, x41 = model.get_params_variability()
sensitivity(fertility, ratio, x1, x14, x18, x28, x41)
# years = [i for i in range(1950, 1950 + (len(coeffs) * 5) - 1, 5)]
# vis.coeff_visualization(coeffs, years)
# model.get_params_variability()
