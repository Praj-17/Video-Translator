import os
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
class FileOrganizer():
    def __init__(self) -> None:
        pass
    def create_folder_if_not_exists(self, folder_path):
        """
        Check if a folder exists, if not, create it.

        Parameters:
        folder_path (str): Path to the folder to be checked/created.
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        else:
            pass
    def extract_file_name_from_path(self, file_path):
        """
        Extracts the file name from the given file path.

        Parameters:
        file_path (str): The path of the file.

        Returns:
        str: The file name.
        """
        file_name = os.path.basename(file_path)
        return file_name
    def get_file_name_without_extension(self, file_name):
        return file_name.split(".")[0]
    def get_file_name_without_extension_from_path(self, file_path):
        basename = self.extract_file_name_from_path(file_path)
        return self.get_file_name_without_extension(basename)

    def initialize(self, video_file_name: str):
        created_folder_path = os.path.join(os.getenv("default_output_folder_name"), self.get_file_name_without_extension_from_path(video_file_name))
        self.create_folder_if_not_exists(created_folder_path)
        output_folder = os.path.join(created_folder_path, os.getenv("default_audio_split_files_folder_name"))
        self.create_folder_if_not_exists(output_folder)
        updated_video_path = os.path.join(created_folder_path, os.path.basename(video_file_name))
        return created_folder_path,updated_video_path
    def get_mp3_name_from_video_name(self, video_name):
        return os.path.join(os.path.dirname(video_name), self.get_file_name_without_extension_from_path(video_name) + ".mp3")
    def get_srt_name_from_video_name(self, video_name):
        return os.path.join( os.path.dirname(video_name), os.getenv("default_srt_file_name"))
    def get_audio_split_path(self, video_name):
        return os.path.join(os.path.dirname(video_name), os.getenv("default_audio_split_files_folder_name"))
    def get_merged_file_name(self, video_name):
        return os.path.join(os.path.dirname(video_name), os.getenv("default_merged_file_with_silence_name"))
    def get_corrected_srt_name(self, video_name):
        return  os.path.join(os.path.dirname(video_name), os.getenv("corrected_srt_name"))
    def get_final_video_name(self, video_name):
        return os.path.join(os.path.dirname(video_name), self.get_file_name_without_extension_from_path(video_name) + "_translated" +  ".mp4")
    def get_initial_silence_output_path(self, video_name):
        return os.path.join(os.path.dirname(video_name), os.getenv("default_initial_silence_save_name"))
    
    
        