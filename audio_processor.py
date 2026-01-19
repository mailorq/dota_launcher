import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer


class AudioProcessor:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
        self.q = queue.Queue()

        self.model = Model("vosk-model-small-ru-0.22")
        self.recognizer = KaldiRecognizer(self.model, self.sample_rate)

    def _callback(self, indata, frames, time, status):
        self.q.put(bytes(indata))

    def listen_and_recognize(self, duration=3):
        self.recognizer.Reset()

        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self._callback
        ):
            for _ in range(int(self.sample_rate / 8000 * duration)):
                data = self.q.get()
                self.recognizer.AcceptWaveform(data)

        result = json.loads(self.recognizer.FinalResult())
        return result.get("text", "")

    def is_phrase_detected(self, trigger_phrases):
        text = self.listen_and_recognize()
        text_lower = text.lower()

        for phrase in trigger_phrases:
            if phrase in text_lower:
                return True, text

        return False, text
