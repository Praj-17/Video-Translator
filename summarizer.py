from openai import OpenAI
from dotenv import load_dotenv
import os
from modules.file_organizer import FileOrganizer


# Load environment variables from .env file
load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
from modules.srt_parser import SRTParser
# from lang_translator import Translator


class OpenAISummarizer:
    def __init__(self) -> None:
        self.srt_parser = SRTParser()
        # self.translator = Translator()
        self.fo = FileOrganizer()
    def call_openai(self, text_chunk, dest_lang = "spanish"):

        
        completion = client.chat.completions.create(
        model=os.getenv("model_name"),
        messages=[
            {"role": "system", "content": "You are a helpful teaching assistant that generates a concise summary of the given lecture transcript. Do not put any place holders. Return the Summary in {dest_lang}"},
            {"role": "user", "content": text_chunk}
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
        text_chunks = self.split_text_into_chunks(text)
        summaries = []
        for chunk in text_chunks:
            summary = self.call_openai(chunk, language)
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
        try:
            with open(text_to_read, "r") as f:
                context = f.read()
        except Exception as e:
            print("Please translate the video first")
        return self.generate_summary(text=context,language = language)



if __name__ == "__main__":
    # Example usage

    summarizer = OpenAISummarizer()
    video_input = "test2.mp4"
    summary = summarizer.generate_summary_from_given_video(video_input)

    print("Summary:", summary)
