import logging

import requests

import config

logger = logging.getLogger(__name__)


def _send_simple_message(from_name, to, subject, text):
    return requests.post(
        'https://api.mailgun.net/v3/{}/messages'.format(config.RAILGUN['HOST']),
        auth=('api', config.RAILGUN['API_KEY']),
        data={
            'from': '{} <postmaster@{}>'.format(from_name, config.RAILGUN['HOST']),
            'to': to,
            'subject': subject,
            'text': text
        }
    )


def on_ip_change(new_ip, log_handler=logger):
    log_handler.debug(
        'Sending email to "{}", becuase IP changed to "{}"'.format(config.RAILGUN['EMAIL_RECIPIENT'], new_ip))

    response = _send_simple_message(
        from_name=config.RAILGUN['FROM_NAME'],
        to=config.RAILGUN['EMAIL_RECIPIENT'],
        subject=config.RAILGUN['EMAIL_SUBJECT'],
        text=config.RAILGUN['EMAIL_TEXT_TEMPLATE'].format(new_ip)
    )

    log_handler.debug('Email server response: "{}"'.format(response.json()))

    return response.status_code == 200
