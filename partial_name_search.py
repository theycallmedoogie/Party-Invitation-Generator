#!/usr/bin/env python3
"""
Search for partial name matches - first name or surname only
"""

import pandas as pd
from pathlib import Path
from improved_contact_matcher import ImprovedContactMatcher

def search_partial_names():
    """Search for contacts using partial names"""
    
    print("=== SEARCHING FOR PARTIAL NAME MATCHES ===\n")
    
    # Problem contacts that returned no matches
    problem_contacts = [
        "Hancock Matt",        # Try: Matt, Hancock
        "Charles Michael",     # Try: Charles, Michael  
        "Baratta Brigid",      # Try: Brigid, Baratta
        "Baratta John",        # Try: John, Baratta
        "Prishan David",       # Try: Prishan, David (note: we know about Anita Jacob David)
        "Liaw Grace",          # Try: Grace, Liaw
        "Chung Wayne",         # Try: Wayne, Chung
        "Coorey Dao",          # Try: Dao, Coorey
        "Coorey Adrian",       # Try: Adrian, Coorey
        "Benton Campbell",     # Try: Campbell, Benton (we know about Mariska Benton)
        "Scott Lara"           # Try: Lara, Scott
    ]
    
    matcher = ImprovedContactMatcher()
    
    # Load the contact data directly to search by parts
    email_analysis_path = Path(r"C:\Users\micha\OneDrive\Desktop\RooCode projects\Email Analysis\data")
    
    # Load main contacts file
    yahoo_file = email_analysis_path / "yahoo_contacts_export.csv"
    
    if not yahoo_file.exists():
        print(f"Could not find {yahoo_file}")
        return
    
    print("Loading contact data...")
    
    # Read with different approaches to handle encoding issues
    try:
        df = pd.read_csv(yahoo_file, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(yahoo_file, encoding='latin-1')
        except:
            df = pd.read_csv(yahoo_file, encoding='cp1252')
    
    print(f"Loaded {len(df)} contacts from yahoo_contacts_export.csv")
    
    results = {}
    
    for contact_name in problem_contacts:
        print(f"\n=== SEARCHING: {contact_name} ===")
        
        # Split name into parts
        parts = contact_name.split()
        if len(parts) == 2:
            first_part, second_part = parts
        else:
            first_part = parts[0]
            second_part = " ".join(parts[1:]) if len(parts) > 1 else ""
        
        print(f"  Searching for: '{first_part}' and '{second_part}'")
        
        matches_found = []
        
        # Search in the Name columns (all string columns)
        for col in df.columns:
            if df[col].dtype == 'object':  # String columns
                
                # Search for first part
                first_matches = df[df[col].str.contains(first_part, case=False, na=False)]
                
                if not first_matches.empty:
                    print(f"  Found '{first_part}' in column '{col}': {len(first_matches)} matches")
                    
                    for idx, row in first_matches.head(3).iterrows():  # Show first 3
                        email = row.get('Email', 'N/A')
                        name_val = row.get(col, 'N/A')
                        print(f"    {name_val} | Email: {email}")
                        
                        matches_found.append({
                            'search_term': first_part,
                            'column': col,
                            'name': name_val,
                            'email': email,
                            'row_data': dict(row)
                        })
                
                # Search for second part if it exists
                if second_part:
                    second_matches = df[df[col].str.contains(second_part, case=False, na=False)]
                    
                    if not second_matches.empty:
                        print(f"  Found '{second_part}' in column '{col}': {len(second_matches)} matches")
                        
                        for idx, row in second_matches.head(3).iterrows():  # Show first 3
                            email = row.get('Email', 'N/A')
                            name_val = row.get(col, 'N/A')
                            print(f"    {name_val} | Email: {email}")
                            
                            matches_found.append({
                                'search_term': second_part,
                                'column': col,
                                'name': name_val,
                                'email': email,
                                'row_data': dict(row)
                            })
        
        results[contact_name] = matches_found
        
        if not matches_found:
            print(f"  No partial matches found for {contact_name}")
    
    # Summary
    print("\n=== PARTIAL SEARCH RESULTS SUMMARY ===")
    
    contacts_with_matches = 0
    contacts_without_matches = 0
    
    for contact, matches in results.items():
        if matches:
            contacts_with_matches += 1
            print(f"\n{contact}: {len(matches)} potential matches")
            
            # Group by email to avoid duplicates
            unique_emails = {}
            for match in matches:
                email = match['email']
                if email != 'N/A' and pd.notna(email) and email not in unique_emails:
                    unique_emails[email] = match
            
            for email, match in unique_emails.items():
                print(f"  {email} (found via '{match['search_term']}' in {match['column']})")
        else:
            contacts_without_matches += 1
    
    print(f"\nContacts with potential matches: {contacts_with_matches}")
    print(f"Contacts with no matches: {contacts_without_matches}")
    
    return results

if __name__ == "__main__":
    results = search_partial_names()