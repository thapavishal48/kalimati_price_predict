 
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('data/', views.kalimati_data),
    path('select/', views.select_veg),
    path('graph/', views.pickle_training_testing),
    path('team/', views.team),
    path('trend/', views.time_series_trend),
    path('seasonality/', views.time_series_seasonal),
    path('residual/', views.time_series_residual),
    path('observed/', views.time_series_observed)
]