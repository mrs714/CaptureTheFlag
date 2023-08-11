from datetime import datetime
import os

_log_object = None
_logfile_dir = "logs"
_max_logs = 3
DEBUG = 0
INFO = 1
ERROR = 2

class Log:
    
    def __init__(self, level):
        if 0 <= level <= 2:
            self._level = level
        else:
            self._level = ERROR
        
        self._logfile_path = f"{_logfile_dir}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f')}.log"

    
    def _allocate_logs(self):
        """
        removes the oldest log file if the number of logs is equal or greater than _max_logs
        returns True if any change was made, False otherwise
        """
        if not os.path.exists(_logfile_dir):
            os.mkdir(_logfile_dir)
        
        logs = os.listdir(_logfile_dir)
        if len(logs) >= _max_logs:
            oldest_log = min([(f"{_logfile_dir}/{log}", os.path.getmtime(f"{_logfile_dir}/{log}")) for log in logs])[0]
            os.remove(oldest_log)
            return True
        return False      
    
    def _define_dir(self):
        if self._allocate_logs():
            self._logfile_path = f"{_logfile_dir}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f')}.log"
    
    def write(self, level, msg):
        if 2 >= level >= self._level:
            self._define_dir()
            with open(self._logfile_path, "a") as f:
                type_str = "[DEBUG]" if level == DEBUG else "[INFO]" if level == INFO else "[ERROR]"
                time_str = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
                f.write(f"{type_str}{time_str}: {msg}\n")

def _init_log():
    global _log_object
    if _log_object is not None:
        return
    correct = False
    while not correct:
        try:
            level = int(input("Enter the log level (0: DEBUG, 1: INFO, 2: ERROR): "))
            if 0 <= level <= 2:
                correct = True
        except:
            print("Error")
    _log_object = Log(level)
        
    
def w(level, msg):
    """
    Writes a message to the log file
    """
    _init_log()
    _log_object.write(level, msg)

def d(msg):
    w(DEBUG, msg)

def i(msg):
    w(INFO, msg)

def e(msg):
    w(ERROR, msg)

_init_log()