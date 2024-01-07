import logging
from sys import stdout
from os import path

# Define logger
logger = logging.getLogger("Tong")#avoid other package's logger

logger.setLevel(logging.DEBUG)  # set logger level
logFormatter = logging.Formatter(
    "%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s"
)

consoleHandler = logging.StreamHandler(stdout)  # set streamhandler to stdout
consoleHandler.setFormatter(logFormatter)
if path.isdir("/data/logs"):
    logspath = "/data/logs/"
else:
    # 获取当前脚本所在的目录
    script_dir = path.dirname(path.abspath(__file__))

    # 将项目根目录添加到 sys.path
    logspath = path.abspath(path.join(script_dir, ".."))

fileHandler = logging.FileHandler(filename=logspath + "logging.log",mode="w")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)
logger.info("logger starts running")
