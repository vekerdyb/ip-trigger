import logging

import requests

import config

logger = logging.getLogger(__name__)

URL = 'https://dynamicdns.park-your-domain.com/update?'


def on_ip_change(new_ip, log_handler=logger):
    log_handler.debug('Attempting to update Namecheap IP for host {} to {}'.format(
        config.NAMECHEAP['domain'],
        new_ip
    ))

    data = config.NAMECHEAP
    data['ip'] = new_ip

    response = requests.get(URL, data)

    log_handler.debug('Constructed Namecheap url: {}{}'.format(response.request.url, response.request.body))

    log_handler.debug('Namecheap server response: "{}"'.format(response.content))

    return response.status_code == 200
