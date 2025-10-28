#!/usr/bin/env python3
"""
Focused search for Coorey family in key databases
"""

import pandas as pd
import sqlite3
from pathlib import Path
import re

def focused_coorey_search():
    """Focused search for Coorey family in contact databases"""
    
    print("=== FOCUSED COOREY FAMILY SEARCH ===\n")
    
    email_analysis_path = Path(r"C:\Users\micha\OneDrive\Desktop\RooCode projects\Email Analysis\data")
    
    coorey_emails = set()
    findings = []
    
    # 1. Search main contact CSV files
    print("1. SEARCHING CONTACT CSV FILES")
    print("-" * 30)
    
    csv_files = [
        "yahoo_contacts_export.csv",
        "extracted_contacts.csv", 
        "outlook_contacts_20250807_184605.csv"
    ]
    
    for csv_file in csv_files:
        file_path = email_analysis_path / csv_file
        if file_path.exists():
            print(f"  Searching {csv_file}...")
            
            try:
                df = pd.read_csv(file_path, encoding='utf-8', low_memory=False)
                
                # Search all columns for Coorey
                coorey_rows = df[df.apply(lambda row: 'coorey' in str(row).lower(), axis=1)]
                
                if not coorey_rows.empty:
                    print(f"    FOUND {len(coorey_rows)} Coorey mentions!")
                    
                    for idx, row in coorey_rows.iterrows():
                        # Extract emails from this row
                        row_str = str(dict(row))
                        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                        emails = re.findall(email_pattern, row_str)
                        
                        for email in emails:
                            coorey_emails.add(email)
                            print(f"      Email found: {email}")
                        
                        # Show key fields
                        key_fields = ['First Name', 'Last Name', 'Email', 'Company', 'Notes']
                        print(f"      Row {idx} details:")
                        for field in key_fields:
                            if field in row and pd.notna(row[field]):
                                value = str(row[field])
                                if len(value) < 100:  # Don't show very long fields
                                    print(f"        {field}: {value}")
                        print()
                
            except Exception as e:
                print(f"    Error reading {csv_file}: {e}")
    
    # 2. Search relationships database
    print("2. SEARCHING RELATIONSHIPS DATABASE")
    print("-" * 35)
    
    relationships_db = email_analysis_path / "relationships.db"
    if relationships_db.exists():
        try:
            conn = sqlite3.connect(relationships_db)
            cursor = conn.cursor()
            
            # Get table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            for table_name in [t[0] for t in tables]:
                try:
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()
                    
                    coorey_rows = [row for row in rows if 'coorey' in str(row).lower()]
                    
                    if coorey_rows:
                        print(f"  FOUND {len(coorey_rows)} Coorey mentions in {table_name}")
                        
                        for row in coorey_rows:
                            row_str = str(row)
                            
                            # Extract emails
                            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                            emails = re.findall(email_pattern, row_str)
                            
                            for email in emails:
                                coorey_emails.add(email)
                                print(f"    Email found: {email}")
                            
                            print(f"    Content: {row_str[:200]}...")
                            print()
                
                except Exception as e:
                    continue
            
            conn.close()
            
        except Exception as e:
            print(f"  Error accessing relationships.db: {e}")
    
    # 3. Search MBOX files (sample search)
    print("3. SEARCHING SAMPLE MBOX FILES")
    print("-" * 30)
    
    mbox_dir = email_analysis_path / "raw_emails"
    if mbox_dir.exists():
        mbox_files = list(mbox_dir.glob("*.mbox"))[:3]  # Just first 3 files to avoid timeout
        
        for mbox_file in mbox_files:
            print(f"  Searching {mbox_file.name}...")
            
            try:
                # Read first chunk of MBOX file
                with open(mbox_file, 'r', encoding='utf-8', errors='ignore') as f:
                    chunk = f.read(1024 * 1024)  # Read 1MB
                
                if 'coorey' in chunk.lower():
                    print(f"    FOUND Coorey mentions in {mbox_file.name}!")
                    
                    # Extract emails from this chunk
                    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                    emails = re.findall(email_pattern, chunk)
                    
                    coorey_related_emails = [email for email in emails if 'coorey' in email.lower()]
                    
                    if coorey_related_emails:
                        for email in coorey_related_emails:
                            coorey_emails.add(email)
                            print(f"      Coorey email found: {email}")
                    
                    # Show context lines
                    lines = chunk.split('\n')
                    coorey_lines = [line for line in lines if 'coorey' in line.lower()]
                    
                    for line in coorey_lines[:3]:  # Show first 3 lines
                        if '@' in line:
                            print(f"      Context with email: {line.strip()[:100]}...")
                        else:
                            print(f"      Context: {line.strip()[:100]}...")
                
            except Exception as e:
                print(f"    Error reading {mbox_file.name}: {e}")
    
    # SUMMARY
    print("4. COOREY FAMILY EMAIL SEARCH RESULTS")
    print("-" * 40)
    
    if coorey_emails:
        print(f"FOUND {len(coorey_emails)} unique email addresses mentioning Coorey:")
        
        current_emails = {'p.coorey@unsw.edu.au'}
        new_emails = coorey_emails - current_emails
        
        print(f"\nCurrent known emails:")
        for email in current_emails:
            if email in coorey_emails:
                print(f"  [OK] {email} (confirmed in search)")
        
        if new_emails:
            print(f"\nNEW email addresses found:")
            for email in sorted(new_emails):
                print(f"  + {email}")
        else:
            print(f"\nNo additional Coorey email addresses found beyond current known emails")
    else:
        print("No Coorey email addresses found in the searched databases")
    
    return list(coorey_emails)

if __name__ == "__main__":
    emails = focused_coorey_search()