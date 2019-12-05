import os, sys
from slack import RTMClient

slack_channel = "doorbell"
slack_token = "xoxb-842066883122-847001127185-FavzDK3PvSPgTfBQF8qrMy7L"
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
        elif ":+1:" in DATA['text']:
            print(DATA['text'])
            rtm_client.stop()
            sys.exit(0)

    except (Warning, Exception) as e:
        print(e)

    finally:
        pass

if __name__ == "__main__":
    rtm_client.start()
