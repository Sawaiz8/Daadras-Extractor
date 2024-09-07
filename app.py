import streamlit as st
import zipfile
import os
import pandas as pd
from modular_imgreader_gs_crop import AssessmentExtractor  
api_key = os.getenv("OPENAI_API_KEY")


prompt = """\
Extract the following information from this image: Student name, age, End time, and all of the scores in the table.
Please be cautious with the numbers and make sure they are correctly interpreted. If a score appears as "null", replace it with 0. Ensure that the output JSON follows this format exactly:
JSON format: 
{
    "name": "<name>",
    "age": <age>,
    "end_time": "<time>",
    "AI(Artificial Intelligence)": <score>,
    "Canva": <score>,
    "Turtle Programming": <score>,
    "Scratch Programming": <score>,
    "Account Creation": <score>,
    "English Comprehension": <score>,
    "Urdu Comprehension": <score>,
    "Hardware/Games/Internet": <score>,
    "Basic Navigation": <score>,
    "Environmental Questions": <score>
}
RESPONSE SHOULD ONLY BE JSON
"""

import shutil
import os

def delete_folders(directory, folder_name):
    """Delete all folders with the specified folder name in the given directory."""
    folder_path = os.path.join(directory, folder_name)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
        print(f"Deleted folder: {folder_path}")
    else:
        print(f"Folder not found: {folder_path}")


def handle_file_upload(uploaded_file, directory):
    if uploaded_file is not None:
        file_path = os.path.join(directory, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"File {uploaded_file.name} uploaded successfully.")

def main():
    st.title("Daadras Assessment Information Extractor")

    tab1, tab2, tab3 = st.tabs(["IT", "Chess", "SEL"])

    
    with tab1:
        st.header("IT")
        uploaded_file = st.file_uploader("Upload a ZIP file for Assessment", type="zip")

        if uploaded_file is not None:
            # Define directories
            zip_dir = './database/uploaded_zips'
            extraction_dir = './database/assessments'
            processed_images_dir = './database/processed_images'
            csv_folder = "./database/csv_files"

            # Delete all existing CSV files, ZIP files, and images
            delete_folders("./database", "assessments")
            delete_folders("./database", "uploaded_zips")  # Assuming images are in PNG format
            delete_folders("./database", "processed_images")
            delete_folders("./database","csv_files")
            

            # Create directories if they don't exist
            if not os.path.exists(zip_dir):
                os.makedirs(zip_dir)
            if not os.path.exists(extraction_dir):
                os.makedirs(extraction_dir)
            if not os.path.exists(processed_images_dir):
                os.makedirs(processed_images_dir)
            if not os.path.exists(csv_folder):
                os.makedirs(csv_folder)

            # Save the uploaded ZIP file with its original name
            zip_path = os.path.join(zip_dir, uploaded_file.name)
            with open(zip_path, "wb") as f:
                f.write(uploaded_file.read())

            # Extract the ZIP file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extraction_dir)

            zip_base_name = os.path.splitext(uploaded_file.name)[0]
            # Initialize the extractor
            extractor = AssessmentExtractor(
                model_name="gpt-4o",
                api_key=api_key,
                prompt=prompt,
                output_dir_csv=csv_folder,
                csv_file_name=zip_base_name
            )

            # Process images
            crop_values = (150, 250, 200, 90)
            extractor.image_processor.input_dir = extraction_dir
            extractor.image_processor.output_dir = processed_images_dir
            extractor.run(crop_values)
            
            output_csv_file = '{}_output.csv'.format(zip_base_name)
            csv_file_path = os.path.join(csv_folder, output_csv_file)

            st.write("Processing complete. Download the CSV file:")
            with open(csv_file_path, 'rb') as f:
                st.download_button(
                    label="Download CSV",
                    data=f,
                    file_name=csv_file_path,
                    mime="text/csv"
                )

    # Tab for Chess
    with tab2:
        st.header("Chess")
        chess_file = st.file_uploader("Upload a ZIP file for Chess", type="zip")
        handle_file_upload(chess_file, './assessments') # change this to seperate uploaded zips directory when necessary

    # Tab for SEL
    with tab3:
        st.header("SEL")
        sel_file = st.file_uploader("Upload a ZIP file for SEL", type="zip")
        handle_file_upload(sel_file, './assessments') #change this as well

if __name__ == "__main__":
    main()
