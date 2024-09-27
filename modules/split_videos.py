from moviepy.video.io.VideoFileClip import VideoFileClip
from .file_organizer import FileOrganizer
from dotenv import load_dotenv

load_dotenv()
import os

class VideoSplitter:
    def __init__(self) -> None:
        self.fo = FileOrganizer()
        self.default_split_dir = os.getenv("default_split_dir_name")
def split_video_into_four_parts(self, video_path):

    video_name = self.fo.get_file_name_without_extension(video_path)
    split_dir = os.path.join(self.fo.default_dir, video_name, 
                            self.default_split_dir )
    # Load the video
    video = VideoFileClip(video_path)
    duration = video.duration

    # Calculate the durations for each part
    part_duration = duration / 4

    # Create and save the video parts
    for i in range(4):
        start_time = i * part_duration
        end_time = (i + 1) * part_duration
        part = video.subclip(start_time, end_time)
        part.write_videofile(, codec="libx264")

if __name__ == "__main__":
    input = "cls.mp4"
    output = "cls_split"
# Example usage
    split_video_into_four_parts(input, output)
