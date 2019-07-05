from django.urls import path
from .views import MetricsView

app_name = 'metrics'

urlpatterns = [
    path('metrics/', MetricsView.as_view()),
]