""" Test module. Auto pytest that can be started in IDE or with

    >>> python -m pytest

in terminal in tests folder.
"""
#%%

import sys
from pathlib import Path
import inspect
import os

sys.path.insert(0, Path(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)).parents[1].as_posix())

import mylogging


def test_warnings():

    mylogging._COLORIZE = 0  # Turn on colorization on all functions

    # We can define whether to
    #   display warnings: debug=1,
    #   ignore warnings: debug=0,
    #   stop warnings as errors: debug=3
    # Beware, that even if no warnings are configured, default warning setings are applied - so warning settings can be overwriten

    mylogging.set_warnings(
        debug=1,
        ignored_warnings=[
            "invalid value encountered in sqrt",
            "encountered in double_scalars"],
        ignored_warnings_module_category=[
            ('statsmodels.tsa.arima_model', FutureWarning)
        ])

    # We can create warning that will be displayed based on warning settings
    mylogging.user_warning('Hessian matrix copmputation failed for example', caption="RuntimeError on model x")

    # In case we don't know exact error reason, we can use traceback_warning in try/except block

    try:
        print(10 / 0)

    except Exception:
        mylogging.traceback_warning("Maybe try to use something different than 0")

    # In case we don't want to warn, but we have error that should be printed anyway and not based on warning settings, we can use user_message that return extended that we can use...

    print(mylogging.user_message("I will be printed anyway"))

    ### Just test if log to file pass
    mylogging._TO_FILE = "delete.log"

    mylogging.user_warning('Hessian matrix copmputation failed for example', caption="RuntimeError on model x")

    try:
        print(10 / 0)

    except Exception:
        mylogging.traceback_warning("Maybe try to use something different than 0")

    os.remove("delete.log") 


if __name__ == "__main__":

    pass

    # test_warnings()

    # import mylogging


### TODO use loguru as option - just save some settings


# from loguru import logger

# logger.add(sys.stdout, level="WARNING", colorize=True, format="<green>{time}</green> <level>{message}</level>")

# logger.opt(exception=True)

# def my_function(x, y, z):
#     # An error? It's caught anyway!
#     return 1 / (x + y + z)


# # try:
# #     1 / x
# # except Exception:
# #     logger.exception("Oups...")


# logger.info("Logging 'WARNING' or higher messages only")


# # logger.warn("Initialization in progress")

# logger.debug("Back to debug messages")

# print('ahoj')

# logger.add("out.log", backtrace=False, diagnose=True, format="{time} {level} \n{message}")


# def func(a, b):
#     return a / b


# def nested(c):
#     try:
#         func(5, c)
#     except ZeroDivisionError:
#         logger.exception("Whaaat?!", backtrace=False)
#         pass

# nested(0)
