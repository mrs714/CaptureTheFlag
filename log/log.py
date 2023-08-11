from datetime import datetime

_logfile_path = "log\log.txt"
DEBUG = 0
INFO = 1
ERROR = 2

class Log:
    
    def __init__(self, level):
        if 0 <= level <= 2:
            self._level = level
        else:
            self._level = ERROR
    
    def w(self, level, msg):
        if level >= self._level:
            with open(_logfile_path, "a") as f:
                type_str = "[DEBUG]" if level == DEBUG else "[INFO]" if level == INFO else "[ERROR]"
                time_str = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
                f.write(f"{type_str}{time_str}: {msg}\n")