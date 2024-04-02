from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import concatenate_videoclips
import os
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()




class SubtitleAdder:
    def __init__(self) -> None:
        pass
    def create_subtitles_clip(self, srt_file):
        # Generate a lambda function to attach subtitles with a maximum of 10 words per line
        def generator(txt):
            words = txt.split()
            lines = []
            current_line = ''
            for word in words:
                if len(current_line.split()) < 10:
                    current_line += ' ' + word
                else:
                    lines.append(current_line.strip())
                    current_line = word
            if current_line:
                lines.append(current_line.strip())

            # Create TextClip objects for each line
            text_clips = [TextClip(line, font='Arial-Bold', fontsize=28, color='yellow', stroke_color='black', stroke_width=2, method = 'caption').on_color(size=(TextClip(line, font='Arial-Bold', fontsize=28, color='yellow', method = 'caption').size[0]+30, TextClip(line, font='Arial-Bold', fontsize=28, color='yellow', method = 'caption').size[1]+20), color=(0,0,0), pos=('center','center'), col_opacity=0.8) for line in lines]

            # Concatenate the TextClip objects into a single clip
            subtitles_clip = concatenate_videoclips(text_clips, method="compose")
                # Create a subtitles clip
            return subtitles_clip
        subtitles = SubtitlesClip(srt_file, generator)
        return subtitles


    # Function to create subtitles clip with custom styling
    def create_subtitles_clip(self, srt_file):
        # Generate a lambda function to attach subtitles using TextClip with custom styling
        generator = lambda txt: TextClip(txt, font='Arial-Bold', fontsize=28, color='yellow', stroke_color='black', stroke_width=2, method = 'caption').on_color(size=(TextClip(txt, font='Arial-Bold', fontsize=28, color='yellow', method = 'caption').size[0]+30, TextClip(txt, font='Arial-Bold', fontsize=28, color='yellow', method = 'caption').size[1]+20), color=(0,0,0), pos=('center','center'), col_opacity=0.8)

        # Create a subtitles clip
        subtitles = SubtitlesClip(srt_file, generator)
        return subtitles

    # Main function to add styled subtitles to video
    def add_subtitles_to_video(self, video_file, srt_file):
        video = VideoFileClip(video_file)
        subtitles = self.create_subtitles_clip(srt_file)

        output_file = os.path.join(os.path.dirname(video_file), os.getenv("final_output_file_name"))
        # Overlay the subtitles on the original video
        final_video = CompositeVideoClip([video, subtitles.set_position(('center', 'bottom'))])
        # Write the result to a file
        final_video.write_videofile(output_file, codec='libx264', temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')
        return output_file

if __name__ == "__main__":
    # Example usage
    video_file = r'output\small_talk\small_talk_translated.mp4'  # Path to your video file
    srt_file = r'output\small_talk\corrected_srt.srt'  # Path to your SRT file\

    subtitler = SubtitleAdder()


    subtitler.add_subtitles_to_video(video_file, srt_file)
