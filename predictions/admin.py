from django.contrib import admin
from .models import Prediction, Intervention

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['student', 'predicted_cgpa', 'risk_level', 'confidence_score', 'predicted_at']
    list_filter = ['risk_level', 'predicted_at']
    search_fields = ['student__student_id', 'student__first_name', 'student__last_name']
    readonly_fields = ['predicted_at']

@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ['prediction', 'intervention_type', 'priority', 'status']
    list_filter = ['intervention_type', 'priority', 'status']
