import json
import logging


def return_story_scenarios(json_filepath="data/data.json"):
    """
    Reads a JSON file containing story scenarios and returns a dictionary
    mapping scenario names to their descriptive text.

    :param json_filepath: str, path to the JSON file containing story scenarios.
    :return: dict, where keys are scenario names and values are scenario descriptions.
    """
    try:
        with open(json_filepath, "r", encoding="utf-8") as file:
            scenarios = json.load(file)
        return scenarios
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.info(f"Error loading JSON file: {e}")
        return {}


def get_scenario_description(scenario):
    """
    Returns the description string for a given scenario key.

    :param scenario: The string key for a scenario (one of the keys in return_story_scenarios()).
    :return: The descriptive text of the chosen scenario or a default message if not found.
    """
    story_scenarios = return_story_scenarios()
    if scenario in story_scenarios.keys():
        return story_scenarios[scenario]['description']['story']
    return "Select a scenario to see the description."

