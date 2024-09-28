import streamlit as st
import os
import io
import sys
import threading
import time

# Import your custom modules
from video_translator import VideoTranslator
from summarizer import OpenAISummarizer
from question_generator import QuestionGenerator

# Initialize the classes from the provided modules
translator = VideoTranslator()
summarizer = OpenAISummarizer()
question_gen = QuestionGenerator()

# Custom class to capture printed output
class StreamToTextIO(io.StringIO):
    """Redirect sys.stdout to capture print statements."""
    def __init__(self):
        super().__init__()
        self.output = ''

    def write(self, s):
        super().write(s)
        self.output += s

    def getvalue(self):
        return self.output

def main():
    st.set_page_config(page_title="Video Translator", layout="wide")
    st.title("🎥 Video Translator")

    # Sidebar for Translation Options and Additional Features
    with st.sidebar:
        st.header("Translation Options")
        voice_type = st.number_input("Voice Type (1-10)", min_value=1, max_value=10, value=1, step=1)
        languages = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'zh', 'ja', 'ko']
        source_language = st.selectbox("Source Language", languages, index=0)
        destination_language = st.selectbox("Destination Language", languages, index=1)
        audio = st.checkbox("Generate Audio", value=False)
        attach = st.checkbox("Attach Audio and Subtitles to Video", value=False)

        st.header("Additional Features")

        # Generate Summary
        if st.button("Generate Summary"):
            if 'video_path' not in st.session_state:
                st.error("Please translate a video first.")
            else:
                with st.spinner("Generating summary..."):
                    summary = summarizer.generate_summary_from_given_video(st.session_state.video_path)
                st.subheader("Video Summary")
                st.text_area("Summary", summary, height=200)
                st.download_button(label="Download Summary", data=summary, file_name="summary.txt", mime="text/plain")

        # Generate Questions
        num_questions = st.number_input("Number of Questions", min_value=1, max_value=20, value=5, step=1)
        if st.button("Generate Questions"):
            if 'video_path' not in st.session_state:
                st.error("Please translate a video first.")
            else:
                with st.spinner("Generating questions..."):
                    questions = question_gen.generate_questions_from_given_video(st.session_state.video_path, num_questions)
                st.subheader("Generated Questions")
                questions_text = '\n'.join(questions)
                st.text_area("Questions", questions_text, height=200)
                st.download_button(label="Download Questions", data=questions_text, file_name="questions.txt", mime="text/plain")

    # Main Page for Video Input and Translation
    st.header("Video Input")

    # Option to upload a video file or input a local video path
    uploaded_file = st.file_uploader("Upload a video", type=['mp4', 'avi', 'mov'])
    video_path_input = st.text_input("Or input a local video path")

    # Button to start translation
    if st.button("Translate"):
        # Determine the video path
        if uploaded_file is not None:
            # Save the uploaded file to a temporary location
            temp_dir = "temp_videos"
            os.makedirs(temp_dir, exist_ok=True)
            video_path = os.path.join(temp_dir, uploaded_file.name)
            with open(video_path, 'wb') as f:
                f.write(uploaded_file.read())
        elif video_path_input:
            video_path = video_path_input
            if not os.path.exists(video_path):
                st.error("The provided video path does not exist.")
                st.stop()
        else:
            st.error("Please upload a video file or input a local video path.")
            st.stop()

        # Extract video name without extension
        video_name = os.path.splitext(os.path.basename(video_path))[0]

        # Define the output directory based on video name
        output_dir = os.path.join("output", video_name)
        os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists

        # Save video_path in session state for use in additional features
        st.session_state.video_path = video_path

        # Prepare to capture printed output
        output_captured = StreamToTextIO()
        original_stdout = sys.stdout  # Save the original stdout
        sys.stdout = output_captured  # Redirect stdout to capture prints

        # Placeholder for progress messages
        progress_placeholder = st.empty()

        # Function to run translate
        def run_translate():
            translator.translate(
                video_path,
                voice_type=voice_type,
                source_language=source_language,
                destination_language=destination_language,
                audio=audio,
                attach=attach
            )

        # Run the translate function in a separate thread
        translate_thread = threading.Thread(target=run_translate)
        translate_thread.start()

        # While the thread is alive, update the progress
        while translate_thread.is_alive():
            # Update the progress messages
            progress_placeholder.text(output_captured.getvalue())
            time.sleep(0.5)

        # When done, update the progress messages one last time
        progress_placeholder.text(output_captured.getvalue())

        # Reset stdout
        sys.stdout = original_stdout

        st.success("Translation complete!")

        # Display the translated video, extracted audio file, corrected SRT file, and transcript
        # Display Extracted Audio
        audio_file = translator.file_organizer.get_mp3_name_from_video_name(video_name)
        if os.path.exists(audio_file):
            st.subheader("Extracted Audio")
            st.audio(audio_file)
        else:
            st.warning(f"Extracted audio not found at {audio_file}")
        # Display Translated Video
        final_video = translator.file_organizer.get_final_video_name(audio_file)  # Assuming the translated video is saved as video_name.mp4
        if os.path.exists(final_video):
            st.subheader("Translated Video")
            st.video(final_video)
        else:
            st.warning(f"Translated video not found at {final_video}")

        # Display Extracted Audio
        audio_file = translator.file_organizer.get_mp3_name_from_video_name(video_name)
        if os.path.exists(audio_file):
            st.subheader("Extracted Audio")
            st.audio(audio_file)
        else:
            st.warning(f"Extracted audio not found at {audio_file}")

        # Display Corrected SRT File
        corrected_srt = translator.file_organizer.get_corrected_srt_name(audio_file)
        if os.path.exists(corrected_srt):
            st.subheader("Translated Transcript")
            with open(corrected_srt, 'r', encoding='utf-8') as f:
                srt_content = f.read()
            st.text_area("Corrected SRT Content", srt_content, height=300)
        else:
            st.warning(f"Translated Transcript not found at {corrected_srt}")

        # Display the generated transcript file
        transcript_file = translator.file_organizer.get_original_srt_file_name(audio_file)
        if os.path.exists(transcript_file):
            st.subheader("Original Transcript")
            with open(transcript_file, 'r', encoding='utf-8') as f:
                transcript_content = f.read()
            st.text_area("Transcript", transcript_content, height=300)
            st.download_button(label="Download Transcript", data=transcript_content, file_name="transcript.txt", mime="text/plain")
        else:
            st.warning(f"Transcript file not found at {transcript_file}")

    # Optional: Display session state for debugging
    # st.write(st.session_state)

if __name__ == "__main__":
    main()
