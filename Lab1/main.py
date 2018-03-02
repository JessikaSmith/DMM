import pandas as pd
import numpy as np
from prediction_model import PredictionModel
import vis

name = 'age_data.xls'
fem_sheet = 'f; 1950-2005, estimates'
male_sheet = 'm; 1950-2005, estimates'
both_sheet = 'both; 1950-2005, estimates'

model = PredictionModel(name, fem_sheet, male_sheet, both_sheet)


def print_available_years(data):

    print(", ".join([str(i) for i in data["date"].tolist()]))

    return

prediction = model.pred_model_5_years(5)
#print(prediction)
print_available_years(prediction)
group = ['0-4', '5-9', '10-14', '15-19', '20-24',
         '25-29', '30-34', '35-39', '40-44', '45-49',
         '50-54', '55-59', '60-64', '65-69', '70-74', '75-79',
         '80-84', '85-89', '90-94', '95-99', '100']

vis.show_profile(prediction, 2010, '2010 profile')

prediction = model.pred_model_1_year(5)
#print(prediction)
print_available_years(prediction)