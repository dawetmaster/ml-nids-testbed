import signal
import contextlib

# Define a custom exception for signal handling
class SkipSectionException(Exception):
    pass

# Signal handler that raises the custom exception
def signal_handler(signum, frame):
    raise SkipSectionException()

# Context manager to handle the custom exception
@contextlib.contextmanager
def skip_on_signal():
    original_handler = signal.signal(signal.SIGINT, signal_handler)
    try:
        yield
    except SkipSectionException:
        print("Skipping current section due to Ctrl+C")
    finally:
        signal.signal(signal.SIGINT, original_handler)