
import os
from modules.text_to_speech import TextToSpeech
from datetime import datetime
from .time_parser import TimeParser
from .srt_parser import SRTParser
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()



class SRTToAudioConverter():
    def __init__(self) -> None:
        self.tts = TextToSpeech()
        self.time_parser = TimeParser()
        self.srt_parser = SRTParser()
    def text_to_speech(self, text, output_file,desired_duration_seconds,  voice_type = 0):
        self.tts.text_to_speech_with_duration( text,desired_duration_seconds, output_file, voice_type = voice_type)

    def convert_srt_to_audio(self, srt_file, voice_type):
        output_folder = os.path.dirname(srt_file)
        subs =self.srt_parser.extract_all_subtitle_info(srt_file=srt_file)
        # Add an extra folder to better organize the audio files
        output_folder = os.path.join(output_folder, os.getenv("default_audio_split_files_folder_name"))
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, f'subtitle_{0}.wav')
        initial_silence_output_path = os.path.join(output_folder, os.getenv("default_initial_silence_save_name"))

        start_time, end_time, text_first =  self.srt_parser.extract_first_subtitle_info(srt_file)
        if start_time != '00:00:00':
            #return the when will the iniital audio start
            start_time = self.time_parser.add_miliseconds(start_time)
            start_time = datetime.strptime(start_time, '%H:%M:%S.%f')
            initial_silence = (start_time.hour * 3600 + start_time.minute * 60 + start_time.second + start_time.microsecond / 1000000.0)*1000
        else:
            initial_silence = 0.0
        
        with open(initial_silence_output_path,mode='w', encoding = "utf-8") as initial_silence_file:
            initial_silence_file.write(initial_silence)

        


        # self.text_to_speech(text_first, output_file, self.time_parser.calculate_duration_precise(start_time, end_time),voice_type=voice_type)
        for i, sub in enumerate(subs):
            # print(sub.start, sub.end, type(sub.start))
            # start_time = self.convert_subrip_time_to_str(sub.start)
            # end_time = self.convert_subrip_time_to_str(sub.end)
            text = sub.get("text")
            start_time = sub.get("start")
            end_time = sub.get("end")
            output_file = os.path.join(output_folder, f'subtitle_{i+1}.wav')
            
            if text  != "":
            # Convert text to speech
                self.text_to_speech(text, output_file, self.time_parser.calculate_duration_precise(start_time, end_time),voice_type=voice_type)
        return output_folder , initial_silence_output_path
    


if __name__ == "__main__":

    # Example usage:
    srt_file = 'es_3.srt'
    output_folder = 'demo3'
    os.makedirs(output_folder, exist_ok=True)
    srt_to_audio = SRTToAudioConverter()
    srt_to_audio.__getattribute__convert_srt_to_audio(srt_file, output_folder)


