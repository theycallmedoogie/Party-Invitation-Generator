#!/usr/bin/env python3
"""
Focused search of key database files for shamini22@hotmail.com
"""

import sqlite3
import json
import pandas as pd
from pathlib import Path

def focused_database_search():
    """Search specific database files for the target email"""
    
    print("=== FOCUSED DATABASE SEARCH FOR shamini22@hotmail.com ===\n")
    
    target_email = "shamini22@hotmail.com"
    email_analysis_path = Path(r"C:\Users\micha\OneDrive\Desktop\RooCode projects\Email Analysis\data")
    
    found_locations = []
    
    # 1. Search relationships.db
    print("1. SEARCHING relationships.db...")
    
    db_file = email_analysis_path / "relationships.db"
    if db_file.exists():
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            # Get table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"   Tables found: {[t[0] for t in tables]}")
            
            for table_name in [t[0] for t in tables]:
                # Search for email in this table
                cursor.execute(f"SELECT * FROM {table_name} WHERE lower(cast(* as text)) LIKE '%{target_email.lower()}%'")
                results = cursor.fetchall()
                
                if results:
                    print(f"   ✅ FOUND in table '{table_name}': {len(results)} matches")
                    for result in results[:3]:  # Show first 3 matches
                        print(f"      {result}")
                    found_locations.append(('relationships.db', table_name))
            
            conn.close()
            
        except Exception as e:
            print(f"   Error: {e}")
    else:
        print("   relationships.db not found")
    
    # 2. Search extracted_contacts.json
    print(f"\n2. SEARCHING extracted_contacts.json...")
    
    json_file = email_analysis_path / "extracted_contacts.json"
    if json_file.exists():
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if target_email.lower() in content.lower():
                print(f"   ✅ FOUND in extracted_contacts.json")
                
                # Show context
                pos = content.lower().find(target_email.lower())
                context = content[max(0, pos-100):pos+150]
                print(f"   Context: ...{context}...")
                found_locations.append('extracted_contacts.json')
            else:
                print(f"   Not found in extracted_contacts.json")
                
        except Exception as e:
            print(f"   Error: {e}")
    
    # 3. Search Yahoo contacts export one more time with different encoding
    print(f"\n3. RE-SEARCHING yahoo_contacts_export.csv with different encoding...")
    
    csv_file = email_analysis_path / "yahoo_contacts_export.csv"
    if csv_file.exists():
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'utf-16']
            
            for encoding in encodings:
                try:
                    print(f"   Trying encoding: {encoding}")
                    
                    # Search line by line
                    with open(csv_file, 'r', encoding=encoding) as f:
                        for line_num, line in enumerate(f, 1):
                            if target_email.lower() in line.lower():
                                print(f"   ✅ FOUND in line {line_num} with {encoding} encoding!")
                                print(f"   Line content: {line.strip()}")
                                found_locations.append(f'yahoo_contacts_export.csv (line {line_num}, {encoding})')
                                break
                    
                    # Also try pandas with this encoding
                    df = pd.read_csv(csv_file, encoding=encoding, nrows=1000)  # Sample first 1000 rows
                    df_str = df.to_string().lower()
                    
                    if target_email.lower() in df_str:
                        print(f"   ✅ FOUND in pandas dataframe with {encoding} encoding!")
                        
                        # Find specific row
                        for idx, row in df.iterrows():
                            row_str = ' '.join(str(val) for val in row.values if pd.notna(val)).lower()
                            if target_email.lower() in row_str:
                                print(f"   Row {idx}: {dict(row)}")
                                found_locations.append(f'yahoo_contacts_export.csv (row {idx}, {encoding})')
                                break
                        break
                    
                except UnicodeDecodeError:
                    continue
                    
        except Exception as e:
            print(f"   Error: {e}")
    
    # 4. Search admin_contacts.json
    print(f"\n4. SEARCHING admin_contacts.json...")
    
    admin_file = email_analysis_path / "administrative" / "admin_contacts.json"
    if admin_file.exists():
        try:
            with open(admin_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if target_email.lower() in content.lower():
                print(f"   ✅ FOUND in admin_contacts.json")
                pos = content.lower().find(target_email.lower())
                context = content[max(0, pos-100):pos+150]
                print(f"   Context: ...{context}...")
                found_locations.append('admin_contacts.json')
            else:
                print(f"   Not found in admin_contacts.json")
                
        except Exception as e:
            print(f"   Error: {e}")
    
    # 5. Quick search of vector database
    print(f"\n5. SEARCHING vector database files...")
    
    vector_files = [
        email_analysis_path / "vector_db" / "chroma-GemLaptopWin.sqlite3",
        email_analysis_path / "vector_db" / "vector_db" / "chroma.sqlite3"
    ]
    
    for db_file in vector_files:
        if db_file.exists():
            try:
                print(f"   Searching {db_file.name}...")
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                
                # Get tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                for table_name in [t[0] for t in tables]:
                    try:
                        cursor.execute(f"SELECT * FROM {table_name} WHERE lower(cast(* as text)) LIKE '%shamini%' OR lower(cast(* as text)) LIKE '%{target_email.lower()}%'")
                        results = cursor.fetchall()
                        
                        if results:
                            print(f"      Found shamini references in {table_name}: {len(results)} matches")
                            for result in results[:2]:
                                print(f"         {result}")
                            
                            # Check if target email is in results
                            for result in results:
                                if target_email.lower() in str(result).lower():
                                    print(f"      ✅ FOUND TARGET EMAIL in {table_name}")
                                    found_locations.append(f'{db_file.name}/{table_name}')
                                    break
                    
                    except Exception as e:
                        continue
                
                conn.close()
                
            except Exception as e:
                print(f"   Error with {db_file.name}: {e}")
    
    # Summary
    print(f"\n=== FOCUSED SEARCH RESULTS ===")
    
    if found_locations:
        print(f"✅ FOUND shamini22@hotmail.com in {len(found_locations)} location(s):")
        for location in found_locations:
            print(f"   - {location}")
        print("\nThis explains why it should have been found by our algorithms!")
    else:
        print("❌ shamini22@hotmail.com definitively NOT FOUND in key database files")
        print("\nConclusion: Email comes from external source (personal knowledge/other contacts)")
    
    return found_locations

if __name__ == "__main__":
    locations = focused_database_search()