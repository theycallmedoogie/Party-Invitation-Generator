#!/usr/bin/env python3
"""
Update contacts file with matches found from partial search
"""

import pandas as pd
from pathlib import Path

def update_contacts_from_search():
    """Update the contacts file with the best matches found"""
    
    contacts_file = Path(r"C:\Users\micha\OneDrive\Desktop\contacts_paperless_august2025.csv")
    
    # Read current contacts
    df = pd.read_csv(contacts_file)
    
    print("=== UPDATING CONTACTS WITH SEARCH RESULTS ===\n")
    
    # Key matches found from partial search
    updates = {
        "Hancock Matt": {
            "email": "mat.hancock@gmail.com", 
            "notes": "Found via partial search - mat.hancock@gmail.com matches Matt Hancock pattern"
        },
        
        "Charles Michael": {
            "email": "m_chucky76@hotmail.com",
            "notes": "Found as 'Michael Charles' - likely same person, nickname Chucky"
        },
        
        "Baratta Brigid": {
            "email": "brigidodwyer@yahoo.com.au",
            "notes": "Found as Brigid O'Dwyer - twins with Bede Baratta, maiden name Baratta"
        },
        
        "Prishan David": {
            "email": "prishdavid@hotmail.com", 
            "notes": "Found as 'Prishan and Anita' - husband of Anita (Jacob) David"
        },
        
        "Liaw Grace": {
            "email": "grapiek@hotmail.com",
            "notes": "Found as 'Grace Liaw' - husband Wayne Chung, address 53B Nelson Ave Belmore"
        },
        
        "Chung Wayne": {
            "email": "grapiek@hotmail.com",  # Same as Grace - shared email
            "notes": "Husband of Grace Liaw - shares email grapiek@hotmail.com"
        },
        
        "Coorey Dao": {
            "email": "p.coorey@unsw.edu.au",  # Work email found
            "notes": "Dr Pornsakol Dao Coorey - Thai name is Pornsakol, work email at UNSW"
        },
        
        "Benton Campbell": {
            "email": "mariska.benton@thesoftfact.com",  # Wife's email
            "notes": "Husband of Mariska Benton - use wife's email for invitation"
        }
    }
    
    # Apply updates
    updates_made = 0
    
    for name, details in updates.items():
        # Find the row for this contact
        mask = df['Name'] == name
        
        if mask.any():
            # Update email if currently empty
            if pd.isna(df.loc[mask, 'Email Address'].iloc[0]) or df.loc[mask, 'Email Address'].iloc[0] == '':
                df.loc[mask, 'Email Address'] = details['email']
                
                # Add to notes
                current_notes = df.loc[mask, 'Notes'].iloc[0]
                if pd.isna(current_notes) or current_notes == '':
                    df.loc[mask, 'Notes'] = details['notes']
                else:
                    df.loc[mask, 'Notes'] = f"{current_notes}; {details['notes']}"
                
                print(f"[UPDATE] {name}: {details['email']}")
                updates_made += 1
            else:
                print(f"[SKIP] {name}: Already has email address")
        else:
            print(f"[ERROR] {name}: Not found in contacts file")
    
    # Save updated file
    df.to_csv(contacts_file, index=False)
    
    print(f"\n=== SUMMARY ===")
    print(f"Made {updates_made} updates to {contacts_file}")
    
    # Count remaining contacts without emails
    missing_emails = df[df['Email Address'].isna() | (df['Email Address'] == '')]['Name'].tolist()
    print(f"Contacts still missing emails: {len(missing_emails)}")
    
    if missing_emails:
        print("Remaining contacts without emails:")
        for name in missing_emails[:10]:  # Show first 10
            print(f"  - {name}")
        if len(missing_emails) > 10:
            print(f"  ... and {len(missing_emails) - 10} more")
    
    print(f"\nTotal contacts with emails: {len(df) - len(missing_emails)}/{len(df)}")
    completion_rate = ((len(df) - len(missing_emails)) / len(df)) * 100
    print(f"Completion rate: {completion_rate:.1f}%")

if __name__ == "__main__":
    update_contacts_from_search()