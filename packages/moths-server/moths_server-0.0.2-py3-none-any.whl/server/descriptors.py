import os
import signal
from log.server_log_config import s_log as log


class PortVerifier:
    def __set__(self, inst, val):

        if val < 0:
            log.error('Incorrect port assigned! Shutting down...')
            os.kill(os.getpid(), signal.SIGINT)

        inst.__dict__[self.name] = val

    def __set_name__(self, owner, name):
        self.name = name
