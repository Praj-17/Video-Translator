import gradio as gr
from fpdf import FPDF
from video_translator import VideoTranslator
from summarizer import OpenAISummarizer
from question_generator import QuestionGenerator

# Initialize the classes from the provided modules
translator = VideoTranslator()
summarizer = OpenAISummarizer()
question_gen = QuestionGenerator()

def translate_video(video_path, voice_type):
    """Function to translate the video with voice type selection and return the path."""
    translated_video_path = translator.translate(video_path, voice_type)
    return translated_video_path

def generate_summary(video_path):
    """Generate a summary from the video."""
    print("This is vode", video_path)
    summary = summarizer.generate_summary_from_given_video(video_path)
    return summary

def create_summary_file(summary):
    """Create a .txt file from the summary."""
    path = "summary.txt"
    with open(path, "w") as file:
        file.write(summary)
    return path

def generate_questions(video_path, n):
    """Generate a specified number of questions from the video."""
    questions = question_gen.generate_questions_from_given_video(video_path, n)
    return questions

# Define themes and add toggle button styles
themes = {
    "dark": """
        body, .gradio-container { background-color: #282a36; color: #f8f8f2; }
        button, input, textarea, select, label { 
            background-color: #44475a; 
            color: #f8f8f2; 
            border: 1px solid #6272a4; 
        }
        button:hover { background-color: #6272a4; }
        .gradio-file, .gradio-dropdown, .gradio-slider, .gradio-label, .gradio-container, .gradio-button, .gradio-textbox {
            background-color: #44475a; 
            color: #f8f8f2;
        }
        #toggle-theme {
            position: fixed;
            top: 10px;
            right: 10px;
            font-size: 24px;
            background: transparent;
            border: none;
            cursor: pointer;
        }
    """,
    "light": """
        body, .gradio-container { background-color: #FFF; color: #333; }
        button, input, textarea, select, label { 
            background-color: #EEE; 
            color: #333; 
            border: 1px solid #CCC; 
        }
        button:hover { background-color: #DDD; }
        .gradio-file, .gradio-dropdown, .gradio-slider, .gradio-label, .gradio-container, .gradio-button, .gradio-textbox {
            background-color: #FFF; 
            color: #333;
        }
        #toggle-theme {
            position: fixed;
            top: 10px;
            right: 10px;
            font-size: 24px;
            background: transparent;
            border: none;
            cursor: pointer;
        }
    """
}

current_theme = "dark"  # Default theme

def toggle_theme():
    global current_theme
    new_value = "🌞" if current_theme == "dark" else "🌟"
    current_theme = "light" if current_theme == "dark" else "dark"
    gr.Interface.update()  # Not a real function - just illustrating what would be needed
    return new_value

with gr.Blocks(css=themes[current_theme]) as app:
    with gr.Row():
        theme_toggle = gr.Button(value="🌞" if current_theme == "dark" else "🌟", elem_id="toggle-theme")
        theme_toggle.click(toggle_theme, inputs=[theme_toggle], outputs=theme_toggle)

    with gr.Column():
        video_input = gr.Video(label="Upload your video here", autoplay=True, show_share_button=True, show_download_button=True)
        voice_type_input = gr.Radio(["Male", "Female"], label="Select Voice Type")
        num_questions_input = gr.Dropdown([str(i) for i in range(1, 21)], label="Number of Questions")
        translate_btn = gr.Button("Translate Video")
        summary_btn = gr.Button("Generate Summary")
        questions_btn = gr.Button("Generate Questions")
        translated_video = gr.Video(label="Translated Video")
        video_summary = gr.Textbox(label="Video Summary", lines=10, interactive=True)
        video_questions = gr.Textbox(label="Questions Generated", lines=10, interactive=True)
        copy_summary_btn = gr.Button("Copy Summary")
        copy_questions_btn = gr.Button("Copy Questions")

    translate_btn.click(
        fn=translate_video,
        inputs=[video_input, voice_type_input],
        outputs=translated_video
    )

    summary_btn.click(
        fn=lambda x: (generate_summary(x)),
        inputs=video_input,
        outputs=[video_summary, download_summary_btn]
    )

    questions_btn.click(
        fn=lambda x, n: (generate_questions(x, n)),
        inputs=[video_input, num_questions_input],
        outputs=[video_questions, download_questions_btn]
    )

    copy_summary_btn.click(
        fn=lambda text: text,
        inputs=video_summary,
        outputs=video_summary
    )

    copy_questions_btn.click(
        fn=lambda text: text,
        inputs=video_questions,
        outputs=video_questions
    )

if __name__ == "__main__":
    app.launch(share=True)