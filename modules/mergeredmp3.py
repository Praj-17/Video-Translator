
import os
from os.path import join
import shutil
from pydub import AudioSegment
from pydub import AudioSegment
from pydub.utils import which
from .time_parser import TimeParser
AudioSegment.converter = which("ffmpeg")


class MP3Merger():
    def __init__(self) -> None:
        self.time_parser = TimeParser()
    def merge_mp3_files(self, folder_path):
        # Collect all mp3 files in the folder
        mp3_files = [file for file in os.listdir(folder_path) if file.endswith('.mp3')]
        parent_folder = os.path.dirname(folder_path)
        if not mp3_files:
            print("No mp3 files found in the folder.")
            return
        
        # Sort the mp3 files alphabetically
        mp3_files.sort()
        
        # Create a destination file to merge into
        destination_file = join(parent_folder, os.getenv("default_merged_file_name"))
        
        with open(destination_file, 'wb', errors = "replace") as dest:
            for mp3_file in mp3_files:
                mp3_file_path = join(folder_path, mp3_file)
                with open(mp3_file_path, 'rb', errors = "replace") as src:
                    shutil.copyfileobj(src, dest)
        

        return destination_file
    def merge_wav_files_with_silence(self, initial_silence_output_path, folder_path, srt_file):
        wav_files = [file for file in os.listdir(folder_path) if file.endswith('.wav')]
        parent_folder = os.path.dirname(folder_path)
        if not wav_files:
            print("No WAV files found in the folder.")
            return
        wav_files = self.sort_files_in_sequence(wav_files)
        destination_file = os.path.join(parent_folder, os.getenv("default_merged_file_with_silence_name"))

        #Load the initial_silence
        with open(initial_silence_output_path,mode='r', encoding = "UTF-8", errors = "replace") as initial_silence_file:
           initial_silence =  float((initial_silence_file.read()).strip())

        final_audio = AudioSegment.silent(duration=initial_silence)

        lines = self.parse_srt_file(srt_file)
        for i in range(0, len(wav_files)):
            wav_file_path = os.path.join(folder_path, wav_files[i])
            try:
                audio = AudioSegment.from_file(wav_file_path, format="wav")
            except:
                print(f"Error loading {wav_file_path}, attempting as 'wav' format.")
                audio = AudioSegment.from_file(wav_file_path, format="wav")  # Kept for compatibility; not needed for wav
            if i < len(lines):
                if " --> " in lines[i]:
                    start, end = self.time_parser.parse_srt_time(lines[i])
                    if i+1 < len(wav_files):
                        next_start, _ = self.time_parser.parse_srt_time(lines[i+1])

                        silence_duration = (next_start - end) * 1000
                        if silence_duration > 0:
                            silence = AudioSegment.silent(duration=int(silence_duration))
                            final_audio += audio + silence
                        else:
                            final_audio += audio
                    else:
                        final_audio += audio
                else:
                    pass
            else:
                final_audio += audio
        final_audio.export(destination_file, format="wav")
        return destination_file



    def parse_srt_file(self, file_path):
        with open(file_path, 'r', encoding='UTF-8', errors = "replace") as file:
            lines_with_timestamps = []
            lines = file.readlines()
            lines_with_timestamps = [line for line in lines if " --> " in line]
        return lines_with_timestamps

    
    def sort_files_in_sequence(self, file_paths):
    # Function to extract the numeric part from a filename
        def extract_number(file_path):
            filename = os.path.basename(file_path)
            return int(filename.split("_")[-1].split(".")[0])

        # Sort the list of file paths using the custom sorting function
        return  sorted(file_paths, key=extract_number)
        



if __name__ == "__main__":
    # Example usage:
    merger = MP3Merger()
    folder_name = r"output\ai\audio_files"
    merger.merge_mp3_files_with_silence(folder_name, r"output\ai\es.srt")
