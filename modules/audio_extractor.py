from moviepy.editor import VideoFileClip
import os

class AudioExtractor():
    def __init__(self) -> None:
        
        pass
    def extract_audio_to_mp3(self, video_path, output_path):
        # Load the video clip
        video_clip = VideoFileClip(video_path)

        # Extract the audio
        audio_clip = video_clip.audio
        
        # Save the audio as WAV
        # No codec specification needed for WAV, but specifying for clarity or in case of issues
        audio_clip.write_audiofile(output_path)
        
        # Close the video and audio clips
        video_clip.close()
        audio_clip.close()
        return output_path

if __name__ == "__main__":
    # Example usage:
    video_path = "output\small_talk\small_talk_translated.mp4"
    output_path = "output\small_talk\small_talk_translated.mp3"

    ae = AudioExtractor()
    ae.extract_audio_to_mp3(video_path, output_path)
