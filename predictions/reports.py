from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from datetime import datetime
import os

class PredictionReportGenerator:
    
    @staticmethod
    def generate_report(prediction):
        """Generate PDF report for a prediction"""
        
        filename = f"prediction_report_{prediction.student.student_id}_{datetime.now().strftime('%Y%m%d')}.pdf"
        filepath = os.path.join('media', 'reports', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a365d'),
            spaceAfter=30,
            alignment=1
        )
        title = Paragraph("Student Performance Prediction Report", title_style)
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Student Information
        student_data = [
            ['Student ID:', prediction.student.student_id],
            ['Name:', f"{prediction.student.first_name} {prediction.student.last_name}"],
            ['Department:', prediction.student.department],
            ['Email:', prediction.student.email],
        ]
        
        student_table = Table(student_data, colWidths=[2*inch, 4*inch])
        student_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e2e8f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0'))
        ]))
        story.append(student_table)
        story.append(Spacer(1, 0.4*inch))
        
        # Prediction Results
        story.append(Paragraph("Prediction Results", styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))
        
        risk_color = {
            'high_achiever': colors.green,
            'average': colors.orange,
            'at_risk': colors.red
        }
        
        prediction_data = [
            ['Predicted CGPA:', str(prediction.predicted_cgpa)],
            ['Risk Level:', prediction.get_risk_level_display()],
            ['Confidence Score:', f"{prediction.confidence_score}%"],
            ['Prediction Date:', prediction.predicted_at.strftime('%Y-%m-%d %H:%M')],
        ]
        
        prediction_table = Table(prediction_data, colWidths=[2*inch, 4*inch])
        prediction_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e2e8f0')),
            ('TEXTCOLOR', (1, 1), (1, 1), risk_color.get(prediction.risk_level, colors.black)),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0'))
        ]))
        story.append(prediction_table)
        story.append(Spacer(1, 0.4*inch))
        
        # Input Factors
        story.append(Paragraph("Input Factors Used", styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))
        
        factors_data = [
            ['Factor', 'Value', 'Weight'],
            ['First Semester GPA', f"{prediction.first_semester_gpa:.2f}", '40%'],
            ['Attendance', f"{prediction.attendance_percentage:.1f}%", '15%'],
            ['Assignment Average', f"{prediction.assignment_average:.1f}%", '15%'],
            ['Study Hours/Week', f"{prediction.study_hours:.1f}", '10%'],
            ['Admission Score', f"{prediction.admission_score:.0f}", '10%'],
            ['Socioeconomic Score', f"{prediction.socioeconomic_score:.0f}", '10%'],
        ]
        
        factors_table = Table(factors_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
        factors_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d3748')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(factors_table)
        
        # Interventions (if any)
        interventions = prediction.interventions.all()
        if interventions:
            story.append(Spacer(1, 0.4*inch))
            story.append(Paragraph("Recommended Interventions", styles['Heading2']))
            story.append(Spacer(1, 0.2*inch))
            
            for intervention in interventions:
                story.append(Paragraph(
                    f"<b>{intervention.get_intervention_type_display()}</b> (Priority: {intervention.priority})",
                    styles['Normal']
                ))
                story.append(Paragraph(intervention.description, styles['Normal']))
                story.append(Spacer(1, 0.15*inch))
        
        doc.build(story)
        return filepath
