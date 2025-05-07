from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
import base64
import pandas as pd
import json
import os
from PIL import Image
from .prompts import prompt
import streamlit as st

api_key = os.getenv("OPENAI_API_KEY")

class ImageProcessor:
    def __init__(self):
        pass

    def convert_to_greyscale(self, image_path):
        with Image.open(image_path) as img:
            greyscale_img = img.convert("L")
            greyscale_img.save(image_path)
            print(f"Converted image to greyscale and saved to {image_path}")
            return greyscale_img

    def process_images(self, image_paths):
        for image_path in image_paths:
            self.convert_to_greyscale(image_path)
        print("All images have been processed.")
        return image_paths  # Return the file paths, not Image objects

class Base64Converter:
    @staticmethod
    def image_to_b64(image_path):
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            base64_encoded_data = base64.b64encode(image_data)
            return base64_encoded_data.decode("utf-8")

    def convert_images_to_b64(self, image_paths):
        return [self.image_to_b64(image) for image in image_paths]

class LangchainModel:
    def __init__(self, model_name, api_key):
        self.model = ChatOpenAI(model=model_name, api_key=api_key, temperature=0)

    def extract_assessment_data(self, b64_image, prompt):
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{b64_image}",
                        "detail": "high",
                    },
                },
            ],
        )
        response = self.model.invoke([message])
        clean_json_string = (
            response.content.strip("`")
            .replace("```json", "")
            .replace("```", "")
            .replace("json", "")
            .strip()
        )
        print(clean_json_string)
        return json.loads(clean_json_string)


class AssessmentExtractor:
    def __init__(self, model_name, api_key, prompt):

        self.image_processor = ImageProcessor()
        self.converter = Base64Converter()
        self.langchain_model = LangchainModel(model_name, api_key)
        self.prompt = prompt

    def run(self, image_paths, progress_callback=None):

        processed_images = self.image_processor.process_images(image_paths)
        b64_images = self.converter.convert_images_to_b64(processed_images)

        df = pd.DataFrame()
        num_images = len(b64_images)
        
        for idx, b64_image in enumerate(b64_images):
            # Extract the ID from the image path
            image_path = processed_images[idx]
            image_id = image_path.split("/")[-4].split("_")[0]
            
            parsed_data = self.langchain_model.extract_assessment_data(
                b64_image, self.prompt
            )
            parsed_data['ID'] = image_id  # Add the extracted ID to the parsed data
            
            temp_df = pd.DataFrame([parsed_data])
            temp_df = temp_df.fillna(0.0)
            df = pd.concat([df, temp_df], ignore_index=True)

            if progress_callback:
                progress_callback((idx + 1) / num_images * 100)  # Update progress

        df.columns = df.columns.str.lower()

        # # Add a column called start time with all values at 10:05
        # df['start_time'] = '10:05'
        
        # # Convert all values except 'name' and 'end_time' to integers
        # for col in df.columns:
        #     if col not in ['name', "start_time",'end_time']:
        #         df[col] = df[col].astype(int)

        # # Ensure 'end_time' column values do not have any alphabets
        # df['end_time'] = df['end_time'].str.replace(r'[a-zA-Z]', '', regex=True).str.strip()
        
        # # Ensure 'end_time' has only time values and no alphabets
        # def clean_time(time_str):
        #     try:
        #         # Check if the time_str is in the correct format
        #         pd.to_datetime(time_str, format='%H:%M')  # Updated format
        #         return time_str
        #     except ValueError:
        #         try:
        #             pd.to_datetime(time_str, format='%I:%M %p')
        #             return time_str
        #         except ValueError:
        #             return None
        
        # df['end_time'] = df['end_time'].apply(clean_time)
        # df['start_time'] = df['start_time'].apply(clean_time)

        # # Replace invalid 'end_time' values with the average time
        # valid_times = pd.to_datetime(df['end_time'].dropna(), format='%H:%M')  # Updated format
        # if not valid_times.empty:
        #     average_time = valid_times.mean().strftime('%I:%M %p')
        #     df['end_time'] = df['end_time'].fillna(average_time)
        
        # valid_times = pd.to_datetime(df['start_time'].dropna(), format='%H:%M')  # Updated format
        # if not valid_times.empty:
        #     average_time = valid_times.mean().strftime('%I:%M %p')
        #     df['start_time'] = df['start_time'].fillna(average_time)
        
        # # Create a new column called time_taken and compute the difference between start_time and end_time in minutes
        # df['time_taken'] = (pd.to_datetime(df['end_time'], format='%H:%M') - pd.to_datetime(df['start_time'], format='%H:%M')).dt.total_seconds() / 60        
        # # Create a new column called Average performance and compute the average score for all rows using all the columns except name, end_time, and age
        # score_columns = [col for col in df.columns if col not in ['name', "start_time", "time_taken", 'end_time', 'age']]
        # df['average_performance'] = df[score_columns].mean(axis=1)

        # print(df.columns)
        
        return df

extractor = AssessmentExtractor(
    model_name="gpt-4o",
    api_key=api_key,
    prompt=prompt,
)

