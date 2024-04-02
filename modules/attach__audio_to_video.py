
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips


class VideoAttacher():
    def attach_audio_to_video(self, video_path, audio_path, output_path):
        # Load video and audio clips
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        
        # Extend the audio clip if it's shorter than the video
        if audio_clip.duration < video_clip.duration:
            silence_duration = video_clip.duration - audio_clip.duration
            silent_audio = AudioFileClip(
                audio_path, fps=audio_clip.fps).subclip(0, 0).set_duration(silence_duration)
            audio_clip = concatenate_audioclips([audio_clip, silent_audio])
        
        # Set audio clip to replace the original audio of the video
        video_clip = video_clip.set_audio(audio_clip)
        
        # Write the modified video clip with the attached audio
        fps = 60
        video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps = fps)
        
        # Close the clips
        video_clip.close()
        return  output_path

if __name__ == "__main__":
    # Example usage:
    video_path = "demo_3.mp4"
    audio_path =  "demo3/merged.mp3"
    output_path = "demo4_translated.mp4"
    video_attacher = VideoAttacher()
    video_attacher.attach_audio_to_video(video_path, audio_path, output_path)
