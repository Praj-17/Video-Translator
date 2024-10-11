
from modules import AudioExtractor
from modules import FileOrganizer
from modules import TranscribeSRT
from modules import SRTToAudioConverter
from modules import MP3Merger
from modules import SRTCorrecter
from modules import VideoAttacherAndSubtitler           
# from modules import TempoAnalyzer
# from modules import PitchAnalyzer
import os

class VideoTranslator:
    def __init__(self) -> None:
       self.audio_extractor = AudioExtractor()
       self.file_organizer = FileOrganizer()
       self.transcriber = TranscribeSRT()
       self.audio_generator = SRTToAudioConverter()
       self.mp3_merger = MP3Merger()
       self.audio_attacher_and_subtitler = VideoAttacherAndSubtitler()
       self.correcter = SRTCorrecter()
    #    self.tempo = TempoAnalyzer()
    #    self.pitch_analyzer = PitchAnalyzer()

    def transcribe_given_video(self, path_to_video, source_language = "en"):
        # #Step 1 is to extract the audio
        output_path_folder,updated_video_path = self.file_organizer.initialize(path_to_video)
        



        #get the mp3 file
        mp3_from_video = self.file_organizer.get_mp3_name_from_video_name(path_to_video)
        if not os.path.exists(mp3_from_video):
            print(mp3_from_video, "does not exist") 
            mp3_from_video = self.audio_extractor.extract_audio_to_mp3(path_to_video)

        srt_path = self.transcriber.transcribe_only(mp3_from_video,source_language )
        return srt_path

    def translate(self, path_to_video, voice_type = 1, source_language = "en", destination_language = "es", audio = False, attach = False):
        # #Step 1 is to extract the audio
        output_path_folder,updated_video_path = self.file_organizer.initialize(path_to_video)
        



        #get the mp3 file
        mp3_from_video = self.file_organizer.get_mp3_name_from_video_name(path_to_video)
        if not os.path.exists(mp3_from_video):
            mp3_from_video = self.audio_extractor.extract_audio_to_mp3(path_to_video)
        final_video = self.file_organizer.get_final_video_name(path_to_video)
        if source_language == destination_language:
             srt_path = self.transcriber.transcribe_only(mp3_from_video,source_language )
        else:
            # Step 2 Transcribe the audio
            srt_file = self.file_organizer.get_srt_name_from_video_name(mp3_from_video)
            print(mp3_from_video, srt_file)
            if not os.path.exists(srt_file):
                    srt_file = self.transcriber.mp3_to_translated_srt(mp3_from_video, destination_language, source_language)
            corrected_srt = self.file_organizer.get_corrected_srt_name(path_to_video)
            if not os.path.exists(corrected_srt):
                    # Step-5 Correct the SRT file to be able to parse it
                    corrected_srt   = self.correcter.correct_srt_timestamps(srt_file)
            if audio:

                output_folder = self.file_organizer.get_audio_split_path(srt_file)
                intial_silence_path = self.file_organizer.get_initial_silence_output_path(srt_file)
                if not os.path.exists(output_folder) or  (not os.listdir(output_folder) and os.path.exists(output_folder)):
                # Step-3 Convert SRT files to Audio
                    output_folder, intial_silence_path = self.audio_generator.convert_srt_to_audio(srt_file,voice_type= voice_type)
                
                
                

                merged_file = self.file_organizer.get_merged_file_name(path_to_video)
                if not os.path.exists(merged_file):
                # Step-4 Merge all mp3 files
                    merged_file = self.mp3_merger.merge_wav_files_with_silence(intial_silence_path, output_folder, srt_file)
                if attach:
                    if not os.path.exists(final_video):
                        return self.audio_attacher_and_subtitler.add_subtitles_and_audio_to_video(path_to_video, merged_file, corrected_srt)
            else:

                #Attach new audio to video and also the subtitles
                if attach:
                    if not os.path.exists(final_video):
                        return self.audio_attacher_and_subtitler.add_subtitles_and_audio_to_video(path_to_video, mp3_from_video, corrected_srt)

        return corrected_srt
    def analyse_tempo(self, video_path):
        #Get srt_path_from_video_path
        output_path_folder,updated_video_path = self.file_organizer.initialize(video_path)
        srt_name =  self.file_organizer.get_corrected_srt_name(updated_video_path)

        #Case when the srt file has not been genrated, generate it first!
        if not os.path.exists(srt_name):
               srt_name =  self.prepare_metadata_till_corrected_srt(video_path)

                  
        self.tempo.plot_wpm_over_time_with_matplotlib(srt_name)
    
    def prepare_metadata_till_mp3(self, video_path):
        output_path_folder,updated_video_path = self.file_organizer.initialize(video_path)
        #get the mp3 file
        mp3_from_video = self.file_organizer.get_mp3_name_from_video_name(video_path)
        if not os.path.exists(mp3_from_video):
            mp3_from_video = self.audio_extractor.extract_audio_to_mp3(video_path)
        return mp3_from_video
    
    def prepare_metadata_till_corrected_srt(self, video_path):
        output_path_folder,updated_video_path = self.file_organizer.initialize(video_path)
                #get the mp3 file
        mp3_from_video = self.file_organizer.get_mp3_name_from_video_name(path_to_video)
        if not os.path.exists(mp3_from_video):
            mp3_from_video = self.audio_extractor.extract_audio_to_mp3(path_to_video)


         # Step 2 Transcribe the audio
        srt_file = self.file_organizer.get_srt_name_from_video_name(mp3_from_video)
        if not os.path.exists(srt_file):
                srt_file = self.transcriber.mp3_to_translated_srt(mp3_from_video)
        
        corrected_srt = self.file_organizer.get_corrected_srt_name(path_to_video)
        if not os.path.exists(corrected_srt):
            # Step-5 Correct the SRT file to be able to parse it
            corrected_srt   = self.correcter.correct_srt_timestamps(srt_file)
        return corrected_srt

    def analyze_pitch(self, video_path):
        output_path_folder,updated_video_path = self.file_organizer.initialize(video_path)
        mp3_from_video = self.file_organizer.get_mp3_name_from_video_name(updated_video_path)

        if not os.path.exists(mp3_from_video):
             mp3_from_video = self.prepare_metadata_till_mp3(video_path)
        self.pitch_analyzer.plot_pitch(mp3_from_video)     


if __name__ == "__main__": 

    path_to_video = r"videos\test.mp4"
    
    trans = VideoTranslator()
    trans.translate(path_to_video, audio = False, attach=True)


