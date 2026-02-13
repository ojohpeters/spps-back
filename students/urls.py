from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'results', views.ResultViewSet)
router.register(r'factors', views.AdditionalFactorsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
