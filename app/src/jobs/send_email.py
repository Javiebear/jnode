
# File: node_health.py
# Author: Javier Chung
# Date: 11/13/25
# Description: This program is used to gather data on a node

# Project Modules
import logger
# Python Libraries
from redmail import EmailSender
import os
from datetime import datetime



def sendEmail(email, username, node):

    email = EmailSender(
        host=os.getenv("EMAIL_HOST"),
        port=int(os.getenv("EMAIL_PORT")),
        username=os.getenv("EMAIL_USERNAME"),
        password=os.getenv("EMAIL_PASSWORD"),
        use_starttls=True,
    )

    # Getting date and time
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    email.send(
        subject=f"Node Status Update - {date}",
        receivers=[email],
        html="""
        <div style="background-color:#f4f4f4; padding: 40px 0; text-align:center;">

            <!-- Card Container -->
            <div style="
                max-width: 500px;
                margin: auto;
                background: #ffffff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                font-family: Arial, sans-serif;
                text-align: left;
            ">

                <h1 style="text-align:center; color:#333; margin-top:0;">
                    Node Status
                </h1>

                <p style="font-size:16px; color:#555;">
                    Hello <strong>{{ user_name }}</strong>,
                </p>

                <p style="font-size:16px; color:#555;">
                    The node <strong>{{ node_name }}</strong> is
                    <span style="color:#00c853; font-weight:bold;">Online</span>
                    as of <strong>{{ date }}</strong>.
                </p>

            </div>
        </div>
        """,
        body_params={
            "user_name": username,
            "node_name": node,
            "date": date
        }
    )

