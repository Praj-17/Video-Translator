
from modules import AudioExtractor
from modules import FileOrganizer
from modules import TrascribeSRT
from modules import SRTToAudioConverter
from modules import MP3Merger
from modules import SRTCorrecter
from modules import VideoAttacherAndSubtitler
import os

class VideoTranslator:
    def __init__(self) -> None:
       self.audio_extractor = AudioExtractor()
       self.file_organizer = FileOrganizer()
       self.transcriber = TrascribeSRT()
       self.audio_generator = SRTToAudioConverter()
       self.mp3_merger = MP3Merger()
       self.audio_attacher_and_subtitler = VideoAttacherAndSubtitler()
       self.correcter = SRTCorrecter()


    def translate(self, path_to_video, voice_type = 0):
        print("Video Recieved", path_to_video)
        output_path_folder = self.file_organizer.initialize(path_to_video)
        output_path = os.path.join(output_path_folder, self.file_organizer.get_file_name_without_extension_from_path(path_to_video) + ".mp3")
        output_path_video = os.path.join(output_path_folder, self.file_organizer.get_file_name_without_extension_from_path(path_to_video) + "_translated" +  ".mp4")


        # #Step 1 is to extract the audio
        output_path = self.audio_extractor.extract_audio_to_mp3(path_to_video, output_path)

        # # Step 2 Transcribe the audio
        srt_file = self.transcriber.mp3_to_translated_srt(output_path) 

            # Step-3 Convert SRT files to Audio
        output_folder, initial_silence = self.audio_generator.convert_srt_to_audio(srt_file, output_path_folder, voice_type= 0) 
            
        
        # Step-4 Merge all mp3 files
        merged_file = self.mp3_merger.merge_wav_files_with_silence(initial_silence, output_folder, srt_file)

        # Step-5 Correct the SRT file to be able to parse it
        corrected_srt   = self.correcter.correct_srt_timestamps(srt_file)

        # Step-5 Attach new audio to video
        # translated_video = self.video_attacher.attach_audio_to_video(path_to_video, merged_file, output_path_video)



        #Step=6 Add Subtitles to the video
        # final_video = self.subtitle_adder.add_subtitles_to_video(video_file=translated_video, srt_file = corrected_srt)

        #Attach new audio to video and also the subtitles
        final_video = self.audio_attacher_and_subtitler.add_subtitles_and_audio_to_video(path_to_video, merged_file, corrected_srt, output_path_video)

        return final_video

if __name__ == "__main__": 

    path_to_video = r"n2.mp4"
    
    trans = VideoTranslator()

    trans.translate(path_to_video)


