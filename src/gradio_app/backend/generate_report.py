import json
import logging
from openai import OpenAI

from gradio_app.backend.private_config import OPEN_AI_KEY
from gradio_app.backend.story_scenarios import get_scenario_description

# Global prompt for generating biased news.
BIASED_NEWS_PROMPT = '''
Objective: Given a scenario, write four short, scandalous, and fear-driven newspaper articles designed to outrage the public. Each article must take a strong, one-sided stance, sensationalistic 'culture war' style , twisting or omitting facts to maximize shock and fear.

Perspectives: Create four versions of the controversy. 
1) Villainizing Alex
2) Villainizing Jordan
3) Villainizing Alex (while painting Jordan as a hero)
4) Villainizing Jordan (while painting Alex as a hero)

Writing Style: Use simple, everyday language like a viral blog post, not traditional news. Keep sentences short and punchy with no complex words or neutral analysis. The tone should be dramatic and emotional, making readers angry, scared, or outraged. The writing should be subtly manipulative, leading readers to the conclusion without stating bias outright. End each article with a sense of fear, leaving readers worried about what happens next (not a question).

Article Structure:
- A scandalous headline (bold, dramatic, clickbait-worthy).
- A short report (five to seven sentences, aggressive, biased, designed to provoke).

Output Format (valid JSON):
{
  "villainizing_alex": {
    "headline": "YOUR HEADLINE HERE",
    "report": "YOUR REPORT HERE"
  },
  "villainizing_jordan": {
    "headline": "YOUR HEADLINE HERE",
    "report": "YOUR REPORT HERE"
  },
  "villainizing_alex_painting_jordan_as_hero": {
    "headline": "YOUR HEADLINE HERE",
    "report": "YOUR REPORT HERE"
  },
  "villainizing_jordan_painting_alex_as_hero": {
    "headline": "YOUR HEADLINE HERE",
    "report": "YOUR REPORT HERE"
  }
}

Goal: Make the reader feel like they discovered the "truth" themselves—angry, betrayed, and afraid of what comes next.
'''


def return_biased_news_reports(description_text):
    """
    Given a short description of a scenario, calls GPT
    to generate four biased news articles. Returns the response as parsed JSON.

    :param description_text: The scenario description string.
    :return: A dictionary containing four biased articles from different angles.
    """
    logging.info("Starting request to OpenAI GPT with scenario description.")

    client = OpenAI(api_key=OPEN_AI_KEY)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": BIASED_NEWS_PROMPT
            },
            {
                "role": "user",
                "content": f"Scenario: {description_text}"
            }
        ],
        response_format={"type": "json_object"},
        temperature=1,
        max_completion_tokens=16383,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    logging.info("Request to GPT complete. Parsing JSON response.")
    return json.loads(response.choices[0].message.content)


def generate_news(scenario):
    """
    Top-level function to generate four biased news articles for a given scenario.

    :param scenario: The string key identifying which scenario to use .
    :return: A tuple of 8 items (headline1, report1, headline2, report2, headline3, report3, headline4, report4).
    """
    description = get_scenario_description(scenario)
    logging.info(f"Scenario description retrieved: {description}")

    response = return_biased_news_reports(description)

    # Extract the articles from the JSON response
    return (
        response["villainizing_alex"]["headline"],
        response["villainizing_alex"]["report"],

        response["villainizing_jordan"]["headline"],
        response["villainizing_jordan"]["report"],

        response["villainizing_alex_painting_jordan_as_hero"]["headline"],
        response["villainizing_alex_painting_jordan_as_hero"]["report"],

        response["villainizing_jordan_painting_alex_as_hero"]["headline"],
        response["villainizing_jordan_painting_alex_as_hero"]["report"],
    )
