#!/usr/bin/env python3
"""
Handle remaining contacts - look for family connections and alternative approaches
"""

import pandas as pd
from pathlib import Path

def handle_remaining_contacts():
    """Handle the 17 remaining contacts using family connections and alternative approaches"""
    
    contacts_file = Path(r"C:\Users\micha\OneDrive\Desktop\contacts_paperless_august2025.csv")
    df = pd.read_csv(contacts_file)
    
    print("=== HANDLING REMAINING 17 CONTACTS ===\n")
    
    # Get the missing contacts
    missing = df[df['Email Address'].isna() | (df['Email Address'] == '')]
    
    updates = {}
    
    # 1. FAMILY CONNECTIONS WE CAN USE
    print("1. FAMILY CONNECTIONS:")
    print("-" * 25)
    
    # Yogan Sivayogan - husband of Shamini (we have her email)
    if 'Yogan Sivayogan' in missing['Name'].values:
        shamini_email = df[df['Name'] == 'Shamini Sivayogan']['Email Address'].iloc[0]
        updates['Yogan Sivayogan'] = {
            'email': shamini_email,
            'notes': f"Husband of Shamini Sivayogan - use wife's email {shamini_email}"
        }
        print(f"[OK] Yogan Sivayogan -> use wife Shamini's email: {shamini_email}")
    
    # Kerr Clare - wife of Luke (we have his email)
    if 'Kerr Clare' in missing['Name'].values:
        luke_email = df[df['Name'] == 'Kerr Luke']['Email Address'].iloc[0]
        updates['Kerr Clare'] = {
            'email': luke_email,
            'notes': f"Wife of Luke Kerr - use husband's email {luke_email}"
        }
        print(f"[OK] Kerr Clare -> use husband Luke's email: {luke_email}")
    
    # Carlon Sarah - wife of Phil (we have his email)  
    if 'Carlon Sarah' in missing['Name'].values:
        phil_email = df[df['Name'] == 'Phil Carlon']['Email Address'].iloc[0]
        updates['Carlon Sarah'] = {
            'email': phil_email,
            'notes': f"Wife of Phil Carlon - use husband's email {phil_email}"
        }
        print(f"[OK] Carlon Sarah -> use husband Phil's email: {phil_email}")
    
    # Bowden Tara - wife of Damien (we have his email)
    if 'Bowden Tara' in missing['Name'].values:
        damien_email = df[df['Name'] == 'Bowden Damien']['Email Address'].iloc[0]
        updates['Bowden Tara'] = {
            'email': damien_email,
            'notes': f"Wife of Damien Bowden - use husband's email {damien_email}"
        }
        print(f"[OK] Bowden Tara -> use husband Damien's email: {damien_email}")
    
    # Baratta Leanne - wife of Bede (we have his email)
    if 'Baratta Leanne' in missing['Name'].values:
        bede_email = df[df['Name'] == 'Bede Baratta']['Email Address'].iloc[0]
        updates['Baratta Leanne'] = {
            'email': bede_email,
            'notes': f"Wife of Bede Baratta - use husband's shared email {bede_email}"
        }
        print(f"[OK] Baratta Leanne -> use husband Bede's email: {bede_email}")
    
    # Cranney Sarah - wife of David (we have his email)
    if 'Cranney Sarah' in missing['Name'].values:
        david_email = df[df['Name'] == 'Cranney David']['Email Address'].iloc[0]
        updates['Cranney Sarah'] = {
            'email': david_email,
            'notes': f"Wife of David Cranney - use husband's email {david_email}"
        }
        print(f"[OK] Cranney Sarah -> use husband David's email: {david_email}")
    
    # O'Kane Renee - wife of Matt (we have his email)
    if "O'Kane Renee" in missing['Name'].values:
        matt_email = df[df['Name'] == "Matt O'Kane"]['Email Address'].iloc[0]
        updates["O'Kane Renee"] = {
            'email': matt_email,
            'notes': f"Wife of Matt O'Kane - use husband's email {matt_email}"
        }
        print(f"[OK] O'Kane Renee -> use husband Matt's email: {matt_email}")
    
    # Leo Foster - son of Liz (we have her email)
    if 'Leo Foster' in missing['Name'].values:
        liz_email = df[df['Name'] == 'Liz Foster']['Email Address'].iloc[0]
        updates['Leo Foster'] = {
            'email': liz_email,
            'notes': f"Son of Liz Foster - use mother's email {liz_email}"
        }
        print(f"[OK] Leo Foster -> use mother Liz's email: {liz_email}")
    
    print(f"\nFamily connections found: {len(updates)}")
    
    # 2. CHALLENGING CASES - Document what we know
    print(f"\n2. CHALLENGING CASES:")
    print("-" * 20)
    
    challenging_cases = {
        'Nancy Kusmadi': 'Email missing - not found in contacts (per existing notes)',
        'Steve Kusmadi': 'Email missing - not found in contacts (per existing notes)', 
        'Agnes Chan': 'Email missing - mcdc69@hotmail.com belongs to Dane Chan (per existing notes)',
        'Kathy Rothwell': 'No Pilgrim maiden name emails found - needs investigation (per existing notes)',
        'Iain Rothwell': 'Will use wife\'s contact details when found (per existing notes)',
        'Rebecca (Williams) Lock': 'Found as Rebecca Williams-Loch - need to verify correct contact (per existing notes)',
        'Murray Lock': 'Will use wife Rebecca\'s email when confirmed (per existing notes)',
        'Moses (partner)': 'Partner - manual entry required (per existing notes)',
        'Montin (partner)': 'Partner - manual entry required (per existing notes)'
    }
    
    for name, status in challenging_cases.items():
        if name in missing['Name'].values:
            print(f"- {name}: {status}")
    
    # Apply updates
    print(f"\n3. APPLYING UPDATES:")
    print("-" * 18)
    
    updates_applied = 0
    
    for name, details in updates.items():
        mask = df['Name'] == name
        if mask.any():
            df.loc[mask, 'Email Address'] = details['email']
            
            # Update notes
            current_notes = df.loc[mask, 'Notes'].iloc[0]
            if pd.isna(current_notes) or current_notes == '':
                df.loc[mask, 'Notes'] = details['notes']
            else:
                df.loc[mask, 'Notes'] = f"{current_notes}; {details['notes']}"
            
            print(f"[UPDATED] {name}")
            updates_applied += 1
    
    # Save file
    df.to_csv(contacts_file, index=False)
    
    print(f"\n=== SUMMARY ===")
    print(f"Applied {updates_applied} family connection updates")
    
    # New completion status
    total = len(df)
    with_email = len(df[df['Email Address'].notna() & (df['Email Address'] != '')])
    without_email = total - with_email
    completion_rate = (with_email/total) * 100
    
    print(f"New completion rate: {with_email}/{total} = {completion_rate:.1f}%")
    print(f"Remaining contacts without emails: {without_email}")
    
    return updates_applied

if __name__ == "__main__":
    updates = handle_remaining_contacts()