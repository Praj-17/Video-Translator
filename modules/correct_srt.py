import re
import os
import pysubs2
from .time_parser import TimeParser
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class SRTCorrecter:
    def __init__(self) -> None:
        self.time_parser = TimeParser()
    def convert_srt_to_ssa(self, srt_file):
        output_file = srt_file.split(".")[0] + ".ass"
        subs = pysubs2.load(srt_file)
        subs.save(output_file, format='ass')  # Save as ASS format  # Save as SRT format
    def correct_srt_timestamps(self, input_srt_path):
        # A regex pattern to identify timestamp lines and replace '.' with ',' in timestamps
        output_file = os.path.join(os.path.dirname(input_srt_path), os.getenv("corrected_srt_name"))
        
        with open(input_srt_path, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                # Check if the line contains a timestamp
                if '-->' in line:
                    parts = line.split("-->")
                    start, end = parts[0].strip(), parts[1].strip()
                    start, end = self.time_parser.add_miliseconds(start), self.time_parser.add_miliseconds(end)
                    corrected_line = start + " --> " + end + "\n"
                    corrected_line = corrected_line.replace(".", ",")
                    outfile.write(corrected_line)
                else:
                    outfile.write(line)




            # Open the output file again to remove the last empty newline character
        with open(output_file, 'r+', encoding='utf-8') as outfile:
            content = outfile.readlines()
            if content[-1] == '\n':  # Check if the last line is an empty newline
                outfile.seek(0)  # Go to the beginning of the file
                outfile.writelines(content[:-1])  # Write back all but the last line
                outfile.truncate()
        output_file_ass = self.convert_srt_to_ssa(output_file)
        return output_file_ass

if __name__ == "__main__":
    corecter = SRTCorrecter()

    input_srt_path = r'output\small_talk\es.srt'  # Path to your original SRT file

    corecter.correct_srt_timestamps(input_srt_path)
