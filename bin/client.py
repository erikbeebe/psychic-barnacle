import json
import random
import socket
import threading
import time

from client_config import broker
from confluent_kafka import Consumer, KafkaError, Producer
from subprocess import run, PIPE

## Setup
host_id = socket.gethostname()

# Producer topic - this should be the sink for the packet data
producer_topic = "pb_data"

# CNC source/results topics - this should be where the daemon exchanges command data
commands_topic = "pb_cnc_commands"
response_topic = "pb_cnc_responses"

# Create producer/consumer objects
conf = {
   'bootstrap.servers': broker,
   # consumer options
   'group.id': host_id,
   'default.topic.config': {'auto.offset.reset': 'smallest'}

}

p = Producer(**conf)

# Valid commands for CnC channel
valid_commands = {
            'hostname': '/bin/hostname',
            'uptime':   '/usr/bin/uptime'
           }


class SendData(object):
    def __init__(self):
        self.running = True

    def send_data(self):
        """ Simulate functionality sending stream of packets """
        while self.running:
            data = {'source': host_id,
                    'stuff': random.random()}

            p.produce(producer_topic, json.dumps(data))
            # not performant, wouldn't actually do this in production
            p.poll(0)
            p.flush()

            print("Send thread sent one simulated packet")
            time.sleep(1)

class HandleCommands(object):
    def __init__(self):
        self.running = True
        self.c = Consumer(**conf)
        self.c.subscribe([commands_topic])

    def handle_commands(self):
        """ Simulate thread to execute commands from the mothership """
        while self.running:
            print("Command handler thread waiting for messages")
            msg = self.c.poll()

            if not msg.error():
                print("Command handler thread unblocked, checking for message")
                command = json.loads(msg.value().decode('utf-8'))

                if 'target_host' in command:
                    # check to see if this message is addressed to us, or to
                    # everyone in the fleet
                    if command['target_host'] == host_id or command['target_host'] == "ALL":
                        # it is, verify this command is in the valid commands map and run
                        # it if so
                        if command['command'] in valid_commands:
                            run_command = command['command']
                            output = run(valid_commands[run_command], check=True, stdout=PIPE)

                            # add some logic to make sure this worked
                            # send the output back
                            results = {}
                            results['stdout'] = str(output.stdout)
                            results['hostname'] = host_id

                            p.produce(response_topic, json.dumps(results))
                            print("Sent results successfully")
                    else:
                        # disregard, received a message not for us
                        print("Ignoring message, not targeted to us")
                        pass
            elif msg.error().code() != KafkaError._PARTITION_EOF:
                print("Kafka error: {}".format(msg.error()))

        return self.c.close()


def main():
    send = SendData()
    cmds = HandleCommands()

    send_thread = threading.Thread(target=send.send_data)
    cmds_thread = threading.Thread(target=cmds.handle_commands)

    print("Starting send thread")
    send_thread.start()

    print("Starting command handler thread")
    cmds_thread.start()

if __name__ == "__main__":
    print("Starting emulator, my host id is {}, Kafka broker is {}".format(host_id, broker))
    main()
