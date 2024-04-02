# Given a mp3 file, split them into audios of 10 secs each approximately amd save to wav files.


from pydub import AudioSegment
import os

def split_mp3_to_wav(input_file_path, output_dir, segment_duration_ms=10000):
    """
    Split an MP3 file into segments of approximately 10 seconds each and save them as WAV files.

    Parameters:
    - input_file_path: Path to the input MP3 file.
    - output_dir: Directory to save the output WAV files.
    - segment_duration_ms: Duration of each segment in milliseconds (default is 10,000ms for 10 seconds).

    Returns:
    - A list of file paths to the generated WAV files.
    """

    # Load the MP3 file
    audio = AudioSegment.from_mp3(input_file_path)

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Split the audio
    output_files = []
    for i, chunk in enumerate(audio[::segment_duration_ms]):
        # Format the output file name
        output_file_path = os.path.join(output_dir, f"segment_{i}.wav")

        # Export the chunk to WAV with floating point format and 22,050 sample rate
        chunk.export(output_file_path, format="wav", parameters=["-f", "FLOAT", "-ar", "22050"])

        output_files.append(output_file_path)

    return output_files


if __name__ == "__main__":
    input_file = "output\demo\demo.mp3"
    output_file = "Voices\krish"
    split_mp3_to_wav(input_file, output_file)