#!/usr/bin/env python3
"""
Interactive Party Invitation Contact Matcher
Step-by-step selection of best matches for each invitee
"""

import csv
import json
import pandas as pd
from contact_matcher import ContactMatcher
from pathlib import Path

class InteractiveMatcher:
    def __init__(self):
        self.matcher = ContactMatcher()
        self.selected_contacts = []
        self.paperless_csv_path = Path(r"C:\Users\micha\OneDrive\Desktop\contacts_paperless_august2025.csv")
    
    def get_contact_details(self, contact):
        """Extract key contact details for CSV"""
        # Name
        name = contact.get('Name') or contact.get('DisplayName') or contact.get('Full Name') or 'Unknown'
        
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
            'Name': name,
            'Email Address': email,
            'Phone Number': phone,
            'Company': company,
            'Role': ''
        }
    
    def display_matches(self, invite_name, matches):
        """Display formatted matches for selection"""
        print(f"\n=== SELECTING CONTACT FOR: {invite_name} ===")
        print("Available matches:")
        
        for i, match in enumerate(matches, 1):
            contact = match['contact']
            score = match['score']
            
            print(f"\n{i}. Score: {score:.2f}")
            print(f"   {self.matcher.format_contact_info(contact)}")
        
        print(f"\n0. No match / Manual entry required")
        print(f"s. Skip for now")
    
    def process_single_match(self, invite_name):
        """Process a single invitee match selection"""
        # Skip partner entries
        if "(partner)" in invite_name:
            print(f"\nSkipping {invite_name} (partner entry - manual entry required)")
            return {
                'invite_name': invite_name,
                'action': 'manual',
                'csv_data': {
                    'Name': invite_name,
                    'Email Address': '',
                    'Phone Number': '',
                    'Company': '',
                    'Role': ''
                }
            }
        
        matches = self.matcher.find_matches(invite_name, top_n=3)
        
        if not matches:
            print(f"\nNo matches found for {invite_name}")
            return {
                'invite_name': invite_name,
                'action': 'no_match',
                'csv_data': {
                    'Name': invite_name,
                    'Email Address': '',
                    'Phone Number': '',
                    'Company': '',
                    'Role': ''
                }
            }
        
        while True:
            self.display_matches(invite_name, matches)
            
            try:
                choice = input(f"\nSelect best match for {invite_name} (1-{len(matches)}, 0, or s): ").strip().lower()
                
                if choice == 's':
                    return {
                        'invite_name': invite_name,
                        'action': 'skipped',
                        'matches': matches
                    }
                elif choice == '0':
                    return {
                        'invite_name': invite_name,
                        'action': 'no_match',
                        'csv_data': {
                            'Name': invite_name,
                            'Email Address': '',
                            'Phone Number': '',
                            'Company': '',
                            'Role': ''
                        }
                    }
                elif choice.isdigit() and 1 <= int(choice) <= len(matches):
                    selected_match = matches[int(choice) - 1]
                    csv_data = self.get_contact_details(selected_match['contact'])
                    csv_data['Name'] = invite_name  # Use invite name, not contact name
                    
                    print(f"\nSelected: {self.matcher.format_contact_info(selected_match['contact'])}")
                    return {
                        'invite_name': invite_name,
                        'action': 'selected',
                        'selected_match': selected_match,
                        'csv_data': csv_data
                    }
                else:
                    print("Invalid choice. Please try again.")
                    
            except (ValueError, KeyboardInterrupt):
                print("Invalid input. Please try again.")
    
    def run_interactive_session(self, start_from=0):
        """Run the interactive matching session"""
        print("=== INTERACTIVE PARTY INVITATION CONTACT MATCHING ===")
        print(f"Processing {len(self.matcher.invite_list)} invitees...")
        print("For each person, select the best matching contact or choose no match.")
        print("Commands: 1-3 (select match), 0 (no match), s (skip)\n")
        
        results = []
        
        for i in range(start_from, len(self.matcher.invite_list)):
            invite_name = self.matcher.invite_list[i]
            print(f"\n--- {i+1}/{len(self.matcher.invite_list)} ---")
            
            result = self.process_single_match(invite_name)
            results.append(result)
            
            # Add to CSV if we have data
            if 'csv_data' in result:
                self.selected_contacts.append(result['csv_data'])
                print(f"✓ Added {invite_name} to invitation list")
        
        return results
    
    def save_to_paperless_csv(self):
        """Save selected contacts to Paperless Post CSV"""
        if not self.selected_contacts:
            print("No contacts selected to save.")
            return
        
        print(f"\nSaving {len(self.selected_contacts)} contacts to Paperless Post CSV...")
        
        # Read existing CSV to get headers
        with open(self.paperless_csv_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames or ['Name', 'Email Address', 'Phone Number', 'Company', 'Role']
        
        # Write updated CSV
        with open(self.paperless_csv_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.selected_contacts)
        
        print(f"✓ Saved to: {self.paperless_csv_path}")
        
        # Show summary
        print(f"\nCSV Summary:")
        print(f"Total contacts: {len(self.selected_contacts)}")
        with_email = len([c for c in self.selected_contacts if c['Email Address']])
        with_phone = len([c for c in self.selected_contacts if c['Phone Number']])
        print(f"With email addresses: {with_email}")
        print(f"With phone numbers: {with_phone}")
    
    def show_summary(self, results):
        """Show summary of matching results"""
        selected = len([r for r in results if r['action'] == 'selected'])
        no_match = len([r for r in results if r['action'] == 'no_match'])
        manual = len([r for r in results if r['action'] == 'manual'])
        skipped = len([r for r in results if r['action'] == 'skipped'])
        
        print(f"\n=== MATCHING SUMMARY ===")
        print(f"Total processed: {len(results)}")
        print(f"Contacts selected: {selected}")
        print(f"No matches found: {no_match}")
        print(f"Manual entries (+1): {manual}")
        print(f"Skipped: {skipped}")

def main():
    matcher = InteractiveMatcher()
    
    print("Starting interactive contact matching...")
    print("This will go through each invitee one by one.\n")
    
    # You can start from a specific index if needed (e.g., start_from=10)
    results = matcher.run_interactive_session(start_from=0)
    
    # Show summary
    matcher.show_summary(results)
    
    # Save to CSV
    if input("\nSave selected contacts to Paperless Post CSV? (y/n): ").lower().startswith('y'):
        matcher.save_to_paperless_csv()
    
    print("\nMatching session complete!")

if __name__ == "__main__":
    main()