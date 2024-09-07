 crop_values = (150, 250, 200, 90)
    extractor = AssessmentExtractor(model_name="gpt-4o", api_key="sk-proj-ff6RuHPRd9empF60OpLUT3BlbkFJJhkWb9FWbp8Fruro7d0J", prompt=prompt)
    extractor.run(crop_values)