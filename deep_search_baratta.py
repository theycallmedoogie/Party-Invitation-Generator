#!/usr/bin/env python3
"""
Deep search for Bede and Leanne Baratta email addresses
Looking for bedenlea variations and related contacts
"""

import pandas as pd
import json
from pathlib import Path
import re

def search_all_variations():
    """Search for all possible variations of bedenlea email"""
    
    # Load all contact databases
    email_analysis_path = Path(r"C:\Users\micha\OneDrive\Desktop\RooCode projects\Email Analysis\data")
    
    contact_files = [
        "yahoo_contacts_export.csv",
        "outlook_contacts_20250807_184605.csv", 
        "extracted_contacts.csv"
    ]
    
    # Search patterns - all possible variations
    search_patterns = [
        "bedenlea",
        "bede lea",
        "bedeleanne", 
        "bede leanne",
        "leanne bede",
        "lea bede",
        "baratta bede",
        "baratta leanne",
        "baratta lea",
        "leanne baratta",
        "bede baratta"
    ]
    
    email_patterns = [
        r"bedenlea@.*",
        r"bedeleanne@.*", 
        r"bede.*lea.*@.*",
        r"lea.*bede.*@.*",
        r".*baratta.*@.*"
    ]
    
    print("=== COMPREHENSIVE SEARCH FOR BEDE/LEANNE BARATTA ===\n")
    
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
            
            # Search all text columns for our patterns
            for idx, row in df.iterrows():
                row_matches = []
                row_text = ""
                
                # Combine all text from the row
                for col in df.columns:
                    if pd.notna(row[col]):
                        cell_value = str(row[col]).lower()
                        row_text += f" {cell_value}"
                        
                        # Check for email patterns in this specific cell
                        for email_pattern in email_patterns:
                            if re.search(email_pattern, cell_value, re.IGNORECASE):
                                row_matches.append(f"Email pattern '{email_pattern}' in {col}: {row[col]}")
                
                # Check for name patterns in the combined text
                for pattern in search_patterns:
                    if pattern.lower() in row_text.lower():
                        row_matches.append(f"Name pattern '{pattern}' found")
                
                # If we found matches, record this row
                if row_matches:
                    match_info = {
                        'source': filename,
                        'row_index': idx,
                        'matches': row_matches,
                        'row_data': {}
                    }
                    
                    # Store relevant columns
                    relevant_cols = ['Name', 'name', 'Email', 'email', 'Email Address', 'email_address', 
                                   'Company', 'company', 'Phone', 'phone', 'Full Name', 'DisplayName']
                    
                    for col in df.columns:
                        if any(rel_col.lower() in col.lower() for rel_col in relevant_cols):
                            if pd.notna(row[col]):
                                match_info['row_data'][col] = row[col]
                    
                    all_matches.append(match_info)
        
        except Exception as e:
            print(f"  Error reading {filename}: {e}")
        
        print(f"  Found {len([m for m in all_matches if m['source'] == filename])} potential matches")
    
    # Display results
    print(f"\n=== SEARCH RESULTS: {len(all_matches)} TOTAL MATCHES ===\n")
    
    if all_matches:
        for i, match in enumerate(all_matches, 1):
            print(f"MATCH {i} (from {match['source']}):")
            print(f"  Match reasons: {'; '.join(match['matches'])}")
            
            # Display the contact data
            for key, value in match['row_data'].items():
                print(f"  {key}: {value}")
            print()
    
    # Also search for just "leanne" in case it's under her name
    print("=== SEARCHING FOR JUST 'LEANNE' ===\n")
    leanne_matches = []
    
    for filename in contact_files:
        file_path = email_analysis_path / filename
        if not file_path.exists():
            continue
            
        try:
            df = pd.read_csv(file_path)
            
            for idx, row in df.iterrows():
                row_text = ""
                for col in df.columns:
                    if pd.notna(row[col]):
                        row_text += f" {str(row[col]).lower()}"
                
                if "leanne" in row_text and ("baratta" in row_text or "bede" in row_text):
                    match_info = {
                        'source': filename,
                        'row_data': {}
                    }
                    
                    for col in df.columns:
                        if pd.notna(row[col]):
                            match_info['row_data'][col] = row[col]
                    
                    leanne_matches.append(match_info)
        
        except Exception as e:
            continue
    
    if leanne_matches:
        print(f"Found {len(leanne_matches)} Leanne+Baratta/Bede matches:")
        for i, match in enumerate(leanne_matches, 1):
            print(f"\nLEANNE MATCH {i} (from {match['source']}):")
            for key, value in match['row_data'].items():
                print(f"  {key}: {value}")
    else:
        print("No Leanne+Baratta/Bede matches found")
    
    return all_matches, leanne_matches

def search_vector_database():
    """Search the vector database files for any Baratta references"""
    print("\n=== SEARCHING VECTOR DATABASE ===")
    
    vector_path = Path(r"C:\Users\micha\OneDrive\Desktop\RooCode projects\Email Analysis\data\vector_db")
    
    # Look for JSON files that might contain contact info
    json_files = [
        "stats.json",
        "loading_progress.json", 
        "comprehensive_load_stats.json"
    ]
    
    for json_file in json_files:
        file_path = vector_path / json_file
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Convert to string and search
                data_str = json.dumps(data, indent=2).lower()
                if "baratta" in data_str or "bede" in data_str or "leanne" in data_str:
                    print(f"Found references in {json_file}")
                    # Look for email patterns
                    import re
                    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data_str)
                    if emails:
                        print(f"  Emails found: {', '.join(set(emails))}")
                    else:
                        print(f"  No emails found, but contains Baratta/Bede/Leanne references")
            except Exception as e:
                print(f"Error reading {json_file}: {e}")

if __name__ == "__main__":
    matches, leanne_matches = search_all_variations()
    search_vector_database()
    
    print(f"\n=== SUMMARY ===")
    print(f"Total pattern matches: {len(matches)}")
    print(f"Leanne+Baratta matches: {len(leanne_matches)}")
    
    if not matches and not leanne_matches:
        print("\n*** NO MATCHES FOUND ***")
        print("The bedenlea@hotmail.com email may not be in the current databases")
        print("Consider:")
        print("1. Checking if it's spelled differently (e.g., bedeenlea, bedeleanne)")
        print("2. Looking under different name combinations")
        print("3. The email might be in a different contact source")
    else:
        print(f"\nFound potential matches - review the results above")