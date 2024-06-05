import ntplib
import logging

logger = logging.getLogger(__name__)

class NTPStopwatch(object):
    def __init__(self, server: str="pool.ntp.org", version: int=3):
        self.server = server
        self.version = version
        self.client = ntplib.NTPClient()
        self.__start_time = None
        self.__end_time = None
    
    def test(self):
        try:
            response = self.client.request(self.server, self.version)
            logger.info(f"NTP response: {response}")
        except ntplib.NTPException as e:
            logger.error(f"Failed to contact NTP server {self.server}: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
    
    def start(self):
        try:
            response = self.client.request(self.server, self.version)
            self.__start_time = response.tx_time
        except Exception as e:
            logger.error(f"Error when starting stopwatch: {e}")
    
    def stop(self):
        try:
            response = self.client.request(self.server, self.version)
            self.__end_time = response.tx_time
        except Exception as e:
            logger.error(f"Error when ending stopwatch: {e}")
    
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

