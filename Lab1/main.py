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

type = 'female'
prediction = model.pred_model_5_years(100, type)
vis.show_profile(prediction, 2050, type, '2050 profile for females')
vis.profile_compare_years(prediction, [2010, 2020, 2030], type, 'prediction for 2010 2020 2030 females')

prediction = model.pred_model_1_year(5)
print_available_years(prediction)