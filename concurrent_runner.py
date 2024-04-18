import asyncio
import os
import aiofiles
import psutil
import GPUtil
from video_translator import VideoTranslator
from summarizer import OpenAISummarizer
from question_generator import QuestionGenerator

class AsyncRunner:
    def __init__(self, max_concurrent_tasks=None):
        self.video_translator = VideoTranslator()
        self.question_generator = QuestionGenerator()
        self.summarizer = OpenAISummarizer()
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks if max_concurrent_tasks else self.estimate_tasks())

    def estimate_tasks(self):
        # Memory-based estimation
        avg_memory_per_task = 300  # Example value in MB, adjust based on actual usage
        available_memory = psutil.virtual_memory().available / (1024 * 1024)  # Convert bytes to MB
        memory_based_tasks = int(available_memory / avg_memory_per_task)

        # GPU-based estimation (assuming tasks are GPU-intensive)
        gpus = GPUtil.getGPUs()
        if gpus:
            avg_gpu_load_per_task = 0.1  # Example value, adjust based on actual usage
            gpu_based_tasks = int(1 / avg_gpu_load_per_task)
            return min(memory_based_tasks, gpu_based_tasks)
        else:
            # If no GPU is found or tasks are not GPU-intensive, fallback to memory-based tasks
            return memory_based_tasks

    async def translate(self, file_path):
        return await self.video_translator.translate(file_path)

    async def generate_questions(self, file_path):
        return await self.question_generator.generate_questions_from_given_video(file_path)

    async def generate_summary(self, file_path):
        return await self.summarizer.generate_summary_from_given_video(file_path)

    async def process_video(self, file_path, translate, questions, summary):
        async with self.semaphore:
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
    max_tasks = 10  # Set this number based on empirical testing or dynamic estimation
    runner = AsyncRunner(max_concurrent_tasks=max_tasks)
    asyncio.run(runner.process_folder(folder_path, translate, questions, summary))

if __name__ == "__main__":
    folder_path = 'videos'  # Specify the folder path here
    run_on_a_folder(folder_path, translate=True, questions=True, summary=True)
