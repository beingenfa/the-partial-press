"""
Load some saved examples for the static version of the site
"""
import json
from gradio_app.backend.generate_report import return_biased_news_reports

data = {}

with open("../../gradio_app/data/data.json", "r", encoding="utf-8") as file:
    story_scenarios = json.load(file)

for title, description in story_scenarios.items():
    response = return_biased_news_reports(description)
    data[title] = {'description': description,
                   'biased_reports': response}

with open('data.json', 'w') as f:
    json.dump(data, f)
