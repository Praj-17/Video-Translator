from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
from srt_parser import SRTParser
# from lang_translator import Translator


class OpenAISummarizer:
    def __init__(self) -> None:
        self.srt_parser = SRTParser()
        # self.translator = Translator()
    def call_openai(self, text_chunk, dest_lang = "spanish"):

        
        completion = client.chat.completions.create(
        model=os.getenv("model_name"),
        messages=[
            {"role": "system", "content": "You are a helpful teaching assistant that generates a concise summary of the given lecture transcript. Do not put any place holders. Return the Summary in {dest_lang}"},
            {"role": "user", "content": text_chunk}
        ])



        return completion.choices[0].message.content

    def split_text_into_chunks(self, text, chunk_size=3000):
        chunks = []
        current_chunk = ""
        words = text.split()
        for word in words:
            if len(current_chunk) + len(word) < chunk_size:
                current_chunk += word + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = word + " "
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        return chunks

    def generate_summary(self, text):
        text_chunks = summarizer.split_text_into_chunks(text)
        summaries = []
        for chunk in text_chunks:
            summary = summarizer.call_openai(chunk)
            summaries.append(summary)
            # Concatenate summaries of all chunks
        return   " ".join(summaries)
    
    def generate_summary_from_srt_file(self, srt_file):
            return self.generate_summary(self.srt_parser.get_all_text(srt_file))
    def generate_translated_summary(self, srt_file, lang = 'es'):
            text = self.generate_summary_from_srt_file(srt_file)
            return self.translator(text, lang = lang)



if __name__ == "__main__":
    # Example usage
    long_text = """
 Long years ago we made a tryst with destiny, and now the time comes when we shall redeem our
pledge, not wholly or in full measure, but very substantially. At the stroke of the midnight hour,
when the world sleeps, India will awake to life and freedom. A moment comes, which comes but
rarely in history, when we step out from the old to the new, when an age ends, and when the soul of
a nation, long suppressed, finds utterance. It is fitting that at this solemn moment, we take the
pledge of dedication to the service of India and her people and to the still larger cause of humanity.
At the dawn of history, India started on her unending quest, and trackless centuries are filled with
her striving and grandeur of her success and failures. Through good and ill fortune alike, she has
never lost sight of that quest, forgotten the ideals which gave her strength. We end today a period of
misfortunes and India discovers herself again. The achievement we celebrate today is but a step, an
opening of opportunity to the greater triumphs and achievements that await us. Are we brave
enough and wise enough to grasp this opportunity and accept the challenge of the future?
Freedom and power bring responsibility. The responsibility rests upon this Assembly, a sovereign
body representing the sovereign people of India. Before the birth of freedom, we have endured all
the pains of labour and our hearts are heavy with the memory of this sorrrow. Some of those pains
continue even now. Nevertheless, the past is over and it is the future that beckons us now.
That future is not one of ease or resting but of incessant striving so that we may fulfill the pledges
we have so often taken and the one we shall take today. The service of India means, the service of
the millions who suffer. It means the ending of poverty and ignorance and poverty and disease and
inequality of opportunity. The ambition of the greatest men of our generation has been to wipe
every tear from every eye. That may be beyond us, but as long as there are tears and suffering, so
long our work will not be over.
And so we have to labour and to work, and to work hard, to give reality to our dreams. Those
dreams are for India, but they are also for the world, for all the nations and peoples are too closely
knit together today for any one of them to imagine that it can live apart. Peace is said to be
indivisible, so is freedom, so is prosperity now, and also is disaster in this one world that can no
longer be split into isolated fragments.
To the people of India, whose representatives we are, we make an appeal to join us with faith and
confidence in this great adventure. This is no time for petty and destructive criticism, no time for illwill or blaming others. We have to build the noble mansion of free India where all her children may
dwell.
The appointed day has come -the day appointed by destiny- and India stands forth again, after long
slumber and struggle, awake, vital, free and independent. The past clings on to us still in some
measure and we have to do much before we redeem the pledges we have so often taken.
Yet the turning-point is past, and history begins anew for us, the history which we shall live and act
and others will write about.
It is a fateful moment for us in India, for all Asia and for the world. A new star rises, the star of
freedom in the East, a new hope comes into being, a vision long cherished materializes. May the
star never set and that hope never be betrayed!
We rejoice in that freedom, even though clouds surround us, and many of our people are sorrowstricken and difficult problems encompass us. But freedom brings responsibilities and burdens and
we have to face them in the spirit of a free and disciplined people.
On this day our first thoughts go to the architect of this freedom, the Father of our Nation, who,
embodying the old spirit of India, held aloft the torch of freedom and lighted up the darkness that
surrounded us. We have often been unworthy followers of his and have strayed from his message,
but not only we but succeeding generations will remember this message and bear the imprint in
their hearts of this great son of India, magnificent in his faith and strength and courage and
humility. We shall never allow that torch of freedom to be blown out, however high the wind or
stormy the tempest.
Our next thoughts must be of the unknown volunteers and soldiers of freedom who, without praise
or reward, have served India even unto death.
We think also of our brothers and sisters who have been cut off from us by political boundaries and
who unhappily cannot share at present in the freedom that has come. They are of us and will remain
of us whatever may happen, and we shall be sharers in their good [or] ill fortune alike.
The future beckons to us. Whither do we go and what shall be our endeavour? To bring freedom
and opportunity to the common man, to the peasants and workers of India; to fight and end poverty
and ignorance and disease; to build up a prosperous, democratic and progressive nation, and to
create social, economic and political institutions which will ensure justice and fullness of life to
every man and woman.
We have hard work ahead. There is no resting for any one of us till we redeem our pledge in full,
till we make all the people of India what destiny intended them to be. We are citizens of a great
country on the verge of bold advance, and we have to live up to that high standard. All of us, to
whatever religion we may belong, are equally the children of India with equal rights, privileges and
obligations. We cannot encourage communalism or narrow-mindedness, for no nation can be great
whose people are narrow in thought or in action.
To the nations and peoples of the world we send greetings and pledge ourselves to cooperate with
them in furthering peace, freedom and democracy.
And to India, our much-loved motherland, the ancient, the eternal and the ever-new, we pay our
reverent homage and we bind ourselves afresh to her service
    """

    summarizer = OpenAISummarizer()
    summary = summarizer.generate_summary(long_text)

    print("Summary:", summary)
