from plotly.plotly import image
from plotly.offline import download_plotlyjs, plot
import plotly.graph_objs as go
import numpy as np

path_to_figure = 'Figures\\'

group = ['0-4', '5-9', '10-14', '15-19', '20-24',
         '25-29', '30-34', '35-39', '40-44', '45-49',
         '50-54', '55-59', '60-64', '65-69', '70-74', '75-79',
         '80-84', '85-89', '90-94', '95-99', '100']


def profiles_m_f(fem_data, male_data, year, title):


    return True


def show_profile(data, year, title):

    y = [y*1000 for y in data[data['date'] == year][group].values.tolist()[0]]
    trace = go.Scatter(
        x=group,
        y=y,
        mode='lines+markers',
        name='title',
        line=dict(
            color=('rgb(205, 12, 24)'))
    )
    layout = dict(title='Demographic profile prediction for Russia in '+str(year),
                  xaxis=dict(title='Group'),
                  yaxis=dict(title='Amount of people'),
                  )
    data = [trace]
    fig = go.Figure(data=data, layout=layout)
    image.save_as(fig, filename=path_to_figure + title+'.jpeg')