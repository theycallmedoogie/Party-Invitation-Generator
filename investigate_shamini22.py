#!/usr/bin/env python3
"""
Investigate why shamini22@hotmail.com wasn't found in searches
"""

import pandas as pd
import json
from pathlib import Path
import re

def investigate_shamini22():
    """Search for shamini22@hotmail.com specifically and analyze why it was missed"""
    
    print("=== INVESTIGATING shamini22@hotmail.com ===\n")
    
    target_email = "shamini22@hotmail.com"
    email_analysis_path = Path(r"C:\Users\micha\OneDrive\Desktop\RooCode projects\Email Analysis\data")
    
    # Files to search
    contact_files = [
        "yahoo_contacts_export.csv",
        "outlook_contacts_20250807_184605.csv", 
        "extracted_contacts.csv"
    ]
    
    found_locations = []
    
    # 1. DIRECT EMAIL SEARCH
    print(f"1. SEARCHING FOR EXACT EMAIL: {target_email}")
    
    for filename in contact_files:
        file_path = email_analysis_path / filename
        if not file_path.exists():
            print(f"   {filename}: File not found")
            continue
            
        print(f"   Searching {filename}...")
        
        try:
            # Search in chunks to handle large files
            chunk_size = 1000
            found_in_file = False
            
            for chunk_num, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size)):
                # Convert entire chunk to string for searching
                chunk_str = chunk.to_string().lower()
                
                if target_email.lower() in chunk_str:
                    print(f"      FOUND in chunk {chunk_num}!")
                    found_in_file = True
                    
                    # Find specific row(s)
                    for idx, row in chunk.iterrows():
                        row_str = ' '.join(str(val) for val in row.values if pd.notna(val)).lower()
                        
                        if target_email.lower() in row_str:
                            found_locations.append({
                                'file': filename,
                                'chunk': chunk_num,
                                'row_index': idx,
                                'row_data': dict(row)
                            })
                            
                            print(f"         Row {idx} contains the email")
                            
                            # Show key fields from this row
                            key_fields = ['Name', 'name', 'Email', 'email', 'Email Address', 'First Name', 'Last Name', 'Company', 'Notes']
                            for field in key_fields:
                                if field in row and pd.notna(row[field]):
                                    value = str(row[field])
                                    if len(value) < 200:  # Don't show very long fields
                                        print(f"           {field}: {value}")
                
                # Don't search too many chunks to avoid timeout
                if chunk_num >= 10:
                    break
            
            if not found_in_file:
                print(f"      NOT FOUND in {filename}")
                
        except Exception as e:
            print(f"      Error reading {filename}: {e}")
    
    # 2. SEARCH FOR PARTIAL MATCHES
    print(f"\n2. SEARCHING FOR PARTIAL MATCHES: 'shamini22', 'shamini', '22'")
    
    partial_matches = []
    
    for filename in contact_files[:2]:  # Limit to avoid timeout
        file_path = email_analysis_path / filename
        if not file_path.exists():
            continue
            
        print(f"   Searching {filename} for partial matches...")
        
        try:
            chunk_size = 500
            for chunk_num, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size)):
                chunk_str = chunk.to_string().lower()
                
                # Look for shamini22 without the domain
                if 'shamini22' in chunk_str:
                    print(f"      Found 'shamini22' in chunk {chunk_num}")
                    
                    # Find the specific row
                    for idx, row in chunk.iterrows():
                        row_str = ' '.join(str(val) for val in row.values if pd.notna(val)).lower()
                        if 'shamini22' in row_str:
                            partial_matches.append({
                                'file': filename,
                                'type': 'shamini22',
                                'row_data': dict(row)
                            })
                            print(f"         Found in row {idx}")
                            break
                
                # Also look for any other shamini emails
                elif 'shamini' in chunk_str and '@' in chunk_str:
                    # Look for emails containing shamini
                    email_pattern = r'\b[A-Za-z0-9._%+-]*shamini[A-Za-z0-9._%+-]*@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                    emails = re.findall(email_pattern, chunk_str, re.IGNORECASE)
                    
                    if emails:
                        print(f"      Found shamini-related emails in chunk {chunk_num}: {', '.join(emails)}")
                        for email in emails:
                            if email != target_email.lower():
                                print(f"         Different shamini email: {email}")
                
                if chunk_num >= 5:  # Limit search
                    break
                    
        except Exception as e:
            print(f"      Error: {e}")
    
    # 3. SEARCH VECTOR DATABASE
    print(f"\n3. SEARCHING VECTOR DATABASE...")
    
    vector_path = email_analysis_path / "vector_db"
    if vector_path.exists():
        vector_files = ["stats.json", "loading_progress.json", "comprehensive_load_stats.json"]
        
        for filename in vector_files:
            file_path = vector_path / filename
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                    
                    if target_email.lower() in content:
                        print(f"      FOUND {target_email} in {filename}")
                        
                        # Show context around the email
                        email_pos = content.find(target_email.lower())
                        context_start = max(0, email_pos - 100)
                        context_end = min(len(content), email_pos + 100)
                        context = content[context_start:context_end]
                        print(f"         Context: ...{context}...")
                    
                    elif 'shamini22' in content:
                        print(f"      Found 'shamini22' in {filename}")
                    
                    elif 'shamini' in content:
                        print(f"      Found 'shamini' references in {filename}")
                        
                except Exception as e:
                    print(f"      Error reading {filename}: {e}")
    
    # 4. ANALYSIS AND CONCLUSIONS
    print(f"\n4. ANALYSIS: WHY WAS shamini22@hotmail.com MISSED?")
    
    if found_locations:
        print(f"   ✅ EMAIL WAS FOUND in {len(found_locations)} location(s):")
        for i, location in enumerate(found_locations, 1):
            print(f"      {i}. File: {location['file']}, Row: {location['row_index']}")
            
            # Analyze why our previous search might have missed it
            row_data = location['row_data']
            
            # Check if it was associated with the right name
            name_found = False
            for field in ['Name', 'name', 'First Name', 'Last Name', 'DisplayName']:
                if field in row_data and pd.notna(row_data[field]):
                    name_value = str(row_data[field]).lower()
                    if 'shamini' in name_value:
                        name_found = True
                        print(f"         Associated with name: {row_data[field]}")
                        break
            
            if not name_found:
                print(f"         ⚠️  EMAIL NOT ASSOCIATED WITH SHAMINI NAME")
                print(f"         This explains why name-based search missed it")
                
                # Show what name it IS associated with
                for field in ['Name', 'name', 'First Name', 'Last Name']:
                    if field in row_data and pd.notna(row_data[field]):
                        print(f"         Actually associated with: {row_data[field]}")
                        break
    
    else:
        print(f"   ❌ EMAIL NOT FOUND in any database")
        print(f"   Possible reasons:")
        print(f"      - Email might be from external source")
        print(f"      - Email might be in a different database/file")
        print(f"      - Email might be encoded differently")
        print(f"      - Email might be in processed email content (not contacts)")
    
    return found_locations

if __name__ == "__main__":
    locations = investigate_shamini22()
    
    print(f"\n=== FINAL CONCLUSION ===")
    if locations:
        print(f"shamini22@hotmail.com found in {len(locations)} location(s)")
        print(f"Previous searches likely missed it due to name association issues")
    else:
        print(f"shamini22@hotmail.com not found in current contact databases")
        print(f"Email likely comes from external knowledge or different source")