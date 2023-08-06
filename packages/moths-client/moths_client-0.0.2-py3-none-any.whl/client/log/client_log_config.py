import logging
import sys

logging.basicConfig(
    filename="log/client.log",
    format="%(asctime)s %(levelname)-8s "
           "%(module)s  %(funcName)-16s %(message)s",
    level=logging.DEBUG
)

c_log = logging.getLogger('CLIENT')

c_stream = logging.StreamHandler(sys.stdout)
# c_log.addHandler(c_stream)


def log_deco(func):
    global c_log

    def wrapper(*args, **kwargs):

        out = func(*args, **kwargs)
        c_log.debug(f"{func.__name__}({args} {kwargs}) "
                    f"called from {func.__module__}")

        return out

    return wrapper
