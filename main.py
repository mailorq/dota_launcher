from audio_processor import AudioProcessor
from dota_launcher import DotaLauncher


class VoiceDotaLauncher:
    def __init__(self):
        self.audio_processor = AudioProcessor()
        self.dota_launcher = DotaLauncher()
        self.running = True

        self.trigger_phrases = ["хуета"]

        print("=" * 50)
        print("Скажи фразу для запуска Дотки")
        print("=" * 50)

    def run(self):
        try:
            while self.running:
                detected, text = self.audio_processor.is_phrase_detected(
                    self.trigger_phrases
                )

                print(f"\nРаспознано > '{text}'")

                if detected:
                    print("Ну всё иди там нахуй братиш")

                    if self.dota_launcher.launch():
                        self.running = False

        except KeyboardInterrupt:
            print("\nОстановка...")


def main():
    app = VoiceDotaLauncher()
    app.run()


if __name__ == "__main__":
    main()
