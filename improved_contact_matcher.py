#!/usr/bin/env python3
"""
Improved Contact Matcher with better handling of parentheses and special characters
"""

import pandas as pd
from difflib import SequenceMatcher
from pathlib import Path
import re
import unicodedata

class ImprovedContactMatcher:
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
    
    def normalize_text(self, text):
        """Normalize text by removing special characters, accents, and standardizing format"""
        if not text:
            return ""
        
        text = str(text)
        
        # Remove Unicode accents and normalize
        text = unicodedata.normalize('NFKD', text)
        text = ''.join(char for char in text if not unicodedata.combining(char))
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove or standardize special characters
        text = re.sub(r'[''`´]', "'", text)  # Normalize apostrophes
        text = re.sub(r'["""]', '"', text)   # Normalize quotes
        text = re.sub(r'[–—]', '-', text)    # Normalize dashes
        
        # Remove excessive punctuation but keep basic ones
        text = re.sub(r'[^\w\s\-\'\"()&.,@]', ' ', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def extract_name_variations(self, text):
        """Extract different name variations from text with parentheses"""
        if not text:
            return []
        
        normalized = self.normalize_text(text)
        variations = [normalized]
        
        # Handle parentheses - extract content inside and outside
        paren_pattern = r'\(([^)]+)\)'
        paren_matches = re.findall(paren_pattern, normalized)
        
        # Add content inside parentheses as separate variations
        for match in paren_matches:
            variations.append(match.strip())
            # Also try combining with main name parts
            main_text = re.sub(paren_pattern, '', normalized).strip()
            if main_text:
                variations.append(f"{main_text} {match}".strip())
                variations.append(f"{match} {main_text}".strip())
        
        # Remove parentheses entirely for one variation
        no_parens = re.sub(paren_pattern, ' ', normalized)
        no_parens = re.sub(r'\s+', ' ', no_parens).strip()
        if no_parens and no_parens not in variations:
            variations.append(no_parens)
        
        # Handle apostrophes in names like O'Kane
        apostrophe_variations = []
        for var in variations:
            if "'" in var:
                # Version without apostrophe
                no_apos = var.replace("'", "")
                apostrophe_variations.append(no_apos)
                # Version with space instead
                space_apos = var.replace("'", " ")
                apostrophe_variations.append(space_apos)
        
        variations.extend(apostrophe_variations)
        
        # Remove duplicates and empty strings
        variations = list(set(var for var in variations if var.strip()))
        
        return variations
    
    def load_contact_databases(self):
        """Load all available contact databases with improved text handling"""
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
                    df = pd.read_csv(file_path)
                    
                    # Process each contact with improved text handling
                    contacts = []
                    for _, row in df.iterrows():
                        contact = dict(row)
                        contact['source'] = source
                        
                        # Create normalized versions of key fields for better matching
                        name_fields = ['Name', 'name', 'Full Name', 'full_name', 'DisplayName', 'display_name', 'First Name', 'Last Name']
                        contact['_normalized_names'] = []
                        
                        for field in name_fields:
                            if field in contact and pd.notna(contact[field]):
                                variations = self.extract_name_variations(contact[field])
                                contact['_normalized_names'].extend(variations)
                        
                        # Also normalize email for better matching
                        email_fields = ['Email', 'email', 'Email Address', 'email_address']
                        for field in email_fields:
                            if field in contact and pd.notna(contact[field]):
                                contact['_normalized_email'] = self.normalize_text(contact[field])
                                break
                        
                        contacts.append(contact)
                    
                    self.all_contacts.extend(contacts)
                    print(f"  Loaded {len(contacts)} contacts from {source}")
                    
                except Exception as e:
                    print(f"  Error loading {source}: {e}")
        
        print(f"Total contacts loaded: {len(self.all_contacts)}")
    
    def enhanced_similarity_score(self, name1, name2):
        """Enhanced similarity scoring that handles special characters better"""
        if not name1 or not name2:
            return 0.0
        
        # Normalize both names
        norm1 = self.normalize_text(name1)
        norm2 = self.normalize_text(name2)
        
        # Direct similarity on normalized text
        direct_score = SequenceMatcher(None, norm1, norm2).ratio()
        
        # Get variations of both names
        variations1 = self.extract_name_variations(name1)
        variations2 = self.extract_name_variations(name2)
        
        # Find best match among all variations
        best_score = direct_score
        for var1 in variations1:
            for var2 in variations2:
                score = SequenceMatcher(None, var1, var2).ratio()
                best_score = max(best_score, score)
        
        # Word-based matching (especially good for names with parentheses)
        words1 = set(norm1.split())
        words2 = set(norm2.split())
        
        if words1 and words2:
            common_words = words1.intersection(words2)
            word_score = len(common_words) / max(len(words1), len(words2))
            best_score = max(best_score, word_score * 0.9)  # Slightly penalize word-only matches
        
        return best_score
    
    def find_matches(self, invite_name, top_n=3):
        """Find top N matching contacts with improved algorithm"""
        matches = []
        normalized_invite = self.normalize_text(invite_name)
        invite_variations = self.extract_name_variations(invite_name)
        
        for contact in self.all_contacts:
            best_score = 0
            best_field = ""
            
            # Check against all normalized name variations we stored
            if '_normalized_names' in contact:
                for norm_name in contact['_normalized_names']:
                    score = self.enhanced_similarity_score(invite_name, norm_name)
                    if score > best_score:
                        best_score = score
                        best_field = norm_name
            
            # Also check original fields as fallback
            name_fields = ['Name', 'name', 'Full Name', 'full_name', 'DisplayName', 'display_name']
            for field in name_fields:
                if field in contact and pd.notna(contact[field]):
                    score = self.enhanced_similarity_score(invite_name, contact[field])
                    if score > best_score:
                        best_score = score
                        best_field = str(contact[field])
            
            # Try combining first and last names
            first = contact.get('First Name', '') or ''
            last = contact.get('Last Name', '') or ''
            if first and last:
                full_name = f"{first} {last}"
                score = self.enhanced_similarity_score(invite_name, full_name)
                if score > best_score:
                    best_score = score
                    best_field = full_name
            
            if best_score > 0.1:  # Lower threshold to catch more possibilities
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
        """Format contact information for display (unchanged)"""
        info = []
        
        # Name
        name = contact.get('Name') or contact.get('DisplayName') or contact.get('Full Name') or 'Unknown'
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

def test_improved_matcher():
    """Test the improved matcher with some challenging cases"""
    print("=== TESTING IMPROVED CONTACT MATCHER ===\n")
    
    matcher = ImprovedContactMatcher()
    
    test_cases = [
        "Kanae Yanamoto",
        "Michael Ghirawoo", 
        "O'Kane Matt",
        "Carol O'Carol",
        "Shamini Sivayogan"
    ]
    
    for test_name in test_cases:
        print(f"Testing: {test_name}")
        matches = matcher.find_matches(test_name, top_n=3)
        
        if matches:
            for i, match in enumerate(matches, 1):
                print(f"  {i}. Score: {match['score']:.3f} | {matcher.format_contact_info(match['contact'])}")
        else:
            print("  No matches found")
        print()

if __name__ == "__main__":
    test_improved_matcher()