#!/usr/bin/python3 -OO
'''
Read and parse configuration into ConfigParser object

Default settings.cfg uses system files and doesn't require any changes.

To make use of this, you must:

    * edit /etc/services and make entries for seriouscast
      use port 30000 or any other of your choosing:
          + `seriouscast 30000/tcp`
          + `seriouscast 30000/udp`
    * find or set your hostname in /etc/hostname (on Debian and similar)
    * add an entry in your /etc/hosts for your hostname if it doesn't yet
      exist. `0.0.0.0' is always safe to use for the IP address, as it never
      changes, assuming you want the server to be available to all.
          + `0.0.0.0 myhostname`
    * add an entry in $HOME/.netrc for your hostname:
      `machine MYHOSTNAME:seriouscast login MYUSERNAME password MYPASSWORD`
      (the ALLCAPS words are what must be replaced with their real values)

Otherwise overwrite settings.cfg with the contents of example_settings.cfg
and edit as necessary.
'''
import socket, netrc

def configuration(filename='settings.cfg', hostname='localhost', port='30000'):
    '''
    Parse configuration from given filename
    '''
    authenticators = None
    config = configparser.ConfigParser()
    load(config, filename)
    hostname = config.get('SeriousCast', 'hostname')
    if hostname == '(from socket.gethostname())':
        hostname = socket.gethostname()
        config.set('SeriousCast', 'hostname', hostname)
    netrc_lookup = '%s:seriouscast' % hostname
    port = config.get('SeriousCast', 'port')
    if port == '(from /etc/services)':
        port = socket.getservbyname('seriouscast')
        config.set('SeriousCast', 'port', port)
    username = config.get('SeriousCast', 'username')
    if username == '(from .netrc)':
        authenticators = netrc.netrc()
        username = authenticators.authenticators(netrc_lookup)[0]
        config.set('SeriousCast', 'username', username)
    password = config.get('SeriousCast', 'password')
    if password == '(from .netrc)':
        if authenticators is None:
            authenticators = netrc.netrc()
        password = authenticators.authenticators(netrc_lookup)[2]
        config.set('SeriousCast', 'password', password)

def load(config, filename):
    '''
    Check for existence of configuration file and load it.

    If it doesn't exist, throw an exception.
    '''
    if not os.path.isfile(filename):
        raise ValueError('%s not found', filename)

    config.read(filename)
