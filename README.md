# ip-trigger
Low cost artisan dyndns.

Send emails when the ip address of the host changes. 

# Setup

Clone the repo `git clone git@github.com:vekerdyb/ip-trigger.py`

`cd ip-trigger`

Create venv and add dependencies:
```
pyvenv venv
. venv/bin/activate
pip install -r requirements.txt
```

Create a `config.py` file with

```
RAILGUN_HOST = '<your host>'
RAILGUN_API_KEY = '<your-key>'
EMAIL_BACKEND = 'railgun_backend'

EMAIL_SUBJECT = '<whatever you want, eg: IP change on example.com>'
EMAIL_TEXT_TEMPLATE = '{}' # again, this can be whatever you want, but it must contain a single {} where the new IP will be inserted
EMAIL_RECIPIENT = 'Your Name <you@host.com>'
FROM_NAME = '<whatever you want as the sender name of the email>'
```

Add a cronjob to run `ip-trigger.py` as often as you deem fit.

E.g. I run it once every hour, at half past:
```
30 * * * * /<path>/ip-trigger/venv/bin/python /<path>/ip-trigger/ip-trigger.py
```

