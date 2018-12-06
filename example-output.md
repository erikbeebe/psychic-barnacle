```
$ kafkacat -C -b example.KAFKA.brokers:9092 -t pb_cnc_responses -o beginning -u | jq .
{
  "stdout": "b' 20:43:02 up 36 days, 18:52,  0 users,  load average: 0.39, 0.56, 0.72\\n'",
  "hostname": "python"
}
```
