import os
from datetime import datetime
import subprocess

class DailyOrgan:
    def __init__(self):
        self.base_dir = "/storage/emulated/0/MutableMemory/critter/daily"
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def _today_path(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.base_dir, f"{today}.md")

    def show_today(self):
        path = self._today_path()
        if not os.path.exists(path):
            self._create_default(path)

        with open(path, "r") as f:
            print(f.read())

    def edit_today(self):
        path = self._today_path()
        if not os.path.exists(path):
            self._create_default(path)

        # Open in nano
        subprocess.call(["nano", path])

    def _create_default(self, path):
        template = f"# DAILY — {datetime.now().strftime('%Y-%m-%d')}\n\n"
        template += "## Notes\n\n"
        with open(path, "w") as f:
            f.write(template)





