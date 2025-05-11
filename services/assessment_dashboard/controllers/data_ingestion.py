import zipfile
import io
import pandas as pd
import os
from main.database import mongo_store
import asyncio
import os
from ai_models.ocr_model.ocr import written_exam_extractor, practical_exam_extractor
from ai_models.audio_model.audio_preprocessor import audio_preprocessor
from ai_models.audio_model.transcription_model import transcription_model
import shutil
import zipfile
import tempfile
import streamlit as st
from functools import reduce


def get_data_file_paths(temp_data_dir):
    written_exam_image_file_paths_pretest = []
    written_exam_image_file_paths_posttest = []  
    practical_exam_image_file_paths_pretest = []
    practical_exam_image_file_paths_posttest = []
    viva_exam_audio_file_paths_pretest = []
    viva_exam_audio_file_paths_posttest = []
    for root, dirs, files in os.walk(temp_data_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.wav', ".aac", ".m4a")):
                folder_name = root.split("/")[-3]
                extension = file.split(".")[-1]
                new_file_name = f"{folder_name}_written.{extension}"
                new_file_path = os.path.join(root, new_file_name)
                os.rename(os.path.join(root, file), new_file_path)
                if "Pre_test/Written" in root:
                    written_exam_image_file_paths_pretest.append(new_file_path)
                elif "Post_test/Written" in root:
                    written_exam_image_file_paths_posttest.append(new_file_path)
                elif "Pre_test/Practical" in root:
                    practical_exam_image_file_paths_pretest.append(new_file_path)
                elif "Post_test/Practical" in root:
                    practical_exam_image_file_paths_posttest.append(new_file_path)
                elif "Pre_test/Viva" in root:
                    viva_exam_audio_file_paths_pretest.append(new_file_path)
                elif "Post_test/Viva" in root:
                    viva_exam_audio_file_paths_posttest.append(new_file_path)

    return written_exam_image_file_paths_pretest, written_exam_image_file_paths_posttest, practical_exam_image_file_paths_pretest, practical_exam_image_file_paths_posttest, viva_exam_audio_file_paths_pretest, viva_exam_audio_file_paths_posttest


def create_score_template(students, selected_section):
    with io.BytesIO() as buffer:
        with zipfile.ZipFile(buffer, 'w') as z:
            for student in students:
                folder_name = get_student_folder_name(student)
                pre_test_path = f"{selected_section}/{folder_name}/Pre_test"
                post_test_path = f"{selected_section}/{folder_name}/Post_test"
                
                # Create folders for Pre_test and Post_test
                z.writestr(f"{pre_test_path}/Written/", "")
                z.writestr(f"{pre_test_path}/Viva/", "")
                z.writestr(f"{pre_test_path}/Practical/", "")
                
                z.writestr(f"{post_test_path}/Written/", "")
                z.writestr(f"{post_test_path}/Viva/", "")
                z.writestr(f"{post_test_path}/Practical/", "")
                
        buffer.seek(0)
        return buffer.getvalue()

def verify_folder_structure(base_path, selected_section, students):
    failure_points = []

    if not os.path.exists(os.path.join(base_path, selected_section)):
        failure_points.append(f"Missing section directory: {os.path.join(base_path, selected_section)}")
        return False

    for student in students:
        folder_name = get_student_folder_name(student)
        student_folder_path = os.path.join(base_path, selected_section, folder_name)
        
        if not os.path.exists(student_folder_path):
            failure_points.append(f"Missing student folder: {student_folder_path}")
            return False
        
        pre_test_path = os.path.join(student_folder_path, "Pre_test")
        post_test_path = os.path.join(student_folder_path, "Post_test")
        
        if not os.path.exists(pre_test_path):
            failure_points.append(f"Missing Pre_test folder: {pre_test_path}")
            return False
        if not os.path.exists(post_test_path):
            failure_points.append(f"Missing Post_test folder: {post_test_path}")
            return False
        
        for test_type in ["Written", "Viva", "Practical"]:
            pre_test_type_path = os.path.join(pre_test_path, test_type)
            post_test_type_path = os.path.join(post_test_path, test_type)
            if not os.path.exists(pre_test_type_path):
                failure_points.append(f"Missing Pre_test {test_type} folder: {('/'.join(pre_test_type_path.split('/')[-4:]))}")
                return False
            if not os.path.exists(post_test_type_path):
                failure_points.append(f"Missing Post_test {test_type} folder: {('/'.join(post_test_type_path.split('/')[-4:]))}")
                return False

    if failure_points:
        st.write("Failure Points:")
        for point in failure_points:
            st.write(point)

    return True


def get_student_folder_name(student):
    student_id = str(student.get('id', ''))
    middle_name = student.get('middle_name', '')
    student_name_parts = [str(student.get('first_name', ''))]
    if middle_name:
        student_name_parts.append(str(middle_name))
    student_name_parts.append(str(student.get('last_name', '')))
    student_name = "_".join(filter(None, student_name_parts))
    return f"{student_id}_{student_name}"


def extract_written_exam_data(written_exam_image_file_paths):
    written_exam_dataframe = written_exam_extractor.run_written_exam_flow(written_exam_image_file_paths)
    return written_exam_dataframe

def extract_viva_exam_data(viva_exam_audio_file_paths):
    cleaned_audio_file_paths = audio_preprocessor.clean_audio_files(viva_exam_audio_file_paths)
    transcriptions_dataframe = transcription_model.transcribe_and_translate_audio_files(cleaned_audio_file_paths)
    return transcriptions_dataframe

def extract_practical_exam_data(practical_exam_image_file_paths):
    practical_exam_dataframe = practical_exam_extractor.run_practical_exam_flow(practical_exam_image_file_paths)
    return practical_exam_dataframe

def merge_dataframes_on_id(dataframes):
    if not dataframes:
        return pd.DataFrame()
        
    # Get all unique IDs across all dataframes
    all_ids = set()
    for df in dataframes:
        all_ids.update(df['id'].unique())
    
    # Create base dataframe with all IDs
    base_df = pd.DataFrame({'id': list(all_ids)})
    
    # Merge each dataframe with outer join to keep all IDs
    merged_dataframe = base_df
    for df in dataframes:
        merged_dataframe = pd.merge(merged_dataframe, df, on='id', how='outer')
    
    # Fill missing values with None/NaN
    merged_dataframe = merged_dataframe.fillna(pd.NA)
    
    return merged_dataframe

def save_data_for_exam_type(dataframes, session_name, section_name, exam_type = "pre_test_data"):
    written_df = dataframes.get("written")
    viva_df = dataframes.get("viva")
    practical_df = dataframes.get("practical")

    if written_df is None and viva_df is None and practical_df is None:
        return

    # Get all unique IDs
    all_ids = set()
    if written_df is not None:
        all_ids.update(written_df['id'].unique())
    if viva_df is not None:
        all_ids.update(viva_df['id'].unique())
    if practical_df is not None:
        all_ids.update(practical_df['id'].unique())

    updates = []
    for student_id in all_ids:

        update = (int(student_id), dict())

        written_row = None if written_df is None else written_df[written_df['id'] == student_id].iloc[0] if not written_df[written_df['id'] == student_id].empty else None
        viva_row = None if viva_df is None else viva_df[viva_df['id'] == student_id].iloc[0] if not viva_df[viva_df['id'] == student_id].empty else None
        practical_row = None if practical_df is None else practical_df[practical_df['id'] == student_id].iloc[0] if not practical_df[practical_df['id'] == student_id].empty else None
        
        if written_row is not None:
            written_scores = written_row.to_dict()
            update[1][f"{exam_type}.written_exam_scores"] =  written_scores

        if viva_row is not None:
            viva_data = viva_row.to_dict()
            update[1][f"{exam_type}.viva"] =  viva_data

        if practical_row is not None:
            practical_data = practical_row.to_dict()
            update[1][f"{exam_type}.practical_exam_reports"] =  practical_data

        updates.append(update)
    
    for student_id, update_data in updates:
        asyncio.run(mongo_store.update_student_fields(session_name, section_name, student_id, update_data))

def process_student_data(exam_data_zip, session_name, section_name):
    with tempfile.TemporaryDirectory() as temp_data_dir:
        # Create temporary directory for viva audio files
        viva_temp_dir = os.path.join(temp_data_dir, "temp_viva_files")
        os.makedirs(viva_temp_dir, exist_ok=True)
        with zipfile.ZipFile(exam_data_zip, 'r') as zip_ref:
            zip_ref.extractall(temp_data_dir)
        students = asyncio.run(mongo_store.get_students_by_session_and_section(session_name, section_name))
        if verify_folder_structure(temp_data_dir, section_name, students):
            (
                written_exam_image_file_paths_pre_test, 
                written_exam_image_file_paths_post_test, 
                practical_exam_image_file_paths_pre_test, 
                practical_exam_image_file_paths_post_test, 
                viva_exam_audio_file_paths_pre_test, 
                viva_exam_audio_file_paths_post_test
            ) = get_data_file_paths(temp_data_dir)
            dataframes = {"viva": None, "written": None, "practical": None}
            if written_exam_image_file_paths_pre_test:
               written_exam_dataframe_pre_test = extract_written_exam_data(written_exam_image_file_paths_pre_test)
               dataframes["written"] = written_exam_dataframe_pre_test
            if viva_exam_audio_file_paths_pre_test:
               viva_exam_dataframe_pre_test = extract_viva_exam_data(viva_exam_audio_file_paths_pre_test)
               dataframes["viva"] = viva_exam_dataframe_pre_test
            if practical_exam_image_file_paths_pre_test:
               practical_exam_dataframe_pre_test = extract_practical_exam_data(practical_exam_image_file_paths_pre_test)
               st.write("practical_exam_dataframe_pre_test", practical_exam_dataframe_pre_test)
               dataframes["practical"] = practical_exam_dataframe_pre_test
            if dataframes:
                save_data_for_exam_type(dataframes, session_name, section_name, exam_type="pre_test_data")

            dataframes = {"viva": None, "written": None, "practical": None}
            if written_exam_image_file_paths_post_test:
               written_exam_dataframe_post_test = extract_written_exam_data(written_exam_image_file_paths_post_test)
               dataframes["written"] = written_exam_dataframe_post_test
            if viva_exam_audio_file_paths_post_test:
               viva_exam_dataframe_post_test = extract_viva_exam_data(viva_exam_audio_file_paths_post_test)
               dataframes["viva"] = viva_exam_dataframe_post_test
            if practical_exam_image_file_paths_post_test:
               practical_exam_dataframe_post_test = extract_practical_exam_data(practical_exam_image_file_paths_post_test)
               st.write("practical_exam_dataframe_post_test", practical_exam_dataframe_post_test)
               dataframes["practical"] = practical_exam_dataframe_post_test
            if dataframes:
                save_data_for_exam_type(dataframes, session_name, section_name, exam_type="post_test_data")

        else:
            st.error("Folder structure is not correct")