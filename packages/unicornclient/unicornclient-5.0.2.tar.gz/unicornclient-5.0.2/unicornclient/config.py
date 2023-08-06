import os
import configparser

ENV = os.getenv('PYTHONENV', 'prod')

# Not user configurable
PROC_PATH = os.getenv('PROC_PATH', '/proc')
SYS_PATH = os.getenv('SYS_PATH', '/sys')

SECRET_PATH = '/etc/unicornclient/secret'
CONFIG_PATH = '/etc/unicornclient/config.ini'
if os.path.isfile('./config.ini'):
    CONFIG_PATH = './config.ini'

# Configuration file
_CONFIG = configparser.ConfigParser()
_CONFIG.read(CONFIG_PATH)
_DEFAULT = _CONFIG['DEFAULT']

LOG_LEVEL = _DEFAULT.get('log_level', 'DEBUG')
LOG_FORMAT = _DEFAULT.get('log_format', '%(asctime)s - %(levelname)s - %(message)s')

HOST = _DEFAULT.get('host', 'localhost')
PORT = _DEFAULT.getint('port', 8080)
SSL_VERIFY = _DEFAULT.getboolean('ssl_verify', False)

MQTT_HOST = _DEFAULT.get('mqtt_host', 'localhost')
MQTT_PORT = _DEFAULT.getint('mqtt_port', 1883)
