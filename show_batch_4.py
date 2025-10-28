#!/usr/bin/env python3
"""
Show detailed matches for batch 4
"""

from contact_matcher import ContactMatcher

def show_detailed_matches(people_to_check):
    """Show detailed matches for specific people"""
    matcher = ContactMatcher()
    
    for person_name in people_to_check:
        print(f"\n{'='*60}")
        print(f"PERSON: {person_name}")
        print('='*60)
        
        matches = matcher.find_matches(person_name, top_n=3)
        
        if not matches:
            print("NO MATCHES FOUND")
            continue
        
        for i, match in enumerate(matches, 1):
            contact = match['contact']
            score = match['score']
            
            print(f"\nMATCH {i}: Score {score:.2f}")
            
            # Get key details
            email_fields = ['Email', 'email', 'Email Address', 'email_address']
            email = ""
            for field in email_fields:
                if contact.get(field) and str(contact[field]).lower() != 'nan':
                    email = contact[field]
                    break
            
            company_fields = ['Company', 'company', 'Organization', 'organization']  
            company = ""
            for field in company_fields:
                if contact.get(field) and str(contact[field]).lower() != 'nan':
                    company = contact[field]
                    break
            
            source = contact.get('source', 'unknown')
            
            print(f"  Email: {email}")
            print(f"  Company: {company}")
            print(f"  Source: {source}")
            
            # Highlight relevant companies
            if company and any(keyword in company.lower() for keyword in ['mlc', 'parent', 'macquarie', 'nextsense', 'vision', 'blind']):
                print(f"  ** RELEVANT COMPANY **")

def main():
    # Get remaining people who haven't been processed yet
    # Looking at the CSV, these are the ones still needing attention
    batch_4_candidates = [
        "Ghirawoo Sara",       # Multiple generic matches
        "Ghirawoo Michael",    # Multiple generic matches  
        "Nancy Kusmadi",       # Need to investigate
        "Steve Kusmadi",       # Need to investigate
        "Agnes Chan",          # Has some potential
        "Lock Bec",            # Low matches but let's check
        "Lock Murray",         # Low matches but let's check
        "Shivayogan Shamini",  # Multiple generic matches
        "Shivayogan Yogan",    # Multiple generic matches
        "Yanamoto Kanae"       # Multiple generic matches
    ]
    
    print("=== BATCH 4: NEXT 10 CANDIDATES ===")
    print("These are some of the harder-to-match names")
    print("Looking for any viable email addresses\n")
    
    show_detailed_matches(batch_4_candidates)
    
    print(f"\n{'='*60}")
    print("BATCH 4 SUMMARY:")
    print("=" * 60)
    print("This batch contains mostly difficult matches.")
    print("Most have generic matches (info@sleepcentres.com.au) which aren't useful.")
    print("Focus on any legitimate personal/business emails found.")
    print("\nLIKELY CANDIDATES:")
    print("- Look for any emails with actual names matching")
    print("- Check for any family/business connections")
    print("- Agnes Chan might have better matches")

if __name__ == "__main__":
    main()