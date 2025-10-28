#!/usr/bin/env python3
"""
Search vector database for any mentions of Coorey family
"""

import sqlite3
import json
from pathlib import Path

def search_coorey_vector_database():
    """Search the Email Analysis vector database for Coorey mentions"""
    
    print("=== SEARCHING VECTOR DATABASE FOR COOREY FAMILY ===\n")
    
    email_analysis_path = Path(r"C:\Users\micha\OneDrive\Desktop\RooCode projects\Email Analysis\data")
    vector_db_path = email_analysis_path / "vector_db"
    
    # Vector database files to search
    db_files = [
        vector_db_path / "chroma-GemLaptopWin.sqlite3",
        vector_db_path / "chroma.sqlite3",
        vector_db_path / "vector_db" / "chroma.sqlite3"
    ]
    
    coorey_findings = []
    
    for db_file in db_files:
        if not db_file.exists():
            print(f"Database not found: {db_file}")
            continue
            
        print(f"Searching {db_file.name}...")
        
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            # Get table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            print(f"  Tables found: {[t[0] for t in tables]}")
            
            for table_name in [t[0] for t in tables]:
                try:
                    # Get column info
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = [col[1] for col in cursor.fetchall()]
                    
                    # Search for Coorey mentions
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()
                    
                    for row_idx, row in enumerate(rows):
                        row_str = str(row).lower()
                        
                        # Look for coorey mentions
                        if 'coorey' in row_str:
                            coorey_findings.append({
                                'database': db_file.name,
                                'table': table_name,
                                'row': row_idx,
                                'content': str(row)[:500],  # First 500 chars
                                'full_row': row
                            })
                            
                            print(f"    FOUND COOREY in {table_name}, row {row_idx}")
                            
                            # Look for email addresses in this row
                            row_text = str(row)
                            if '@' in row_text:
                                # Extract potential email addresses
                                words = row_text.split()
                                emails = [word for word in words if '@' in word and '.' in word]
                                if emails:
                                    print(f"      Emails found: {emails}")
                            
                            # Show relevant context
                            if len(str(row)) < 200:
                                print(f"      Content: {row}")
                            else:
                                print(f"      Content preview: {str(row)[:200]}...")
                            print()
                
                except Exception as e:
                    print(f"    Error searching table {table_name}: {e}")
            
            conn.close()
            
        except Exception as e:
            print(f"  Error accessing {db_file.name}: {e}")
    
    # Also search JSON stats files that might contain email addresses
    print(f"\nSearching JSON files for Coorey mentions...")
    
    json_files = [
        vector_db_path / "stats.json",
        vector_db_path / "loading_progress.json",
        vector_db_path / "loading_progress-GemLaptopWin.json",
        vector_db_path / "comprehensive_load_stats.json"
    ]
    
    for json_file in json_files:
        if json_file.exists():
            try:
                print(f"  Searching {json_file.name}...")
                with open(json_file, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                
                if 'coorey' in content:
                    print(f"    FOUND COOREY in {json_file.name}")
                    
                    # Try to load as JSON and search more specifically
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        # Search through the JSON structure
                        json_str = json.dumps(data, indent=2)
                        if 'coorey' in json_str.lower():
                            lines = json_str.split('\n')
                            coorey_lines = [line for line in lines if 'coorey' in line.lower()]
                            
                            for line in coorey_lines:
                                print(f"      {line.strip()}")
                                
                                # Look for email addresses in the line
                                if '@' in line:
                                    print(f"        ^ Contains email address!")
                    
                    except json.JSONDecodeError:
                        # Fall back to text search
                        lines = content.split('\n')
                        coorey_lines = [line for line in lines if 'coorey' in line]
                        for line in coorey_lines[:5]:  # Show first 5 matches
                            print(f"      {line.strip()}")
                
            except Exception as e:
                print(f"    Error reading {json_file.name}: {e}")
    
    # Summary
    print(f"\n=== COOREY SEARCH RESULTS ===")
    
    if coorey_findings:
        print(f"Found {len(coorey_findings)} Coorey mentions in vector databases:")
        
        unique_emails = set()
        for finding in coorey_findings:
            content = finding['content']
            # Extract emails from content
            words = content.split()
            emails = [word.strip('",()[]{}') for word in words if '@' in word and '.' in word]
            for email in emails:
                if 'coorey' in email.lower():
                    unique_emails.add(email)
        
        if unique_emails:
            print(f"\nCOOREY EMAIL ADDRESSES FOUND:")
            for email in sorted(unique_emails):
                print(f"  - {email}")
        else:
            print(f"\nNo additional Coorey email addresses found beyond p.coorey@unsw.edu.au")
            
        print(f"\nDetailed findings:")
        for i, finding in enumerate(coorey_findings, 1):
            print(f"{i}. Database: {finding['database']}, Table: {finding['table']}")
            print(f"   Content: {finding['content'][:100]}...")
            
    else:
        print("No Coorey mentions found in vector databases")
    
    return coorey_findings

if __name__ == "__main__":
    findings = search_coorey_vector_database()