import streamlit as st
import os
import io
import sys
import threading
import time
import json

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

def submit_api_key(api_key):
    """
    Handles the submission of the OpenAI API key.
    Stores the key in environment variables and session state.
    """
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
        st.session_state.api_key = api_key  # Store the API key in session state
        st.session_state.api_key_submitted = True
        st.success("API Key submitted successfully!")
    else:
        st.error("Please enter a valid API Key.")

def is_api_key_submitted():
    """
    Checks if the OpenAI API key has been submitted.
    """
    return st.session_state.get('api_key_submitted', False)

def generate_summary(video_path, language):
    """
    Generates a summary for the given video.
    Passes the API key to the summarizer.
    """
    api_key = st.session_state.get('api_key', None)
    if not api_key:
        st.error("API Key not found. Please submit your API Key.")
        return None
    try:
        summary = summarizer.generate_summary_from_given_video(
            video_path,
            language=language,
            api_key=api_key  # Pass the API key here
        )
        return summary
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return None

def generate_questions(video_path, num_questions, language):
    """
    Generates questions for the given video.
    Passes the API key to the question generator.
    """
    api_key = st.session_state.get('api_key', None)
    if not api_key:
        st.error("API Key not found. Please submit your API Key.")
        return None
    try:
        questions = question_gen.generate_questions_from_given_video(
            video_path,
            num_questions,
            language=language,
            api_key=api_key  # Pass the API key here
        )
        return questions
    except Exception as e:
        st.error(f"Error generating questions: {e}")
        return None

def main():
    st.set_page_config(page_title="Video Translator", layout="wide")
    st.title("🎥 Video Translator")

    # Initialize session state
    if 'api_key_submitted' not in st.session_state:
        st.session_state.api_key_submitted = False
    if 'translation_output' not in st.session_state:
        st.session_state.translation_output = ''
    if 'translation_running' not in st.session_state:
        st.session_state.translation_running = False
    if 'translation_complete' not in st.session_state:
        st.session_state.translation_complete = False

    # Define language mappings
    languages = {
        'English': 'en',
        'Spanish': 'es',
        'French': 'fr',
        'German': 'de',
        'Italian': 'it',
        'Portuguese': 'pt',
        'Russian': 'ru',
        'Chinese': 'zh',
        'Japanese': 'ja',
        'Korean': 'ko'
    }

    # Define voice options
    voices = {
        'Female': 0,
        'Male': 1
    }

    # Sidebar for Translation Options and Additional Features
    with st.sidebar:
        st.header("Translation Options")

        # Voice selection as dropdown
        selected_voice = st.selectbox("Voice Type", list(voices.keys()), index=0)
        voice_type = voices[selected_voice]

        # Full language names in UI
        source_language_name = st.selectbox("Source Language", list(languages.keys()), index=0)
        source_language = languages[source_language_name]

        destination_language_name = st.selectbox("Destination Language", list(languages.keys()), index=1)
        destination_language = languages[destination_language_name]

        audio = st.checkbox("Generate Audio", value=False)
        attach = st.checkbox("Attach Audio and Subtitles to Video", value=False)

        st.header("Additional Features")

        # OpenAI API Key Input
        st.subheader("OpenAI API Key")
        api_key_input = st.text_input("Enter your OpenAI API Key", type="password")
        if st.button("Submit API Key"):
            submit_api_key(api_key_input)

        st.markdown("---")

        # Generate Summary
        st.subheader("Generate Summary")
        summary_language_name = st.selectbox("Summary Language", list(languages.keys()), index=0, key="summary_language")
        summary_language = languages[summary_language_name]

        # Disable button if API key not submitted
        summary_disabled = not is_api_key_submitted()
        if summary_disabled:
            st.warning("Please submit your OpenAI API Key to enable this feature.")

        if st.button("Generate Summary", disabled=summary_disabled):
            if 'video_path' not in st.session_state:
                st.error("Please translate a video first.")
            else:
                with st.spinner("Generating summary..."):
                    summary = generate_summary(st.session_state.video_path, language=summary_language)
                if summary:
                    st.subheader("Video Summary")
                    st.text_area("Summary", summary, height=200)
                    st.download_button(label="Download Summary", data=summary, file_name="summary.txt", mime="text/plain")

        # Generate Questions
        st.subheader("Generate Questions")
        num_questions = st.number_input("Number of Questions", min_value=1, max_value=20, value=5, step=1)
        questions_language_name = st.selectbox("Questions Language", list(languages.keys()), index=0, key="questions_language")
        questions_language = languages[questions_language_name]

        # Disable button if API key not submitted
        questions_disabled = not is_api_key_submitted()
        if questions_disabled:
            st.warning("Please submit your OpenAI API Key to enable this feature.")

        if st.button("Generate Questions", disabled=questions_disabled):
            if 'video_path' not in st.session_state:
                st.error("Please translate a video first.")
            else:
                with st.spinner("Generating questions..."):
                    questions = generate_questions(
                        st.session_state.video_path,
                        num_questions,
                        language=questions_language
                    )
                if questions:
                    st.subheader("Generated Questions")
                    questions_json = {"questions": questions}
                    st.json(questions_json, expanded=True)
                    st.download_button(
                        label="Download Questions",
                        data=json.dumps(questions_json, indent=4),
                        file_name="questions.json",
                        mime="application/json"
                    )

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
            st.session_state.video_uploaded = True  # Flag to indicate video has been uploaded
        elif video_path_input:
            video_path = video_path_input
            if not os.path.exists(video_path):
                st.error("The provided video path does not exist.")
                st.stop()
            st.session_state.video_uploaded = True  # Flag to indicate video has been provided
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

        # Run the translate function directly (back to normal)
        translator.translate(
            video_path,
            voice_type=voice_type,
            source_language=source_language,
            destination_language=destination_language,
            audio=audio,
            attach=attach
        )

        # Reset stdout
        sys.stdout = original_stdout

        # Display progress messages
        st.text(output_captured.getvalue())

        st.success("Translation complete!")

        # Display the translated video, extracted audio file, corrected SRT file, and transcript
        # Display Extracted Audio
        audio_file = translator.file_organizer.get_mp3_name_from_video_name(video_name)
        if os.path.exists(audio_file):
            st.subheader("Extracted Audio")
            st.audio(audio_file)
            # Download button for Extracted Audio
            with open(audio_file, "rb") as af:
                audio_bytes = af.read()
            st.download_button(
                label="Download Extracted Audio",
                data=audio_bytes,
                file_name=os.path.basename(audio_file),
                mime="audio/mpeg"
            )
        else:
            st.warning(f"Extracted audio not found at {audio_file}")

        # Display Translated Video
        final_video = translator.file_organizer.get_final_video_name(audio_file)
        if os.path.exists(final_video):
            st.subheader("Translated Video")
            st.video(final_video)
            # Download button for Translated Video
            with open(final_video, "rb") as vf:
                video_bytes = vf.read()
            st.download_button(
                label="Download Translated Video",
                data=video_bytes,
                file_name=os.path.basename(final_video),
                mime="video/mp4"
            )
        else:
            st.warning(f"Translated video not found at {final_video}")

        # Display Corrected SRT File
        corrected_srt = translator.file_organizer.get_corrected_srt_name(audio_file)
        if os.path.exists(corrected_srt):
            st.subheader("Translated Transcript")
            with open(corrected_srt, 'r', encoding='utf-8') as f:
                srt_content = f.read()
            st.text_area("Corrected SRT Content", srt_content, height=300)
            # Download button for Corrected SRT
            st.download_button(
                label="Download Translated Transcript",
                data=srt_content,
                file_name="translated_transcript.srt",
                mime="text/plain"
            )
        else:
            st.warning(f"Translated Transcript not found at {corrected_srt}")

        # Display the generated transcript file
        transcript_file = translator.file_organizer.get_original_srt_file_name(audio_file)
        if os.path.exists(transcript_file):
            st.subheader("Original Transcript")
            with open(transcript_file, 'r', encoding='utf-8') as f:
                transcript_content = f.read()
            st.text_area("Transcript", transcript_content, height=300)
            st.download_button(
                label="Download Original Transcript",
                data=transcript_content,
                file_name="transcript.txt",
                mime="text/plain"
            )
        else:
            st.warning(f"Transcript file not found at {transcript_file}")

    # Optional: Display session state for debugging
    # st.write(st.session_state)

if __name__ == "__main__":
    main()
