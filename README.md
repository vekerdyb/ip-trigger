# ip-trigger
Low cost artisan dyndns.

Send emails when the ip address of the host changes.

# Requirements

Docker, docker-compose.

# Setup

Clone the repo `git clone git@github.com:vekerdyb/ip-trigger.py`

Rename `config.py.tmp` to `config.py` and change the values.

Run: `docker-compose run ip-trigger python ip-trigger.py` or simply `./run.sh`.

Add a cronjob to run `ip-trigger.py` as often as you deem fit.

E.g. I run it once every hour, at half past:
```
30 * * * * /<path>/ip-trigger/run.sh
```

## On a Raspberry Pi

Do as above but use `./run.pi.py`

