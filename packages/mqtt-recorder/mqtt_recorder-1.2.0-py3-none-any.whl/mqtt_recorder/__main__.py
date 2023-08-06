from mqtt_recorder.recorder import MqttRecorder, SslContext
import argparse
import time

parser = argparse.ArgumentParser(
    prog='mqtt_recorder',
    description="Tool for recording and replaying mqtt messages"
)

parser.add_argument(
    '--host',
    type=str,
    required=True,
    help='MQTT broker address'
)

parser.add_argument(
    '--port',
    type=int,
    default=1883,
    help='MQTT broker port'
)

parser.add_argument(
    '--username',
    type=str,
    default=None,
    required=False,
    help='MQTT broker username'
)

parser.add_argument(
    '--password',
    type=str,
    default=None,
    required=False,
    help='MQTT broker password'
)

parser.add_argument(
    '--enable_ssl',
    type=bool,
    default=False,
    required=False,
    help='True to enable MQTTs support, False otherwise'
)

parser.add_argument(
    '--ca_cert',
    type=str,
    default=None,
    required=False,
    help='path to the Certificate Authority certificate files'
)

parser.add_argument(
    '--certfile',
    type=str,
    default=None,
    required=False,
    help='path to the client certificate'
)

parser.add_argument(
    '--keyfile',
    type=str,
    default=None,
    required=False,
    help='path to the client private key'

)

parser.add_argument(
    '--mode',
    choices=["record", "replay"],
    help='mode: record/replay',
    required=True
)

parser.add_argument(
    '--file',
    type=str,
    help='output/input file',
    required=True
)

parser.add_argument(
    '--loop',
    type=bool,
    help='looping replay',
    default=False
)

parser.add_argument(
    '--qos',
    type=int,
    help='Quality of Service that will be used for subscriptions',
    default=0
)

parser.add_argument(
    '--topics',
    type=str,
    help='json file containing selected topics for subscriptions'
)

parser.add_argument(
    '--encode_b64',
    default=False,
    action='store_true',
    help='Store raw data as base64 encoded string in CSV file instead of UTF-8 encoded string. '
         'Should be used to record binary message payloads'
)


def wait_for_keyboard_interrupt():
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        pass


def main():
    args = parser.parse_args()
    sslContext = SslContext(args.enable_ssl, args.ca_cert, args.certfile, args.keyfile)
    recorder = MqttRecorder(
        args.host,
        args.port,
        args.file,
        args.username,
        args.password,
        sslContext,
        args.encode_b64)
    if args.mode == 'record':
        recorder.start_recording(qos=args.qos, topics_file=args.topics)
        wait_for_keyboard_interrupt()
        recorder.stop_recording()
    elif args.mode == 'replay':
        try:
            recorder.start_replay(args.loop)
        except KeyboardInterrupt:
            pass
    else:
        print('Please select a mode record/replay')


if __name__ == "__main__":
    main()
