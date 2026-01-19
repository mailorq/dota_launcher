import subprocess
import os
import platform
import time


class DotaLauncher:

    def __init__(self):
        self.dota_running = False
        self.last_launch_time = 0
        self.cooldown_seconds = 60

    def find_dota_path(self):
        system = platform.system()
        possible_paths = [
            r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\dota2.exe",
            r"C:\Program Files\Steam\steamapps\common\dota 2 beta\game\bin\win64\dota2.exe",
            r"D:\Steam\steamapps\common\dota 2 beta\game\bin\win64\dota2.exe",
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return path

        return None

    def launch_via_steam(self):
        system = platform.system()
        steam_url = "steam://rungameid/570"

        try:
            os.startfile(steam_url)

            return True
        except Exception as e:
            print(f"Ашибачка > {e}")
            return False

    def launch_direct(self, dota_path=None):
        if dota_path is None:
            dota_path = self.find_dota_path()

        if dota_path is None:
            print("Бля скачай доту че ты как еблан??")
            return False

        try:
            subprocess.Popen([dota_path])
            return True
        except Exception as e:
            print(f"Ошибка прямого запуска: {e}")
            return False

    def can_launch(self):
        current_time = time.time()
        if current_time - self.last_launch_time < self.cooldown_seconds:
            remaining = int(self.cooldown_seconds - (current_time - self.last_launch_time))
            print(f"Кд братишшшшшшшшшшшшшшшшшшшшшшшшш > {remaining} сек")
            return False
        return True

    def launch(self):
        if not self.can_launch():
            return False

        print("Запускаю...")

        if self.launch_via_steam():
            print("Через стим")
            self.last_launch_time = time.time()
            self.dota_running = True
            return True

        if self.launch_direct():
            print("На прямую")
            self.last_launch_time = time.time()
            self.dota_running = True
            return True

        print("Не удалось запустить. У тя че стима нет??")
        return False
