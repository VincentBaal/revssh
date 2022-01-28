from datetime import datetime
import os

INFO = "INFO"
WARNING = "WARN"
ERROR = "ERROR"


def info(message):
    log(INFO, message)


def warning(message):
    log(WARNING, message)


def error(message):
    log(ERROR, message)


def log(tag, message):
    log_folder = os.path.dirname(os.path.realpath(__file__)) + "/log"
    if not os.path.exists(log_folder):
        os.mkdir(log_folder)
    t = datetime.now()
    text = str(t) + ' (' + tag + ') ' + message
    log_file_name = log_folder + '/' + str(t.date()) + '.log'
    f = open(log_file_name, 'a')
    f.write(text + "\n")
    print(text)
