#!/usr/bin/env python3
"""
Find Prishan David's email address
"""

from contact_matcher import ContactMatcher

def find_prishan_emails():
    print("Loading contacts...")
    matcher = ContactMatcher()
    
    print(f"\n=== SEARCHING FOR: Prishan David ===")
    search_terms = ["prishan", "david"]
    
    matches = []
    
    for contact in matcher.all_contacts:
        contact_matched = False
        match_reasons = []
        
        # Check name fields
        name_fields = ['Name', 'name', 'Full Name', 'full_name', 'DisplayName', 'display_name']
        for field in name_fields:
            if field in contact and contact[field]:
                name_value = str(contact[field]).lower()
                if "prishan" in name_value and "david" in name_value:
                    contact_matched = True
                    match_reasons.append(f"Name field '{field}': {contact[field]}")
                elif "prishan" in name_value:
                    contact_matched = True
                    match_reasons.append(f"Name contains 'prishan': {contact[field]}")
        
        # Check email addresses
        email_fields = ['Email', 'email', 'Email Address', 'email_address', 'E-mail Address']
        for field in email_fields:
            if field in contact and contact[field] and str(contact[field]).lower() != 'nan':
                email_value = str(contact[field]).lower()
                if "prishan" in email_value:
                    contact_matched = True
                    match_reasons.append(f"Email contains 'prishan': {contact[field]}")
                elif "prishdavid" in email_value:  # From earlier search
                    contact_matched = True
                    match_reasons.append(f"Email contains 'prishdavid': {contact[field]}")
        
        if contact_matched:
            # Get all emails for this contact
            emails = []
            for field in email_fields:
                if field in contact and contact[field] and str(contact[field]).lower() != 'nan':
                    emails.append(contact[field])
            
            if emails:
                match_info = {
                    'source': contact.get('source', 'unknown'),
                    'match_reasons': match_reasons,
                    'emails': list(set(emails)),
                    'contact': contact
                }
                matches.append(match_info)
    
    print(f"Found {len(matches)} potential records:")
    
    all_emails = set()
    for i, match in enumerate(matches, 1):
        print(f"\nRECORD {i} (from {match['source']}):")
        print(f"  Matched because: {'; '.join(match['match_reasons'])}")
        print(f"  Email addresses: {', '.join(match['emails'])}")
        all_emails.update(match['emails'])
        
        # Show other details
        contact = match['contact']
        names = []
        name_fields = ['Name', 'name', 'Full Name', 'full_name', 'DisplayName', 'display_name']
        for field in name_fields:
            if field in contact and contact[field] and str(contact[field]).lower() != 'nan':
                names.append(contact[field])
        if names:
            print(f"  Names: {', '.join(set(names))}")
    
    print(f"\n=== SUMMARY ===")
    print(f"All email addresses for Prishan David:")
    for email in sorted(all_emails):
        print(f"  - {email}")
    
    return list(all_emails)

if __name__ == "__main__":
    find_prishan_emails()