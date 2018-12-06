# Very Naive CNC emulator
Quick and dirty CNC emulator (requires Python 3).  Just an example for testing, no one should use this for anything.

Rough list commands to get this going (may require tweaks depending on your environment):

```
- create topics:
  - pb_data
  - pb_cnc_commands
  - pb_cnc_responses

- pip3 install -r requirements.txt
- cd bin
- set Kafka brokers in client_config.py
- python3 client.py (should connect to kafka and start scrolling)
- set the target hostname in client.py to whatever your emulated client hostname is
- python3 send_command.py (to send a command to the client)
- kafkacat -C -b <broker> -t pb_cnc_responses -o beginning (to view the command responses)
```
