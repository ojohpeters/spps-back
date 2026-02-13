import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spps_project.settings')
django.setup()

from students.models import Student

# Student data matching the CSV file
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
    },
    {
        'student_id': 'STU004',
        'first_name': 'Sarah',
        'last_name': 'Williams',
        'email': 'sarah.williams@student.edu',
        'department': 'Computer Science',
        'admission_year': 2023,
        'admission_score': 270
    },
    {
        'student_id': 'STU005',
        'first_name': 'David',
        'last_name': 'Brown',
        'email': 'david.brown@student.edu',
        'department': 'Computer Science',
        'admission_year': 2023,
        'admission_score': 320
    }
]

print("Creating students...")
print("=" * 50)

for data in students_data:
    student, created = Student.objects.get_or_create(
        student_id=data['student_id'],
        defaults=data
    )
    if created:
        print(f"✓ Created: {student.student_id} - {student.first_name} {student.last_name}")
    else:
        print(f"⚠ Already exists: {student.student_id} - {student.first_name} {student.last_name}")

print("=" * 50)
print(f"Total students in database: {Student.objects.count()}")
print("\nDone! You can now upload the test_student_results.csv file.")
