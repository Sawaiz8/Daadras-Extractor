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