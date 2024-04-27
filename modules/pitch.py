import numpy as np
import matplotlib.pyplot as plt
import wave
from pydub import AudioSegment
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()
# Parameters
CHUNK = int(os.getenv("CHUNK"))  # Frame size
FORMAT = np.int16  # Data type for audio samples
RATE = int(os.getenv("RATE"))  # Sample rate

# Volume thresholds
VOLUME_THRESHOLD_LOW = int(os.getenv("VOLUME_THRESHOLD_LOW"))  # Threshold for low volume
VOLUME_THRESHOLD_HIGH = int(os.getenv("VOLUME_THRESHOLD_HIGH"))  # Threshold for high volume
VOLUME_ALERT_DURATION = int(os.getenv("VOLUME_ALERT_DURATION"))  # Seconds before alerting about sustained high/low volume
FREQUENCY_AVERAGE_INTERVAL = float(os.getenv("FREQUENCY_AVERAGE_INTERVAL"))  # Interval in seconds to average frequencies

class PitchAnalyzer:
    def __init__(self) -> None:
        self.CHUNK = 1024  # Frame size
        self.FORMAT = np.int16  # Data type for audio samples
        self.RATE = 44100  # Sample rate

        self.VOLUME_THRESHOLD_LOW = 100  # Threshold for low volume
        self.VOLUME_THRESHOLD_HIGH = 120  # Threshold for high volume
        self.VOLUME_ALERT_DURATION = 6  # Seconds before alerting about sustained high/low volume
        self.FREQUENCY_AVERAGE_INTERVAL = 6.1  # Interval in seconds to average frequencies
    def read_wav(self, filename):
        with wave.open(filename, 'rb') as wf:
            n_frames = wf.getnframes()
            data = wf.readframes(n_frames)
            samples = np.frombuffer(data, dtype=FORMAT)
        return samples, wf.getframerate()

    def rms(self, frame):
        if np.any(frame):  # Check if the frame is not all zeros
            sum_squares = np.sum(np.square(frame))
            return np.sqrt(sum_squares / len(frame))
        else:
            return 0
    def convert_mp3_to_wav(self, mp3_file_path):
        # Load the MP3 file
        audio = AudioSegment.from_mp3(mp3_file_path)
        output_path = os.path.join(os.path.dirname(mp3_file_path), os.getenv("default_audio_wav_save_name"))

        # Export the audio as a WAV file
        audio.export(output_path, format="wav")
        return output_path

    def calculate_frequencies(self, frame):
        n = len(frame)
        if n == 0:
            return np.array([]), np.array([])
        frequency = np.fft.rfftfreq(n, d=1./RATE)
        magnitude = np.abs(np.fft.rfft(frame)) / n
        return frequency, magnitude

    def process_wav_file(self, filename):
        audio_samples, framerate = self.read_wav(filename)
        num_frames = len(audio_samples) // CHUNK
        times = np.arange(num_frames) * (CHUNK / framerate)/120 #convert seconds to minutes
        volumes = np.array([self.rms(audio_samples[i * CHUNK:(i + 1) * CHUNK]) for i in range(num_frames)])
        frequencies = []
        frequency_times = []
        
        frame_indices_for_frequency_average = int(FREQUENCY_AVERAGE_INTERVAL * framerate / CHUNK)
        frame_aggregate_frequencies = np.zeros(int(CHUNK/2 + 1))


        # Calculate frequency data and store average frequencies
        for i in range(num_frames):
            frame = audio_samples[i * CHUNK:(i + 1) * CHUNK]
            _, mag = self.calculate_frequencies(frame)
            frame_aggregate_frequencies += mag

            if (i + 1) % frame_indices_for_frequency_average == 0:
                average_magnitude = np.mean(frame_aggregate_frequencies / frame_indices_for_frequency_average)
                frequencies.append(average_magnitude)
                frequency_times.append(times[i])
                frame_aggregate_frequencies = np.zeros(int(CHUNK/2 + 1))
        
        # Handling volume alerts for low and high periods
        volume_periods = {'low': [], 'high': []}
        start_time_low = start_time_high = None

        for i, volume in enumerate(volumes):
            if volume < VOLUME_THRESHOLD_LOW:
                if start_time_low is None:
                    start_time_low = times[i]
            else:
                if start_time_low is not None and times[i] - start_time_low >= VOLUME_ALERT_DURATION/120:
                    volume_periods['low'].append((start_time_low, times[i]))
                start_time_low = None

            if volume > VOLUME_THRESHOLD_HIGH:
                if start_time_high is None:
                    start_time_high = times[i]
            else:
                if start_time_high is not None and times[i] - start_time_high >= VOLUME_ALERT_DURATION/120:
                    volume_periods['high'].append((start_time_high, times[i]))
                start_time_high = None

        # Ensure the last period is added if it ends at the file end
        if start_time_low is not None and times[-1] - start_time_low >= VOLUME_ALERT_DURATION/120:
            volume_periods['low'].append((start_time_low, times[-1]))
        if start_time_high is not None and times[-1] - start_time_high >= VOLUME_ALERT_DURATION/120:
            volume_periods['high'].append((start_time_high, times[-1]))

        return times, volumes, frequencies, frequency_times, volume_periods
    def read_mp3(self, filename):
        audio = AudioSegment.from_file(filename)
        audio = audio.set_frame_rate(self.RATE).set_channels(1)
        data = np.array(audio.get_array_of_samples(), dtype=self.FORMAT)
        return data, audio.frame_rate

    def rms(self, frame):
        if np.any(frame):
            sum_squares = np.sum(np.square(frame))
            return np.sqrt(sum_squares / len(frame))
        else:
            return 0

    def calculate_frequencies(self, frame):
        n = len(frame)
        if n == 0:
            return np.array([]), np.array([])
        frequency = np.fft.rfftfreq(n, d=1./self.RATE)
        magnitude = np.abs(np.fft.rfft(frame)) / n
        return frequency, magnitude

    def process_mp3_file(self, filename):
        audio_samples, framerate = self.read_mp3(filename)
        num_frames = len(audio_samples) // self.CHUNK
        times = np.arange(num_frames) * (self.CHUNK / framerate)
        volumes = np.array([self.rms(audio_samples[i * self.CHUNK:(i + 1) * self.CHUNK]) for i in range(num_frames)])
        frequencies = []
        frequency_times = []
        
        frame_indices_for_frequency_average = int(self.FREQUENCY_AVERAGE_INTERVAL * framerate / self.CHUNK)
        frame_aggregate_frequencies = np.zeros(int(self.CHUNK/2 + 1))

        for i in range(num_frames):
            frame = audio_samples[i * self.CHUNK:(i + 1) * self.CHUNK]
            _, mag = self.calculate_frequencies(frame)
            frame_aggregate_frequencies += mag

            if (i + 1) % frame_indices_for_frequency_average == 0:
                average_magnitude = frame_aggregate_frequencies / frame_indices_for_frequency_average
                frequencies.append(average_magnitude)
                frequency_times.append(times[i])
                frame_aggregate_frequencies = np.zeros(int(self.CHUNK/2 + 1))
        
        volume_periods = {'low': [], 'high': []}
        start_time_low = start_time_high = None

        for i, volume in enumerate(volumes):
            if volume < self.VOLUME_THRESHOLD_LOW:
                if start_time_low is None:
                    start_time_low = times[i]
            else:
                if start_time_low is not None and times[i] - start_time_low >= self.VOLUME_ALERT_DURATION:
                    volume_periods['low'].append((start_time_low, times[i]))
                start_time_low = None

            if volume > self.VOLUME_THRESHOLD_HIGH:
                if start_time_high is None:
                    start_time_high = times[i]
            else:
                if start_time_high is not None and times[i] - start_time_high >= self.VOLUME_ALERT_DURATION:
                    volume_periods['high'].append((start_time_high, times[i]))
                start_time_high = None

        if start_time_low is not None and times[-1] - start_time_low >= self.VOLUME_ALERT_DURATION:
            volume_periods['low'].append((start_time_low, times[-1]))
        if start_time_high is not None and times[-1] - start_time_high >= self.VOLUME_ALERT_DURATION:
            volume_periods['high'].append((start_time_high, times[-1]))

        return times, volumes, frequencies, frequency_times, volume_periods
    def plot_given_values_for_pitch(self, times, volumes,frequencies, frequency_times, volume_periods ):
        plt.figure(figsize=(8, 6))

        # Plot volume over time
        plt.subplot(2, 1, 1)
        plt.plot(times, volumes, label='Volume', linewidth=1.5)
        plt.axhline(y=VOLUME_THRESHOLD_LOW, color='red', linestyle='--', label='Low Volume Threshold')
        plt.axhline(y=VOLUME_THRESHOLD_HIGH, color='green', linestyle='--', label='High Volume Threshold')
        plt.title('Volume over Time')
        plt.ylabel('Volume')
        plt.legend()
        plt.grid(True)

        # Plot average frequency
        plt.subplot(2, 1, 2)
        plt.plot(frequency_times, frequencies, label='Average Frequency', color='b', linewidth=1.5)
        # Label low and high volume periods on frequency plot
        for period in volume_periods['low']:
            plt.axvspan(period[0], period[1], color='red', alpha=0.3, label='Low Volume Period' if 'Low Volume Period' not in plt.gca().get_legend_handles_labels()[1] else "")
        for period in volume_periods['high']:
            plt.axvspan(period[0], period[1], color='green', alpha=0.3, label='High Volume Period' if 'High Volume Period' not in plt.gca().get_legend_handles_labels()[1] else "")
        plt.xlabel('Time')
        plt.ylabel('Average Frequency Magnitude')
        plt.legend()
        plt.grid(True)

        plt.show()
    def plot_pitch(self, mp3_file):
        
        #convert mp3 to wav
        wav_file = self.convert_mp3_to_wav(mp3_file)

        times, volumes, frequencies, frequency_times, volume_periods = self.process_wav_file(wav_file)
        self.plot_given_values_for_pitch(times, volumes, frequencies, frequency_times, volume_periods)


if __name__ == "__main__":
    filename = r"output\test2\test2.mp3"  # Update this path
    obj = PitchAnalyzer()
    times, volumes, frequencies, frequency_times, volume_periods = obj.process_wav_file(filename)
    
    plt.figure(figsize=(14, 10))
    
    # Plot volume over time
    plt.subplot(2, 1, 1)
    plt.plot(times, volumes, label='Volume', linewidth=1.5)
    plt.axhline(y=VOLUME_THRESHOLD_LOW, color='red', linestyle='--', label='Low Volume Threshold')
    plt.axhline(y=VOLUME_THRESHOLD_HIGH, color='green', linestyle='--', label='High Volume Threshold')
    plt.title('Volume over Time')
    plt.ylabel('Volume')
    plt.legend()
    plt.grid(True)
    
    # Plot average frequency
    plt.subplot(2, 1, 2)
    plt.plot(frequency_times, frequencies, label='Average Frequency', color='b', linewidth=1.5)
    # Label low and high volume periods on frequency plot
    for period in volume_periods['low']:
        plt.axvspan(period[0], period[1], color='red', alpha=0.3, label='Low Volume Period' if 'Low Volume Period' not in plt.gca().get_legend_handles_labels()[1] else "")
    for period in volume_periods['high']:
        plt.axvspan(period[0], period[1], color='green', alpha=0.3, label='High Volume Period' if 'High Volume Period' not in plt.gca().get_legend_handles_labels()[1] else "")
    plt.xlabel('Time (seconds)')
    plt.ylabel('Average Frequency Magnitude')
    plt.legend()
    plt.grid(True)
    
    plt.show()