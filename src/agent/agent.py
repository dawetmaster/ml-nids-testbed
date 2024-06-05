from utils.sysmonitor import create_server
from utils.log import setup_logging
import logging

setup_logging()

logger = logging.getLogger(__name__)

def main(port: int=5758):
    try:
        server = create_server(port=5758)
        server.start()
        logger.info(f"Starting server on port {port}")
        server.wait_for_termination()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        logger.info("Shutting down server gracefully...")
        server.stop(0)
        logger.info("Server stopped")

if __name__ == '__main__':
    main(port=5758)