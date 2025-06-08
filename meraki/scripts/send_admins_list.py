"""
Script: send_admins_list.py

Description:
This script connects to the Meraki Dashboard API to retrieve the list of administrators 
for an organization along with their details, exports this information to an Excel file, 
and automatically sends it via email.

Features:
- Secure connection to Meraki Dashboard API to fetch admins and network info.
- Data processing and sorting using pandas.
- Export of admin list to an Excel spreadsheet.
- Automatic email delivery of the Excel report via SMTP (configured for Gmail).
- Email body dynamically includes the current month.

Prerequisites:
- Valid Meraki API Key and Organization ID.
- Configured sender and receiver email credentials.
- Installed Python libraries: meraki, pandas.
- SMTP access enabled for the sender email (e.g., Gmail app passwords or “less secure apps” enabled).

Usage:
- Set the API_KEY, ORG_ID, EMAIL_SENDER, EMAIL_PASS, and EMAIL_TARGET variables with appropriate values.
- Run the script periodically to send updated Meraki admin reports.

This script is useful for automated security and network administration reporting in Meraki environments.

"""

import meraki
import pandas as pd
import smtplib
from email.message import EmailMessage
import os
import datetime

date = datetime.datetime.now()
current_month = date.strftime("%B")


# Meraki setup
API_KEY = "XXX"
ORG_ID = "XXX"

# Email setup
EMAIL_SENDER = "sender@gmail.com"
EMAIL_TARGET = "target@gmail.com"
EMAIL_PASS = "XXX"
SUBJECT = f"List of Meraki admins - {current_month}"
BODY = f"""\
Hello,

Please find attached an Excel file containing the list of Meraki administrators for the month of {current_month}.

This message was generated automatically.
  
If you notice any issues or discrepancies, kindly report them to the network team at XXX.
"""
# Create the message
msg = EmailMessage()
msg["Subject"] = SUBJECT
msg["From"] = EMAIL_SENDER
msg["To"] = EMAIL_TARGET
msg.set_content(BODY)

# Connect with the Meraki API
dashboard = meraki.DashboardAPI(API_KEY, print_console=False)

# Obtain admins of the organization
admins = dashboard.organizations.getOrganizationAdmins(ORG_ID)

# Obtain all the networks of the organization
networks_list = dashboard.organizations.getOrganizationNetworks(ORG_ID)

# Create a dictionary to map IDs to network names
network_id_to_name = {net['id']:net['name'] for net in networks_list}

def replace_networks(networks):
    if not networks:  # If the list is empty or None
        return "Full Organization"
    else:
        names = []
        for net in networks:
            net_id = net.get('id')
            if net_id in network_id_to_name:
                names.append(network_id_to_name[net_id])
            else:
                names.append("Unknown network")
        return ", ".join(names)

df = pd.DataFrame(admins)

# Delete the columns not desired
df = df.drop(columns=["tags", "id"])

# Sort by 'twoFactorAuthEnabled'
df = df.sort_values(by="twoFactorAuthEnabled")

# Apply a function to replace the list of networks by names or "Full Organization"
df['networks'] = df['networks'].apply(replace_networks)

# Export to Excel
df.to_excel("admins_meraki.xlsx", index=False)

# Attach the excel file
filename = "admins_meraki.xlsx"
with open(filename, "rb") as f:
    file_data = f.read()
    msg.add_attachment(file_data, maintype="application", subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=filename)

# Sent email using SMTP (GMAIL in this case)
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_SENDER, EMAIL_PASS)
    smtp.send_message(msg)
