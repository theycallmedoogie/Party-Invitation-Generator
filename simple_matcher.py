#!/usr/bin/env python3
"""
Simple Contact Matcher - Shows best matches for review
"""

from contact_matcher import ContactMatcher

def main():
    print("Loading contacts...")
    matcher = ContactMatcher()
    
    print(f"\n=== BEST MATCHES FOR PARTY INVITATIONS ===")
    print(f"Total people: {len(matcher.invite_list)}")
    
    high_confidence = []
    needs_review = []
    partner_entries = []
    
    for i, invite_name in enumerate(matcher.invite_list, 1):
        if "(partner)" in invite_name:
            partner_entries.append(invite_name)
            continue
            
        matches = matcher.find_matches(invite_name, top_n=3)
        
        if matches and matches[0]['score'] >= 0.85:
            high_confidence.append((invite_name, matches[0]))
        else:
            needs_review.append((invite_name, matches))
    
    print(f"\nHIGH CONFIDENCE MATCHES ({len(high_confidence)}):")
    print("-" * 60)
    for invite_name, match in high_confidence:
        contact = match['contact']
        score = match['score']
        
        # Get email
        email_fields = ['Email', 'email', 'Email Address', 'email_address']
        email = ""
        for field in email_fields:
            if contact.get(field) and str(contact[field]).lower() != 'nan':
                email = contact[field]
                break
        
        print(f"{i:2d}. {invite_name:<20} Score: {score:.2f} Email: {email}")
    
    print(f"\nNEEDS REVIEW ({len(needs_review)}):")
    print("-" * 60)
    for invite_name, matches in needs_review:
        if matches:
            best_match = matches[0]
            score = best_match['score']
            contact = best_match['contact']
            
            # Get email
            email = ""
            email_fields = ['Email', 'email', 'Email Address', 'email_address']
            for field in email_fields:
                if contact.get(field) and str(contact[field]).lower() != 'nan':
                    email = contact[field]
                    break
            
            print(f"{invite_name:<20} Best: {score:.2f} Email: {email}")
        else:
            print(f"{invite_name:<20} NO MATCHES FOUND")
    
    print(f"\nPARTNER ENTRIES ({len(partner_entries)}):")
    print("-" * 60)
    for name in partner_entries:
        print(f"{name} - Manual entry required")
    
    print(f"\nSUMMARY:")
    print(f"- High confidence matches: {len(high_confidence)}")
    print(f"- Need manual review: {len(needs_review)}")
    print(f"- Partner entries: {len(partner_entries)}")
    print(f"- Total: {len(high_confidence) + len(needs_review) + len(partner_entries)}")

if __name__ == "__main__":
    main()