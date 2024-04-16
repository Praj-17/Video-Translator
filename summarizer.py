from openai import OpenAI

from modules.file_organizer import FileOrganizer
from modules.GetTextFromVideo import GetTextFromVideo
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
from modules.srt_parser import SRTParser
# from lang_translator import Translator


class OpenAISummarizer:
    def __init__(self) -> None:
        self.srt_parser = SRTParser()
        # self.translator = Translator()
        self.get_text = GetTextFromVideo()
        self.fo = FileOrganizer()
        self.prompt_file_location = os.getenv("summary_prompt_file_location")
    def call_openai(self, summary_prompt):

        
        completion = client.chat.completions.create(
        model=os.getenv("model_name"),
        messages=[
            {"role": "system", "content": f"You are a helpful teaching assistant that generates a concise summary of the given lecture transcript."},
            {"role": "user", "content": summary_prompt}
        ])



        return completion.choices[0].message.content

    def split_text_into_chunks(self, text, chunk_size=3000):
        chunks = []
        current_chunk = ""
        words = text.split()
        for word in words:
            if len(current_chunk) + len(word) < chunk_size:
                current_chunk += word + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = word + " "
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        return chunks

    def generate_summary(self, text, language = "spanish"):
        prompt = "create summary in {dest_lang} for {content}"
        text_chunks = self.split_text_into_chunks(text)
        summaries = []

        with open(self.prompt_file_location, "r") as f:
            prompt = f.read()
            f.close()
        for chunk in text_chunks:
            summary_prompt = prompt.format(dest_lang = language, content = chunk )
            summary = self.call_openai(summary_prompt)
            summaries.append(summary)
            # Concatenate summaries of all chunks
        return   " ".join(summaries)
    
    def generate_summary_from_srt_file(self, srt_file):
            return self.generate_summary(self.srt_parser.get_all_text(srt_file))
    def generate_translated_summary(self, srt_file, lang = 'es'):
            text = self.generate_summary_from_srt_file(srt_file)
            return self.translator(text, lang = lang)
    
    def generate_summary_from_given_video(self, video_name, language = "spanish"):
        text_to_read = os.path.join(os.getenv("default_output_folder_name"), self.fo.get_file_name_without_extension_from_path(video_name), os.getenv("default_text_save_file_name"))
        if not os.path.exists(text_to_read):
            text_to_read = self.get_text.get_text_from_video(video_name, language = language)

        try:
            with open(text_to_read, "r") as f:
                context = f.read()
        except Exception as e:
            print("Please translate the video first")
        return self.generate_summary(text=context,language = language)



if __name__ == "__main__":
    # Example usage

    summarizer = OpenAISummarizer()
    video_input = "test.mp4"
    summary = summarizer.generate_summary_from_given_video(video_input)

    print("Summary:", summary)
