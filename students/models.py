from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    admission_year = models.IntegerField()
    admission_score = models.FloatField(help_text="JAMB or entrance exam score")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'students'
        ordering = ['student_id']
    
    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"
    
    def calculate_gpa(self, semester=None):
        results = self.results.all()
        if semester:
            results = results.filter(semester=semester)
        
        if not results.exists():
            return 0.0
        
        total_points = sum(r.quality_points for r in results)
        total_credits = sum(r.credit_units for r in results)
        
        return round(total_points / total_credits, 2) if total_credits > 0 else 0.0

class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    course_title = models.CharField(max_length=200)
    credit_units = models.IntegerField()
    department = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'courses'
    
    def __str__(self):
        return f"{self.course_code} - {self.course_title}"

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    score = models.FloatField()
    grade = models.CharField(max_length=2)
    credit_units = models.IntegerField()
    quality_points = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'results'
        unique_together = ['student', 'course', 'semester']
    
    def save(self, *args, **kwargs):
        self.grade = self.calculate_grade()
        self.quality_points = self.calculate_quality_points()
        super().save(*args, **kwargs)
    
    def calculate_grade(self):
        if self.score >= 70: return 'A'
        elif self.score >= 60: return 'B'
        elif self.score >= 50: return 'C'
        elif self.score >= 45: return 'D'
        elif self.score >= 40: return 'E'
        else: return 'F'
    
    def calculate_quality_points(self):
        grade_points = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1, 'F': 0}
        return grade_points.get(self.grade, 0) * self.credit_units
    
    def __str__(self):
        return f"{self.student.student_id} - {self.course.course_code}: {self.grade}"

class AdditionalFactors(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='factors')
    attendance_percentage = models.FloatField(default=0)
    assignment_average = models.FloatField(default=0)
    study_hours_per_week = models.FloatField(default=0)
    socioeconomic_status = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ])
    extracurricular_participation = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'additional_factors'
    
    def __str__(self):
        return f"Factors for {self.student.student_id}"
