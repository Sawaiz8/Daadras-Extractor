import json

# Load the JSON schema from the file
with open('data/schemas/student_data_schema.json', 'r') as file:
    schema = json.load(file)

# Extract the JSON format for pre_test_data's written_exam_score
json_format = schema["pre_test_data"]["written_exam_scores"]

prompt = f"""\
Extract the following information from this image: Student name, age, End time, and all of the scores in the table.
Please be cautious with the numbers and make sure they are correctly interpreted. If a score appears as "null" or empty, replace it with 0. Ensure that the output JSON follows this format exactly:
JSON format: 
{json.dumps(json_format, indent=4)}
"""