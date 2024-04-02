
import openai
from openai import OpenAI
from dotenv import load_dotenv
from .file_organizer import FileOrganizer
import os

# Load environment variables from .env file
load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY") )
import os
import json



class QuestionGenerator:
    def __init__(self) -> None:
        self.prompt_file_location = os.getenv("qna_prompt_file_location")

        with open(os.getenv("qna_constrain_file_location"), 'r') as json_file:
            self.q_and_a_json_constrain = json.load(json_file)
        self.fo = FileOrganizer()
    def run_openai(self, questions_prompt, functions = []):
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
    def generate_questions(self, context, n = 10, language = "spanish"):
        with open(self.prompt_file_location, "r") as f:
            prompt = f.read()
            prompt = prompt.format(n = n, language = language, context = context)
            f.close()
        return self.run_openai(questions_prompt=prompt, functions = [self.q_and_a_json_constrain])
    def generate_questions_from_given_video(self, video_name, n = 10, language = "spanish"):
        text_to_read = os.path.join(os.getenv("default_output_folder_name"), self.fo.get_file_name_without_extension_from_path(video_name), os.getenv("default_text_save_file_name"))
        try:
            with open(text_to_read, "r") as f:
                context = f.read()
        except Exception as e:
            print("Please translate the video first")
        return self.generate_questions(context=context, n=n, language= language)



if __name__ == "__main__":
    gen = QuestionGenerator()
    video_input = "test2.mp4"
    response =  gen.generate_questions(video_input, n  = 5)
    print(response)