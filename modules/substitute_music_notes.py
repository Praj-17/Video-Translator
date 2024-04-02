from pydub import AudioSegment, silence

from pydub import AudioSegment, silence

def mix_voice_and_music(voice_silence_audio_path, music_voice_audio_path, output_path):
    """
    Mixes voice from the voice+silence audio file with music from the music+voice audio file.
    Replaces the voice in the music+voice file with the voice from the voice+silence file.

    Parameters:
    - voice_silence_audio_path: Path to the audio file with voice and silence.
    - music_voice_audio_path: Path to the audio file with music and voice.
    - output_path: Path to save the final mixed audio file.
    """
    # Load the audio files
    voice_silence_audio = AudioSegment.from_file(voice_silence_audio_path)
    music_voice_audio = AudioSegment.from_file(music_voice_audio_path)

    # Detect non-silent chunks in the voice+silence audio
    non_silent_chunks = silence.detect_nonsilent(
        voice_silence_audio, 
        min_silence_len=1000, 
        silence_thresh=-50
    )

    final_audio = music_voice_audio[:0]  # Initialize an empty AudioSegment with the same characteristics

    last_end = 0
    for start_i, end_i in non_silent_chunks:
        voice_segment = voice_silence_audio[start_i :end_i]

        # Append the music part from the last end to the current start
        final_audio += music_voice_audio[last_end :start_i]
        
        # Append the new voice segment
        final_audio += voice_segment

        last_end = end_i

    # Append the remaining part of the music+voice audio after the last voice segment
    final_audio += music_voice_audio[last_end:]

    # Export the final audio
    final_audio.export(output_path, format="mp3")
    print("Audio mixing completed successfully. Output file saved at:", output_path)



# Example usage:
    
if __name__ == "__main__":
    mix_voice_and_music(r"output\small_talk\small_talk_translated.mp3", r"output\small_talk\small_talk.mp3", r"output\small_talk\final.mp3")
