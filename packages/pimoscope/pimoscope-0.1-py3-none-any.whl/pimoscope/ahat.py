"""Automation HAT web app.

"""
import logging
import os
import sys
from bottle import Bottle, request

if 'raspberrypi' in os.uname():
    import automationhat
else:
    try:
        import mock
    except ImportError:
        import unittest.mock as mock
    finally:    
        sys.modules['explorerhat'] = mock.Mock()
    
log = logging.getLogger(__name__)

app = Bottle()


@app.get('/')
def index():
    """Affirms AutomationHAT is physically present.

    **Example request**:

    .. sourcecode:: http

      GET /dut HTTP/1.1
      Host: 192.168.1.87:8080
      Accept: */*

    **Example response**:

    .. sourcecode:: http

      HTTP/1.0 200 OK
      Server: WSGIServer/0.1 Python/2.7.9
      Content-Length: 25
      Content-Type: application/json

      {"isautomationhat": true}

    :status 200: successful
    :resjson string isautomationhat: True if AutomationHAT is present

    """
    return {'isautomationhat': automationhat.is_automation_hat()}


@app.get('/relay')
def status():
    """Status of all three relays as reported by AutomationHAT software.

    **Example request**:

    .. sourcecode:: http

      GET /dut/relay HTTP/1.1
      Host: 192.168.1.88:8080
      Accept: */*

    **Example response**:

    .. sourcecode:: http

      HTTP/1.0 200 OK
      Server: WSGIServer/0.1 Python/2.7.9
      Content-Length: 44
      Content-Type: application/json

      {"three": false, "two": false, "one": false}

    :status 200: succesful
    :resjson boolean three: application state of relay three
    :resjson boolean two: application state of relay two
    :resjson boolean one: application state of relay one

    """
    return automationhat.relay.is_on()


@app.post('/relay')
def toggle():
    """Toggle of all three relays on AutomationHAT.

    **Example request**:

    .. sourcecode:: http

      POST /dut/relay HTTP/1.1
      Host: 192.168.1.88:8080
      Accept: */*

    **Example response**:

    .. sourcecode:: http

      HTTP/1.0 200 OK
      Server: WSGIServer/0.1 Python/2.7.9
      Content-Length: 41
      Content-Type: application/json

      {"three": true, "two": true, "one": true}

    :status 200: succesful
    :resjson boolean three: application state of relay three
    :resjson boolean two: application state of relay two
    :resjson boolean one: application state of relay one

    """
    automationhat.relay.toggle()
    return automationhat.relay.is_on()


@app.get('/relay/<relay>')
def read(relay):
    """Status of specified relay as reported by AutomationHAT software.

    **Example request**:

    .. sourcecode:: http

      GET /dut/relay/one HTTP/1.1
      Host: 192.168.1.88:8080
      Accept: */*

    **Example response**:

    .. sourcecode:: http

      HTTP/1.0 200 OK
      Server: WSGIServer/0.1 Python/2.7.9
      Content-Length: 13
      Content-Type: application/json

      {"relay": "one", "state": true}

    :status 200: succesful
    :resjson boolean relay: relay identifier, e.g. one, two, three
    :resjson boolean state: application state of relay

    """
    if 'one' in relay:
        r = 0
    elif 'two' in relay:
        r = 1
    elif 'three' in relay:
        r = 2
    return {'relay': relay, 'state': automationhat.relay[r].is_on()}


@app.post('/relay/<relay>')
def control(relay):
    """Control the state of an individual relay.

    **Example request**:

    .. sourcecode:: http

      POST /dut/relay/one HTTP/1.1
      Host: 192.168.1.88:8080
      Accept: */*
      Content-Type: application/json
      Content-Length: 12

    **Example response**:

    .. sourcecode:: http

      HTTP/1.0 200 OK
      Server: WSGIServer/0.1 Python/2.7.9
      Content-Length: 14
      Content-Type: application/json

      {"relay": "one", "state": true}

    :status 200: succesful
    :reqjson int state: 1 to turn ON, 0 to turn OFF
    :resjson boolean relay: relay identifier, e.g. one, two, three
    :resjson boolean state: application state of relay

    """
    if 'one' in relay:
        r = 0
    elif 'two' in relay:
        r = 1
    elif 'three' in relay:
        r = 2
    automationhat.relay[r].write(int(request.json['state']))
    return {'relay': relay, 'state': automationhat.relay[r].is_on()}


def initialize():
    log.debug('Detected AutomationHAT.')
    if automationhat.is_automation_hat():
        automationhat.relay.off()
        automationhat.light.off()
        automationhat.light.power.on()
        automationhat.light.comms.on()
    else:
        raise RuntimeError('Failed to detect AutomationHAT.')
    return app
