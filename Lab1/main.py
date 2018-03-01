import pandas as pd
import numpy as np
from prediction_model import PredictionModel

name = 'age_data.xls'
fem_sheet = 'f; 1950-2005, estimates'
male_sheet = 'm; 1950-2005, estimates'
both_sheet = 'both; 1950-2005, estimates'

model = PredictionModel(name, fem_sheet, male_sheet, both_sheet)

def print_available_years():
    return True

prediction = model.pred_model_5_years(5)
print(prediction)

prediction = model.pred_model_1_year(5)
print(prediction)
