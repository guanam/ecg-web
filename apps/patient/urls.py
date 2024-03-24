from django.urls import path
from . import views
from django.urls import path
from .views import run_prediction_view, generate_ecg_plot

urlpatterns = [
    path('predict/<int:patient_id>/', run_prediction_view, name='patient_predict'),
    path('ecg-plot/<int:patient_id>/', generate_ecg_plot, name='generate_ecg_plot'),
]

from rest_framework.routers import SimpleRouter,DefaultRouter

router = DefaultRouter()
urlpatterns += router.urls