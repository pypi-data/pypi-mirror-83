import time
import sys
from subprocess import Popen
from os.path import join, dirname, exists

_KILL_TIMEOUT = 3
_PID_FILE = 'sallron.pid'

def send_message():
    """
    To be implemented.
    The idea here is:
        1. overwrite standard exception flow with custom exception_logger found in util/logger.py
        2. send message with resulting logs on every restart
        3. accompany message with deploy + customer name
    """
    if exists(_PID_FILE):
        print("sallron had to be restarted, take a look at the error logs...")
    pass

def write_pid(pid):
    with open(_PID_FILE, 'w') as w:
        w.write(pid)

def kill_pid(delete_file=True):
    '''Kill processes.'''
    with open(_PID_FILE, 'r') as rapid:
        pid = rapid.read()
    if delete_file:
        Popen(f'rm {_PID_FILE}', shell=True)
        print('.pid file purged')
    Popen('kill %s' % pid, shell=True)
    print('pid killed')

def eternal_runner(filepath):
    while True:
        try:
            send_message()
            p = Popen(f"python3 {filepath}", shell=True)
            p.wait()
        except (KeyboardInterrupt, SystemExit):
            print('Exit signal received, shutting down.')
            time.sleep(_KILL_TIMEOUT)
            kill_pid()
            sys.exit()
            print("That's all folks.")