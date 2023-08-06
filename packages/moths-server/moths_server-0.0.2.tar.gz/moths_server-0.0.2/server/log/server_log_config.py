import logging
import sys
import datetime

cur_date = str(datetime.datetime.now().strftime('%Y_%m_%d'))

logging.basicConfig(
    filename=f"log/server_logs/server__"
             f"{str(datetime.datetime.now())[:10]}.log",
    format="%(asctime)s %(levelname)-8s %(module)s  "
           "%(funcName)-16s %(message)s",
    level=logging.DEBUG
)

s_log = logging.getLogger('SERVER')

s_stream = logging.StreamHandler(sys.stdout)
# s_log.addHandler(s_stream)


def log_deco(func):
    global s_log

    def wrapper(*args, **kwargs):
        out = func(*args, **kwargs)
        s_log.debug(f"{func.__name__}({args} {kwargs}) "
                    f"called from {func.__module__}")

        return out

    return wrapper
