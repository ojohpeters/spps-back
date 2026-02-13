from django.db import models
from students.models import Student

class Prediction(models.Model):
    RISK_LEVELS = [
        ('high_achiever', 'High Achiever'),
        ('average', 'Average'),
        ('at_risk', 'At Risk'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='predictions')
    predicted_cgpa = models.FloatField()
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS)
    confidence_score = models.FloatField()
    
    # Input factors used for prediction
    first_semester_gpa = models.FloatField()
    attendance_percentage = models.FloatField()
    assignment_average = models.FloatField()
    study_hours = models.FloatField()
    admission_score = models.FloatField()
    socioeconomic_score = models.FloatField()
    
    # Metadata
    predicted_at = models.DateTimeField(auto_now_add=True)
    semester = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'predictions'
        ordering = ['-predicted_at']
    
    def __str__(self):
        return f"{self.student.student_id} - {self.predicted_cgpa} ({self.risk_level})"

class Intervention(models.Model):
    INTERVENTION_TYPES = [
        ('academic_counseling', 'Academic Counseling'),
        ('tutoring', 'Tutoring Support'),
        ('study_skills', 'Study Skills Workshop'),
        ('mentorship', 'Peer Mentorship'),
        ('financial_aid', 'Financial Aid Support'),
    ]
    
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE, related_name='interventions')
    intervention_type = models.CharField(max_length=50, choices=INTERVENTION_TYPES)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=[
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ])
    status = models.CharField(max_length=20, choices=[
        ('recommended', 'Recommended'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], default='recommended')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'interventions'
    
    def __str__(self):
        return f"{self.get_intervention_type_display()} for {self.prediction.student.student_id}"
