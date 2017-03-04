#!/usr/bin/env python
"""
Use ipify.org to check the current ip address.
If the ip address has changed, trigger an event.
"""
import config
import logging
import subprocess

import requests
import importlib

logger = logging.getLogger(__name__)

STORAGE_FILE = 'ip-trigger-storage'
GET_IP_URL = 'https://api.ipify.org?format=json'

EMAIL_BACKEND = 'railgun_backend'

email_backend = importlib.import_module(EMAIL_BACKEND)

def store_ip(ip):
    logger.debug('Attempting to open "{}" for appending'.format(STORAGE_FILE))
    file = open(STORAGE_FILE, 'a')
    file.write(ip + '\n')
    file.close()
    logger.debug('IP {} stored in file'.format(ip))


def retrieve_last_ip_from_storage():
    logger.debug('Attempting to retrieve last IP from "{}"'.format(STORAGE_FILE))
    last_ip = subprocess.check_output(['tail', '-1', STORAGE_FILE])
    last_ip = last_ip.strip().decode('utf-8')
    logger.debug('Last IP: "{}"'.format(last_ip))
    return last_ip


def detect_current_ip():
    logger.debug('Attempting to connect to "{}"'.format(GET_IP_URL))
    response = requests.get(GET_IP_URL)
    logger.debug('Response status code "{}"'.format(response.status_code))
    logger.debug('Response body "{}"'.format(response.json()))
    return response.json()['ip']


def is_update_needed(last_ip, current_ip):
    update_needed = last_ip != current_ip
    logger.debug('Update of IP {} needed'.format('is' if update_needed else 'not'))
    return update_needed


def init_logger():
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('{asctime} [{levelname:^10}] {name}: {message}', style='{')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


import os
def touch(fname, mode=0o666, dir_fd=None, **kwargs):
    flags = os.O_CREAT | os.O_APPEND
    with os.fdopen(os.open(fname, flags=flags, mode=mode, dir_fd=dir_fd)) as f:
        os.utime(f.fileno() if os.utime in os.supports_fd else fname,
            dir_fd=None if os.supports_fd else dir_fd, **kwargs)

def run():
    touch(STORAGE_FILE)
    current_ip = detect_current_ip()
    last_ip = retrieve_last_ip_from_storage()
    if is_update_needed(last_ip, current_ip):
        trigger_update(last_ip, current_ip)
        store_ip(current_ip)


def trigger_update(old_ip, new_ip):
    logger.debug('Sending email to "{}", becuase IP changed from "{}" to "{}"'.format(config.EMAIL_RECIPIENT, old_ip, new_ip))
    response = email_backend.send_simple_message(
        from_name=config.FROM_NAME,
        to=config.EMAIL_RECIPIENT,
        subject=config.EMAIL_SUBJECT,
        text=config.EMAIL_TEXT_TEMPLATE.format(new_ip)
    )
    logger.debug('Email server response: "{}"'.format(response.json()))

if __name__ == '__main__':
    init_logger()
    run()
