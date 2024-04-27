import speech_recognition as sr
import wave
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from .time_parser import TimeParser
from .srt_parser import SRTParser
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()





class TempoAnalyzer:
    def __init__(self) -> None:
        self.tp = TimeParser()
        self.srt = SRTParser()
        self.r = sr.Recognizer()
    def get_audio_length(self, audio_file_path):
        with wave.open(audio_file_path, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration_seconds = frames / float(rate)
        return duration_seconds




    def calculate_wpm_for_segments(self, audio_file_path, segment_length_sec=30):
        audio_length_seconds = self.get_audio_length(audio_file_path)
        segment_starts = np.arange(0, audio_length_seconds, segment_length_sec)
        wpms = []
        
        # Initialize the recognizer
        
        
        for start in segment_starts:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.r.record(source, duration=segment_length_sec, offset=start)
            try:
                # Recognize the speech using Google Web Speech API
                text = self.r.recognize_google(audio)
            
                words = text.split()
                num_words = len(words)
                wpm = num_words / (segment_length_sec / 60)  # Convert segment length to minutes
                wpms.append(wpm)
            except (sr.UnknownValueError, sr.RequestError):
                wpms.append(0)  # Assume 0 WPM if the speech could not be recognized or there was an error
        
        return segment_starts, wpms
    def count_words_per_minute(self, srt_path):
        """
        Aggregates text from subtitles within 1-minute windows and counts words.
        
        Args:
        subtitles (list of dicts): Each dictionary has 'start', 'end', and 'text' keys.
        
        Returns:
        list of tuples: Each tuple contains (minute, word_count).
        """
        # Initialize data structures
        word_counts = {}
        subtitles = self.srt.extract_all_subtitle_info(srt_path)
        for subtitle in subtitles:
            start_seconds = self.tp.total_seconds_from_corrected_srt(subtitle['start'])
            text = subtitle['text']
            minute = int(start_seconds // 60)  # find which minute the subtitle belongs to
            
            # Accumulate words by minutes
            if minute in word_counts:
                word_counts[minute] += len(text.split())
            else:
                word_counts[minute] = len(text.split())
        
        return word_counts
    def alert_if_wpm_too_high(self, wpms, threshold, duration_seconds, segment_length_sec):
        consecutive_time = 0
        for wpm in list(wpms.values()):
            if wpm > threshold:
                consecutive_time += segment_length_sec
                if consecutive_time > duration_seconds:
                    # Using Tkinter for the alert dialog
                    root = tk.Tk()
                    root.withdraw()  # Hide the main window
                    messagebox.showwarning("Slow Down", "You need to speak slower!")
                    break
            else:
                consecutive_time = 0  # Reset if the WPM falls below the threshold

    def plot_wpm_over_time_with_matplotlib(self, srt_path, threshold=os.getenv("words_per_minute_threshold")):
        wpms = self.count_words_per_minute(srt_path)
        print(wpms)
        plt.figure(figsize=(10, 6))
        plt.plot(wpms.keys(),wpms.values(), marker='o', label='WPM')
        plt.axhline(y=threshold, color='r', linestyle='--', label='Threshold')
        
        plt.title('Words Per Minute Over Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Words Per Minute (WPM)')
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
# Example usage
    temp = TempoAnalyzer()
    audio_file_path = "C:\\Users\\TI-SJL-0010\\Desktop\\Pitch and Tempo\\Python Pitch and Tempo\\Small Talk.wav"  
    temp.plot_wpm_over_time_with_matplotlib(audio_file_path)






