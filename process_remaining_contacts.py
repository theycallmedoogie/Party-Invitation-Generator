#!/usr/bin/env python3
"""
Process remaining unprocessed contacts from invitation list
"""

import pandas as pd
import json
from pathlib import Path
from improved_contact_matcher import ImprovedContactMatcher

def process_remaining_contacts():
    """Process the remaining contacts that don't have email addresses"""
    
    print("=== PROCESSING REMAINING UNPROCESSED CONTACTS ===\n")
    
    # Read current contact list to see what's missing
    contacts_file = Path(r"C:\Users\micha\OneDrive\Desktop\contacts_paperless_august2025.csv")
    
    if contacts_file.exists():
        df = pd.read_csv(contacts_file)
        
        # Find contacts without email addresses
        missing_emails = df[df['Email Address'].isna() | (df['Email Address'] == '')]['Name'].tolist()
        
        print(f"Found {len(missing_emails)} contacts without email addresses:")
        for i, name in enumerate(missing_emails[:15], 1):  # Show first 15
            print(f"  {i}. {name}")
        
        if len(missing_emails) > 15:
            print(f"  ... and {len(missing_emails) - 15} more")
    
    # Focus on the main unprocessed contacts from the conversation
    remaining_contacts = [
        "Hancock Matt",
        "Charles Michael", 
        "Baratta Brigid",
        "Baratta John",
        "Prishan David",
        "Liaw Grace",
        "Chung Wayne", 
        "Coorey Dao",
        "Coorey Adrian",
        "Benton Campbell",
        "Scott Lara"
    ]
    
    print(f"\n=== SEARCHING FOR PRIORITY CONTACTS ===")
    print(f"Processing {len(remaining_contacts)} priority contacts...\n")
    
    # Initialize matcher
    matcher = ImprovedContactMatcher()
    
    results = []
    
    for i, contact_name in enumerate(remaining_contacts, 1):
        print(f"{i}/{len(remaining_contacts)}: {contact_name}")
        print("-" * 40)
        
        # Get matches
        matches = matcher.find_matches(contact_name, top_n=5)
        
        if matches:
            print(f"Found {len(matches)} potential matches:")
            for j, match in enumerate(matches, 1):
                score = match.get('similarity_score', 0)
                email = match.get('email', 'N/A')
                phone = match.get('phone', 'N/A')
                company = match.get('company', 'N/A')
                source = match.get('source', 'Unknown')
                
                print(f"  {j}. Score: {score:.3f} | Email: {email}")
                if phone != 'N/A' and str(phone) != 'nan':
                    print(f"     Phone: {phone}")
                if company != 'N/A' and str(company) != 'nan':
                    print(f"     Company: {company}")
                print(f"     Source: {source}")
                print()
            
            # Store results for analysis
            results.append({
                'name': contact_name,
                'matches': matches
            })
            
        else:
            print("  No matches found")
            results.append({
                'name': contact_name,
                'matches': []
            })
        
        print()
    
    # Summary
    print("=== PROCESSING SUMMARY ===")
    
    found_contacts = [r for r in results if r['matches']]
    not_found_contacts = [r for r in results if not r['matches']]
    
    print(f"Contacts with matches: {len(found_contacts)}")
    for contact in found_contacts:
        best_match = contact['matches'][0]
        print(f"  {contact['name']}: {best_match.get('email', 'N/A')} (score: {best_match.get('similarity_score', 0):.3f})")
    
    print(f"\nContacts without matches: {len(not_found_contacts)}")
    for contact in not_found_contacts:
        print(f"  {contact['name']}")
    
    # Save results for manual review
    results_file = Path("remaining_contacts_search_results.json")
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed results saved to: {results_file}")
    
    return results

if __name__ == "__main__":
    results = process_remaining_contacts()
    
    print("\n=== NEXT STEPS ===")
    print("1. Review the matches above")
    print("2. Update contacts_paperless_august2025.csv with confirmed matches")
    print("3. For contacts without matches, consider:")
    print("   - Alternative name spellings")
    print("   - Maiden names or married names")
    print("   - Different databases or sources")
    print("   - Manual research")