from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def save_attendance_pdf(student_dict, program_name, section, output_file_path, rows_per_page=30):
    c = canvas.Canvas(output_file_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Attendance Sheet")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Program Name: {program_name}   Section: {section}   Date: ____________")
    
    # Calculate the starting y position for the grid
    y_start = height - 120
    y = y_start
    
    # Draw the header row
    c.drawString(50, y, "ID")
    c.drawString(100, y, "Student Name")
    c.drawString(300, y, "Age")
    c.drawString(350, y, "Gender")
    c.drawString(420, y, "Attendance")
    y -= 20
    
    # Draw grid lines for the header
    c.line(45, y_start + 10, 550, y_start + 10)
    c.line(45, y, 550, y)
    c.line(45, y_start + 10, 45, y)  # Left vertical line
    c.line(550, y_start + 10, 550, y)  # Right vertical line
    c.line(95, y_start + 10, 95, y)  # Vertical line between ID and Name
    c.line(290, y_start + 10, 290, y)  # Vertical line between Name and Age
    c.line(340, y_start + 10, 340, y)  # Vertical line between Age and Gender
    c.line(410, y_start + 10, 410, y)  # Vertical line between Gender and Attendance
    
    # Draw the student rows
    row_count = 0
    total_rows = rows_per_page * 2  # Two pages with 15 rows each
    for i in range(total_rows):
        if row_count >= rows_per_page:
            c.showPage()
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, "Attendance Sheet")
            c.setFont("Helvetica", 12)
            c.drawString(50, height - 80, f"Program Name: {program_name}   Section: {section}   Date: ____________")
            y = y_start
            c.drawString(50, y, "ID")
            c.drawString(100, y, "Student Name")
            c.drawString(300, y, "Age")
            c.drawString(350, y, "Gender")
            c.drawString(420, y, "Attendance")
            y -= 20
            c.line(45, y_start + 10, 550, y_start + 10)
            c.line(45, y, 550, y)
            c.line(45, y_start + 10, 45, y)  # Left vertical line
            c.line(550, y_start + 10, 550, y)  # Right vertical line
            c.line(95, y_start + 10, 95, y)  # Vertical line between ID and Name
            c.line(290, y_start + 10, 290, y)  # Vertical line between Name and Age
            c.line(340, y_start + 10, 340, y)  # Vertical line between Age and Gender
            c.line(410, y_start + 10, 410, y)  # Vertical line between Gender and Attendance
            row_count = 0
        
        if i < len(student_dict):
            student = student_dict[i]
            student_id = str(student.get('id', ''))
            name = f"{student.get('first_name', '')} {student.get('middle_name', '') or ''} {student.get('last_name', '')}".strip()
            c.drawString(50, y - 15, student_id)
            c.drawString(100, y - 15, name)
            c.drawString(300, y - 15, str(student.get('age', '')))
            c.drawString(350, y - 15, str(student.get('gender', '')))
            c.drawString(420, y - 15, "")
        
        # Draw grid lines for each row
        c.line(45, y, 550, y)
        c.line(45, y + 20, 45, y)  # Left vertical line for each row
        c.line(550, y + 20, 550, y)  # Right vertical line for each row
        c.line(95, y + 20, 95, y)  # Vertical line between ID and Name
        c.line(290, y + 20, 290, y)  # Vertical line between Name and Age
        c.line(340, y + 20, 340, y)  # Vertical line between Age and Gender
        c.line(410, y + 20, 410, y)  # Vertical line between Gender and Attendance
        
        y -= 20
        row_count += 1
    
    # Draw the final line at the bottom of the last page
    c.line(45, y, 550, y)
    c.line(45, y, 45, y + 20)  # Final left vertical line
    c.line(550, y, 550, y + 20)  # Final right vertical line
    c.line(95, y, 95, y + 20)  # Final vertical line between ID and Name
    c.line(290, y, 290, y + 20)  # Final vertical line between Name and Age
    c.line(340, y, 340, y + 20)  # Final vertical line between Age and Gender
    c.line(410, y, 410, y + 20)  # Final vertical line between Gender and Attendance
    
    c.save()
