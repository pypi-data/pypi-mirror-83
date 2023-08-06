import requests
import time

from logreporter.report.abstractreporter import AbstractReporter

class DiscordWHReporter(object):
  """
  Reporter notifications using Discord webhooks.
  """
  def __init__(self, url):
    """
    constructor.

    Parameters
    ----
    url: str
      Webhook URL
      ex). https://discordapp.com/api/webhooks/***
    """
    self.url = str(url)

  def request_report(self, log_handler, message=""):
    """
    Send logs using Discord's Webhook.
    """
    def send(text):
      payload = {
        "content": message[:2000] if message != "" else __class__.__name__,
        "embeds": [
          {
            "type": "article",
            "description": text
          }
        ]
      }
      res = requests.post(self.url, json=payload, headers=headers)
      res.raise_for_status()
      return True
    headers = {"Content-Type": "application/json"}
    while log_handler.has_text:
      log_handler.get_text(max_length=2000, report=send)
      time.sleep(0.01)