# scp *.py doorid@104.211.16.184:.
import os, sys
from slack import RTMClient, WebClient

state = 0 # 0: waiting, 1: recognized, 2: unrecognized
slack_channel = "doorbell"
slack_token ="xoxb-842066883122-847001127185-FavzDK3PvSPgTfBQF8qrMy7L"
web_client = WebClient(token=slack_token)
rtm_client = RTMClient(token=slack_token)

@RTMClient.run_on(event="message")
def say_hello(**payload):
    global state
    DATA = payload['data']
    channel_id = DATA['channel']
    thread_ts = DATA['ts']

    try:
        if ":-1:" in DATA['text']:
            print("Unauthorized")
            rtm_client.stop()
            sys.exit(0)
        elif ":+1:" in DATA['text'] or ":the_horns:" in DATA['text']:
            print("Authorized")
            rtm_client.stop()
            sys.exit(0)
        elif ":eggplant:" in DATA['text'] and ":sweat_drops:" in DATA['text']:
            print("Booty Call")
            rtm_client.stop()
            sys.exit(0)

    except (Warning, Exception) as e:
        print(e)

    finally:
        pass

def send_message(message="", slack_channel="doorbell"):
    web_client.chat_postMessage(
      channel=slack_channel,
      text=message
    )

def send_file(filepath="", slack_channel="doorbell"):
    web_client.files_upload(
      channels=slack_channel,
      file=filepath,
      title="Unrecognized person"
    )

if __name__ == "__main__":
    send_file(filepath="uploads/user.jpg")
    send_message(message="Someone knocked, what is your response?")
    rtm_client.start()
