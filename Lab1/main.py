import vis
from prediction_model import PredictionModel

name = 'age_data.xls'
fem_sheet = 'f; 1950-2005, estimates'
male_sheet = 'm; 1950-2005, estimates'
both_sheet = 'both; 1950-2005, estimates'

model = PredictionModel(name, fem_sheet, male_sheet, both_sheet)


def print_available_years(data):
    print(", ".join([str(i) for i in data["date"].tolist()]))
    return


def get_population(years, fertility, type):
    test = model.pred_model_1_year_with_fertility(years, fertility, type)
    population = []
    for i in range(2005, 2005 + years + 1):
        population.append(list(model.total_population(test, i)))
    return ([fertility, population])


def main():
    type = 'both'
    for i in range(130, 201):
        print(get_population(100, i / 100, type))
        # print("")
    # vis.show_profile(prediction, 2018, type, '1 year model 2018 profile for '+type)
    # print(prediction[prediction['date'] == 2050])
    # given = model.extract_given_prediction(type)
    # vis.compare_profiles(test, given, 2045, 'prediction_comp_2045 (fert = 1.37)')


if __name__ == '__main__':
    main()
