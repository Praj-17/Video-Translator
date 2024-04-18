from moviepy.editor import VideoFileClip
from modules.file_organizer import FileOrganizer
import os
import ffmpeg


class AudioExtractor():
    def __init__(self) -> None:
        self.fo = FileOrganizer()
        pass
    def extract_audio_from_video(self, video_path):
        video_clip = VideoFileClip(video_path) 


        output_path_folder,updated_video_path = self.fo.initialize(video_path)
        output_path = os.path.join(output_path_folder, self.fo.get_file_name_without_extension_from_path(video_path) + ".mp3")
        # Load the video clip

        # Extract the audio
        audio_clip = video_clip.audio
        
        # Save the audio as WAV
        # No codec specification needed for WAV, but specifying for clarity or in case of issues
        audio_clip.write_audiofile(output_path)
        
        # Close the video and audio clips
        video_clip.close()
        audio_clip.close()
        return output_path
    def extract_audio_to_mp3(self, video_path):
        output_path_folder,updated_video_path = self.fo.initialize(video_path)
        output_path = os.path.join(output_path_folder, self.fo.get_file_name_without_extension_from_path(video_path) + ".mp3")

        # Load the video file
        input_file = ffmpeg.input(video_path)

        # Extract the audio and save it as an MP3 file
        input_file.output(output_path, acodec='mp3').overwrite_output().run()
        return output_path

if __name__ == "__main__":
    # Example usage:
    video_path = "output\small_talk\small_talk_translated.mp4"
    output_path = "output\small_talk\small_talk_translated.mp3"

    ae = AudioExtractor()
    ae.extract_audio_to_mp3(video_path, output_path)
