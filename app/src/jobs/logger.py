# File: logger.py
# Author: Javier Chung
# Date: 11/10/25
# Description: This program contructs a logger 

# Python Libraries
import logging
import logging.handlers
from queue import Queue
from threading import Thread

def setup_logger():
    """
    Production-safe logger for Debian SBCs.
    Routes logs to:
      - syslog (RAM-based)
      - console (journald)
      - rotating file (buffered)
    """

    # Create a logging queue
    log_queue = Queue(-1) # -1 means no size limit

    # Main node
    logger = logging.getLogger("j-node")
    logger.setLevel(logging.INFO)

    # -------- Console Handler (journald) --------
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    ))

    # -------- Syslog Handler (RAM-friendly) --------
    # this is used to send messages to syslog daemon (in ram)
    syslog = logging.handlers.SysLogHandler(address="/dev/log")
    syslog.setFormatter(logging.Formatter(
        "j-node: %(levelname)s - %(message)s"
    ))

    # -------- Rotating File Handler (SD-friendly) --------
    # Rotates between 3 files once they reach 3 mb each 
    rotating = logging.handlers.RotatingFileHandler(
        "/var/log/j-node.log",
        maxBytes=3 * 1024 * 1024,  # 3 MB
        backupCount=3              # 9 MB max
    )
    rotating.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    ))

    # -------- Queue Handler (buffers writes heavily!) --------
    # All logs are written into the queue
    queue_handler = logging.handlers.QueueHandler(log_queue)
    logger.addHandler(queue_handler)

    # -------- Queue Listener --------
    # This actually writes the logs
    listener = logging.handlers.QueueListener(
        log_queue,
        console,
        syslog,
        rotating,
        respect_handler_level=True
    )
    listener.start()

    return logger, listener
