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

def create_questions_file(questions):
    """Create a PDF file from the questions."""
    path = "questions.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for question in questions:
        pdf.cell(200, 10, txt=question, ln=True)
    pdf.output(path)
    return path

with gr.Blocks() as app:
    with gr.Row():
        with gr.Column():
            video_input = gr.Video(label="Upload your video here", autoplay = True, show_share_button = True, show_download_button = True)
            voice_type_input = gr.Radio(["Male", "Female"], label="Select Voice Type")
            num_questions_input = gr.Slider(1, 10, 1, label="Number of Questions")
            translate_btn = gr.Button("Translate Video")
            summary_btn = gr.Button("Generate Summary")
            questions_btn = gr.Button("Generate Questions")
        with gr.Column():
            translated_video = gr.Video(label="Translated Video")
            video_summary = gr.Textbox(label="Video Summary", lines=10, interactive=True)
            download_summary_btn = gr.File(label="Download Summary")
            video_questions = gr.Textbox(label="Questions Generated", lines=10, interactive=True)
            download_questions_btn = gr.File(label="Download Questions")
            copy_summary_btn = gr.Button("Copy Summary")
            copy_questions_btn = gr.Button("Copy Questions")

    translate_btn.click(
        fn=translate_video,
        inputs=[video_input, voice_type_input],
        outputs=translated_video
    )

    summary_btn.click(
        fn=lambda x: (generate_summary(x), create_summary_file(generate_summary(x))),
        inputs=video_input,
        outputs=[video_summary, download_summary_btn]
    )

    questions_btn.click(
        fn=lambda x, n: (generate_questions(x, n), create_questions_file(generate_questions(x, n))),
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