import plotly.graph_objs as go
from plotly.offline import plot
from plotly.plotly import image

path_to_figure = 'Figures\\'


def coeff_visualization(data, years):
    year_categories = [i for i in range(len(data[0]))]
    trace = []
    for i in range(len(data)):
        trace += [go.Scatter(
            x=year_categories,
            y=data[i],
            name=years[i],
            mode='lines+markers'
        )]
    layout = dict(title='Checking validity of coeffs',
                  xaxis=dict(title='Transition to age group'),
                  yaxis=dict(title='Value'),
                  )
    fig = go.Figure(data=trace, layout=layout)
    image.save_as(fig, filename=path_to_figure + 'check_coeffs.jpeg')


def sensitivity_analysis(si, names, year, num=0):
    trace1 = go.Bar(
        x=names[num:],
        y=si["S1"][num:],
        name='S1',
        error_y=dict(
            type='data',
            array=si['S1_conf'][num:],
            visible=True
        )

    )
    trace2 = go.Bar(
        x=names[num:],
        y=si['ST'][num:],
        name='Total',
        error_y=dict(
            type='data',
            array=si['ST_conf'][num:],
            visible=True
        )
    )
    data = [trace1, trace2]
    layout = go.Layout(
        barmode='group',
        title=''.join(['Sensitivity analysis for ', str(year)])
    )
    if num:
        title = '_groups_coeffs_'
    else:
        title = '_full_coeffs_'
    fig = go.Figure(data=data, layout=layout)
    image.save_as(fig, filename=''.join([path_to_figure, title, str(year), '.jpeg']))


# list with max and min values
#
def uncertainty_plot(min_population, max_population, average_population, simulated_years):
    trace1 = go.Scatter(
        y=min_population,
        x=simulated_years,
        mode='lines',
        line=dict(
            color=('rgb(205, 12, 24)')
        )
    )
    trace2 = go.Scatter(
        y=max_population,
        x=simulated_years,
        mode='lines',
        line=dict(
            color=('rgb(205, 12, 24)')
        )
    )
    trace3 = go.Scatter(
        y=average_population,
        x=simulated_years,
        mode='lines'
    )
    layout = go.Layout(
        title='Uncertainty analysis',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Population'),
    )
    data = [trace1, trace2, trace3]
    fig = go.Figure(data=data, layout=layout)
    image.save_as(fig, filename=''.join([path_to_figure, 'uncertanty', '.jpeg']))
