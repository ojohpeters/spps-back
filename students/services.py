import pandas as pd
from django.db import transaction
from .models import Student, Course, Result

class CSVImportService:
    
    @staticmethod
    def process_results_csv(file, semester):
        """
        Process uploaded CSV file containing student results
        Expected columns: student_id, course_code, score, credit_units
        """
        try:
            df = pd.read_csv(file)
            
            required_columns = ['student_id', 'course_code', 'score', 'credit_units']
            if not all(col in df.columns for col in required_columns):
                return {
                    'success': False,
                    'error': f'Missing required columns. Expected: {", ".join(required_columns)}'
                }
            
            results_created = 0
            errors = []
            
            with transaction.atomic():
                for index, row in df.iterrows():
                    try:
                        student = Student.objects.get(student_id=row['student_id'])
                        course, _ = Course.objects.get_or_create(
                            course_code=row['course_code'],
                            defaults={
                                'course_title': row.get('course_title', f'Course {row["course_code"]}'),
                                'credit_units': int(row['credit_units']),
                                'department': student.department
                            }
                        )
                        
                        result, created = Result.objects.update_or_create(
                            student=student,
                            course=course,
                            semester=semester,
                            defaults={
                                'score': float(row['score']),
                                'credit_units': int(row['credit_units'])
                            }
                        )
                        
                        if created:
                            results_created += 1
                            
                    except Student.DoesNotExist:
                        errors.append(f"Row {index + 1}: Student {row['student_id']} not found")
                    except Exception as e:
                        errors.append(f"Row {index + 1}: {str(e)}")
            
            return {
                'success': True,
                'results_created': results_created,
                'total_processed': len(df),
                'errors': errors
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to process CSV: {str(e)}'
            }
