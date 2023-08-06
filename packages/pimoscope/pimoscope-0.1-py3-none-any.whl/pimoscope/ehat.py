"""Explorer HAT web app.

"""
import logging
import os
import sys
import time
from bottle import Bottle

if 'raspberrypi' in os.uname():
    import explorerhat
else:
    try:
        import mock
    except ImportError:
        import unittest.mock as mock
    finally:    
        sys.modules['explorerhat'] = mock.Mock()

log = logging.getLogger(__name__)

app = Bottle()
passkey = []


@app.get('/')
def index():
    """Affirms ExplorerHAT is physically present.

    **Example request**:

    .. sourcecode:: http

      GET /ate HTTP/1.1
      Host: 192.168.1.87:8080
      Accept: */*

    **Example response**:

    .. sourcecode:: http

      HTTP/1.0 200 OK
      Server: WSGIServer/0.1 Python/2.7.9
      Content-Length: 23
      Content-Type: application/json

      {"isexplorerpro": true}

    :status 200: successful
    :resjson string isexplorerpro: True if Explorer Pro HAT is present

    """
    return {'isexplorerpro': explorerhat.is_explorer_pro()}


@app.get('/input')
def status():
    """Status of all digital input on ExplorerHAT.

    **Example request**:

    .. sourcecode:: http

      GET /ate/input HTTP/1.1
      Host: 192.168.1.87:8080
      Accept: */*

    **Example response**:

    .. sourcecode:: http

      HTTP/1.0 200 OK
      Server: WSGIServer/0.1 Python/2.7.9
      Content-Length: 43
      Content-Type: application/json

      {"four": 0, "three": 0, "two": 0, "one": 0}

    :status 200: successful
    :resjson int four: status of relay four
    :resjson int three: status of relay three
    :resjson int two: status of relay two
    :resjson int one: status of relay one

    """
    return explorerhat.input.read()


def _handler_passkey(channel, event):
    global passkey
    if event == 'press' and channel <= 4:
        passkey.append(channel)
        explorerhat.light[len(passkey)-1].on()
        log.debug(len(passkey)*'*')


def promt_passkey():
    # get passkey from ExplorerHAT
    global passkey
    passkey = []
    explorerhat.light.off()
    explorerhat.light.pulse()
    while len(passkey) < 4:
        explorerhat.touch.pressed(_handler_passkey)
        time.sleep(0.05)
    log.debug('Passkey is {}'.format(''.join(str(p) for p in passkey)))
    return ''.join(str(p) for p in passkey)


def initialize():
    if explorerhat.is_explorer_pro():
            log.debug('Detected ExplorerHAT Pro.')
            explorerhat.light.off()
            explorerhat.light.green.on()
            explorerhat.light.blue.on()
    else:
        raise RuntimeError('Failed to detect ExplorerHAT Pro.')
    return app
