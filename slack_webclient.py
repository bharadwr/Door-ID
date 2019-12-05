import os, sys
from slack import WebClient

slack_channel = "doorbell"
slack_token = "xoxb-842066883122-847001127185-FavzDK3PvSPgTfBQF8qrMy7L"
web_client = WebClient(token=slack_token)

def send_message(message="", slack_channel="doorbell"):
    web_client.chat_postMessage(
      channel=slack_channel,
      text=message
    )

def send_file(file_path="", slack_channel="doorbell", file_title=""):
    web_client.files_upload(
      channels=slack_channel,
      file=file_path,
      title=file_title
    )

if __name__ == "__main__":
    send_message(message="Testing")
