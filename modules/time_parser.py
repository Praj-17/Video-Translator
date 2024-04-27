from datetime import datetime
import re
class TimeParser():
    def __init__(self) -> None:
        pass
    def convert_subrip_time_to_str(self, sub_time):
        # Assuming you have your time duration stored in a variable

        # Convert to a string in the desired format
        converted_time = "{:02d}:{:02d}:{:02d}.{:02d}".format(
            sub_time.hours, sub_time.minutes, sub_time.seconds, int(sub_time.milliseconds / 10)
)       
        return converted_time
    def parse_srt_time(self, time_string):
        parts = time_string.split(" --> ")
        if len(parts) != 2:
            raise ValueError("Invalid time format in SRT file")
        start, end = parts
        start = self.convert_srt_time_to_seconds(start.strip())
        end = self.convert_srt_time_to_seconds(end.strip())
        return start, end
    def calculate_duration_precise(self, start:str, end:str):
        start = self.convert_srt_time_to_seconds(start.strip())
        end = self.convert_srt_time_to_seconds(end.strip())
        return end-start
    def total_seconds_from_corrected_srt(self, timestr):
        """Converts a time string 'HH:MM:SS,mmm' to total seconds."""
        hours, minutes, seconds = re.split('[:]', timestr)
        seconds, milliseconds = re.split('[,]', seconds)
        total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000000
        return total_seconds
    def convert_srt_time_to_seconds(self, time_string):
        time_components = time_string.split(":")
        hours = int(time_components[0])
        minutes = int(time_components[1])
        seconds = float(time_components[2])
        
        total_seconds = hours * 3600 + minutes * 60 + seconds 
        return total_seconds
    def convert_subrip_time_to_str(self, sub_time):
        # Assuming you have your time duration stored in a variable

        # Convert to a string in the desired format
        converted_time = "{:02d}:{:02d}:{:02d}.{:02d}".format(
            sub_time.hours, sub_time.minutes, sub_time.seconds, int(sub_time.milliseconds / 10)
)       
        return converted_time
    def calculate_duration(self, start_time_str, end_time_str):


        start_time_str = self.add_miliseconds(start_time_str)
        end_time_str = self.add_miliseconds(end_time_str)
        


        # Convert start and end time strings to datetime objects
        start_time = datetime.strptime(start_time_str, '%H:%M:%S.%f')
        end_time = datetime.strptime(end_time_str, '%H:%M:%S.%f')

        # Calculate duration
        duration = end_time - start_time
        total_seconds = duration.total_seconds()
        # Return duration as a timedelta object
        # Format to show exactly 10 decimal places
        # or using an f-string

        return total_seconds
    def add_miliseconds(self, time, sep = "."):
        split = time.split(sep)
        if not len(split) > 1:
            time = time +  sep + "00"
        return time