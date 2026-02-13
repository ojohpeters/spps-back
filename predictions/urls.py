from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'predictions', views.PredictionViewSet)
router.register(r'interventions', views.InterventionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('predictions/<int:pk>/report/', views.generate_report, name='generate_report'),
]
