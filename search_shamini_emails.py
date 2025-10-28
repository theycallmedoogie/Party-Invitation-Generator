#!/usr/bin/env python3
"""
Search for all emails associated with Shamini Sivayogan
"""

from contact_matcher import ContactMatcher

def search_shamini_emails():
    """Find all email addresses for Shamini"""
    print("Loading contacts...")
    matcher = ContactMatcher()
    
    print(f"\n=== SEARCHING FOR ALL SHAMINI SIVAYOGAN EMAILS ===")
    
    shamini_contacts = []
    
    for contact in matcher.all_contacts:
        contact_matched = False
        match_reason = ""
        
        # Check all fields for shamini or sivayogan
        all_text = ""
        for field, value in contact.items():
            if value and str(value).lower() != 'nan':
                text_value = str(value).lower()
                all_text += f" {text_value}"
                
                # Check for shamini and sivayogan combinations
                if ('shamini' in text_value and 'sivayogan' in text_value) or \
                   ('shamini' in text_value and 'shivayogan' in text_value):
                    contact_matched = True
                    match_reason = f"Found shamini+sivayogan in {field}: {value}"
                    break
        
        # Also check if just "shamini" appears with any reasonable email
        if not contact_matched:
            email_fields = ['Email', 'email', 'Email Address', 'email_address']
            name_fields = ['Name', 'name', 'First Name', 'Last Name', 'DisplayName']
            
            has_shamini = False
            has_email = False
            
            for field in name_fields:
                if contact.get(field) and 'shamini' in str(contact[field]).lower():
                    has_shamini = True
                    break
            
            for field in email_fields:
                if contact.get(field) and str(contact[field]).lower() != 'nan' and '@' in str(contact[field]):
                    has_email = True
                    break
            
            if has_shamini and has_email:
                contact_matched = True
                match_reason = "Found shamini name with email"
        
        if contact_matched:
            # Extract all available information
            contact_info = {
                'match_reason': match_reason,
                'source': contact.get('source', 'unknown'),
                'all_emails': [],
                'names': [],
                'other_info': {}
            }
            
            # Get all emails
            email_fields = ['Email', 'email', 'Email Address', 'email_address', 'E-mail Address']
            for field in email_fields:
                if contact.get(field) and str(contact[field]).lower() != 'nan':
                    contact_info['all_emails'].append(contact[field])
            
            # Get all names
            name_fields = ['Name', 'name', 'Full Name', 'First Name', 'Last Name', 'DisplayName']
            for field in name_fields:
                if contact.get(field) and str(contact[field]).lower() != 'nan':
                    contact_info['names'].append(f"{field}: {contact[field]}")
            
            # Get other relevant info
            other_fields = ['Company', 'Phone', 'Mobile', 'Notes']
            for field in other_fields:
                if contact.get(field) and str(contact[field]).lower() != 'nan':
                    contact_info['other_info'][field] = contact[field]
            
            # Remove duplicates from emails
            contact_info['all_emails'] = list(set(contact_info['all_emails']))
            
            if contact_info['all_emails'] or 'shamini' in match_reason.lower():
                shamini_contacts.append(contact_info)
    
    # Display results
    if shamini_contacts:
        print(f"Found {len(shamini_contacts)} Shamini-related contacts:")
        
        all_emails = set()
        for i, contact in enumerate(shamini_contacts, 1):
            print(f"\nCONTACT {i} (from {contact['source']}):")
            print(f"  Matched because: {contact['match_reason']}")
            
            if contact['all_emails']:
                print(f"  Email addresses: {', '.join(contact['all_emails'])}")
                all_emails.update(contact['all_emails'])
            
            if contact['names']:
                for name in contact['names'][:3]:  # Show first 3 names
                    print(f"  {name}")
            
            if contact['other_info']:
                for field, value in contact['other_info'].items():
                    if len(str(value)) < 100:  # Don't show very long fields
                        print(f"  {field}: {value}")
        
        print(f"\n=== ALL UNIQUE EMAIL ADDRESSES FOR SHAMINI ===")
        for email in sorted(all_emails):
            print(f"  - {email}")
        
        return list(all_emails)
    else:
        print("No Shamini contacts found")
        return []

if __name__ == "__main__":
    search_shamini_emails()