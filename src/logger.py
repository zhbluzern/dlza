import logging
import sys
from datetime import datetime

class SimpleLogger:
    def __init__(self, log_file='process.log'):
        self.logger = logging.getLogger('SimpleLogger')
        self.logger.setLevel(logging.INFO)

        # Formatter: timestamp \t message
        formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        # File handler
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Stream handler (optional: prints to terminal)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def log(self, message: str):
        self.logger.info(message)

if __name__ == "__main__":
    logger = SimpleLogger('logs/zentralgut_inventory.log')

    logger.log("#0098 Starting download...")
    # download logic
    logger.log("Download complete.")

    logger.log("Writing data to JSON...")
    # write logic
    logger.log("JSON file saved.")
