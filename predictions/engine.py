from students.models import Student, AdditionalFactors
from .models import Prediction, Intervention

class PredictionEngine:
    """
    Simulated ML prediction engine using weighted statistical scoring
    This approach provides interpretable predictions without requiring model training
    """
    
    # Prediction weights (must sum to 100%)
    WEIGHTS = {
        'first_semester_gpa': 0.40,    # 40% - Strongest predictor
        'attendance': 0.15,             # 15% - Regular attendance is key
        'assignments': 0.15,            # 15% - Consistent work ethic
        'study_hours': 0.10,            # 10% - Time investment
        'admission_score': 0.10,        # 10% - Initial capability
        'socioeconomic': 0.10,          # 10% - Support system
    }
    
    @classmethod
    def normalize_score(cls, value, min_val, max_val):
        """Convert any score to 0-100 scale"""
        if max_val == min_val:
            return 50
        return ((value - min_val) / (max_val - min_val)) * 100
    
    @classmethod
    def calculate_socioeconomic_score(cls, status):
        """Convert categorical socioeconomic status to numeric score"""
        mapping = {'low': 30, 'medium': 65, 'high': 90}
        return mapping.get(status, 50)
    
    @classmethod
    def predict_cgpa(cls, student_id, semester='Current'):
        """
        Generate prediction for a student using weighted scoring approach
        """
        try:
            student = Student.objects.get(student_id=student_id)
            factors = student.factors
            
            # Extract and normalize input factors
            first_sem_gpa = student.calculate_gpa(semester='First')
            gpa_score = cls.normalize_score(first_sem_gpa, 0, 5.0)  # Already 0-100
            
            attendance_score = factors.attendance_percentage
            assignment_score = factors.assignment_average
            study_score = cls.normalize_score(factors.study_hours_per_week, 0, 40)
            admission_score = cls.normalize_score(student.admission_score, 100, 400)
            socio_score = cls.calculate_socioeconomic_score(factors.socioeconomic_status)
            
            # Calculate weighted composite score
            composite_score = (
                gpa_score * cls.WEIGHTS['first_semester_gpa'] +
                attendance_score * cls.WEIGHTS['attendance'] +
                assignment_score * cls.WEIGHTS['assignments'] +
                study_score * cls.WEIGHTS['study_hours'] +
                admission_score * cls.WEIGHTS['admission_score'] +
                socio_score * cls.WEIGHTS['socioeconomic']
            )
            
            # Convert composite score back to CGPA scale (0-5)
            predicted_cgpa = (composite_score / 100) * 5.0
            predicted_cgpa = round(predicted_cgpa, 2)
            
            # Determine risk level and confidence
            risk_level, confidence = cls.classify_risk(predicted_cgpa, composite_score)
            
            # Create prediction record
            prediction = Prediction.objects.create(
                student=student,
                predicted_cgpa=predicted_cgpa,
                risk_level=risk_level,
                confidence_score=confidence,
                first_semester_gpa=first_sem_gpa,
                attendance_percentage=factors.attendance_percentage,
                assignment_average=factors.assignment_average,
                study_hours=factors.study_hours_per_week,
                admission_score=student.admission_score,
                socioeconomic_score=socio_score,
                semester=semester
            )
            
            # Generate interventions for at-risk students
            if risk_level == 'at_risk':
                cls.generate_interventions(prediction, factors)
            
            return prediction
            
        except Student.DoesNotExist:
            raise ValueError(f"Student {student_id} not found")
        except Exception as e:
            raise ValueError(f"Prediction failed: {str(e)}")
    
    @classmethod
    def classify_risk(cls, predicted_cgpa, composite_score):
        """
        Classify student into risk categories based on predicted performance
        Returns: (risk_level, confidence_score)
        """
        if predicted_cgpa >= 3.5:
            return 'high_achiever', round(composite_score, 2)
        elif predicted_cgpa >= 2.5:
            return 'average', round(composite_score, 2)
        else:
            return 'at_risk', round(composite_score, 2)
    
    @classmethod
    def generate_interventions(cls, prediction, factors):
        """Generate recommended interventions for at-risk students"""
        interventions = []
        
        if factors.attendance_percentage < 75:
            interventions.append({
                'type': 'academic_counseling',
                'description': 'Address attendance issues and identify barriers to regular class participation',
                'priority': 'high'
            })
        
        if factors.assignment_average < 60:
            interventions.append({
                'type': 'tutoring',
                'description': 'Provide subject-specific tutoring to improve assignment performance',
                'priority': 'high'
            })
        
        if factors.study_hours_per_week < 10:
            interventions.append({
                'type': 'study_skills',
                'description': 'Enroll in time management and study skills workshop',
                'priority': 'medium'
            })
        
        if factors.socioeconomic_status == 'low':
            interventions.append({
                'type': 'financial_aid',
                'description': 'Connect with financial aid office for support resources',
                'priority': 'medium'
            })
        
        interventions.append({
            'type': 'mentorship',
            'description': 'Assign peer mentor for academic and social support',
            'priority': 'medium'
        })
        
        for intervention_data in interventions:
            Intervention.objects.create(
                prediction=prediction,
                intervention_type=intervention_data['type'],
                description=intervention_data['description'],
                priority=intervention_data['priority']
            )
    
    @classmethod
    def get_prediction_statistics(cls):
        """Generate summary statistics across all predictions"""
        predictions = Prediction.objects.all()
        
        total = predictions.count()
        if total == 0:
            return {
                'total_predictions': 0,
                'average_predicted_cgpa': 0,
                'risk_distribution': {}
            }
        
        risk_counts = {
            'high_achiever': predictions.filter(risk_level='high_achiever').count(),
            'average': predictions.filter(risk_level='average').count(),
            'at_risk': predictions.filter(risk_level='at_risk').count(),
        }
        
        avg_cgpa = sum(p.predicted_cgpa for p in predictions) / total
        
        return {
            'total_predictions': total,
            'average_predicted_cgpa': round(avg_cgpa, 2),
            'risk_distribution': risk_counts,
            'risk_percentages': {
                key: round((count / total) * 100, 1)
                for key, count in risk_counts.items()
            }
        }
