import os
import requests
import speech_recognition as sr
from os.path import join
from watson_developer_cloud import TextToSpeechV1
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS
from conversation import Conversation


class Speech(object):

    def __init__(self, user, password, launch_phrase={}, debugger_enabled=True):

        self.user = user
        self.password = password
        self.launch_phrase = launch_phrase
        self.debugger_enabled = debugger_enabled
        self.__debugger_microphone(enable=False)
        self.counter = 0

    def listen_to_voice(self):  # obtain audio from the microphone

        # Creates a new Recognizer instance, which represents a collection of speech recognition functionality.
        r = sr.Recognizer()
        # Creates a new Microphone instance, which represents a physical microphone on the computer.
        m = sr.Microphone()

        with m as source:  # open the microphone and start recording, source is the microphone(m's) instance
            r.adjust_for_ambient_noise(source)
            # r.dynamic_energy_threshold = True
            r.energy_threshold = 4000
            r.pause_threshold = 0.6  # minimum length of silence that will be considered as the end of phrase
            self.__debugger_microphone(enable=True)
            print("I'm listening")
            audio1 = r.listen(source)
            if audio1 is not None:
                present = True
                requests.get("http://localhost:8080/Found_audio?present=%s" % str(present))
                self.__debugger_microphone(enable=False)
                print("Found audio")

        return r, audio1

    def google_speech_recognition(self, recognizer, audio):
        speech = None
        try:
            speech = recognizer.recognize_google(audio)
            print("Zieana thinks you said " + speech)
        except sr.UnknownValueError:
            pass
            # print("audio not foundn")
            # self.listen_to_voice()
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        else:
            return speech

    def is_call_to_action(self, recognizer, audio):   # method used for the launch Phrase recognition
        speech = self.google_speech_recognition(recognizer, audio)

        for key, value in self.launch_phrase.items():
            if speech is not None and value in speech.lower():
                return True, key

        key = "charming"
        return False, key

    def __debugger_microphone(self, enable=True):
        if self.debugger_enabled:
            try:
                r = requests.get("http://localhost:8080/microphone?enabled=%s" % str(enable))
                if r.status_code != 200:
                    print("Used wrong endpoint for microphone debugging")
            except Exception as e:
                print(e)

    def text_to_speech(self, text):  # converts the given text to vocals using IBM watson

        text = text
        text_to_speech = TextToSpeechV1(username=self.user, password=self.password)
        path = join(os.getcwd(), 'output.ogg')

        # synthesize method returns bytes of audio so we have to write it inside a file
        with open(path, 'wb') as audio_file:
            audio_file.write(
                text_to_speech.synthesize(text, accept='audio/ogg;codecs=vorbis', voice="en-US_AllisonVoice"))
        # playing the created vocals
        voice = AudioSegment.from_ogg(path)
        play(voice)
        os.remove(path)

    def synthesize_text(self, text):
        tts = gTTS(text=text, lang='en-uk')
        tts.save("tmp.mp3")
        song = AudioSegment.from_mp3("tmp.mp3")
        play(song)
        os.remove("tmp.mp3")


if __name__ == '__main__':
    speech_obj = Speech('a40fb4ee-2f84-47ab-acce-c2828b277b08', '1jQFSMbVBjiX', launch_phrase={'vinay': 'banana apple smoothie', 'chanan': 'speaker geek'})
    conversation_obj = Conversation('vinay')
    data, value = speech_obj.is_call_to_action()
