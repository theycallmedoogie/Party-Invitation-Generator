#!/usr/bin/env python3
"""
Final targeted search for the last 3 contacts
"""

import pandas as pd
from pathlib import Path

def search_final_three():
    """Search for Coorey Adrian, Baratta John, Scott Lara with targeted approach"""
    
    print("=== FINAL SEARCH FOR LAST 3 CONTACTS ===\n")
    
    email_analysis_path = Path(r"C:\Users\micha\OneDrive\Desktop\RooCode projects\Email Analysis\data")
    yahoo_file = email_analysis_path / "yahoo_contacts_export.csv"
    
    # Load data
    df = pd.read_csv(yahoo_file, encoding='utf-8', low_memory=False)
    
    results = {}
    
    # 1. COOREY ADRIAN - we know there are Coorey entries
    print("1. SEARCHING FOR COOREY ADRIAN")
    print("-" * 30)
    
    # From partial search, we know:
    # - There are contacts with last name "Coorey" 
    # - There is "Adrian (Cathy's dad, Dao's Husband)" which could be Adrian Coorey
    
    # Look for Adrian specifically in context with Coorey family
    coorey_rows = df[df.apply(lambda row: 'coorey' in str(row).lower(), axis=1)]
    
    print(f"Found {len(coorey_rows)} rows mentioning 'coorey':")
    
    for idx, row in coorey_rows.iterrows():
        # Check if this row mentions Adrian
        if 'adrian' in str(row).lower():
            email = row.get('Email', 'N/A')
            first_name = row.get('First Name', 'N/A')
            notes = str(row.get('Notes', ''))[:200]  # First 200 chars of notes
            
            print(f"  FOUND ADRIAN CONNECTION:")
            print(f"    First Name: {first_name}")
            print(f"    Email: {email}")
            print(f"    Notes: {notes}...")
            print()
            
            results['Coorey Adrian'] = {
                'email': email,
                'source': 'Context search - Adrian mentioned with Coorey family'
            }
    
    # 2. BARATTA JOHN - we know Brigid married John O'Dwyer
    print("2. SEARCHING FOR BARATTA JOHN")
    print("-" * 30)
    
    # From Brigid's notes: "Married to John O'Dwyer"
    # Look for John O'Dwyer specifically
    
    john_odwyer = df[df.apply(lambda row: 'john' in str(row).lower() and "o'dwyer" in str(row).lower(), axis=1)]
    
    if not john_odwyer.empty:
        for idx, row in john_odwyer.iterrows():
            email = row.get('Email', 'N/A')
            name_field = row.get('First Name', 'N/A')
            notes = str(row.get('Notes', ''))[:200]
            
            print(f"  FOUND JOHN O'DWYER:")
            print(f"    Name: {name_field}")
            print(f"    Email: {email}")
            print(f"    Notes: {notes}...")
            
            results['Baratta John'] = {
                'email': email if email != 'N/A' else 'brigidodwyer@yahoo.com.au',
                'source': "Married to Brigid O'Dwyer (nee Baratta) - use wife's email"
            }
    else:
        # Fallback - use Brigid's email since they're married
        results['Baratta John'] = {
            'email': 'brigidodwyer@yahoo.com.au',
            'source': "Husband of Brigid O'Dwyer (nee Baratta) - use wife's email"
        }
        print(f"  No direct match found - will use wife Brigid's email")
    
    print()
    
    # 3. SCOTT LARA - from partial search we saw "Larissa 'Lara' (Jade Scott-Rogers' Mum)"
    print("3. SEARCHING FOR SCOTT LARA")
    print("-" * 30)
    
    # Look for Lara Scott connections
    lara_scott = df[df.apply(lambda row: 'lara' in str(row).lower() and 'scott' in str(row).lower(), axis=1)]
    
    if not lara_scott.empty:
        for idx, row in lara_scott.iterrows():
            email = row.get('Email', 'N/A')
            first_name = row.get('First Name', 'N/A')
            company = row.get('Company', 'N/A')
            notes = str(row.get('Notes', ''))[:200]
            
            print(f"  FOUND LARA/SCOTT CONNECTION:")
            print(f"    Name: {first_name}")
            print(f"    Email: {email}")
            print(f"    Company: {company}")
            print(f"    Notes: {notes}...")
            print()
            
            if email != 'N/A' and pd.notna(email):
                results['Scott Lara'] = {
                    'email': email,
                    'source': 'Found via Lara Scott family connection'
                }
    
    # Also check if it's actually "Lara Scott" (reversed name)
    if 'Scott Lara' not in results:
        # Try "larissascott@yahoo.com.au" which appeared in partial search
        results['Scott Lara'] = {
            'email': 'larissascott@yahoo.com.au',
            'source': "Could be 'Lara Scott' - use Larissa Scott email"
        }
        print(f"  Using Larissa Scott email as potential match")
    
    print("\n=== FINAL THREE SEARCH RESULTS ===")
    
    for name, details in results.items():
        print(f"{name}: {details['email']}")
        print(f"  Source: {details['source']}")
        print()
    
    return results

if __name__ == "__main__":
    results = search_final_three()