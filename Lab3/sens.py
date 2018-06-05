import numpy as np
from SALib.sample.saltelli import sample

from Lab1.prediction_model import PredictionModel


def model(x1, x2, x3):
    return x1 + x2 + x3


def eval(param_values):
    predictions = list()
    name = '../Lab1/age_data.xls'
    fem_sheet = 'f; 1950-2005, estimates'
    male_sheet = 'm; 1950-2005, estimates'
    both_sheet = 'both; 1950-2005, estimates'
    for params in param_values:
        print(params)
        fertility, babies_fraction = params
        model = PredictionModel(name, fem_sheet, male_sheet, both_sheet, babies_fraction)
        predicted = model.pred_model_1_year_with_fertility(101, fertility)
        # years = [2015, 2025, 2055, 2070, 2105]
        # population = list()
        # for year in years:
        #     population.append(model.total_population(predicted, year))
        predictions.append(model.total_population(predicted, 2025))
    return np.array(predictions)


problem = {
    'num_vars': 2,
    'names': ['fertility', 'babies_fraction'],
    'bounds': [[1, 3],
               [0.05, 1]]
}

# param_values = sample(problem, 1000)
# y = eval(param_values)
#
# si = sobol.analyze(problem, y, print_to_console=True)


samples = sample(problem, 2)
total = eval(samples)
print(total)
