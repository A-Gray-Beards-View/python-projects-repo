import sys
import time
import threading

class ProgressSpinner:
    def __init__(self, message="Processing"):
        self.spinner = ['|', '/', '-', '\\']
        self.idx = 0
        self.message = message
        self.stop_running = False
        self.thread = None

    def start(self):
        if self.thread is not None and self.thread.is_alive():
            self.stop()
        self.stop_running = False
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.stop_running = True
        if self.thread is not None:
            self.thread.join()
            self.thread = None  # Explicitly set the thread to None
        sys.stdout.write('\r' + ' ' * (len(self.message) + 4) + '\r')  # Clear the spinner line
        sys.stdout.flush()
        sys.stdout.write(f'\r{self.message} finished.\n')  # Print the finished message with a newline
        sys.stdout.flush()

    def run(self):
        while not self.stop_running:
            sys.stdout.write(f'\r{self.message} {self.spinner[self.idx]}')
            sys.stdout.flush()
            self.idx = (self.idx + 1) % len(self.spinner)
            time.sleep(0.1)

    def is_running(self):
        return self.thread is not None and self.thread.is_alive()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

# Example usage
if __name__ == "__main__":
    with ProgressSpinner("Processing"):
        try:
            # Simulate some work
            time.sleep(5)
        finally:
            print("Done")