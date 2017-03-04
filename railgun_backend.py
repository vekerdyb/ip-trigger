import config
import requests


def send_simple_message(from_name, to, subject, text):
    return requests.post(
        'https://api.mailgun.net/v3/{}/messages'.format(config.RAILGUN_HOST),
        auth=('api', config.RAILGUN_API_KEY),
        data={'from': '{} <postmaster@{}>'.format(from_name, config.RAILGUN_HOST),
              'to': to,
              'subject': subject,
              'text': text})
