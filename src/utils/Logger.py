import logging
from pathlib import Path
from datetime import date
class Logger:
    def __init__(self):
        current_dir = Path(__file__).parent
        self.project_root = current_dir.parent.parent
        logFileName = "error-" + str(date.today().strftime("%Y-%m-%d")) + ".log"
        logging.basicConfig(filename=self.project_root / "logs" / logFileName,format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S',level=logging.INFO)

    def error(self,message):
        logging.error(message)
    
    def exception(self,e):
        logging.exception(e)

    def critical(self,message):
        logging.critical(message)

    def info(self,message):
        logging.info(message)

    def debug(self,message):
        logging.debug(message)