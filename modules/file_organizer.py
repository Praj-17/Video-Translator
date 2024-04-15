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
        return created_folder_path
        