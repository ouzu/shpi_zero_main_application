import config
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

try:
    import core.peripherals as peripherals
except:
    pass

try:
    import paho.mqtt.publish as publish
    import paho.mqtt.client as mqtt
except ImportError:
    exit("Please run: (sudo) pip3 install paho-mqtt")


client = None


def publishall():
    global client
    try:
        for path in vars(peripherals.eg_object):
            if path == 'led':
                client.publish(config.MQTT_PATH + "/" + path,
                               (str)(getattr(peripherals.eg_object, path)))
            else:
                client.publish(config.MQTT_PATH + "/" + path,
                               getattr(peripherals.eg_object, path))
    except:
        pass


def publish(path, value):
    global client
    try:
        client.publish(config.MQTT_PATH + "/" + path, value)
    except:
        pass


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")


def on_message(client, userdata, message):
    if config.MQTT_SERVER != "mqtt.eclipse.org":  # deactivate for demo server
        msg = message.payload.decode("utf-8")
        print("message received ", str(msg))
        print("message topic=", message.topic)
        print("message qos=", message.qos)
        print("message retain flag=", message.retain)

        if message.topic.startswith(config.MQTT_PATH + "/set/relais"):
            channel = int(message.topic[-1])
            assert 0 < channel < 4, 'channel outside 1..3'
            if msg == 'ON':
                peripherals.controlrelays(channel, 1)
                publish("relais"+channel, 'ON')
            elif msg == 'OFF':
                peripherals.controlrelays(channel, 0)
                publish("relais"+channel, 'OFF')
            else:
                print('unknown:' + message.topic + ' message:' + msg)

        if message.topic == (config.MQTT_PATH + "/set/buzzer"):

            if msg == 'ON':
                peripherals.controlrelays(4, 1)
                publish("buzzer", 'ON')
            elif msg == 'OFF':
                peripherals.controlrelays(4, 0)
                publish("buzzer", 'OFF')
            else:
                print('unknown:' + message.topic + ' message:' + msg)

        if message.topic == (config.MQTT_PATH + "/set/d13"):

            if msg == 'ON':
                peripherals.controlrelays(5, 1)
                publish("d13", 'ON')
            elif msg == 'OFF':
                peripherals.controlrelays(5, 0)
                publish("d13", 'OFF')
            else:
                print('unknown:' + message.topic + ' message:' + msg)

        if message.topic == (config.MQTT_PATH + "/set/alert"):

            if msg == 'ON':
                peripherals.eg_object.alert = 1
                publish("alert", 'ON')
            elif msg == 'OFF':
                peripherals.eg_object.alert = 0
            else:
                print('unknown:' + message.topic + ' message:' + msg)

        if message.topic == (config.MQTT_PATH + "/set/max_backlight"):
            assert 0 < (int)(msg) < 32, 'value outside 1..31'
            peripherals.eg_object.max_backlight = (int)(msg)
            peripherals.controlbacklight((int)(msg))

        if message.topic == (config.MQTT_PATH + "/set/vent_pwm"):
            assert -1 < (int)(msg) < 256, 'value outside 0..255'
            peripherals.controlvent((int)(msg))

        if message.topic == (config.MQTT_PATH + "/set/set_temp"):
            assert 0 < (float)(msg) < 50, 'value outside 1..50'
            peripherals.eg_object.set_temp = (float)(msg)

        if message.topic == (config.MQTT_PATH + "/set/led"):
            value = msg.split(',')
            if len(value) == 3:
                peripherals.controlled(value)


def init():
    global client
    client = mqtt.Client()
    if len(config.MQTT_USER) and len(config.MQTT_PW):
        client.username_pw_set(config.MQTT_USER, config.MQTT_PW)

    client.connect(config.MQTT_SERVER, config.MQTT_PORT, 60)
    client.loop_start()
    client.subscribe(config.MQTT_PATH + "/set/relais1", qos=config.MQTT_QOS)
    client.subscribe(config.MQTT_PATH + "/set/relais2", qos=config.MQTT_QOS)
    client.subscribe(config.MQTT_PATH + "/set/relais3", qos=config.MQTT_QOS)
    client.subscribe(config.MQTT_PATH + "/set/buzzer", qos=config.MQTT_QOS)
    client.subscribe(config.MQTT_PATH + "/set/d13", qos=config.MQTT_QOS)
    #client.subscribe(MQTT_PATH + "/hwb", qos=0)
    client.subscribe(config.MQTT_PATH + "/set/alert", qos=config.MQTT_QOS)
    client.subscribe(config.MQTT_PATH + "/set/max_backlight",
                     qos=config.MQTT_QOS)
    client.subscribe(config.MQTT_PATH + "/set/set_temp", qos=config.MQTT_QOS)
    client.subscribe(config.MQTT_PATH + "/set/vent_pwm", qos=config.MQTT_QOS)
    client.subscribe(config.MQTT_PATH + "/set/led", qos=config.MQTT_QOS)

    client.on_connect = on_connect
    client.on_message = on_message
