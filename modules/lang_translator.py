from googletrans import Translator

class LangTranslator:
    def __init__(self) -> None:
        self.translator = Translator()
    def get_translation(self, text, lang = 'es'):
        translated_text = self.translator.translate(text, dest=lang)
        return translated_text.text
    
if __name__ == "__main__":

    translator = LangTranslator()
    translation = translator.get_translation("Summary: The transcript is a speech that reflects on India's independence and the responsibilities that come with it. It calls for dedication to serving the people and humanity. It acknowledges past struggles and emphasizes the need for continued efforts to eradicate poverty, ignorance, and inequality. The speech stresses the interconnectedness of nations and the importance of unity and cooperation. It concludes with a call for faith, confidence, and unity in building a free and prosperous India. The lecture transcript discusses the significance of freedom in India and the responsibilities that come with it. It emphasizes the need to honor the Father of the Nation and the sacrifices made by volunteers and soldiers of freedom. The goal is to work towards creating a prosperous, democratic, and progressive nation that ensures justice and fullness of life to all citizens. It also stresses the importance of unity and cooperation, rejecting communalism and narrow-mindedness. The transcript concludes with a commitment to further peace, freedom, and democracy globally and a tribute to India as a beloved and eternal motherland. The lecture discusses the concept of being  It emphasizes the importance of approaching tasks with renewed energy, dedication, and enthusiasm. By being  individuals can bring a sense of vigor and commitment to their responsibilities, ultimately leading to greater success and fulfillment.")
    print(translation)