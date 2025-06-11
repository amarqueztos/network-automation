# Meraki Scripts

This folder contains small scripts to automate tasks with Meraki devices and the Meraki API.

---

## send_admins_list.py

This script connects to the Meraki Dashboard API to retrieve the list of administrators for a given organization.  
It processes the data, customizes the output for better readability, and exports it to an Excel file.  
Then, it sends this Excel report as an email attachment via SMTP (configured for Gmail).

The email includes a subject and body that mention the current month, making the report easier to track.

### Key features:
- Fetches admin info and networks using the Meraki API.
- Maps network IDs to network names for clarity.
- Sorts admins by two-factor authentication status.
- Exports results to an Excel file.
- Sends the Excel file via email automatically.

### Dependencies

Make sure to install these Python packages before running the script:

```bash
pip install meraki pandas openpyxl
```

## export_meraki_devices.py

This script connects to the Meraki Dashboard API to retrieve the list of devices for a given organization.
It processes the data, replaces network IDs with human-readable names, and exports it to an Excel file for better readability and reporting.

### Key features:
- Fetches device and network information using the Meraki API.
- Maps network IDs to network names for clarity.
- Removes irrelevant metadata columns from the dataset.
- Sorts devices by their associated network.
- Exports results to an Excel file (devices_meraki.xlsx).

### Dependencies

Make sure to install these Python packages before running the script:

```bash
pip install meraki pandas openpyxl
```

