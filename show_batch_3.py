#!/usr/bin/env python3
"""
Show detailed matches for batch 3
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
    # Next batch of promising candidates
    batch_3_candidates = [
        "Carlon Phil",         # Multiple potential emails
        "Montin Luke",         # lukamontin@gmail.com - close match
        "Medves Mike",         # mmedves@gmail.com - good match
        "Liz Foster",          # Multiple foster emails
        "Leo Foster",          # Multiple foster emails
        "O'Kane Matt",         # matt@okane.com.au potential
        "Baratta Bede",        # bede.baratta@cgu.com.au - exact match
        "Charles Kylie",       # kbmc25@gmail.com potential
        "Rothwell Kathy",      # No clear matches but let's check
        "Rothwell Iain"        # No clear matches but let's check
    ]
    
    print("=== BATCH 3: NEXT 10 CANDIDATES ===")
    print("Looking for the next best potential matches")
    print("Some have exact name matches, others need investigation\n")
    
    show_detailed_matches(batch_3_candidates)
    
    print(f"\n{'='*60}")
    print("BATCH 3 SUMMARY:")
    print("=" * 60)
    print("STRONG MATCHES:")
    print("- Baratta Bede -> bede.baratta@cgu.com.au (exact match)")
    print("- Montin Luke -> lukamontin@gmail.com (close name match)")
    print("- Medves Mike -> mmedves@gmail.com (good match)")
    print("- O'Kane Matt -> matt@okane.com.au (O'Kane Internet Consulting)")
    print("\nNEED INVESTIGATION:")
    print("- Carlon Phil -> multiple emails to choose from")
    print("- Charles Kylie -> kbmc25@gmail.com (needs verification)")  
    print("- Liz Foster -> multiple Foster emails")
    print("- Leo Foster -> multiple Foster emails")
    print("\nLOW CONFIDENCE:")
    print("- Rothwell Kathy -> no clear matches")
    print("- Rothwell Iain -> no clear matches")

if __name__ == "__main__":
    main()