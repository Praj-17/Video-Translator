import asyncio
import os
import aiofiles
from video_translator import VideoTranslator
from summarizer import OpenAISummarizer
from question_generator import QuestionGenerator


class AsyncRunner:
    def __init__(self):
        self.video_translator = VideoTranslator()
        self.question_generator = QuestionGenerator()
        self.summarizer = OpenAISummarizer()

    async def translate(self, file_path):
        # Assuming `translate_video` is an async method of `VideoTranslator`
        return await self.video_translator.translate_video(file_path)

    async def generate_questions(self, file_path):
        # Assuming `generate_video_questions` is an async method of `QuestionGenerator`
        return await self.question_generator.generate_video_questions(file_path)

    async def generate_summary(self, file_path):
        # Assuming `summarize_video` is an async method of `OpenAISummarizer`
        return await self.summarizer.summarize_video(file_path)

    async def process_video(self, file_path, translate, questions, summary):
        tasks = []
        if translate:
            tasks.append(self.translate(file_path))
        if questions:
            tasks.append(self.generate_questions(file_path))
        if summary:
            tasks.append(self.generate_summary(file_path))

        if tasks:
            await asyncio.gather(*tasks)

    async def process_folder(self, folder_path, translate=False, questions=False, summary=False):
        for dirpath, _, filenames in os.walk(folder_path):
            video_files = [os.path.join(dirpath, filename) for filename in filenames if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv'))]
            await asyncio.gather(*(self.process_video(file, translate, questions, summary) for file in video_files))

def run_on_a_folder(folder_path, translate=False, questions=False, summary=False):
    runner = AsyncRunner()
    asyncio.run(runner.process_folder(folder_path, translate, questions, summary))

if __name__ == "__main__":
    folder_path = 'path_to_your_folder'  # Specify the folder path here
    run_on_a_folder(folder_path, translate=True, questions=True, summary=True)