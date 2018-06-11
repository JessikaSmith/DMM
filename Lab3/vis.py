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


def sensitivity_analysis(si, names, year):
    trace1 = go.Bar(
        x=names,
        y=si["S1"],
        name='S1',
        error_y=dict(
            type='data',
            array=si['S1_conf'],
            visible=True
        )

    )
    trace2 = go.Bar(
        x=names,
        y=si['ST'],
        name='Total',
        error_y=dict(
            type='data',
            array=si['ST_conf'],
            visible=True
        )
    )
    data = [trace1,trace2]
    layout = go.Layout(
        barmode='group',
        title=''.join(['Sensitivity analysis for ',str(year)])
    )
    fig = go.Figure(data=data, layout=layout)
    image.save_as(fig, filename=''.join([path_to_figure,'sensitivity',str(year),'.jpeg']))
