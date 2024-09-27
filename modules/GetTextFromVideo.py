from modules.transcribe import TranscribeSRT
from modules.audio_extractor import AudioExtractor

class GetTextFromVideo:
    def __init__(self) -> None:
        self.extractor = AudioExtractor()
        self.trans = TranscribeSRT()
    def get_text_from_video(self, vidoe_name, language = "es"):
        output_path = self.extractor.extract_audio_to_mp3(vidoe_name)

        #Save the text
        text_path = self.trans.save_text(output_path,destination_language=language)
        return text_path

