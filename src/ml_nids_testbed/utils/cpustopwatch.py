import logging
import time

logger = logging.getLogger(__name__)

class CPUStopwatch(object):
    def __init__(self):
        self.__start_time = None
        self.__end_time = None

    def start(self):
        self.__start_time = time.time()
    
    def stop(self):
        self.__end_time = time.time()
    
    def reset(self):
        self.__start_time = None
        self.__end_time = None
    
    def calculate_time(self):
        if self.__start_time is None or self.__end_time is None:
            raise ValueError("Stopwatch has not been started or ended")
        else:
            return self.__end_time - self.__start_time

    @property
    def start_time(self):
        return self.__start_time
    
    @property
    def end_time(self):
        return self.__end_time

