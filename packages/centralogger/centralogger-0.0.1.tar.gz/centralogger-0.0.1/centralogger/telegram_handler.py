import logging
import json

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request


class TelegramLogHandler(logging.Handler):
    ICONS = {
        logging.NOTSET: "ℹ️",
        logging.DEBUG: "ℹ️",
        logging.INFO: "ℹ️",
        logging.WARNING: "⚠️",
        logging.ERROR: "❌",
        logging.CRITICAL: "🛑",
    }

    API_END_POINT = "https://api.telegram.org/bot{}/{}"

    def __init__(
        self,
        bot_token,
        chat_id,
        format=" %(levelname)s %(asctime)s [%(name)s]: %(message)s",
    ):
        logging.Handler.__init__(self)
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.formatter = logging.Formatter(format)

    def _create_message(self, record):
        print(record)
        icon = self.ICONS[record.levelno]
        text = self.format(record)
        message = "{} {}".format(icon, text)
        return message

    def _send_message(self, message):
        URL = self.API_END_POINT.format(self.bot_token, "sendMessage")
        content = {"chat_id": self.chat_id, "text": message}
        req = Request(URL)
        req.add_header("Content-Type", "application/json")
        urlopen(req, json.dumps(content).encode("utf-8"))

    def emit(self, record):
        message = self._create_message(record)
        try:
            self._send_message(message)
        except:
            self.handleError(record)
