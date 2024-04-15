import gradio as gr
from video_translator import VideoTranslator
from summarizer import OpenAISummarizer
from question_generator import QuestionGenerator

# Initialize the classes from the provided modules
translator = VideoTranslator()
summarizer = OpenAISummarizer()
question_gen = QuestionGenerator()

def translate_video(video_path):
    """Function to translate the video and return the path to the translated video."""
    translated_video_path = translator.translate(video_path)
    return translated_video_path

def generate_summary(video_path):
    """Function to generate a summary from the video."""
    summary = summarizer.generate_summary_from_given_video(video_path)
    return summary

def generate_questions(video_path):
    """Function to generate questions from the video."""
    questions = question_gen.generate_questions_from_given_video(video_path)
    return questions

# Create a Gradio interface
with gr.Blocks() as app:
    with gr.Row():
        with gr.Column():
            video_input = gr.Video(label="Upload your video here")
            translate_btn = gr.Button("Translate Video")
            summary_btn = gr.Button("Generate Summary")
            questions_btn = gr.Button("Generate Questions")
            
        with gr.Column():
            translated_video = gr.Video(label="Translated Video")
            video_summary = gr.Textbox(label="Video Summary", lines=10)
            video_questions = gr.Textbox(label="Questions Generated from Video", lines=10)

    # Interaction logic
    translate_btn.click(
        fn=translate_video,
        inputs=video_input,
        outputs=translated_video
    )

    summary_btn.click(
        fn=generate_summary,
        inputs=video_input,
        outputs=video_summary
    )

    questions_btn.click(
        fn=generate_questions,
        inputs=video_input,
        outputs=video_questions
    )

app.launch()
