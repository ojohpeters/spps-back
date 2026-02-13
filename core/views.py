from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from students.models import Student, Result
from predictions.models import Prediction

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get overall dashboard statistics"""
    
    total_students = Student.objects.count()
    total_predictions = Prediction.objects.count()
    at_risk_count = Prediction.objects.filter(risk_level='at_risk').count()
    high_achievers = Prediction.objects.filter(risk_level='high_achiever').count()
    
    recent_predictions = Prediction.objects.order_by('-predicted_at')[:5]
    
    return Response({
        'total_students': total_students,
        'total_predictions': total_predictions,
        'at_risk_students': at_risk_count,
        'high_achievers': high_achievers,
        'recent_predictions': [{
            'id': p.id,
            'student_id': p.student.student_id,
            'student_name': f"{p.student.first_name} {p.student.last_name}",
            'predicted_cgpa': p.predicted_cgpa,
            'risk_level': p.risk_level,
            'predicted_at': p.predicted_at
        } for p in recent_predictions]
    })
