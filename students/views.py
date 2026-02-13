from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Student, Course, Result, AdditionalFactors
from .serializers import (
    StudentSerializer, CourseSerializer, ResultSerializer,
    AdditionalFactorsSerializer, CSVUploadSerializer
)
from .services import CSVImportService

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def upload_csv(self, request):
        serializer = CSVUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            semester = serializer.validated_data['semester']
            
            result = CSVImportService.process_results_csv(file, semester)
            
            if result['success']:
                return Response(result, status=status.HTTP_201_CREATED)
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def gpa(self, request, pk=None):
        student = self.get_object()
        return Response({
            'student_id': student.student_id,
            'current_gpa': student.calculate_gpa(),
            'first_semester_gpa': student.calculate_gpa(semester='First')
        })

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        student_id = self.request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(student__student_id=student_id)
        return queryset

class AdditionalFactorsViewSet(viewsets.ModelViewSet):
    queryset = AdditionalFactors.objects.all()
    serializer_class = AdditionalFactorsSerializer
    permission_classes = [IsAuthenticated]
