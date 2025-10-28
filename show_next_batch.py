#!/usr/bin/env python3
"""
Show detailed matches for the next batch of promising candidates
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
            print(f"  {matcher.format_contact_info(contact)}")
            
            # Show additional details if available
            if contact.get('Company') and str(contact['Company']).lower() != 'nan':
                company = contact['Company']
                if any(keyword in company.lower() for keyword in ['mlc', 'parent', 'macquarie', 'nextsense']):
                    print(f"  ** Relevant company: {company}")

def main():
    # Focus on the most promising candidates from the "needs review" list
    promising_candidates = [
        "Liu Jenny",           # jenny.liu@macquarie.com - good match
        "West Shane",          # shane@skyvent.com.au - good match  
        "Bowden Damien",       # damien.bowden@cba.com.au - good match
        "Henderson Liz",       # eheiner@gmail.com - MLC parent connection
        "Henderson Tim",       # t.henderson@gmail.com - MLC parent connection
        "Benton Mariska",      # mariska.benton@thesoftfact.com - exact match
        "Moses Bianca",        # biancam@eml.cc - good match
        "Hancock Anita",       # anita.hancock@gmail.com - vision impaired parent
        "Kerr Luke",          # luke.kerr@gmail.com - good match
        "Cranney David"       # dcranney@hotmail.com - good match
    ]
    
    print("=== NEXT BATCH: MOST PROMISING CANDIDATES ===")
    print("These are the people with the best potential matches from the remaining list")
    print("Looking for scores > 0.75 and relevant email addresses\n")
    
    show_detailed_matches(promising_candidates)
    
    print(f"\n{'='*60}")
    print("RECOMMENDATIONS:")
    print("=" * 60)
    print("STRONG CANDIDATES (likely correct matches):")
    print("- Liu Jenny → jenny.liu@macquarie.com")
    print("- West Shane → shane@skyvent.com.au") 
    print("- Bowden Damien → damien.bowden@cba.com.au")
    print("- Benton Mariska → mariska.benton@thesoftfact.com")
    print("- Moses Bianca → biancam@eml.cc")
    print("- Cranney David → dcranney@hotmail.com")
    print("\nPARENT CONNECTIONS (MLC-related):")
    print("- Henderson Liz/Tim → eheiner@gmail.com / t.henderson@gmail.com")
    print("- Hancock Anita → anita.hancock@gmail.com (vision impaired parent)")
    print("\nGOOD POTENTIAL:")
    print("- Kerr Luke → luke.kerr@gmail.com")

if __name__ == "__main__":
    main()