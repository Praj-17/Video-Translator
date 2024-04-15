from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip,TextClip, AudioFileClip
from moviepy.video.tools.subtitles import SubtitlesClip
import os
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_audioclips
from moviepy.audio.AudioClip import AudioClip



class VideoAttacherAndSubtitler:
    def __init__(self) -> None:
        pass

    def attach_audio_to_video(self, video_path, audio_path, output_path):
        video_clip = VideoFileClip(video_path)
        audio_clip = VideoFileClip(audio_path)
        
        if audio_clip.duration < video_clip.duration:
            silence_duration = video_clip.duration - audio_clip.duration
            silent_audio = audio_clip.subclip(0, 0).set_duration(silence_duration)
            audio_clip = concatenate_videoclips([audio_clip, silent_audio])
        
        video_clip = video_clip.set_audio(audio_clip)
        
        video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=60)
        
        video_clip.close()

        return output_path

    def create_subtitles_clip(self, srt_file):
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

            text_clips = [TextClip(line, font='Arial-Bold', fontsize=28, color='yellow', stroke_color='black', stroke_width=2, method='caption').on_color(size=(TextClip(line, font='Arial-Bold', fontsize=28, color='yellow', method='caption').size[0]+30, TextClip(line, font='Arial-Bold', fontsize=28, color='yellow', method='caption').size[1]+20), color=(0,0,0), pos=('center','center'), col_opacity=0.8) for line in lines]

            subtitles_clip = concatenate_videoclips(text_clips, method="compose")

            return subtitles_clip

        subtitles = SubtitlesClip(srt_file, generator)
        return subtitles
        # Function to create subtitles clip with custom styling
    def create_subtitles_clip_2(self, srt_file):
        # Generate a lambda function to attach subtitles using TextClip with custom styling
        generator = lambda txt: TextClip(txt, 
                                        font='Arial-Bold', 
                                        fontsize=28, 
                                        color='yellow', 
                                        stroke_color='black', 
                                        stroke_width=2, 
                                        method='caption'). \
                                        on_color(size=(TextClip(txt, 
                                                                font='Arial-Bold', 
                                                                fontsize=28, 
                                                                color='yellow', 
                                                                method='caption').size[0]+200, 
                                                        max(TextClip(txt, 
                                                                    font='Arial-Bold', 
                                                                    fontsize=28, 
                                                                    color='yellow', 
                                                                    method='caption').size[1], 1)), 
                                                color=(0,0,0), 
                                                pos=('center','center'), 
                                                col_opacity=0.8)

        # Create a subtitles clip
        subtitles = SubtitlesClip(srt_file, generator)
        return subtitles




    def add_subtitles_and_audio_to_video(self, video_path, audio_path, srt_file, output_path):
        print("Video Path:", video_path)
        print("Audio Path:", audio_path)
        print("SRT file:", srt_file)
        print("Output path:", output_path)

        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)

        if audio_clip.duration < video_clip.duration:
            silence_duration = video_clip.duration - audio_clip.duration
            # Generate silent audio segment
            silent_audio = AudioClip(lambda t: [0] * audio_clip.nchannels, duration=silence_duration, fps=audio_clip.fps)
            # Concatenate audio clip with silent audio to match the video's duration
            audio_clip = concatenate_audioclips([audio_clip, silent_audio])

        video_clip = video_clip.set_audio(audio_clip)

        subtitles = self.create_subtitles_clip_2(srt_file)

        final_video = CompositeVideoClip([video_clip, subtitles.set_position(('center', 'bottom'))])

        final_video.write_videofile(output_path, codec='libx264', temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')

        video_clip.close()

        return output_path



    def add_subtitles_and_audio_to_video_2(self, video_path, audio_path, srt_file, output_path):
            
            print("Vidoe Path ", video_path)
            print("audio Path ", audio_path)
            print("srt file ", srt_file)
            print("output path", output_path)
            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(audio_path)
            
            if audio_clip.duration < video_clip.duration :
                silence_duration = video_clip.duration - audio_clip.duration
                silent_audio = AudioSegment.silent(duration=silence_duration)
                print(audio_clip, silent_audio)
                print(type(audio_clip), type(silent_audio))
                audio_clip = audio_clip + silent_audio
            
            video_clip = video_clip.set_audio(audio_clip)

            subtitles = self.create_subtitles_clip_2(srt_file)

            final_video = CompositeVideoClip([video_clip, subtitles.set_position(('center', 'bottom'))])

            final_video.write_videofile(output_path, codec='libx264', temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')
            
            video_clip.close()

            return output_path

if __name__ == "__main__":
    # Example usage
    video_file = r'output\small_talk\small_talk_translated.mp4'  # Path to your video file
    audio_file = r'path_to_audio_file.mp3'  # Path to your audio file
    srt_file = r'output\small_talk\corrected_srt.srt'  # Path to your SRT file
    output_file = r'output\small_talk\output_with_subtitles.mp4'  # Output path for the final video

    video_attacher_and_subtitler = VideoAttacherAndSubtitler()
    video_attacher_and_subtitler.add_subtitles_and_audio_to_video(video_file, audio_file, srt_file, output_file)
