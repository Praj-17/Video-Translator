
from modules import AudioExtractor
from modules import FileOrganizer
from modules import TrascribeSRT
from modules import SRTToAudioConverter
from modules import MP3Merger
from modules import VideoAttacher
from modules import SRTCorrecter
from modules import SubtitleAdder
import os


audio_extractor = AudioExtractor()
file_organizer = FileOrganizer()
transcriber = TrascribeSRT()
audio_generator = SRTToAudioConverter()
mp3_merger = MP3Merger()
video_attacher = VideoAttacher()
correcter = SRTCorrecter()
subtitle_adder = SubtitleAdder()
if __name__ == "__main__": 

    path_to_video = r"test`.mp4"
   
    output_path_folder = file_organizer.initialize(path_to_video)
    output_path = os.path.join(output_path_folder, file_organizer.get_file_name_without_extension_from_path(path_to_video) + ".mp3")
    output_path_video = os.path.join(output_path_folder, file_organizer.get_file_name_without_extension_from_path(path_to_video) + "_translated" +  ".mp4")




    # #Step 1 is to extract the audio
    # output_path = audio_extractor.extract_audio_to_mp3(path_to_video, output_path)

    # # Step 2 Transcribe the audio
    # srt_file = transcriber.mp3_to_translated_srt(output_path) 

    srt_file = r"output\test\es.srt"

    # Step-3 Convert SRT files to Audio
    output_folder, initial_silence = audio_generator.convert_srt_to_audio(srt_file, output_path_folder, voice_type= 0) 
        
    
    # Step-4 Merge all mp3 files
    merged_file = mp3_merger.merge_wav_files_with_silence(initial_silence, output_folder, srt_file)

    # Step-5 Attach new audio to video
    translated_video = video_attacher.attach_audio_to_video(path_to_video, merged_file, output_path_video)

    # Step-5 Correct the SRT file to be able to parse it
    corrected_srt_ass   = correcter.correct_srt_timestamps(srt_file)

    #Step=6 Add Subtitles to the video
    final_video = subtitle_adder.add_subtitles_to_video(video_file=r"output\test\test_translated.mp4", srt_file = r"output\test\corrected_srt.srt")


