from django.shortcuts import render
from .code.data_preprocessing import DataPreprocessing
from .code.pickle_train_test import TrainingTesting
from django.shortcuts import render
from django.http import HttpResponseRedirect
import plotly.graph_objects as go
import plotly.express as px
import statsmodels.api as sm


# import numpy as np
# from django.http import HttpResponse
# Create your views here.


def index(request):
    return render(request, "index.html")


def kalimati_data(request):
    return render(request, "data_show.html")


def select_veg(request):
    return render(request, "select_veg.html")

from jinja2 import Template, Environment, FileSystemLoader
from plotly.offline import plot
from plotly.graph_objs import Scatter

def pickle_training_testing(request):

    veg_name = request.POST['vegetableSelect']
    data_processing = DataPreprocessing("./home/data/kalimati_price_list.csv")
    data_train_test = TrainingTesting(data_processing)


    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data_train_test.df1[(data_train_test.df1.Items == veg_name)].index,
        y=data_train_test.df1[(data_train_test.df1.Items == veg_name)]['Real Price'],
        name='Real Price',
        mode='markers',
        marker_color='rgba(152, 0, 0, .8)'
    ))
    fig.add_trace(go.Scatter(
        x=data_train_test.df1[(data_train_test.df1.Items == veg_name)].index,
        y=data_train_test.df1[(data_train_test.df1.Items == veg_name)]['Estimated Price'],
        name='Estimated Price',
        marker_color='rgba(255, 182, 193, .9)'
    ))
    # Set options common to all traces with fig.update_traces
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=10)
    fig.update_layout(title=veg_name,
                      yaxis_zeroline=False, xaxis_zeroline=False)

    fig.write_html('./graph_show/veg_graph.html', auto_open=True)

    return HttpResponseRedirect('/select/')


def team(request):
    return render(request, "team.html")


def time_series_trend(request):
    data_processing = DataPreprocessing("./home/data/kalimati_price_list.csv")

    y = data_processing.data1['Average'].resample('W').mean()
    decomposition = sm.tsa.seasonal_decompose(y, model='additive')
    trend = decomposition.trend
    fig = px.line(trend)
    fig.show()
    return HttpResponseRedirect('/')


def time_series_seasonal(request):
    data_processing = DataPreprocessing("./home/data/kalimati_price_list.csv")

    y = data_processing.data1['Average'].resample('W').mean()
    decomposition = sm.tsa.seasonal_decompose(y, model='additive')

    seasonal = decomposition.seasonal
    fig = px.line(seasonal)
    fig.show()
    return HttpResponseRedirect('/')


def time_series_residual(request):
    data_processing = DataPreprocessing("./home/data/kalimati_price_list.csv")

    y = data_processing.data1['Average'].resample('W').mean()
    decomposition = sm.tsa.seasonal_decompose(y, model='additive')

    residual = decomposition.resid
    fig = px.line(residual)
    fig.show()
    return HttpResponseRedirect('/')


def time_series_observed(request):
    data_processing = DataPreprocessing("./home/data/kalimati_price_list.csv")
    y = data_processing.data1['Average'].resample('W').mean()
    decomposition = sm.tsa.seasonal_decompose(y, model='additive')

    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid
    observed = trend + seasonal + residual

    fig = px.line(observed)
    fig.show()
    return HttpResponseRedirect('/')