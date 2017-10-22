import logging

import requests

import config

logger = logging.getLogger(__name__)

URL = 'https://api.cloudflare.com/client/v4/'


def on_ip_change(new_ip, log_handler=logger):
    log_handler.debug('Attempting to update Cloudflare IP for host {} to {}'.format(
        config.CLOUDFLARE['dnsRecordData']['name'],
        new_ip
    ))

    headers = {
        'X-Auth-Email': config.CLOUDFLARE['email'],
        'X-Auth-Key': config.CLOUDFLARE['apiKey'],
        'Content-Type': 'application/json'
    }

    data = config.CLOUDFLARE['dnsRecordData']
    data['content'] = new_ip

    url = config.CLOUDFLARE['baseUrl'] + 'zones/{}/dns_records/{}'.format(
        config.CLOUDFLARE['zoneId'],
        config.CLOUDFLARE['dnsRecordId']
    )

    response = requests.put(url, json=data, headers=headers)

    log_handler.debug('Constructed Cloudflare url: {}{}'.format(response.request.url, response.request.body))

    log_handler.debug('Cloudflare server response: "{}"'.format(response.content))

    return response.status_code == 200
