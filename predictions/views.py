from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Prediction, Intervention
from .serializers import (
    PredictionSerializer, InterventionSerializer, PredictionRequestSerializer
)
from .engine import PredictionEngine
from .reports import PredictionReportGenerator

class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        student_id = self.request.query_params.get('student_id')
        risk_level = self.request.query_params.get('risk_level')
        
        if student_id:
            queryset = queryset.filter(student__student_id=student_id)
        if risk_level:
            queryset = queryset.filter(risk_level=risk_level)
        
        return queryset
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate new prediction for a student"""
        serializer = PredictionRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                prediction = PredictionEngine.predict_cgpa(
                    serializer.validated_data['student_id'],
                    serializer.validated_data.get('semester', 'Current')
                )
                return Response(
                    PredictionSerializer(prediction).data,
                    status=status.HTTP_201_CREATED
                )
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get prediction statistics"""
        stats = PredictionEngine.get_prediction_statistics()
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def at_risk(self, request):
        """Get all at-risk students"""
        at_risk = Prediction.objects.filter(risk_level='at_risk').order_by('-predicted_at')
        return Response(PredictionSerializer(at_risk, many=True).data)

class InterventionViewSet(viewsets.ModelViewSet):
    queryset = Intervention.objects.all()
    serializer_class = InterventionSerializer
    permission_classes = [IsAuthenticated]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_report(request, pk):
    """Generate PDF report for a prediction"""
    try:
        prediction = Prediction.objects.get(pk=pk)
        pdf_path = PredictionReportGenerator.generate_report(prediction)
        
        return Response({
            'message': 'Report generated successfully',
            'file_path': pdf_path
        })
    except Prediction.DoesNotExist:
        return Response({'error': 'Prediction not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
