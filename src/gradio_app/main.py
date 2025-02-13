from gradio_app.frontend.layout import return_page_layout


def main():
    demo = return_page_layout()
    demo.launch()


if __name__ == "__main__":
    main()
