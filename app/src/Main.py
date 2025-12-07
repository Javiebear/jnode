# File: Main.py
# Author: Javier Chung
# Date: 11/05/25
# Description: This program will use a machine Learning Alrogithm to predict the weather

# Project Modules
from jobs.logger import setup_logger 
from jobs.node_health import get_data
from jobs.send_email import sendEmail

# Python Libraries
import threading
import time

# Logger setup
logger, listener = setup_logger()

def node_data_worker():
    """
        this method is used to control a process to constanly send data
    """
    while True:
        data = get_data()
        logger.info(f"Node health: {data}")
        #TODO: SEND DATA TO CLOUD
        time.sleep(30)

# Main Program
if __name__ == "__main__":
    logger.info(f"Starting all processes within Main")

    #TODO: Currently will not send to anyone as there is no unique identifier for different nodes
    # Sends email to user if their node is online
    logger.info(f"Sending online status via email to user.")
    # sendEmail(email, user, node)


    threading.Thread(target=node_data_worker, daemon=True).start()


