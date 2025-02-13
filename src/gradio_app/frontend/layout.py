import gradio as gr

from src.gradio_app.backend.generate_report import generate_news
from src.gradio_app.backend.story_scenarios import return_story_scenarios, get_scenario_description


def return_page_layout():
    """
    Builds and returns a Gradio Blocks interface for generating biased news reports.

    This UI consists of:
    1. A header with a logo and subtitle.
    2. A Dropdown menu to select one of several scenarios.
    3. Four boxes displaying different biased headlines/reports when 'Generate Report' is clicked.
    """
    with gr.Blocks(css="""
        @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;700&family=Merriweather:wght@300;400;700&display=swap');

        body { 
            background-color: #fff; 
            font-family: 'Merriweather', serif; 
            color: #111; 
        }

        .container { 
            padding: 20px; 
            max-width: 1100px; 
            margin: auto; 
        }

        .title { 
            text-align: center; 
            font-size: 70px; 
            font-weight: bold; 
            font-family: 'Old English Text MT', serif; 
            color: #000; 
            margin-bottom: 2px; 
        }

        .sub-title { 
            text-align: center; 
            font-size: 18px; 
            font-weight: normal; 
            color: #555; 
        }

        .news-box { 
            font-size: 18px; 
            padding: 20px; 
            background: #fff; 
            border: 2px solid black; 
            position: relative; 
            min-height: 150px;
            font-family: 'Merriweather', serif; 
            line-height: 1.5; 
            text-align: justify; 
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1); 
            border-radius: 0px; 
        }

        .news-header { 
            font-size: 22px; 
            font-weight: bold; 
            text-align: center; 
            border-bottom: 2px solid black; 
            padding-bottom: 5px; 
            margin-bottom: 10px; 
            font-family: 'Lora', serif; 
        }

        .tag { 
            font-size: 12px; 
            font-weight: bold; 
            color: white; 
            background: grey; 
            padding: 3px 8px; 
            position: absolute; 
            bottom: 10px; 
            right: 10px; 
            border-radius: 3px; 
        }

        .submit-btn { 
            width: 100%; 
            padding: 12px; 
            font-size: 20px; 
            font-weight: bold; 
            background: #222; 
            color: white; 
            border: none; 
        }

        .submit-btn:hover { 
            background: #444; 
        }

        /* Remove internal grey box styling for text input areas inside .news-box */
        .news-box select, .news-box textarea, .news-box input {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
                 
        }
    """) as demo:
        # Header section with custom branding
        gr.Markdown(
            """<div style='display: flex; align-items: center; justify-content: center; gap: 15px; font-family: "Old English Text MT", serif;'>
                <img src='https://raw.githubusercontent.com/beingenfa/the-partial-press/49bd8ae134785ea8d53c102b948154ce5301f4c4/docs/images/logo_with_name.svg' 
                     alt='The Partial Press Logo' 
                     style='max-width: 200px; height: auto;'>
                <div style='text-align: center;'>
                    <h1 style='font-size: 70px; font-weight: bold; margin-bottom: 2px;'>The Partial Press</h1>
                    <p style='font-size: 18px; font-style: italic;'>Half the story, twice the spin.</p>      
                </div>
            </div> 
            <hr style='border: 3px solid black; margin-top: 5px;'> """
        )

        # Left column: scenario selection
        with gr.Row():
            with gr.Column(scale=2):
                with gr.Column():
                    gr.Markdown("<div class='news-header'>Select a Scenario</div>")
                    scenario_dropdown = gr.Dropdown(
                        choices=list(return_story_scenarios().keys()),
                        label="",  # Label suppressed so we can use custom HTML above
                        interactive=True,
                        container=False
                    )
                    scenario_output = gr.Markdown("<p></p>", elem_classes=["no-background"])

                    # Whenever user changes the scenario dropdown, update the scenario description below it
                    scenario_dropdown.change(
                        fn=get_scenario_description,
                        inputs=scenario_dropdown,
                        outputs=scenario_output
                    )

                    submit_button = gr.Button("Generate Report", elem_classes=["submit-btn"])

            # Right column: display the four different biased articles
            with gr.Column(scale=4):
                with gr.Row():
                    with gr.Column(scale=1):
                        villainizing_alex = gr.Markdown(
                            "<div class='news-box'><div class='news-header'></div><p></p></div><span class='tag'>Villainizing Alex</span>",
                        )
                with gr.Row():
                    with gr.Column(scale=1):
                        villainizing_jordan = gr.Markdown(
                            "<div class='news-box'><div class='news-header'></div><p></p></div><span class='tag'>Villainizing Jordan</span>",
                        )
                with gr.Row():
                    with gr.Column(scale=1):
                        villainizing_alex_painting_jordan_as_hero = gr.Markdown(
                            "<div class='news-box'><div class='news-header'></div><p></p></div><span class='tag'>Villainizing Alex & Painting Jordan as Hero</span>",
                        )
                with gr.Row():
                    with gr.Column(scale=1):
                        villainizing_jordan_painting_alex_as_hero = gr.Markdown(
                            "<div class='news-box'><div class='news-header'></div><p></p></div><span class='tag'>Villainizing Jordan & Painting Alex as Hero</span>",
                        )

                # On click, we call generate_news(scenario) and show the results in the four boxes
                submit_button.click(
                    fn=lambda scenario: tuple(
                        f"<div class='news-box'><div class='news-header'>{headline}</div><p>{text}</p></div><span class='tag'>{key}</span>"
                        for key, (headline, text) in zip(
                            [
                                'villainizing_alex',
                                'villainizing_jordan',
                                'villainizing_alex_painting_jordan_as_hero',
                                'villainizing_jordan_painting_alex_as_hero'
                            ],
                            zip(*[iter(generate_news(scenario))] * 2)
                        )
                    ),
                    inputs=scenario_dropdown,
                    outputs=[
                        villainizing_alex,
                        villainizing_jordan,
                        villainizing_alex_painting_jordan_as_hero,
                        villainizing_jordan_painting_alex_as_hero
                    ]
                )
    return demo
