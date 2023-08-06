from abc import ABCMeta, abstractmethod


class AbstractPlugin(metaclass=ABCMeta):

    def __init__(self, SKILL):
        self._SKILL = {**{"media": None, "speech": None, "nlp": None, "mqtt": None,"serial": None,"thread": None}, **SKILL}
        
        self.media = self._SKILL["media"]
        self.speech = self._SKILL["speech"]
        self.nlp = self._SKILL["nlp"]
        self.mqtt = self._SKILL["mqtt"]
        self.serial = self._SKILL["serial"]
        self.thread = self._SKILL["thread"]

    def say(self, text):
        self.speech.TTS(text)
        self.media.play()

    def play(self, path):
        self.media.play(path)


    def sayThread(self, text):
        self.speech.TTS(text)
        self.media.playThread()

    def playThread(self, path):
        self.media.playThread(path)

        

    @abstractmethod
    def isValid(self, query):
        return False

    @abstractmethod
    def handle(self, query):
        return None
