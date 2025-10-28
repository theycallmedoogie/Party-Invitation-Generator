#!/usr/bin/env python3
"""
Deep search for Shamini Sivayogan using enhanced methods
Including vector database search and comprehensive contact analysis
"""

import pandas as pd
import json
from pathlib import Path
import re
from improved_contact_matcher import ImprovedContactMatcher

def deep_shamini_search():
    """Comprehensive search for all Shamini-related contacts and emails"""
    
    print("=== DEEP SEARCH FOR SHAMINI SIVAYOGAN EMAILS ===\n")
    
    # Initialize improved matcher
    matcher = ImprovedContactMatcher()
    
    # Search variations including common misspellings and variations
    search_variations = [
        "shamini sivayogan",
        "shamini shivayogan", 
        "shamini siva",
        "shamini yogan",
        "sivayogan shamini",
        "shivayogan shamini",
        "shamini",
        "sivayogan",
        "monai@rocketmail.com",
        "monai rocketmail",
        "yogan shamini",
        "shamini hotmail",
        "shamini gmail"
    ]
    
    email_analysis_path = Path(r"C:\Users\micha\OneDrive\Desktop\RooCode projects\Email Analysis\data")
    
    all_shamini_data = {}
    
    # 1. ENHANCED CONTACT DATABASE SEARCH
    print("1. SEARCHING CONTACT DATABASES WITH ENHANCED MATCHING...")
    
    for contact in matcher.all_contacts:
        matched_terms = []
        contact_text = ""
        
        # Build comprehensive text from contact
        for field, value in contact.items():
            if value and str(value).lower() != 'nan' and not field.startswith('_'):
                text_val = str(value).lower()
                contact_text += f" {text_val}"
        
        # Check for any of our search variations
        for variation in search_variations:
            if variation.lower() in contact_text:
                matched_terms.append(variation)
        
        if matched_terms:
            source = contact.get('source', 'unknown')
            if source not in all_shamini_data:
                all_shamini_data[source] = []
            
            # Extract all emails from this contact
            emails = []
            email_fields = ['Email', 'email', 'Email Address', 'email_address']
            for field in email_fields:
                if contact.get(field) and str(contact[field]).lower() != 'nan':
                    emails.append(contact[field])
            
            contact_info = {
                'matched_terms': matched_terms,
                'emails': emails,
                'raw_contact': contact,
                'all_text': contact_text.strip()
            }
            all_shamini_data[source].append(contact_info)
    
    # Display contact database results
    for source, contacts in all_shamini_data.items():
        if contacts:
            print(f"\n--- {source} ---")
            for i, contact_info in enumerate(contacts, 1):
                print(f"Contact {i}:")
                print(f"  Matched terms: {', '.join(contact_info['matched_terms'])}")
                if contact_info['emails']:
                    print(f"  Emails: {', '.join(contact_info['emails'])}")
                
                # Show key fields
                contact = contact_info['raw_contact']
                key_fields = ['Name', 'name', 'First Name', 'Last Name', 'Company', 'Phone', 'Mobile']
                for field in key_fields:
                    if contact.get(field) and str(contact[field]).lower() != 'nan':
                        print(f"  {field}: {contact[field]}")
                print()
    
    # 2. SEARCH PROCESSED EMAIL DATA
    print("\n2. SEARCHING PROCESSED EMAIL DATA...")
    processed_path = email_analysis_path / "processed"
    
    if processed_path.exists():
        json_files = list(processed_path.glob("*.json"))
        
        for json_file in json_files[:2]:  # Limit to avoid timeout
            try:
                print(f"\nSearching {json_file.name}...")
                
                with open(json_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if any Shamini-related terms appear
                content_lower = content.lower()
                found_terms = []
                
                for variation in search_variations[:8]:  # Check main variations
                    if variation in content_lower:
                        found_terms.append(variation)
                
                if found_terms:
                    print(f"  Found terms: {', '.join(found_terms)}")
                    
                    # Try to extract email addresses from the vicinity of matches
                    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                    
                    # Find emails near Shamini mentions
                    sentences = content.split('\n')
                    relevant_emails = set()
                    
                    for sentence in sentences:
                        sentence_lower = sentence.lower()
                        if any(term in sentence_lower for term in found_terms):
                            emails_in_sentence = re.findall(email_pattern, sentence)
                            relevant_emails.update(emails_in_sentence)
                    
                    if relevant_emails:
                        print(f"  Associated emails: {', '.join(relevant_emails)}")
                    
            except Exception as e:
                print(f"  Error reading {json_file.name}: {e}")
    
    # 3. SEARCH VECTOR DATABASE FILES
    print("\n3. SEARCHING VECTOR DATABASE...")
    vector_path = email_analysis_path / "vector_db"
    
    if vector_path.exists():
        # Search stats and progress files
        vector_files = [
            "stats.json",
            "loading_progress.json",
            "comprehensive_load_stats.json"
        ]
        
        for filename in vector_files:
            file_path = vector_path / filename
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    data_str = json.dumps(data, indent=2).lower()
                    
                    found_shamini_terms = []
                    for variation in search_variations[:6]:  # Main variations only
                        if variation in data_str:
                            found_shamini_terms.append(variation)
                    
                    if found_shamini_terms:
                        print(f"\nFound in {filename}: {', '.join(found_shamini_terms)}")
                        
                        # Look for email patterns
                        email_pattern = r'\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b'
                        emails = re.findall(email_pattern, data_str)
                        unique_emails = set(emails)
                        
                        if unique_emails:
                            print(f"  Related emails found: {', '.join(sorted(unique_emails)[:5])}...")  # Show first 5
                
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
    
    # 4. COMPREHENSIVE EMAIL EXTRACTION
    print("\n4. COMPREHENSIVE EMAIL ANALYSIS...")
    
    all_shamini_emails = set()
    all_related_emails = set()
    
    # Collect all emails from contacts that mentioned Shamini
    for source, contacts in all_shamini_data.items():
        for contact_info in contacts:
            all_shamini_emails.update(contact_info['emails'])
            
            # Also look for emails in the raw text that might be nearby
            text = contact_info['all_text']
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            found_emails = re.findall(email_pattern, text, re.IGNORECASE)
            all_related_emails.update(found_emails)
    
    print(f"\n=== COMPREHENSIVE RESULTS FOR SHAMINI SIVAYOGAN ===")
    print(f"Direct emails found: {len(all_shamini_emails)}")
    if all_shamini_emails:
        for email in sorted(all_shamini_emails):
            print(f"  - {email}")
    
    print(f"\nRelated emails found: {len(all_related_emails)}")
    if all_related_emails:
        for email in sorted(all_related_emails)[:10]:  # Show first 10
            print(f"  - {email}")
    
    # 5. YOGAN SEARCH (her husband)
    print(f"\n5. SEARCHING FOR YOGAN SIVAYOGAN (husband)...")
    
    yogan_contacts = []
    for contact in matcher.all_contacts:
        contact_text = ""
        for field, value in contact.items():
            if value and str(value).lower() != 'nan' and not field.startswith('_'):
                contact_text += f" {str(value).lower()}"
        
        if 'yogan' in contact_text and ('sivayogan' in contact_text or 'shivayogan' in contact_text):
            # Extract emails
            emails = []
            email_fields = ['Email', 'email', 'Email Address', 'email_address']
            for field in email_fields:
                if contact.get(field) and str(contact[field]).lower() != 'nan':
                    emails.append(contact[field])
            
            if emails:
                yogan_contacts.append({
                    'emails': emails,
                    'contact': contact
                })
    
    if yogan_contacts:
        print("Found Yogan contacts with emails:")
        for i, yogan_info in enumerate(yogan_contacts, 1):
            print(f"  {i}. Emails: {', '.join(yogan_info['emails'])}")
    else:
        print("No Yogan contacts with emails found")
    
    return {
        'shamini_emails': list(all_shamini_emails),
        'related_emails': list(all_related_emails),
        'yogan_emails': [info['emails'] for info in yogan_contacts]
    }

if __name__ == "__main__":
    results = deep_shamini_search()
    
    print(f"\n=== FINAL SUMMARY ===")
    print(f"Shamini direct emails: {len(results['shamini_emails'])}")
    print(f"Related emails found: {len(results['related_emails'])}")
    print(f"Yogan (husband) emails: {len(results['yogan_emails'])}")
    
    if results['shamini_emails']:
        print(f"\nBEST OPTIONS FOR SHAMINI:")
        for email in results['shamini_emails']:
            print(f"  - {email}")
    else:
        print("\nNo additional emails found for Shamini beyond monai@rocketmail.com")