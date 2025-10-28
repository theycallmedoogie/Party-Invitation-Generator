#!/usr/bin/env python3
"""
Batch Contact Matcher - Shows matches for manual selection
Displays matches for each person for you to review
"""

import csv
import json
from contact_matcher import ContactMatcher
from pathlib import Path

class BatchMatcher:
    def __init__(self):
        self.matcher = ContactMatcher()
        self.paperless_csv_path = Path(r"C:\Users\micha\OneDrive\Desktop\contacts_paperless_august2025.csv")
    
    def show_all_matches(self, start_index=0, count=10):
        """Show matches for a batch of invitees"""
        print(f"=== CONTACT MATCHES FOR BATCH {start_index+1} - {min(start_index+count, len(self.matcher.invite_list))} ===\n")
        
        end_index = min(start_index + count, len(self.matcher.invite_list))
        
        for i in range(start_index, end_index):
            invite_name = self.matcher.invite_list[i]
            print(f"\n{'='*60}")
            print(f"PERSON {i+1}/{len(self.matcher.invite_list)}: {invite_name}")
            print('='*60)
            
            # Skip partner entries
            if "(partner)" in invite_name:
                print("PARTNER ENTRY - Manual entry required")
                continue
            
            matches = self.matcher.find_matches(invite_name, top_n=3)
            
            if not matches:
                print("NO MATCHES FOUND")
                continue
            
            for j, match in enumerate(matches, 1):
                contact = match['contact']
                score = match['score']
                
                print(f"\nMATCH {j}: Score {score:.2f}")
                print(f"  {self.matcher.format_contact_info(contact)}")
        
        print(f"\n{'='*60}")
        print(f"BATCH COMPLETE - Showing {end_index - start_index} people")
        print('='*60)
    
    def create_selection_template(self):
        """Create a template file for manual selection"""
        template_path = Path("selection_template.txt")
        
        with open(template_path, 'w', encoding='utf-8') as file:
            file.write("PARTY INVITATION CONTACT SELECTION TEMPLATE\n")
            file.write("=" * 50 + "\n\n")
            file.write("Instructions: For each person, write the match number (1, 2, 3) or 0 for no match\n")
            file.write("Format: PersonName: [MatchNumber]\n\n")
            
            for i, invite_name in enumerate(self.matcher.invite_list, 1):
                file.write(f"{i:2d}. {invite_name}: _____\n")
        
        print(f"Selection template created: {template_path}")
        return template_path
    
    def show_best_automatic_matches(self):
        """Show the best automatic matches for review"""
        print("=== BEST AUTOMATIC MATCHES (Score > 0.8) ===\n")
        
        high_confidence = []
        needs_review = []
        
        for invite_name in self.matcher.invite_list:
            if "(partner)" in invite_name:
                continue
                
            matches = self.matcher.find_matches(invite_name, top_n=1)
            
            if matches and matches[0]['score'] > 0.8:
                high_confidence.append((invite_name, matches[0]))
            else:
                needs_review.append(invite_name)
        
        print(f"HIGH CONFIDENCE MATCHES ({len(high_confidence)}):")
        print("-" * 40)
        for invite_name, match in high_confidence:
            contact = match['contact']
            score = match['score']
            print(f"{invite_name:20} → {self.matcher.format_contact_info(contact)}")
        
        print(f"\nNEEDS MANUAL REVIEW ({len(needs_review)}):")
        print("-" * 40)
        for name in needs_review:
            print(f"  {name}")
        
        print(f"\nSTATISTICS:")
        print(f"  Total people: {len(self.matcher.invite_list)}")
        print(f"  Partner entries: {len([n for n in self.matcher.invite_list if '(partner)' in n])}")
        print(f"  High confidence: {len(high_confidence)}")
        print(f"  Needs review: {len(needs_review)}")
    
    def export_high_confidence_matches(self):
        """Export high confidence matches to CSV"""
        selected_contacts = []
        
        for invite_name in self.matcher.invite_list:
            if "(partner)" in invite_name:
                # Add partner entry for manual completion
                selected_contacts.append({
                    'Name': invite_name,
                    'Email Address': '',
                    'Phone Number': '',
                    'Company': '',
                    'Role': ''
                })
                continue
                
            matches = self.matcher.find_matches(invite_name, top_n=1)
            
            if matches and matches[0]['score'] > 0.8:
                # High confidence match
                contact = matches[0]['contact']
                csv_data = self.get_contact_details(contact)
                csv_data['Name'] = invite_name
                selected_contacts.append(csv_data)
            else:
                # No match or low confidence - manual entry needed
                selected_contacts.append({
                    'Name': invite_name,
                    'Email Address': '',
                    'Phone Number': '',
                    'Company': '',
                    'Role': ''
                })
        
        # Save to CSV
        with open(self.paperless_csv_path, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['Name', 'Email Address', 'Phone Number', 'Company', 'Role']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(selected_contacts)
        
        print(f"\nExported {len(selected_contacts)} contacts to {self.paperless_csv_path}")
        
        # Statistics
        with_email = len([c for c in selected_contacts if c['Email Address']])
        print(f"Contacts with email addresses: {with_email}")
    
    def get_contact_details(self, contact):
        """Extract contact details for CSV"""
        # Email
        email_fields = ['Email', 'email', 'Email Address', 'email_address', 'E-mail Address']
        email = ""
        for field in email_fields:
            if contact.get(field) and str(contact[field]).lower() != 'nan':
                email = contact[field]
                break
        
        # Phone
        phone_fields = ['Phone', 'phone', 'Phone Number', 'phone_number', 'Mobile Phone']
        phone = ""
        for field in phone_fields:
            if contact.get(field) and str(contact[field]).lower() != 'nan':
                phone = contact[field]
                break
        
        # Company
        company_fields = ['Company', 'company', 'Organization', 'organization']
        company = ""
        for field in company_fields:
            if contact.get(field) and str(contact[field]).lower() != 'nan':
                company = contact[field]
                break
        
        return {
            'Name': '',  # Will be set by caller
            'Email Address': email,
            'Phone Number': phone,
            'Company': company,
            'Role': ''
        }

def main():
    matcher = BatchMatcher()
    
    print("Party Invitation Contact Matcher - Batch Mode")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Show best automatic matches summary")
        print("2. Show detailed matches (batch 1-10)")
        print("3. Show detailed matches (batch 11-20)")
        print("4. Show detailed matches (batch 21-30)")
        print("5. Show detailed matches (batch 31-40)")
        print("6. Show detailed matches (batch 41-50)")
        print("7. Show detailed matches (batch 51-56)")
        print("8. Export high confidence matches to CSV")
        print("9. Create selection template")
        print("0. Exit")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            matcher.show_best_automatic_matches()
        elif choice == '2':
            matcher.show_all_matches(0, 10)
        elif choice == '3':
            matcher.show_all_matches(10, 10)
        elif choice == '4':
            matcher.show_all_matches(20, 10)
        elif choice == '5':
            matcher.show_all_matches(30, 10)
        elif choice == '6':
            matcher.show_all_matches(40, 10)
        elif choice == '7':
            matcher.show_all_matches(50, 10)
        elif choice == '8':
            matcher.export_high_confidence_matches()
        elif choice == '9':
            matcher.create_selection_template()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")
    
    print("Goodbye!")

if __name__ == "__main__":
    main()