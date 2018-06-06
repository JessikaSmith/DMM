import numpy as np
from SALib.analyze import sobol
from SALib.sample.saltelli import sample

from Lab1.prediction_model import PredictionModel

INITIAL_YEAR = 2005


def sensitivity():
    model = init_model()
    problem = {
        'num_vars':7,
        'names': ['fertility', 'babies_fraction', 'x1', 'x14', 'x18', 'x28', 'x41'],
        'bounds': [[1, 3],
                   [0.4, 0.6],
                   [0.1, 1],
                   [0.1, 1],
                   [0.1, 1],
                   [0.1, 1],
                   [0.1, 1]]
    }

    params = sample(problem, 10)
    years = [2015, 2025, 2055, 2070, 2105]

    for year in years:
        print("YEAR: ", year)
        population = eval(model, params, year)
        population = population.flatten()
        si = sobol.analyze(problem, population, print_to_console=False)
        print(si['S1'])


def init_model():
    name = '../Lab1/age_data.xls'
    fem_sheet = 'f; 1950-2005, estimates'
    male_sheet = 'm; 1950-2005, estimates'
    both_sheet = 'both; 1950-2005, estimates'
    model = PredictionModel(name, fem_sheet, male_sheet, both_sheet)

    return model


# several years at the same time
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


sensitivity()
