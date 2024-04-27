from deep_translator import GoogleTranslator
import whisper_timestamped as whisper
import datetime
import os
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()





class TrascribeSRT():
  def __init__(self) -> None:
    model_size = os.getenv("model_size")
    self.model = whisper.load_model(model_size, device="cpu")

  def mp3_to_translated_srt(self, mp3_file,destination_language = "es"):

    '''
    Function that transcribes an MP3 audio file then trnaslates the string into
    a specified language. The function outputs the Python string as an SRT file.

    Module Requirements
    ----------
    GitHub Repo: https://github.com/guillaumekln/faster-whisper
    from faster_whisper import WhisperModel

    PyPI Link: https://pypi.org/project/deep-translator/
    from deep_translator import GoogleTranslator

    Parameters
    ----------
    audio_file: mp3 file that will be transcribed into a Python string using the
    fast-whisper module.

    destination_language: Language that the string will be translated into using
    the deep-translator model and Google Translate. To check all available
    languages run the following function:
    GoogleTranslator().get_supported_languages(as_dict=True)

    Outputs
    ----------
    Original SRT File: writes an SRT file containing the text in its original
    language and timestamps.

    Translated SRT File: writes an SRT file containing the translated text and
    timestamps.
    '''

    #use the WhisperModel to transcribe the mp3 file
  
    if os.path.exists(mp3_file):
      print("This is the mp3 file", mp3_file)
      audio = whisper.load_audio(mp3_file)
    else:
      raise ValueError(f"The Audio file {mp3_file} not found")
    # results = self.model.transcribe(mp3_file, beam_size=5)
    results = whisper.transcribe(self.model, audio, language="en")

    original_subs = ''

    for idx,segment in enumerate(results['segments']):
      original_subs += f'{idx+1}\n'
      original_subs += str(datetime.timedelta(seconds=segment['start']))
      original_subs += ' --> '
      original_subs += f'{str(datetime.timedelta(seconds=segment['end']))}'

      #write the text in its original language
      original_subs += f'\n{segment['text'][1:]}\n\n'

    

    #translate the text
    #text length is limited to 5000 characters
    translated_subs = ''
    for line in original_subs.split('\n'):
      translated_subs += f"{GoogleTranslator(source='auto', target=destination_language).translate(line)}\n"

    with open(os.path.join(os.path.dirname(mp3_file), os.getenv("default_text_save_file_name") ), mode="w", encoding = "utf-8") as txt_output:
      txt_output.write(results['text'])
    with open(os.path.join( os.path.dirname(mp3_file), os.getenv("defualt_original_subtitles_name")),mode='w', encoding = "utf-8") as sub_output:
      sub_output.write(original_subs)

    with open(os.path.join( os.path.dirname(mp3_file), os.getenv("default_srt_file_name")),mode='w',  encoding = "utf-8") as sub_output:
      sub_output.write(translated_subs)

    print('Translation Complete')
    
    return os.path.join( os.path.dirname(mp3_file), os.getenv("default_srt_file_name"))


  def srt_translate(self, srt_file,destination_language):

    '''
    Function that translates an SRT file to a specified language.

    Module Requirements
    ----------
    PyPI Link: https://pypi.org/project/deep-translator/
    from deep_translator import GoogleTranslator

    Parameters
    ----------
    srt_file: SRT file that will be translated.
    destination_language: Language that the string will be translated into using
    the deep-translator model and Google Translate.

    Output
    ----------
    SRT File: writes an SRT file containing the translated text and timestamps.
    '''

    with open(srt_file,mode='r',  encoding = "utf-8") as og_subs:
      text = og_subs.readlines()

    translated_str = ''
    for line in text:
      translated_str += f"{GoogleTranslator(source='auto', target=destination_language).translate(line)}\n"

    with open(os.path.join( os.path.dirname(srt_file), f'{destination_language}.srt'),mode='w',  encoding = "utf-8") as sub_output:
      sub_output.write(translated_str)

    print('Translation Complete')

  def save_text(self, mp3_file,destination_language, source_language = "en"):
     #use the WhisperModel to transcribe the mp3 file
    audio = whisper.load_audio(mp3_file)
    # results = self.model.transcribe(mp3_file, beam_size=5)
    results = whisper.transcribe(self.model, audio, language=source_language)

    original_subs = ''

    for idx,segment in enumerate(results['segments']):
      original_subs += f'{idx+1}\n'
      original_subs += str(datetime.timedelta(seconds=segment['start']))
      original_subs += ' --> '
      original_subs += f'{str(datetime.timedelta(seconds=segment['end']))}'

      #write the text in its original language
      original_subs += f'\n{segment['text'][1:]}\n\n'
   
    file_name = os.path.join(os.path.dirname(mp3_file), os.getenv("default_text_save_file_name") )
    with open(file_name, mode="w", encoding = "utf-8") as txt_output:
      txt_output.write(results['text'])
      return file_name

if __name__ == "__main__":
    print("Transcribing the video now....This may take a while on CPU")
    ts = TrascribeSRT()
    ts.mp3_to_translated_srt('demo4.mp3','es')
    ts.srt_translate('es_3.srt','es')