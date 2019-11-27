import paho.mqtt.client as mqtt
import os

# Define event callbacks
looper = True
verdict = False

def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    global looper, verdict
    looper = False
    if "ok" in str(msg.payload) or "OK" in str(msg.payload):
        verdict = True
    else:
        verdict = False

    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

def publish_and_wait(imageLink=""):
    global looper, verdict
    looper = True
    verdict = False
    mqttc = mqtt.Client()
    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe

    # Uncomment to enable debug messages
    mqttc.on_log = on_log

    # Parse CLOUDMQTT_URL (or fallback to localhost)
    url_str = os.environ.get('CLOUDMQTT_URL', 'farmer.cloudmqtt.com')

    # Connect
    mqttc.username_pw_set("xvreyrjq", "Oe-CyySBFJLF")
    mqttc.connect("farmer.cloudmqtt.com", 13760)

    # Publish image link
    mqttc.publish("joe", "This here dude trynna enter your crib " + imageLink)

    # Start subscribe, with QoS level 0
    mqttc.subscribe("joe", 0)

    # Continue the network loop, exit when an error occurs
    rc = 0
    while looper:
        mqttc.loop()

    return verdict
