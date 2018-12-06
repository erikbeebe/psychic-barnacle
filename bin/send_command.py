import json

from client_config import broker
from confluent_kafka import Producer

## Kafka setup
topic = "pb_cnc_commands"

conf = {
   'bootstrap.servers': broker
}

p = Producer(**conf)

def main():
    # in this case, target_host should be the hostname of the target host
    # we're running the command on, or ALL to run on the whole fleet
    # note if you're running the client in docker, the hostname is probably
    # the name of the container.
    cmd = {'command': 'uptime',
           'target_host': 'python'}

    p.produce(topic, json.dumps(cmd))
    p.poll(0)
    p.flush()

if __name__ == "__main__":
    main()

