

import pyttsx3 #import the library
import librosa
import soundfile as sf


class TextToSpeech:
    def __init__(self):
        self.eng = pyttsx3.init()
    def text_to_speech_py3(self, text, desired_duration_seconds, filename, voice_type=0):
        ## Voice type: 0 for male and 1 for female
        # Initialize an instance
        voice = self.eng.getProperty('voices')  # get the available voices
        self.eng.setProperty('voice', voice[int(voice_type)].id)  # set the voice to the specified type
        
        # Set the volume (range is 0.0 to 1.0, where 1.0 is the maximum volume)
        self.eng.setProperty('volume', 1.0)  # Set to maximum volume
        
        # Calculate the rate
        words = len(text.split())
        words_per_second = words / desired_duration_seconds
        rate = int(words_per_second * 60)  # Convert words per second to words per minute
        self.eng.setProperty('rate', rate)
        
        self.eng.save_to_file(text, filename)  # Save text to the specified file
        self.eng.runAndWait()

    
    def text_to_speech_with_duration(self, text, desired_duration_seconds, filename, voice_type=0):
        # Generate speech and save to file
        if voice_type == "Male":
            voice_type =0
        else: voice_type = 1
        voice = self.eng.getProperty('voices')[int(voice_type)]  # Select voice; might need refinement for gender selection
        self.eng.setProperty('voice', voice.id)
        self.eng.save_to_file(text, filename)
        self.eng.runAndWait()
        
        # Load generated audio
        y, sr = librosa.load(filename, sr=None)
        
        # Calculate current and desired duration, then compute stretch factor
        current_duration = librosa.get_duration(y=y, sr=sr)
        stretch_factor = current_duration / desired_duration_seconds
        
        # Apply time-stretching
        y_stretched = librosa.effects.time_stretch(y=y, rate=stretch_factor)
        
        # Save stretched audio back to file
        sf.write(filename, y_stretched, sr)                                                                                                                                                                                                

if __name__ == "_main_":
    tts  = TextToSpeech()



    tts.text_to_speech_py3("hola Mi nombre es krish naik y bienvenido a mi canal de youtube", voice_type=0)