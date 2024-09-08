from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
import base64
import pandas as pd
import json
import os
from PIL import Image
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


class ImageProcessor:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def crop_borders(self, image_path, crop_values):
        with Image.open(image_path) as img:
            width, height = img.size
            crop_area = (
                crop_values[0],
                crop_values[1],
                width - crop_values[2],
                height - crop_values[3],
            )
            cropped_img = img.crop(crop_area)
            return cropped_img

    def convert_to_greyscale(self, image):
        return image.convert("L")

    def process_images(self, crop_values, greyscale=True):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        processed_images = []
        for file in os.listdir(self.input_dir):
            image_path = os.path.join(self.input_dir, file)
            cropped_img = self.crop_borders(image_path, crop_values)
            if greyscale:
                cropped_img = self.convert_to_greyscale(cropped_img)
            output_path = os.path.join(self.output_dir, f"processed_{file}")
            cropped_img.save(output_path)
            processed_images.append(output_path)
            print(f"Processed image saved to {output_path}")

        return processed_images


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
    def __init__(self, model_name, api_key, prompt, output_dir_csv, csv_file_name):

        self.image_processor = ImageProcessor(
            "./assesments", "./assesments_cropped_greyscale"
        )
        self.converter = Base64Converter()
        self.langchain_model = LangchainModel(model_name, api_key)
        self.prompt = prompt
        self.output_dir_csv = output_dir_csv
        self.csv_file_name = csv_file_name

    def run(self, crop_values, progress_callback=None):

        os.makedirs(self.output_dir_csv, exist_ok=True)

        processed_images = self.image_processor.process_images(crop_values)
        b64_images = self.converter.convert_images_to_b64(processed_images)

        df = pd.DataFrame()
        num_images = len(b64_images)
        
        for idx, b64_image in enumerate(b64_images):
            parsed_data = self.langchain_model.extract_assessment_data(
                b64_image, self.prompt
            )
            temp_df = pd.DataFrame([parsed_data])
            temp_df = temp_df.fillna(0.0)
            df = pd.concat([df, temp_df], ignore_index=True)

            if progress_callback:
                progress_callback((idx + 1) / num_images * 100)  # Update progress

        output_csv_path = os.path.join(
            self.output_dir_csv, "{}_output.csv".format(self.csv_file_name)
        )
        df.to_csv(output_csv_path, index=False)


# Usage Example
if __name__ == "__main__":

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
    """
    crop_values = (150, 250, 200, 90)
    extractor = AssessmentExtractor(
        model_name="gpt-4o",
        api_key=api_key,
        prompt=prompt,
    )
    extractor.run(crop_values)
