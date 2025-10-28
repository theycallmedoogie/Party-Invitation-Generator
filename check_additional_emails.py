#!/usr/bin/env python3
"""
Check for additional email addresses for specific contacts
"""

from contact_matcher import ContactMatcher
import pandas as pd
from pathlib import Path

def find_all_emails_for_person(matcher, person_name, search_terms):
    """Find all email addresses associated with a person"""
    print(f"\n=== SEARCHING FOR: {person_name} ===")
    print(f"Search terms: {search_terms}")
    
    all_matches = []
    
    for contact in matcher.all_contacts:
        # Check if this contact might be the person
        contact_matched = False
        match_reasons = []
        
        # Check name fields
        name_fields = ['Name', 'name', 'Full Name', 'full_name', 'DisplayName', 'display_name']
        for field in name_fields:
            if field in contact and contact[field]:
                name_value = str(contact[field]).lower()
                for term in search_terms:
                    if term.lower() in name_value:
                        contact_matched = True
                        match_reasons.append(f"Name field '{field}': {contact[field]}")
                        break
        
        # Check email addresses for name parts
        email_fields = ['Email', 'email', 'Email Address', 'email_address', 'E-mail Address']
        for field in email_fields:
            if field in contact and contact[field] and str(contact[field]).lower() != 'nan':
                email_value = str(contact[field]).lower()
                for term in search_terms:
                    if term.lower() in email_value:
                        contact_matched = True
                        match_reasons.append(f"Email contains '{term}': {contact[field]}")
                        break
        
        # Check company field for name
        company_fields = ['Company', 'company', 'Organization', 'organization']
        for field in company_fields:
            if field in contact and contact[field] and str(contact[field]).lower() != 'nan':
                company_value = str(contact[field]).lower()
                for term in search_terms:
                    if term.lower() in company_value:
                        contact_matched = True
                        match_reasons.append(f"Company contains '{term}': {contact[field]}")
                        break
        
        if contact_matched:
            # Extract all available info
            contact_info = {
                'source': contact.get('source', 'unknown'),
                'match_reasons': match_reasons,
                'emails': [],
                'names': [],
                'companies': [],
                'phones': []
            }
            
            # Collect all emails
            for field in email_fields:
                if field in contact and contact[field] and str(contact[field]).lower() != 'nan':
                    contact_info['emails'].append(contact[field])
            
            # Collect all names
            for field in name_fields:
                if field in contact and contact[field] and str(contact[field]).lower() != 'nan':
                    contact_info['names'].append(contact[field])
            
            # Collect companies
            for field in company_fields:
                if field in contact and contact[field] and str(contact[field]).lower() != 'nan':
                    contact_info['companies'].append(contact[field])
            
            # Collect phones
            phone_fields = ['Phone', 'phone', 'Phone Number', 'phone_number', 'Mobile Phone']
            for field in phone_fields:
                if field in contact and contact[field] and str(contact[field]).lower() != 'nan':
                    contact_info['phones'].append(contact[field])
            
            # Remove duplicates
            contact_info['emails'] = list(set(contact_info['emails']))
            contact_info['names'] = list(set(contact_info['names']))
            contact_info['companies'] = list(set(contact_info['companies']))
            contact_info['phones'] = list(set(contact_info['phones']))
            
            if contact_info['emails']:  # Only add if there are emails
                all_matches.append(contact_info)
    
    # Display results
    if all_matches:
        print(f"Found {len(all_matches)} potential contact records:")
        for i, match in enumerate(all_matches, 1):
            print(f"\nRECORD {i} (from {match['source']}):")
            print(f"  Matched because: {'; '.join(match['match_reasons'])}")
            if match['emails']:
                print(f"  Email addresses: {', '.join(match['emails'])}")
            if match['names']:
                print(f"  Names: {', '.join(match['names'])}")
            if match['companies']:
                print(f"  Companies: {', '.join(match['companies'])}")
            if match['phones']:
                print(f"  Phones: {', '.join(match['phones'])}")
    else:
        print("No additional records found")
    
    return all_matches

def main():
    print("Loading contact databases...")
    matcher = ContactMatcher()
    
    # Search for the three people
    people_to_search = [
        ("West Lakshmi", ["lakshmi", "west"]),
        ("Erron Gardner", ["erron", "gardner"]),
        ("Anita David", ["anita", "david"])
    ]
    
    all_results = {}
    
    for person_name, search_terms in people_to_search:
        results = find_all_emails_for_person(matcher, person_name, search_terms)
        all_results[person_name] = results
    
    print(f"\n{'='*60}")
    print("SUMMARY OF ADDITIONAL EMAIL OPTIONS:")
    print('='*60)
    
    for person_name, results in all_results.items():
        print(f"\n{person_name}:")
        all_emails = set()
        for result in results:
            all_emails.update(result['emails'])
        
        if all_emails:
            for email in sorted(all_emails):
                print(f"  - {email}")
        else:
            print("  No email addresses found")

if __name__ == "__main__":
    main()