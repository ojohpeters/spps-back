from rest_framework import serializers
from .models import Student, Course, Result, AdditionalFactors

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    course_details = CourseSerializer(source='course', read_only=True)
    
    class Meta:
        model = Result
        fields = '__all__'
        read_only_fields = ['grade', 'quality_points']

class AdditionalFactorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalFactors
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    current_gpa = serializers.SerializerMethodField()
    first_semester_gpa = serializers.SerializerMethodField()
    results = ResultSerializer(many=True, read_only=True)
    factors = AdditionalFactorsSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'
    
    def get_current_gpa(self, obj):
        return obj.calculate_gpa()
    
    def get_first_semester_gpa(self, obj):
        return obj.calculate_gpa(semester='First')

class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    semester = serializers.CharField(max_length=20)
