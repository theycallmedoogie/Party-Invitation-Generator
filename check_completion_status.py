#!/usr/bin/env python3
"""
Check completion status of contact list
"""

import pandas as pd
from pathlib import Path

def check_completion_status():
    contacts_file = Path(r"C:\Users\micha\OneDrive\Desktop\contacts_paperless_august2025.csv")
    df = pd.read_csv(contacts_file)

    # Count contacts with and without emails
    total = len(df)
    with_email = len(df[df['Email Address'].notna() & (df['Email Address'] != '')])
    without_email = total - with_email

    print(f'=== CONTACT COMPLETION STATUS ===')
    print(f'Total contacts: {total}')
    print(f'With emails: {with_email}')
    print(f'Missing emails: {without_email}')
    print(f'Completion rate: {(with_email/total)*100:.1f}%')

    print(f'\n=== CONTACTS MISSING EMAILS ===')
    missing = df[df['Email Address'].isna() | (df['Email Address'] == '')]
    for i, (idx, row) in enumerate(missing.iterrows(), 1):
        print(f'{i:2d}. {row["Name"]}')

    print(f'\n=== SHARED EMAIL SITUATIONS ===')
    # Find duplicate emails
    emails = df[df['Email Address'].notna() & (df['Email Address'] != '')]['Email Address']
    duplicates = emails.value_counts()
    duplicates = duplicates[duplicates > 1]

    if not duplicates.empty:
        for email, count in duplicates.items():
            print(f'{email}: {count} people')
            contacts = df[df['Email Address'] == email]['Name'].tolist()
            for contact in contacts:
                print(f'  - {contact}')
            print()
    else:
        print('No shared email situations found')

if __name__ == "__main__":
    check_completion_status()