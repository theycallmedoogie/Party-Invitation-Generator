#!/usr/bin/env python3
"""
Search for contacts with corrected names and details
"""

from contact_matcher import ContactMatcher
import pandas as pd
from pathlib import Path

def search_specific_contacts():
    """Search for specific contacts with corrected information"""
    
    print("Loading contacts...")
    matcher = ContactMatcher()
    
    # Searches to perform with corrected information
    searches = [
        {
            'name': 'Agnes Chan',
            'search_terms': ['dane chan', 'dchan'],
            'note': 'Check if mcdc69@hotmail.com belongs to Dane Chan'
        },
        {
            'name': 'Rebecca (Williams) Lock / Bec Lock',
            'search_terms': ['rebecca williams', 'williams rebecca', 'bec williams', 'rebecca lock', 'bec lock'],
            'note': 'Maiden name Williams, goes by Bec'
        },
        {
            'name': 'Michael Ghirawoo',
            'search_terms': ['michael jackson dad visionedu', 'jackson dad', 'ghirawoo michael', 'visionedu michael'],
            'note': 'Listed as "Michael (Jackson\'s Dad VisionEd) Ghirawoo"'
        },
        {
            'name': 'Shamini Sivayogan',
            'search_terms': ['shamini sivayogan', 'sivayogan shamini', 'shamini hotmail'],
            'note': 'Correct spelling: Sivayogan (not Shivayogan), should have hotmail'
        },
        {
            'name': 'Kanae Yanamoto',
            'search_terms': ['kanae yanamoto', 'yanamoto kanae', 'sora bohme mum', 'bohme mum', 'kanae sora'],
            'note': 'Listed as "Kanae (Sora Bohme\'s Mum) Yanamoto"'
        },
        {
            'name': 'Sara (Harris) Ghirawoo',
            'search_terms': ['sara harris', 'harris sara', 'sara ghirawoo', 'ghirawoo sara'],
            'note': 'Maiden name Harris'
        }
    ]
    
    all_results = {}
    
    for search_info in searches:
        print(f"\n{'='*60}")
        print(f"SEARCHING FOR: {search_info['name']}")
        print(f"Note: {search_info['note']}")
        print('='*60)
        
        found_contacts = []
        
        for contact in matcher.all_contacts:
            contact_matched = False
            match_reasons = []
            
            # Check all text fields for our search terms
            all_text = ""
            
            # Collect all text from contact
            for field, value in contact.items():
                if value and str(value).lower() != 'nan':
                    all_text += f" {str(value).lower()}"
            
            # Check each search term
            for term in search_info['search_terms']:
                if term.lower() in all_text:
                    contact_matched = True
                    match_reasons.append(f"Contains '{term}'")
            
            if contact_matched:
                # Extract key details
                contact_details = {
                    'match_reasons': match_reasons,
                    'source': contact.get('source', 'unknown'),
                    'emails': [],
                    'names': [],
                    'companies': []
                }
                
                # Get emails
                email_fields = ['Email', 'email', 'Email Address', 'email_address']
                for field in email_fields:
                    if contact.get(field) and str(contact[field]).lower() != 'nan':
                        contact_details['emails'].append(contact[field])
                
                # Get names
                name_fields = ['Name', 'name', 'Full Name', 'full_name', 'DisplayName', 'display_name', 'First Name', 'Last Name']
                for field in name_fields:
                    if contact.get(field) and str(contact[field]).lower() != 'nan':
                        contact_details['names'].append(f"{field}: {contact[field]}")
                
                # Get companies
                company_fields = ['Company', 'company', 'Organization', 'organization', 'Notes']
                for field in company_fields:
                    if contact.get(field) and str(contact[field]).lower() != 'nan':
                        if len(str(contact[field])) < 200:  # Don't show super long notes
                            contact_details['companies'].append(f"{field}: {contact[field]}")
                
                # Remove duplicates
                contact_details['emails'] = list(set(contact_details['emails']))
                
                found_contacts.append(contact_details)
        
        # Display results
        if found_contacts:
            print(f"Found {len(found_contacts)} potential matches:")
            for i, contact in enumerate(found_contacts, 1):
                print(f"\nMATCH {i} (from {contact['source']}):")
                print(f"  Matched because: {'; '.join(contact['match_reasons'])}")
                if contact['emails']:
                    print(f"  Email addresses: {', '.join(contact['emails'])}")
                if contact['names']:
                    for name in contact['names'][:3]:  # Show first 3 name fields
                        print(f"  {name}")
                if contact['companies']:
                    for company in contact['companies'][:2]:  # Show first 2 company/note fields
                        print(f"  {company}")
        else:
            print("No matches found")
        
        all_results[search_info['name']] = found_contacts
    
    # Special check for Dane Chan and mcdc69@hotmail.com
    print(f"\n{'='*60}")
    print("SPECIAL CHECK: Is mcdc69@hotmail.com associated with Dane Chan?")
    print('='*60)
    
    dane_found = False
    for contact in matcher.all_contacts:
        # Look for this specific email
        email_fields = ['Email', 'email', 'Email Address', 'email_address']
        for field in email_fields:
            if contact.get(field) and 'mcdc69@hotmail.com' in str(contact[field]).lower():
                dane_found = True
                print("FOUND mcdc69@hotmail.com in contact:")
                
                # Show all details for this contact
                for key, value in contact.items():
                    if value and str(value).lower() != 'nan':
                        print(f"  {key}: {value}")
                break
    
    if not dane_found:
        print("mcdc69@hotmail.com not found in any contact")
    
    return all_results

if __name__ == "__main__":
    search_specific_contacts()