import logging
import argparse
import uuid
import threading
import sys

import bottle
from knilb import agent

log = logging.getLogger(__name__)

app = bottle.Bottle()
passkey = []


@app.get('/')
def index():
    """Show all routes on web app.

    Returns:
        A dict mapping each URI with available HTTP Method, e.g. {'/': 'GET'}
    """
    return {r.rule: r.method for r in app.routes}

# def _thread_bottle(port, debug=False):
#     log.debug('Starting web server.')
#     for r in app.routes:
#         log.info('{} http://host:{}{}'.format(r.method, port, r.rule))
#     bottle.run(app=app, host='0.0.0.0', port=port, debug=False, reloader=False)


def _thread_agent(user, passkey, cloud):
    try:
        while True:
            a = agent.Agent(user, passkey, cloud)
            if a.register():
                a.run()
            else:
                log.info('Agent register FAIL, try again.')
    except KeyboardInterrupt as e:
        log.debug('Goodbye')
    except Exception as e:
        log.critical(e)
    finally:
        log.debug('All Done')


def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    d = '''Pimo contains examples of Device Under Test (using a Pimoroni
           AutomationHAT) and Automated Test Equipment (using a Pimoroni
           ExplorerHAT).'''
    parser = argparse.ArgumentParser(description=d)
    parser.add_argument('app', type=str, choices=['ate', 'dut'],
                        help='''ate for Automated Test Equipment or dut for 
                                device under test.''')
    # group = parser.add_mutually_exclusive_group(required=True)
    # group.add_argument('-a', '--ahat', action='store_true',
    #                    help='Device Under Test using Pimoroni AutomationHAT.')
    # group.add_argument('-e', '--ehat', action='store_true',
    #                    help='''Automated Test Equipment using Pimoroni
    #                         ExplorerHAT Pro.''')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print copious debug statements.')
    parser.add_argument('-p', dest='port', type=int,
                        metavar='<port>', default=8080,
                        help='''Port on localhost of Web App API. Default 8080.
                                Recommended 8081 for ATE or
                                Recommended 8082 for Device Under Test.''')
    parser.add_argument('-c', dest='cloud', type=str, nargs=2,
                        # metavar='<foo> <API Key>', nargs=2,
                        help='''Cloud URL and API key.
                                This causes Agent to run automatically.
                                URL must be <scheme://ipaddress:port>,
                                for example http://192.168.1.2:8080''')
    args = parser.parse_args()

    # Modify logging for verbose
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        log.debug('OK, VERBOSE DEBUGGING ON.')

    # DESIGN: automationhat and explorerhat compete for GPIO pins.
    # DESIGN: do conditional import to avoid race condition for pins.
    try:
        if args.app == 'ate':
            from pimoscope import ehat
            subapp = ehat.initialize()
            # passkey = ehat.promt_passkey() if args.cloud else None
            app.mount('ate', subapp)
            log.info('Starting Automation on port {}'.format(args.port))
        if args.app == 'dut':
            from pimoscope import ahat
            subapp = ahat.initialize()
            app.mount('dut', subapp)
            log.info('Starting Explorer on port {}'.format(args.port))
    except RuntimeError as e:
        log.critical(e)
        sys.exit()
    except Exception as e:
        log.critical(e)
        sys.exit()
    else:
        if args.cloud and args.app == 'ate':
            a = threading.Thread(name='Agent={}'.format(uuid.getnode()),
                                 target=_thread_agent,
                                 args=(uuid.getnode(), passkey, args.cloud))
            a.setDaemon(True)
            a.start()
        elif args.cloud:
            log.warning('Agent runs IF ONLY IF configured as ate.')

    for r in app.routes:
        log.info('{} http://host:{}{}'.format(r.method, args.port, r.rule))
    bottle.run(app=app, host='0.0.0.0', port=args.port, debug=False)


if __name__ == '__main__':
    main()
