from authentication.models import CustomUser
from students.models import Student, Course, Result, AdditionalFactors
from predictions.engine import PredictionEngine

# Create Admin User
admin = CustomUser.objects.create_user(
    username='admin',
    password='admin123',
    email='admin@spps.edu',
    role='admin',
    first_name='System',
    last_name='Administrator',
    is_staff=True,
    is_superuser=True
)
print("✓ Admin created: admin/admin123")

# Create Advisor User
advisor = CustomUser.objects.create_user(
    username='advisor',
    password='advisor123',
    email='advisor@spps.edu',
    role='advisor',
    first_name='Academic',
    last_name='Advisor'
)
print("✓ Advisor created: advisor/advisor123")

# Create Sample Students
students_data = [
    {
        'student_id': 'STU001',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@student.edu',
        'department': 'Computer Science',
        'admission_year': 2023,
        'admission_score': 285
    },
    {
        'student_id': 'STU002',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane.smith@student.edu',
        'department': 'Computer Science',
        'admission_year': 2023,
        'admission_score': 310
    },
    {
        'student_id': 'STU003',
        'first_name': 'Mike',
        'last_name': 'Johnson',
        'email': 'mike.johnson@student.edu',
        'department': 'Computer Science',
        'admission_year': 2023,
        'admission_score': 240
    }
]

for data in students_data:
    student = Student.objects.create(**data)
    print(f"✓ Student created: {student.student_id}")

# Create Sample Courses
courses_data = [
    {'course_code': 'CSC101', 'course_title': 'Introduction to Computing', 'credit_units': 3, 'department': 'Computer Science'},
    {'course_code': 'MTH101', 'course_title': 'Calculus I', 'credit_units': 3, 'department': 'Mathematics'},
    {'course_code': 'PHY101', 'course_title': 'Physics I', 'credit_units': 3, 'department': 'Physics'},
    {'course_code': 'GST101', 'course_title': 'Use of English', 'credit_units': 2, 'department': 'General Studies'},
    {'course_code': 'CSC102', 'course_title': 'Programming Fundamentals', 'credit_units': 4, 'department': 'Computer Science'},
]

for data in courses_data:
    course = Course.objects.create(**data)
    print(f"✓ Course created: {course.course_code}")

# Create Sample Results for STU001 (High Performer)
stu001 = Student.objects.get(student_id='STU001')
results_stu001 = [
    {'course_code': 'CSC101', 'score': 75, 'credit_units': 3},
    {'course_code': 'MTH101', 'score': 82, 'credit_units': 3},
    {'course_code': 'PHY101', 'score': 78, 'credit_units': 3},
    {'course_code': 'GST101', 'score': 80, 'credit_units': 2},
    {'course_code': 'CSC102', 'score': 88, 'credit_units': 4},
]

for data in results_stu001:
    course = Course.objects.get(course_code=data['course_code'])
    Result.objects.create(
        student=stu001,
        course=course,
        semester='First',
        score=data['score'],
        credit_units=data['credit_units']
    )

# Create Sample Results for STU002 (High Achiever)
stu002 = Student.objects.get(student_id='STU002')
results_stu002 = [
    {'course_code': 'CSC101', 'score': 90, 'credit_units': 3},
    {'course_code': 'MTH101', 'score': 85, 'credit_units': 3},
    {'course_code': 'PHY101', 'score': 88, 'credit_units': 3},
    {'course_code': 'GST101', 'score': 82, 'credit_units': 2},
    {'course_code': 'CSC102', 'score': 92, 'credit_units': 4},
]

for data in results_stu002:
    course = Course.objects.get(course_code=data['course_code'])
    Result.objects.create(
        student=stu002,
        course=course,
        semester='First',
        score=data['score'],
        credit_units=data['credit_units']
    )

# Create Sample Results for STU003 (At Risk)
stu003 = Student.objects.get(student_id='STU003')
results_stu003 = [
    {'course_code': 'CSC101', 'score': 55, 'credit_units': 3},
    {'course_code': 'MTH101', 'score': 48, 'credit_units': 3},
    {'course_code': 'PHY101', 'score': 52, 'credit_units': 3},
    {'course_code': 'GST101', 'score': 60, 'credit_units': 2},
    {'course_code': 'CSC102', 'score': 58, 'credit_units': 4},
]

for data in results_stu003:
    course = Course.objects.get(course_code=data['course_code'])
    Result.objects.create(
        student=stu003,
        course=course,
        semester='First',
        score=data['score'],
        credit_units=data['credit_units']
    )

print(f"✓ Results created for all students")

# Create Additional Factors
AdditionalFactors.objects.create(
    student=stu001,
    attendance_percentage=85.0,
    assignment_average=78.0,
    study_hours_per_week=20.0,
    socioeconomic_status='medium',
    extracurricular_participation=True
)

AdditionalFactors.objects.create(
    student=stu002,
    attendance_percentage=95.0,
    assignment_average=90.0,
    study_hours_per_week=25.0,
    socioeconomic_status='high',
    extracurricular_participation=True
)

AdditionalFactors.objects.create(
    student=stu003,
    attendance_percentage=65.0,
    assignment_average=55.0,
    study_hours_per_week=8.0,
    socioeconomic_status='low',
    extracurricular_participation=False
)

print("✓ Additional factors created for all students")

# Generate Predictions
for student_id in ['STU001', 'STU002', 'STU003']:
    prediction = PredictionEngine.predict_cgpa(student_id, 'First')
    print(f"✓ Prediction generated for {student_id}: {prediction.predicted_cgpa} ({prediction.risk_level})")

print("\n=== SEEDING COMPLETE ===")
print("Login credentials:")
print("  Admin:   admin/admin123")
print("  Advisor: advisor/advisor123")
