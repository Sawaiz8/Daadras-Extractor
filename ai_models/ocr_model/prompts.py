import json

# Load the JSON schema from the file
with open('data/schemas/student_data_schema.json', 'r') as file:
    schema = json.load(file)

# Extract the JSON format for pre_test_data's written_exam_score
json_format_written_exam = schema["pre_test_data"]["written_exam_scores"]
json_format_practical_exam = schema["pre_test_data"]["practical_exam_reports"]

written_exam_prompt = f"""\
Extract the following information from this image: Student name, age, End time, and all of the scores in the table.
Please be cautious with the numbers and make sure they are correctly interpreted. If a score appears as "null" or empty, replace it with 0. Ensure that the output JSON follows this format exactly:
JSON format: 
{json.dumps(json_format_written_exam, indent=4)}
"""

practical_exam_prompt = f"""\
Extract the following information from this image: student name, start time, End time, and the text of the report. Student name is not included in the json format but include that key as well.
JSON format: 
{json.dumps(json_format_practical_exam, indent=4)}
"""
