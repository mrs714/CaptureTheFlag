from datetime import datetime, date
import os

_log_object = None
_logfile_dir = "logs"
_max_logs = 10

#Log levels
_max_level = 2
DEBUG = 0
INFO = 1
ERROR = 2


class Log:
    
    def __init__(self, level):
        if 0 <= level <= _max_level:
            self.__level = level
        else:
            self.__level = ERROR
        
        self.__logfile_path = None
        self.__date = None
    
    def _allocate_logs(self):
        """
        removes the oldest log file if the number of logs is equal or greater than _max_logs
        """       
        logs = os.listdir(_logfile_dir)
        if len(logs) >= _max_logs:
            oldest_log = min([(f"{_logfile_dir}/{log}", os.path.getmtime(f"{_logfile_dir}/{log}")) for log in logs])[0]
            os.remove(oldest_log)    
    
    def _define_dir(self):
        if self.__date != date.today():
            self.__date = date.today()
            self._allocate_logs()
            self.__logfile_path = f"{_logfile_dir}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f')}.log"
    
    def write(self, level, msg):
        if _max_level >= level >= self.__level:
            self._define_dir()
            try:
                with open(self.__logfile_path, "a") as f:
                    type_str = "[DEBUG]" if level == DEBUG else "[INFO]" if level == INFO else "[ERROR]"
                    time_str = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
                    f.write(f"{type_str}{time_str}: {msg}\n")
            except:
                print("Error writing to log file")

def _init_log():
    global _log_object
    if _log_object is not None:
        return
    correct = False
    while not correct:
        try:
            level = int(input(f"Enter the log level ({DEBUG}: DEBUG, {INFO}: INFO, {ERROR}: ERROR): "))
            if 0 <= level <= _max_level:
                correct = True
        except:
            print("Error")
    _log_object = Log(level)
    _log_object._define_dir()      
    
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