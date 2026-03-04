# LANGUAGE VIEWER — emerald ascension display of language packets

class LanguageViewer:
    def __init__(self):
        self.last_language = None

    def accept(self, packet):
        if packet.get("type") == "language":
            self.last_language = packet["payload"]

    def render(self):
        if self.last_language is None:
            return "[LanguageViewer] …waiting for language spark…"

        text = self.last_language
        return f"[LanguageViewer • Emerald Ascension] {text}"
