#!/usr/bin/env python3
"""
Export updated high-confidence matches with corrections
"""

import csv
from pathlib import Path

def export_updated_matches():
    paperless_csv_path = Path(r"C:\Users\micha\OneDrive\Desktop\contacts_paperless_august2025.csv")
    
    # Updated high-confidence matches with corrections
    selected_contacts = [
        # Perfect matches - corrected as requested
        {
            'Name': 'Kiara Casley',
            'Email Address': 'kcasley@gmail.com',
            'Phone Number': '',
            'Company': 'KPMG',
            'Role': '',
            'Notes': ''
        },
        {
            'Name': 'West Lakshmi',
            'Email Address': 'lakshmi_west@hotmail.com',  # Keep unchanged as requested
            'Phone Number': '',
            'Company': '',
            'Role': '',
            'Notes': ''
        },
        {
            'Name': 'Abbey Durez',
            'Email Address': 'abbyduruz@gmail.com',
            'Phone Number': '',
            'Company': '',
            'Role': '',
            'Notes': ''
        },
        {
            'Name': "Carol O'Carol",
            'Email Address': 'carol_ocarroll@yahoo.com.au',
            'Phone Number': '',
            'Company': '',
            'Role': '',
            'Notes': ''
        },
        {
            'Name': 'Elizabeth Canham',
            'Email Address': 'e_canham@hotmail.com',
            'Phone Number': '',
            'Company': '',
            'Role': '',
            'Notes': ''
        },
        {
            'Name': 'Erron Gardner',
            'Email Address': 'errong@hotmail.com',  # Changed to personal email as requested
            'Phone Number': '',
            'Company': '',
            'Role': '',
            'Notes': ''
        },
        {
            'Name': 'Anita David',
            'Email Address': 'prishdavid@hotmail.com',  # Using husband's email as requested
            'Phone Number': '',
            'Company': '',
            'Role': '',
            'Notes': 'Email address belongs to husband Prishan David - Anita\'s email out of date'
        },
        
        # Add the remaining people with empty entries for manual completion
        {'Name': 'Ghirawoo Sara', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Ghirawoo Michael', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Nancy Kusmadi', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Steve Kusmadi', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Agnes Chan', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Liu Jenny', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Rothwell Kathy', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Rothwell Iain', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'West Shane', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Lock Bec', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Lock Murray', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Shivayogan Shamini', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Shivayogan Yogan', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Yanamoto Kanae', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Hancock Matt', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Hancock Anita', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Kerr Luke', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Kerr Clare', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Carlon Phil', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Carlon Sarah', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Bowden Damien', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Bowden Tara', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Charles Michael', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Charles Kylie', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Baratta Brigid', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Baratta John', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Baratta Bede', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Baratta Leanne', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Cranney David', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Cranney Sarah', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Prishan David', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Henderson Liz', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Henderson Tim', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Liaw Grace', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Chung Wayne', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Coorey Dao', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Coorey Adrian', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Benton Mariska', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Benton Campbell', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Scott Lara', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': "O'Kane Matt", 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': "O'Kane Renee", 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Moses Bianca', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Moses (partner)', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': 'Partner - manual entry required'},
        {'Name': 'Montin Luke', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Montin (partner)', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': 'Partner - manual entry required'},
        {'Name': 'Medves Mike', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Liz Foster', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
        {'Name': 'Leo Foster', 'Email Address': '', 'Phone Number': '', 'Company': '', 'Role': '', 'Notes': ''},
    ]
    
    # Save to CSV
    with open(paperless_csv_path, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['Name', 'Email Address', 'Phone Number', 'Company', 'Role', 'Notes']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(selected_contacts)
    
    print(f"✓ Exported {len(selected_contacts)} contacts to {paperless_csv_path}")
    
    # Show summary
    with_email = len([c for c in selected_contacts if c['Email Address']])
    with_notes = len([c for c in selected_contacts if c['Notes']])
    
    print(f"\nSUMMARY:")
    print(f"- Total contacts: {len(selected_contacts)}")
    print(f"- With email addresses: {with_email}")
    print(f"- With notes: {with_notes}")
    print(f"- Ready for Paperless Post import")
    
    print(f"\n✅ COMPLETED CONTACTS:")
    completed = [c for c in selected_contacts if c['Email Address']]
    for contact in completed:
        note = f" ({contact['Notes']})" if contact['Notes'] else ""
        print(f"  {contact['Name']} → {contact['Email Address']}{note}")

if __name__ == "__main__":
    export_updated_matches()