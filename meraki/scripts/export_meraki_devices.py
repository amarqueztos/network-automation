"""
Script: export_meraki_devices.py

Description:
This script connects to the Meraki Dashboard API to retrieve the list of devices 
belonging to an organization. It replaces network IDs with their corresponding 
human-readable names and exports the cleaned and sorted data to an Excel file.

Features:
- Secure connection to the Meraki Dashboard API to fetch devices and network info.
- Dictionary mapping of network IDs to names for better readability.
- Data cleaning and sorting using pandas.
- Export of the device list to an Excel spreadsheet.

Prerequisites:
- Valid Meraki API Key and Organization ID.
- Installed Python libraries: meraki, pandas, openpyxl.

Usage:
- Set the API_KEY and ORG_ID variables with appropriate values.
- Run the script to generate an up-to-date Excel report of the devices in the organization.

This script is useful for inventory management, network audits, and reporting in Meraki environments.
"""

import os
import meraki
import pandas as pd

# --- Meraki setup ---
# Replace with your actual API key and organization ID
API_KEY = "XXX"
ORG_ID = "XXX"

# Initialize the Meraki Dashboard API client
dashboard = meraki.DashboardAPI(API_KEY, print_console=False)

# Get all devices from the specified organization
devices = dashboard.organizations.getOrganizationDevices(ORG_ID, total_pages='all')

# Get all networks from the organization
networks_list = dashboard.organizations.getOrganizationNetworks(ORG_ID)

# Create a mapping from network ID to network name
network_id_to_name = {net["id"]: net["name"] for net in networks_list}

# Function to replace network ID with network name
def replace_network_id(net_id):
    return network_id_to_name.get(net_id, "Unknown network")

# Create a DataFrame from the device list
df = pd.DataFrame(devices)

# Drop columns that are not needed in the report
columns_to_drop = [
    "lat", "lng", "url", "imei", "details", "address",
    "notes", "tags", "configurationUpdatedAt", "firmware"
]
df = df.drop(columns=columns_to_drop, errors="ignore")  # Ignore if any column doesn't exist

# Sort the devices by network ID
df = df.sort_values(by="networkId")

# Replace network IDs with network names
df["networkId"] = df["networkId"].apply(replace_network_id)

# Export the final DataFrame to an Excel file
df.to_excel("devices_meraki.xlsx", index=False)

