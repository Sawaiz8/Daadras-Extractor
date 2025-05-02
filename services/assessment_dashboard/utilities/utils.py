import zipfile
import io
import pandas as pd
def create_written_exam_template(students, selected_section):
    with io.BytesIO() as buffer:
        with zipfile.ZipFile(buffer, 'w') as z:
            for student in students:
                folder_name = get_student_folder_name(student)
                z.writestr(f"{selected_section}/{folder_name}/{folder_name}_english.jpg", "")
                z.writestr(f"{selected_section}/{folder_name}/{folder_name}_urdu.jpg", "")
        buffer.seek(0)
        return buffer.getvalue()

def create_viva_audio_template(students, selected_section):
    with io.BytesIO() as buffer:
        with zipfile.ZipFile(buffer, 'w') as z:
            for student in students:
                folder_name = get_student_folder_name(student)
                z.writestr(f"{selected_section}/{folder_name}/{folder_name}.jpg", "")
        buffer.seek(0)
        return buffer.getvalue()

def create_practical_exam_template(students, selected_section):
    with io.BytesIO() as buffer:
        with zipfile.ZipFile(buffer, 'w') as z:
            for student in students:
                folder_name = get_student_folder_name(student)
                z.writestr(f"{selected_section}/{folder_name}/{folder_name}.mp3", "")
        buffer.seek(0)
        return buffer.getvalue()

def get_student_folder_name(student):
    student_id = str(student.get('id', ''))
    middle_name = str(student.get('middle_name', ''))
    student_name_parts = [str(student.get('first_name', ''))]
    if middle_name:
        student_name_parts.append(middle_name)
    student_name_parts.append(str(student.get('last_name', '')))
    student_name = "_".join(filter(None, student_name_parts))
    return f"{student_id}_{student_name}"


def load_file_as_dataframe(uploaded_file):
    file_extension = uploaded_file.name.split('.')[-1]
    if file_extension in ['xlsx', 'ods']:
        return pd.read_excel(uploaded_file, engine='openpyxl')
    elif file_extension == 'xls':
        return pd.read_excel(uploaded_file, engine='xlrd')
    elif file_extension == 'csv':
        return pd.read_csv(uploaded_file)
    else:
        return None
