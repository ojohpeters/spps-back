from rest_framework import serializers
from .models import Prediction, Intervention
from students.serializers import StudentSerializer

class InterventionSerializer(serializers.ModelSerializer):
    intervention_type_display = serializers.CharField(source='get_intervention_type_display', read_only=True)
    
    class Meta:
        model = Intervention
        fields = '__all__'

class PredictionSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(source='student', read_only=True)
    interventions = InterventionSerializer(many=True, read_only=True)
    risk_level_display = serializers.CharField(source='get_risk_level_display', read_only=True)
    
    class Meta:
        model = Prediction
        fields = '__all__'

class PredictionRequestSerializer(serializers.Serializer):
    student_id = serializers.CharField()
    semester = serializers.CharField(default='Current')
