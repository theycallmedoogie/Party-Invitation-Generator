#!/usr/bin/env python3
"""
Targeted search for Shamini alternative emails
"""

import pandas as pd
import json
from pathlib import Path
import re

def targeted_shamini_search():
    """Focused search for Shamini's alternative email addresses"""
    
    print("=== TARGETED SEARCH FOR SHAMINI ALTERNATIVE EMAILS ===\n")
    
    email_analysis_path = Path(r"C:\Users\micha\OneDrive\Desktop\RooCode projects\Email Analysis\data")
    
    # 1. Search extracted contacts more thoroughly for any Shamini variations
    print("1. DETAILED SEARCH OF EXTRACTED CONTACTS...")
    
    extracted_file = email_analysis_path / "extracted_contacts.csv"
    shamini_emails = set()
    
    if extracted_file.exists():
        try:
            # Read in chunks to handle large file
            chunk_size = 500
            for chunk_num, chunk in enumerate(pd.read_csv(extracted_file, chunksize=chunk_size)):
                # Convert to string and search for shamini-related content
                chunk_str = chunk.to_string().lower()
                
                if 'shamini' in chunk_str or 'sivayogan' in chunk_str or 'monai' in chunk_str:
                    print(f"Found Shamini references in chunk {chunk_num}")
                    
                    # Look for specific rows
                    for idx, row in chunk.iterrows():
                        row_str = ' '.join(str(val) for val in row.values).lower()
                        
                        if any(term in row_str for term in ['shamini', 'sivayogan', 'shivayogan', 'monai']):
                            print(f"  Row {idx} contains Shamini reference:")
                            
                            # Extract emails from this row
                            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                            emails_in_row = re.findall(email_pattern, row_str, re.IGNORECASE)
                            
                            for email in emails_in_row:
                                shamini_emails.add(email)
                                print(f"    Email: {email}")
                            
                            # Show key fields
                            for col in ['name', 'email', 'email_address']:
                                if col in row and pd.notna(row[col]):
                                    print(f"    {col}: {row[col]}")
                
                if chunk_num >= 5:  # Limit to first few chunks to avoid timeout
                    break
                    
        except Exception as e:
            print(f"Error reading extracted_contacts.csv: {e}")
    
    # 2. Search the vector database stats for email patterns
    print(f"\n2. SEARCHING VECTOR DATABASE...")
    
    vector_path = email_analysis_path / "vector_db"
    vector_emails = set()
    
    if vector_path.exists():
        stats_file = vector_path / "stats.json"
        if stats_file.exists():
            try:
                with open(stats_file, 'r', encoding='utf-8') as f:
                    stats_data = json.load(f)
                
                stats_str = json.dumps(stats_data).lower()
                
                if 'shamini' in stats_str or 'sivayogan' in stats_str or 'monai' in stats_str:
                    print("  Found Shamini references in stats.json")
                    
                    # Extract email patterns
                    email_pattern = r'\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b'
                    emails = re.findall(email_pattern, stats_str)
                    
                    for email in emails:
                        if any(term in email for term in ['shamini', 'sivayogan', 'monai']) or \
                           any(term in stats_str[max(0, stats_str.find(email)-50):stats_str.find(email)+50] 
                               for term in ['shamini', 'sivayogan']):
                            vector_emails.add(email)
                            print(f"    Found: {email}")
            
            except Exception as e:
                print(f"  Error reading stats.json: {e}")
    
    # 3. Search Yahoo contacts more carefully for similar names
    print(f"\n3. SEARCHING YAHOO CONTACTS FOR SIMILAR NAMES...")
    
    yahoo_file = email_analysis_path / "yahoo_contacts_export.csv"
    yahoo_emails = set()
    
    if yahoo_file.exists():
        try:
            df = pd.read_csv(yahoo_file)
            
            # Look for rows that might be related to Shamini
            for idx, row in df.iterrows():
                row_contains_shamini = False
                
                # Check all text fields
                for col in df.columns:
                    if pd.notna(row[col]):
                        cell_value = str(row[col]).lower()
                        
                        # Look for various spellings and related terms
                        if any(term in cell_value for term in [
                            'shamini', 'sivayogan', 'shivayogan', 'monai', 
                            'yogan shamini', 'shamini yogan'
                        ]):
                            row_contains_shamini = True
                            break
                
                if row_contains_shamini:
                    # Extract email if present
                    email_fields = ['Email', 'email', 'Email Address']
                    for field in email_fields:
                        if field in row and pd.notna(row[field]):
                            email = str(row[field])
                            if '@' in email:
                                yahoo_emails.add(email)
                    
                    # Show the contact
                    name_fields = ['First Name', 'Last Name', 'Name']
                    for field in name_fields:
                        if field in row and pd.notna(row[field]):
                            print(f"  Found contact: {field}={row[field]}")
                            break
                    
                    if 'Email' in row and pd.notna(row['Email']):
                        print(f"    Email: {row['Email']}")
                    
        except Exception as e:
            print(f"Error reading yahoo_contacts_export.csv: {e}")
    
    # 4. Summary
    print(f"\n=== SEARCH RESULTS SUMMARY ===")
    
    all_found_emails = shamini_emails.union(vector_emails).union(yahoo_emails)
    
    print(f"Emails from extracted contacts: {len(shamini_emails)}")
    for email in shamini_emails:
        print(f"  - {email}")
    
    print(f"\nEmails from vector database: {len(vector_emails)}")
    for email in vector_emails:
        print(f"  - {email}")
    
    print(f"\nEmails from yahoo contacts: {len(yahoo_emails)}")
    for email in yahoo_emails:
        print(f"  - {email}")
    
    print(f"\nALL UNIQUE EMAILS FOR SHAMINI: {len(all_found_emails)}")
    for email in sorted(all_found_emails):
        print(f"  - {email}")
    
    return list(all_found_emails)

if __name__ == "__main__":
    emails = targeted_shamini_search()
    
    if len(emails) > 1:
        print(f"\n✅ FOUND {len(emails)} EMAIL OPTIONS FOR SHAMINI")
        print("Consider using a more modern email if available")
    else:
        print(f"\n❌ Only found existing email: monai@rocketmail.com")
        print("No alternative email addresses located in the databases")