#!/usr/bin/env python3
"""
Search for specific email addresses and name variations
"""

from contact_matcher import ContactMatcher

def search_for_emails():
    print("Loading contacts...")
    matcher = ContactMatcher()
    
    # Search for bedenlea@hotmail.com
    print(f"\n=== SEARCHING FOR: bedenlea@hotmail.com ===")
    found_bedenlea = False
    
    for contact in matcher.all_contacts:
        email_fields = ['Email', 'email', 'Email Address', 'email_address', 'E-mail Address']
        for field in email_fields:
            if field in contact and contact[field] and "bedenlea" in str(contact[field]).lower():
                found_bedenlea = True
                print(f"FOUND: {contact[field]} in {contact.get('source', 'unknown')}")
                # Show other details
                names = []
                name_fields = ['Name', 'name', 'Full Name', 'full_name', 'DisplayName', 'display_name']
                for nfield in name_fields:
                    if contact.get(nfield) and str(contact[nfield]).lower() != 'nan':
                        names.append(contact[nfield])
                if names:
                    print(f"  Names: {', '.join(set(names))}")
                
                company_fields = ['Company', 'company']
                for cfield in company_fields:
                    if contact.get(cfield) and str(contact[cfield]).lower() != 'nan':
                        print(f"  Company: {contact[cfield]}")
                        break
    
    if not found_bedenlea:
        print("bedenlea@hotmail.com NOT FOUND")
    
    # Search for Kathy/Pilgrim variations
    print(f"\n=== SEARCHING FOR: Kathy Pilgrim / Rothwell Pilgrim ===")
    search_terms = ["kathy pilgrim", "pilgrim kathy", "kathleen pilgrim", "pilgrim rothwell", "kathy rothwell"]
    
    found_pilgrim = []
    
    for contact in matcher.all_contacts:
        contact_matched = False
        match_reason = ""
        
        # Check name fields
        name_fields = ['Name', 'name', 'Full Name', 'full_name', 'DisplayName', 'display_name']
        for field in name_fields:
            if field in contact and contact[field]:
                name_value = str(contact[field]).lower()
                for term in search_terms:
                    if term in name_value:
                        contact_matched = True
                        match_reason = f"Name contains '{term}': {contact[field]}"
                        break
                if contact_matched:
                    break
        
        # Check email addresses for pilgrim
        if not contact_matched:
            email_fields = ['Email', 'email', 'Email Address', 'email_address', 'E-mail Address']
            for field in email_fields:
                if field in contact and contact[field] and str(contact[field]).lower() != 'nan':
                    email_value = str(contact[field]).lower()
                    if "pilgrim" in email_value:
                        contact_matched = True
                        match_reason = f"Email contains 'pilgrim': {contact[field]}"
                        break
        
        if contact_matched:
            # Get all available info
            contact_info = {
                'match_reason': match_reason,
                'source': contact.get('source', 'unknown'),
                'emails': [],
                'names': [],
                'companies': []
            }
            
            # Collect emails
            for field in email_fields:
                if field in contact and contact[field] and str(contact[field]).lower() != 'nan':
                    contact_info['emails'].append(contact[field])
            
            # Collect names
            for field in name_fields:
                if field in contact and contact[field] and str(contact[field]).lower() != 'nan':
                    contact_info['names'].append(contact[field])
            
            # Collect companies
            company_fields = ['Company', 'company', 'Organization', 'organization']
            for field in company_fields:
                if field in contact and contact[field] and str(contact[field]).lower() != 'nan':
                    contact_info['companies'].append(contact[field])
            
            # Remove duplicates
            contact_info['emails'] = list(set(contact_info['emails']))
            contact_info['names'] = list(set(contact_info['names']))
            contact_info['companies'] = list(set(contact_info['companies']))
            
            found_pilgrim.append(contact_info)
    
    if found_pilgrim:
        print(f"Found {len(found_pilgrim)} potential Pilgrim records:")
        for i, record in enumerate(found_pilgrim, 1):
            print(f"\nRECORD {i} (from {record['source']}):")
            print(f"  Matched because: {record['match_reason']}")
            if record['emails']:
                print(f"  Email addresses: {', '.join(record['emails'])}")
            if record['names']:
                print(f"  Names: {', '.join(record['names'])}")
            if record['companies']:
                print(f"  Companies: {', '.join(record['companies'])}")
    else:
        print("No Pilgrim records found")

if __name__ == "__main__":
    search_for_emails()