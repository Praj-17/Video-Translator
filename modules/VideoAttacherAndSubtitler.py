from moviepy.editor import (
    VideoFileClip,
    CompositeVideoClip,
    TextClip,
    AudioFileClip,
    concatenate_audioclips,
    AudioClip,
)
from moviepy.video.tools.subtitles import SubtitlesClip
import os
from modules.file_organizer import FileOrganizer


class VideoAttacherAndSubtitler:
    def __init__(self):
        self.fo = FileOrganizer()

    def attach_audio_to_video(self, video_path, audio_path, output_path):
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)

        # Ensure audio duration matches video duration
        if audio_clip.duration < video_clip.duration:
            silence_duration = video_clip.duration - audio_clip.duration
            silent_audio = AudioClip(
                lambda t: [0] * audio_clip.nchannels,
                duration=silence_duration,
                fps=audio_clip.fps,
            )
            audio_clip = concatenate_audioclips([audio_clip, silent_audio])
        else:
            audio_clip = audio_clip.subclip(0, video_clip.duration)

        video_clip = video_clip.set_audio(audio_clip)
        video_clip.write_videofile(
            output_path, codec="libx264", audio_codec="aac", fps=60
        )
        video_clip.close()
        audio_clip.close()
        return output_path
    def create_subtitles_clip(self, srt_file, video_width, video_height):
        # Subtitles occupy full width
        subtitle_width = int(video_width)
        
        # Reduced font size for less obtrusive subtitles
        fontsize = 18  # Adjust as needed to reduce height further
        
        # Generator function to create TextClips with custom styling and wrapping
        def subtitle_generator(txt):
            # Set size to (subtitle_width - padding, None) to allow automatic height adjustment
            text_clip = TextClip(
                txt,
                font="Arial-Bold",
                fontsize=fontsize,
                color="yellow",
                stroke_color="black",
                stroke_width=1,
                method="caption",
                size=(subtitle_width - 40, None),  # Padding of 20 pixels on each side
                align="center",
            )
            # Create a semi-transparent background that spans the full width
            from moviepy.editor import ColorClip

            background = ColorClip(
                size=(subtitle_width, text_clip.h + 20),  # Padding of 10 pixels on top and bottom
                color=(0, 0, 0)
            ).set_opacity(0.7)
            
            # Composite the text over the background
            text_with_bg = CompositeVideoClip(
                [background, text_clip.set_position(("center", "center"))],
                size=(subtitle_width, text_clip.h + 20),
                bg_color=(0,0,0,0)  # Ensure the background is transparent outside the background clip
            )
            return text_with_bg

        subtitles = SubtitlesClip(srt_file, subtitle_generator)
        # Set position to bottom center
        subtitles = subtitles.set_position(("center", "bottom"))
        return subtitles



    def add_subtitles_and_audio_to_video(self, video_path, audio_path, srt_file):
        output_path_folder = os.path.dirname(audio_path)
        output_path = os.path.join(
            output_path_folder,
            self.fo.get_file_name_without_extension_from_path(video_path)
            + "_translated.mp4",
        )

        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)

        # Ensure audio duration matches video duration
        if audio_clip.duration < video_clip.duration:
            silence_duration = video_clip.duration - audio_clip.duration
            silent_audio = AudioClip(
                lambda t: [0] * audio_clip.nchannels,
                duration=silence_duration,
                fps=audio_clip.fps,
            )
            audio_clip = concatenate_audioclips([audio_clip, silent_audio])
        else:
            audio_clip = audio_clip.subclip(0, video_clip.duration)

        video_clip = video_clip.set_audio(audio_clip)

        # Create subtitles clip with proper width and height
        subtitles = self.create_subtitles_clip(srt_file, video_clip.w, video_clip.h)

        # Composite the video with subtitles
        final_video = CompositeVideoClip([video_clip, subtitles])

        final_video.write_videofile(
            output_path,
            codec="libx264",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            audio_codec="aac",
        )

        video_clip.close()
        audio_clip.close()
        final_video.close()

        return output_path


if __name__ == "__main__":
    # Example usage
    video_file = r"D:\Video-Translator\videos\test.mp4"  # Path to your video file
    audio_file = r"D:\Video-Translator\output\test\test.mp3"  # Path to your audio file
    srt_file = r"D:\Video-Translator\output\test_medium\corrected_srt.srt"  # Path to your SRT file
    output_file = r"output_with_subtitles.mp4"  # Output path for the final video

    video_attacher_and_subtitler = VideoAttacherAndSubtitler()
    video_attacher_and_subtitler.add_subtitles_and_audio_to_video(
        video_file, audio_file, srt_file
    )
