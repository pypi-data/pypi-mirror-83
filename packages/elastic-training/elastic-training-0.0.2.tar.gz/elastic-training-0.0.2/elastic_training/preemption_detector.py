
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from multiprocessing import Value
from ctypes import c_bool
from datetime import datetime
import logging

DIRECTORY_TO_WATCH = "/usr/share"

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class PreemptHandler(FileSystemEventHandler):
    def __init__(self):
        super(PreemptHandler, self).__init__()
        self.is_preempted = Value(c_bool, False)
        self.exit_function = None

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith("/to-be-preempted"):
            logger.info("detected preempt signal, should stop and return.")
            self.is_preempted.value = True
            if self.exit_function is not None:
                logger.info("start running exit function.")
                self.exit_function()
                logger.info("completed running exit function")

class PreemptDetector:
    def __init__(self):
        self.observer = Observer()
        self.event_handler = PreemptHandler()

    def run(self):
        self.observer.schedule(self.event_handler, DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()

    def is_preempted(self):
        return self.event_handler.is_preempted.value

    def stop(self):
        self.observer.stop()