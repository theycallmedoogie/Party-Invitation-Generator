#!/usr/bin/env python3
"""
Party Invitation Contact Matcher
Matches invite list names with contacts from Email Analysis project
"""

import csv
import json
import pandas as pd
from difflib import SequenceMatcher
from pathlib import Path
import re
import unicodedata

class ContactMatcher:
    def __init__(self):
        self.invite_list = [
            "Ghirawoo Sara", "Ghirawoo Michael", "Kiara Casley", "Nancy Kusmadi", "Steve Kusmadi", "Agnes Chan",
            "Liu Jenny", "Rothwell Kathy", "Rothwell Iain", "West Lakshmi", "West Shane",
            "Lock Bec", "Lock Murray", "Shivayogan Shamini", "Shivayogan Yogan",
            "Abbey Durez", "Carol O'Carol", "Yanamoto Kanae", "Hancock Matt", "Hancock Anita", 
            "Kerr Luke", "Kerr Clare", "Carlon Phil", "Carlon Sarah", "Bowden Damien", "Bowden Tara", 
            "Charles Michael", "Charles Kylie", "Baratta Brigid", "Baratta John", "Baratta Bede", "Baratta Leanne",
            "Cranney David", "Cranney Sarah", "Elizabeth Canham", "Erron Gardner", "Anita David", "Prishan David",
            "Henderson Liz", "Henderson Tim", "Liaw Grace", "Chung Wayne", "Coorey Dao", "Coorey Adrian", 
            "Benton Mariska", "Benton Campbell", "Scott Lara", "O'Kane Matt", "O'Kane Renee",
            "Moses Bianca", "Moses (partner)", "Montin Luke", "Montin (partner)", "Medves Mike",
            "Liz Foster", "Leo Foster"
        ]
        
        self.all_contacts = []
        self.load_contact_databases()
    
    def load_contact_databases(self):
        """Load all available contact databases"""
        email_analysis_path = Path(r"C:\Users\micha\OneDrive\Desktop\RooCode projects\Email Analysis\data")
        
        contact_sources = [
            "yahoo_contacts_export.csv",
            "outlook_contacts_20250807_184605.csv", 
            "extracted_contacts.csv"
        ]
        
        for source in contact_sources:
            file_path = email_analysis_path / source
            if file_path.exists():
                try:
                    print(f"Loading {source}...")
                    if source.endswith('.csv'):
                        df = pd.read_csv(file_path)
                        # Convert to list of dictionaries and add source info
                        contacts = df.to_dict('records')
                        for contact in contacts:
                            contact['source'] = source
                        self.all_contacts.extend(contacts)
                        print(f"  Loaded {len(contacts)} contacts from {source}")
                except Exception as e:
                    print(f"  Error loading {source}: {e}")
        
        print(f"Total contacts loaded: {len(self.all_contacts)}")
    
    def similarity_score(self, name1, name2):
        """Calculate similarity between two names"""
        if not name1 or not name2:
            return 0.0
        
        # Convert to lowercase for comparison
        name1_lower = str(name1).lower()
        name2_lower = str(name2).lower()
        
        # Direct similarity
        direct_score = SequenceMatcher(None, name1_lower, name2_lower).ratio()
        
        # Check if names contain each other (partial matches)
        words1 = name1_lower.split()
        words2 = name2_lower.split()
        
        word_matches = 0
        total_words = max(len(words1), len(words2))
        
        for word1 in words1:
            for word2 in words2:
                if word1 in word2 or word2 in word1:
                    word_matches += 1
                    break
        
        word_score = word_matches / total_words if total_words > 0 else 0
        
        # Combine scores (favor word matches for names)
        return max(direct_score, word_score * 0.8)
    
    def find_matches(self, invite_name, top_n=3):
        """Find top N matching contacts for an invite name"""
        matches = []
        
        for contact in self.all_contacts:
            # Try matching against various name fields
            name_fields = []
            
            # Common field names to check
            possible_name_fields = [
                'Name', 'name', 'Full Name', 'full_name', 'DisplayName', 'display_name',
                'First Name', 'first_name', 'Last Name', 'last_name', 'Contact Name'
            ]
            
            for field in possible_name_fields:
                if field in contact and contact[field]:
                    name_fields.append(str(contact[field]))
            
            # Also try combining first and last names if available
            first = contact.get('First Name') or contact.get('first_name') or ''
            last = contact.get('Last Name') or contact.get('last_name') or ''
            if first and last:
                name_fields.append(f"{first} {last}")
            
            # Calculate best match score
            best_score = 0
            best_field = ""
            
            for name_field in name_fields:
                score = self.similarity_score(invite_name, name_field)
                if score > best_score:
                    best_score = score
                    best_field = name_field
            
            if best_score > 0.1:  # Only include if some similarity
                match_info = {
                    'contact': contact,
                    'score': best_score,
                    'matched_name': best_field,
                    'invite_name': invite_name
                }
                matches.append(match_info)
        
        # Sort by score and return top N
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches[:top_n]
    
    def format_contact_info(self, contact):
        """Format contact information for display"""
        info = []
        
        # Name
        name = contact.get('Name') or contact.get('DisplayName') or 'Unknown'
        info.append(f"Name: {name}")
        
        # Email
        email_fields = ['Email', 'email', 'Email Address', 'email_address', 'E-mail Address']
        email = None
        for field in email_fields:
            if contact.get(field):
                email = contact[field]
                break
        if email:
            info.append(f"Email: {email}")
        
        # Phone
        phone_fields = ['Phone', 'phone', 'Phone Number', 'phone_number', 'Mobile Phone']
        phone = None
        for field in phone_fields:
            if contact.get(field):
                phone = contact[field]
                break
        if phone:
            info.append(f"Phone: {phone}")
        
        # Company
        company_fields = ['Company', 'company', 'Organization', 'organization']
        company = None
        for field in company_fields:
            if contact.get(field):
                company = contact[field]
                break
        if company:
            info.append(f"Company: {company}")
        
        # Source
        source = contact.get('source', 'Unknown')
        info.append(f"Source: {source}")
        
        return " | ".join(info)
    
    def interactive_matching(self):
        """Interactive matching process for all invite names"""
        print("=== Party Invitation Contact Matching ===\n")
        print(f"Processing {len(self.invite_list)} invitees...\n")
        
        selected_matches = []
        
        for i, invite_name in enumerate(self.invite_list, 1):
            print(f"\n--- {i}/{len(self.invite_list)}: {invite_name} ---")
            
            # Skip +1 entries for now
            if "+1" in invite_name:
                print("Skipping +1 entry (manual entry required)")
                selected_matches.append({
                    'invite_name': invite_name,
                    'selected_contact': None,
                    'action': 'manual'
                })
                continue
            
            matches = self.find_matches(invite_name)
            
            if not matches:
                print("No potential matches found")
                selected_matches.append({
                    'invite_name': invite_name,
                    'selected_contact': None,
                    'action': 'no_match'
                })
                continue
            
            print("Top 3 potential matches:")
            for j, match in enumerate(matches):
                print(f"{j+1}. Score: {match['score']:.2f} | {self.format_contact_info(match['contact'])}")
            
            # For now, just store the matches - we'll make this interactive later
            selected_matches.append({
                'invite_name': invite_name,
                'matches': matches,
                'action': 'needs_selection'
            })
        
        return selected_matches

if __name__ == "__main__":
    matcher = ContactMatcher()
    results = matcher.interactive_matching()
    
    print(f"\nProcessing complete. Found matches for {len([r for r in results if r.get('matches')])} names.")