
from modules import AudioExtractor
from modules import FileOrganizer
from modules import TrascribeSRT
from modules import SRTToAudioConverter
from modules import MP3Merger
from modules import SRTCorrecter
from modules import VideoAttacherAndSubtitler
from modules import TempoAnalyzer
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
       self.tempo = TempoAnalyzer()


    def translate(self, path_to_video, voice_type = 0):
        # #Step 1 is to extract the audio
        print("Recieved: ",path_to_video)
        output_path_folder,updated_video_path = self.file_organizer.initialize(path_to_video)
        



        #get the mp3 file
        mp3_from_video = self.file_organizer.get_mp3_name_from_video_name(path_to_video)
        if not os.path.exists(mp3_from_video):
            mp3_from_video = self.audio_extractor.extract_audio_to_mp3(path_to_video)

         # Step 2 Transcribe the audio
        srt_file = self.file_organizer.get_srt_name_from_video_name(mp3_from_video)
        if not os.path.exists(srt_file):
                srt_file = self.transcriber.mp3_to_translated_srt(mp3_from_video)


        output_folder = self.file_organizer.get_audio_split_path(srt_file)
        intial_silence_path = self.file_organizer.get_initial_silence_output_path(srt_file)
        if not os.path.exists(output_folder) or  (not os.listdir(output_folder) and os.path.exists(output_folder)):
        # Step-3 Convert SRT files to Audio
            output_folder, intial_silence_path = self.audio_generator.convert_srt_to_audio(srt_file,voice_type= voice_type)
        

        merged_file = self.file_organizer.get_merged_file_name(path_to_video)
        if not os.path.exists(merged_file):
        # Step-4 Merge all mp3 files
            merged_file = self.mp3_merger.merge_wav_files_with_silence(intial_silence_path, output_folder, srt_file)


        corrected_srt = self.file_organizer.get_corrected_srt_name(path_to_video)
        if not os.path.exists(corrected_srt):
            # Step-5 Correct the SRT file to be able to parse it
            corrected_srt   = self.correcter.correct_srt_timestamps(srt_file)
        

        #Attach new audio to video and also the subtitles
        final_video = self.file_organizer.get_final_video_name(path_to_video)
        if not os.path.exists(final_video):
            final_video = self.audio_attacher_and_subtitler.add_subtitles_and_audio_to_video(path_to_video, merged_file, corrected_srt)

        return final_video
    def analyse_tempo(self, video_path):
        #Get srt_path_from_video_path
        print("Recieved: ",video_path)
        output_path_folder,updated_video_path = self.file_organizer.initialize(video_path)
        srt_name =  os.path.join(os.path.dirname(updated_video_path), os.getenv("corrected_srt_name"))
        self.tempo.plot_wpm_over_time_with_matplotlib(srt_name)

if __name__ == "__main__": 

    path_to_video = r"videos\test2.mp4"
    
    trans = VideoTranslator()

    trans.analyse_tempo(path_to_video)


