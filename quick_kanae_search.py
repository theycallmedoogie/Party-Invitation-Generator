#!/usr/bin/env python3
"""
Quick search for Kanae's email address
"""

import pandas as pd
from pathlib import Path

def quick_search():
    """Quick search for kjamamoto0307@gmail.com"""
    
    email_analysis_path = Path(r"C:\Users\micha\OneDrive\Desktop\RooCode projects\Email Analysis\data")
    target_email = "kjamamoto0307@gmail.com"
    
    print(f"=== QUICK SEARCH FOR: {target_email} ===\n")
    
    # Search the main contact files
    contact_files = [
        "yahoo_contacts_export.csv",
        "extracted_contacts.csv"
    ]
    
    for filename in contact_files:
        file_path = email_analysis_path / filename
        if not file_path.exists():
            continue
            
        print(f"Searching {filename}...")
        
        try:
            # Read file in chunks to handle large files
            chunk_size = 1000
            found_matches = []
            
            for chunk_num, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size)):
                # Convert entire chunk to string and search
                chunk_str = chunk.to_string().lower()
                
                if target_email.lower() in chunk_str:
                    print(f"  FOUND in chunk {chunk_num}!")
                    
                    # Find the specific rows
                    for idx, row in chunk.iterrows():
                        row_str = ' '.join(str(val) for val in row.values).lower()
                        if target_email.lower() in row_str:
                            found_matches.append(dict(row))
                            print(f"    Row {idx}: CONTAINS TARGET EMAIL")
                            
                            # Show key fields
                            for col in ['Name', 'name', 'Email', 'email', 'First Name', 'Last Name']:
                                if col in row and pd.notna(row[col]):
                                    print(f"      {col}: {row[col]}")
                
                # Also quick check for kanae or yanamoto
                if 'kanae' in chunk_str or 'yanamoto' in chunk_str:
                    print(f"  Found kanae/yanamoto references in chunk {chunk_num}")
            
            if not found_matches:
                print(f"  No exact matches found in {filename}")
            else:
                print(f"  Total matches in {filename}: {len(found_matches)}")
                
        except Exception as e:
            print(f"  Error reading {filename}: {e}")
    
    print(f"\n=== CONCLUSION ===")
    print(f"Search completed for {target_email}")

if __name__ == "__main__":
    quick_search()