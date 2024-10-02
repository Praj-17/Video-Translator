
import openai
from openai import OpenAI
from dotenv import load_dotenv
from modules.file_organizer import FileOrganizer
import os
from modules.GetTextFromVideo import GetTextFromVideo
# Load environment variables from .env file
load_dotenv()

import os
import json



class QuestionGenerator:
    def __init__(self) -> None:
        self.prompt_file_location = os.getenv("qna_prompt_file_location")

        with open(os.getenv("qna_constrain_file_location"), 'r') as json_file:
            self.q_and_a_json_constrain = json.load(json_file)
        self.fo = FileOrganizer()
        self.get_text = GetTextFromVideo()
    def run_openai(self, api_key , questions_prompt, functions = []):
        client = OpenAI(api_key =api_key)
        completion = client.chat.completions.create(
        model = os.getenv("model_name"),
        temperature = float(os.getenv("temperature")),
        messages=[
            {"role": "user", "content":"You are helful question-answer generating agent which return output in a JSON format.",
            "role": "user", "content":questions_prompt}],
            functions=functions
        )
        nep_question = completion.choices[0].message.function_call.arguments

        return json.loads(nep_question)
    def generate_questions(self, context,api_key, n = 10, language = "spanish"):
        with open(self.prompt_file_location, "r") as f:
            prompt = f.read()
            prompt = prompt.format(n = n, language = language, context = context)
            f.close()
        return self.run_openai(api_key =api_key, questions_prompt=prompt, functions = [self.q_and_a_json_constrain])
    def save_generated_questions(self, text_to_read, questions):
        questions_save_file = os.path.join(os.path.dirname(text_to_read), os.getenv("default_questions_save_path"))
        print("saved to ", questions_save_file)
        with open(questions_save_file, 'w') as file:
            json.dump(questions, file, indent=4, ensure_ascii=False, sort_keys=True)
        return questions_save_file

    def generate_questions_from_given_video(self, video_name, api_key, n = 10, language = "spanish"):
        text_to_read = os.path.join(os.getenv("default_output_folder_name"), self.fo.get_file_name_without_extension_from_path(video_name), os.getenv("default_text_save_file_name"))
        if not os.path.exists(text_to_read):
            text_to_read = self.get_text.get_text_from_video(video_name, language = language)
        context = ""
        try:
            with open(text_to_read, "r") as f:
                context = f.read()
        except Exception as e:
            print("Please translate the video first")
        questions = self.generate_questions(context=context,api_key = api_key,  n=n, language= language)
        questions_save_file = self.save_generated_questions(text_to_read, questions)
        return questions



if __name__ == "__main__":
    gen = QuestionGenerator()
    video_input = "n2.mp4"
    response =  gen.generate_questions_from_given_video(video_input, n  = 5)
    print(response)