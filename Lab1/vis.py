from plotly.plotly import image
from plotly.offline import download_plotlyjs, plot
import plotly.graph_objs as go
import numpy as np

path_to_figure = 'Figures\\'

group = ['0-4', '5-9', '10-14', '15-19', '20-24',
         '25-29', '30-34', '35-39', '40-44', '45-49',
         '50-54', '55-59', '60-64', '65-69', '70-74', '75-79',
         '80-84', '85-89', '90-94', '95-99', '100']


def show_profile(data, year, type, title):

    y = [y*1000 for y in data[data['date'] == year][group].values.tolist()[0]]
    trace = go.Scatter(
        x=group,
        y=y,
        mode='lines+markers',
        name='title',
        line=dict(
            color=('rgb(205, 12, 24)')
        )
    )
    layout = dict(title='Demographic profile prediction for Russia in '+str(year) + ' (' + type + ')',
                  xaxis=dict(title='Age group'),
                  yaxis=dict(title='Amount of people'),
                  )
    data = [trace]
    fig = go.Figure(data=data, layout=layout)
    image.save_as(fig, filename=path_to_figure + title+'.jpeg')


def profile_compare_years(data, years, type, title):

    traces = []
    for year in years:
        y = [y * 1000 for y in data[data['date'] == year][group].values.tolist()[0]]
        traces += [go.Scatter(
            x=group,
            y=y,
            mode='lines+markers',
            name=year)]
    years = [str(year) for year in years]
    layout = dict(title='Demographic profile prediction for Russia in ' + ', '.join(years) + ' (' + type + ')',
                  xaxis=dict(title='Age group'),
                  yaxis=dict(title='Amount of people'),
                  )
    fig = go.Figure(data=traces, layout=layout)
    image.save_as(fig, filename=path_to_figure + title + '.jpeg')


def profiles_m_f(fem_data, male_data, year, title):

    y = [y * 1000 for y in fem_data[fem_data['date'] == year][group].values.tolist()[0]]
    trace1 = go.Scatter(
        x=group,
        y=y,
        mode='lines+markers',
        name='female')
    y = [y * 1000 for y in male_data[male_data['date'] == year][group].values.tolist()[0]]
    trace2 = go.Scatter(
        x=group,
        y=y,
        mode='lines+markers',
        name='male')
    layout = dict(title='Demographic profile prediction for Russia in ' + str(year),
                  xaxis=dict(title='Age group'),
                  yaxis=dict(title='Amount of people'),
                  )
    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)
    image.save_as(fig, filename=path_to_figure + title + '.jpeg')