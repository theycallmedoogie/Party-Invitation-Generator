#!/usr/bin/env python3
"""
Search for Kanae's email address in all contact databases
Specifically looking for kjamamoto0307@gmail.com
"""

import pandas as pd
import json
from pathlib import Path
import re

def search_kanae_email():
    """Search for kjamamoto0307@gmail.com and any Kanae/Yanamoto references"""
    
    email_analysis_path = Path(r"C:\Users\micha\OneDrive\Desktop\RooCode projects\Email Analysis\data")
    
    target_email = "kjamamoto0307@gmail.com"
    
    print("=== SEARCHING FOR KANAE'S EMAIL ADDRESS ===")
    print(f"Target email: {target_email}")
    print(f"Also searching for: kanae, yanamoto, yamamoto, bohme\n")
    
    # Files to search
    contact_files = [
        "yahoo_contacts_export.csv",
        "outlook_contacts_20250807_184605.csv", 
        "extracted_contacts.csv"
    ]
    
    all_matches = []
    
    for filename in contact_files:
        file_path = email_analysis_path / filename
        if not file_path.exists():
            print(f"File not found: {filename}")
            continue
            
        print(f"Searching {filename}...")
        
        try:
            df = pd.read_csv(file_path)
            print(f"  Loaded {len(df)} records")
            
            # Search for exact email match
            email_matches = []
            kanae_matches = []
            yanamoto_matches = []
            
            for idx, row in df.iterrows():
                row_text = ""
                email_found = False
                kanae_found = False
                yanamoto_found = False
                
                # Check each column
                for col in df.columns:
                    if pd.notna(row[col]):
                        cell_value = str(row[col])
                        row_text += f" {cell_value.lower()}"
                        
                        # Check for exact email
                        if target_email.lower() in cell_value.lower():
                            email_found = True
                        
                        # Check for kanae
                        if 'kanae' in cell_value.lower():
                            kanae_found = True
                            
                        # Check for yanamoto variations
                        if any(name in cell_value.lower() for name in ['yanamoto', 'yamamoto']):
                            yanamoto_found = True
                
                # Record matches
                if email_found:
                    match_info = {'type': 'email_match', 'row_data': dict(row), 'source': filename}
                    email_matches.append(match_info)
                    all_matches.append(match_info)
                
                if kanae_found:
                    match_info = {'type': 'kanae_match', 'row_data': dict(row), 'source': filename}
                    kanae_matches.append(match_info)
                    if not email_found:  # Don't double-count
                        all_matches.append(match_info)
                
                if yanamoto_found:
                    match_info = {'type': 'yanamoto_match', 'row_data': dict(row), 'source': filename}
                    yanamoto_matches.append(match_info)
                    if not email_found and not kanae_found:  # Don't double-count
                        all_matches.append(match_info)
            
            print(f"  Found {len(email_matches)} exact email matches")
            print(f"  Found {len(kanae_matches)} Kanae mentions")  
            print(f"  Found {len(yanamoto_matches)} Yanamoto mentions")
            
        except Exception as e:
            print(f"  Error reading {filename}: {e}")
    
    # Display all matches
    print(f"\n=== DETAILED RESULTS ===")
    
    if all_matches:
        for i, match in enumerate(all_matches, 1):
            print(f"\nMATCH {i} ({match['type']} from {match['source']}):")
            
            # Show relevant fields
            row = match['row_data']
            relevant_fields = ['Name', 'name', 'Email', 'email', 'Email Address', 'First Name', 'Last Name', 'Company', 'Notes']
            
            for field in relevant_fields:
                if field in row and pd.notna(row[field]) and str(row[field]).lower() != 'nan':
                    value = str(row[field])
                    if len(value) < 200:  # Don't show super long values
                        print(f"  {field}: {value}")
    else:
        print("No matches found for Kanae, Yanamoto, or the email address")
    
    # Also search in processed email files
    print(f"\n=== SEARCHING PROCESSED EMAIL FILES ===")
    processed_path = email_analysis_path / "processed"
    
    if processed_path.exists():
        json_files = list(processed_path.glob("*.json"))
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    
                if target_email.lower() in content or 'kanae' in content or 'yanamoto' in content:
                    print(f"Found references in {json_file.name}")
                    
                    # Try to load as JSON to get more details
                    try:
                        f.seek(0)
                        data = json.load(f)
                        
                        # Look for the specific email
                        data_str = json.dumps(data).lower()
                        if target_email.lower() in data_str:
                            print(f"  EXACT EMAIL MATCH found in {json_file.name}")
                        if 'kanae' in data_str:
                            print(f"  'kanae' found in {json_file.name}")
                        if 'yanamoto' in data_str:
                            print(f"  'yanamoto' found in {json_file.name}")
                            
                    except json.JSONDecodeError:
                        print(f"  {json_file.name} contains references but couldn't parse JSON")
                        
            except Exception as e:
                print(f"Error reading {json_file}: {e}")
    
    return len(all_matches) > 0

if __name__ == "__main__":
    found = search_kanae_email()
    
    print(f"\n=== SUMMARY ===")
    if found:
        print("References to Kanae/Yanamoto found - see details above")
    else:
        print("No references to Kanae, Yanamoto, or kjamamoto0307@gmail.com found in any database")
        print("This email address may be from an external source or manual entry")