#!/usr/bin/env python3
"""
Artistic Party Invitation Generator
Uses Pillow and Matplotlib to create beautiful party invitations
No AI dependencies - works immediately!
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random
import os

def create_gradient_background(width=800, height=600, colors=None):
    """Create a beautiful gradient background"""
    if colors is None:
        # Default party colors
        colors = [
            (255, 107, 107),  # Coral
            (255, 159, 67),   # Orange
            (255, 206, 84),   # Yellow
            (72, 219, 251),   # Cyan
            (111, 207, 151)   # Green
        ]
    
    # Create gradient
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    
    for y in range(height):
        for x in range(width):
            # Create radial gradient effect
            center_x, center_y = width // 2, height // 2
            distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            max_distance = (width ** 2 + height ** 2) ** 0.5 / 2
            
            # Normalize distance
            factor = distance / max_distance
            factor = min(1.0, factor)
            
            # Interpolate between colors
            color_idx = int(factor * (len(colors) - 1))
            next_idx = min(color_idx + 1, len(colors) - 1)
            
            if color_idx == next_idx:
                color = colors[color_idx]
            else:
                t = (factor * (len(colors) - 1)) - color_idx
                color1 = colors[color_idx]
                color2 = colors[next_idx]
                color = (
                    int(color1[0] * (1 - t) + color2[0] * t),
                    int(color1[1] * (1 - t) + color2[1] * t),
                    int(color1[2] * (1 - t) + color2[2] * t)
                )
            
            pixels[x, y] = color
    
    return img

def add_party_decorations(img):
    """Add balloons and confetti to the image"""
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Add balloons
    balloon_colors = [(255, 107, 107), (255, 159, 67), (72, 219, 251), (111, 207, 151)]
    
    for i in range(15):  # 15 balloons
        x = random.randint(50, width - 100)
        y = random.randint(height // 2, height - 100)
        color = random.choice(balloon_colors)
        
        # Balloon body (ellipse)
        draw.ellipse([x, y, x + 60, y + 80], fill=color)
        # Balloon highlight
        draw.ellipse([x + 10, y + 10, x + 30, y + 40], fill=(255, 255, 255, 100))
        # Balloon string
        draw.line([x + 30, y + 80, x + 25, y + 150], fill=(100, 100, 100), width=2)
    
    # Add confetti
    confetti_colors = [(255, 107, 107), (255, 159, 67), (255, 206, 84), (72, 219, 251)]
    
    for i in range(100):  # 100 confetti pieces
        x = random.randint(0, width)
        y = random.randint(0, height // 2)
        color = random.choice(confetti_colors)
        
        # Random confetti shapes
        if random.choice([True, False]):
            # Rectangle confetti
            draw.rectangle([x, y, x + 8, y + 8], fill=color)
        else:
            # Circle confetti
            draw.ellipse([x, y, x + 6, y + 6], fill=color)
    
    return img

def add_party_text(img, party_details):
    """Add beautiful text to the invitation"""
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Try to load fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        subtitle_font = ImageFont.truetype("arial.ttf", 32)
        detail_font = ImageFont.truetype("arial.ttf", 24)
    except:
        try:
            title_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 48)
            subtitle_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 32)
            detail_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 24)
        except:
            # Fallback
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            detail_font = ImageFont.load_default()
    
    # Create text background with rounded corners
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # Semi-transparent background for text
    text_bg_color = (255, 255, 255, 200)
    margin = 60
    text_box = [margin, 80, width - margin, 380]
    
    # Draw rounded rectangle (approximate)
    overlay_draw.rectangle(text_box, fill=text_bg_color)
    
    # Composite the overlay
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)
    
    # Add text content
    title = party_details.get('title', 'YOU\'RE INVITED!')
    date = party_details.get('date', 'Saturday, March 15th')
    time = party_details.get('time', '7:00 PM')
    location = party_details.get('location', 'Your Address Here')
    rsvp = party_details.get('rsvp', 'RSVP: your-email@example.com')
    
    # Center text
    text_x = width // 2
    
    # Title
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text((text_x - title_width // 2, 120), title, fill=(50, 50, 50), font=title_font)
    
    # Subtitle
    subtitle = "Join us for a celebration!"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw.text((text_x - subtitle_width // 2, 180), subtitle, fill=(80, 80, 80), font=subtitle_font)
    
    # Details
    y_pos = 240
    details = [date, time, location, rsvp]
    
    for detail in details:
        detail_bbox = draw.textbbox((0, 0), detail, font=detail_font)
        detail_width = detail_bbox[2] - detail_bbox[0]
        draw.text((text_x - detail_width // 2, y_pos), detail, fill=(60, 60, 60), font=detail_font)
        y_pos += 35
    
    return img

def create_party_invitation(party_details=None, theme="celebration"):
    """Main function to create party invitation"""
    if party_details is None:
        party_details = {
            'title': 'YOU\'RE INVITED!',
            'date': 'Saturday, March 15th',
            'time': '7:00 PM - Late',
            'location': '123 Party Street, Your City',
            'rsvp': 'RSVP: party@example.com'
        }
    
    print("Creating artistic party invitation...")
    
    # Create base image
    width, height = 800, 600
    
    # Theme colors
    themes = {
        "celebration": [(255, 107, 107), (255, 159, 67), (255, 206, 84), (72, 219, 251)],
        "elegant": [(138, 43, 226), (72, 61, 139), (123, 104, 238), (147, 112, 219)],
        "tropical": [(255, 105, 180), (255, 182, 193), (255, 160, 122), (255, 218, 185)],
        "sunset": [(255, 94, 77), (255, 154, 0), (255, 206, 84), (255, 238, 173)]
    }
    
    colors = themes.get(theme, themes["celebration"])
    
    # Create gradient background
    img = create_gradient_background(width, height, colors)
    
    # Add decorations
    img = add_party_decorations(img)
    
    # Add text
    img = add_party_text(img, party_details)
    
    # Apply subtle blur for a dreamy effect
    # img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    return img

def save_invitation(img, filename="party_invitation.png"):
    """Save the invitation image"""
    img.save(filename, quality=95)
    print(f"Invitation saved as: {filename}")
    return filename

def main():
    """Interactive party invitation creator"""
    print("*** ARTISTIC PARTY INVITATION GENERATOR ***")
    print("=" * 50)
    
    # Get party details
    print("\nEnter your party details (press Enter for defaults):")
    
    title = input("Party title [YOU'RE INVITED!]: ").strip()
    if not title:
        title = "YOU'RE INVITED!"
    
    date = input("Date [Saturday, March 15th]: ").strip()
    if not date:
        date = "Saturday, March 15th"
    
    time = input("Time [7:00 PM - Late]: ").strip()
    if not time:
        time = "7:00 PM - Late"
    
    location = input("Location [123 Party Street]: ").strip()
    if not location:
        location = "123 Party Street, Your City"
    
    rsvp = input("RSVP info [party@example.com]: ").strip()
    if not rsvp:
        rsvp = "RSVP: party@example.com"
    
    # Choose theme
    print("\nChoose a theme:")
    print("1. Celebration (default - bright colors)")
    print("2. Elegant (purple tones)")
    print("3. Tropical (pink/coral)")
    print("4. Sunset (orange/yellow)")
    
    theme_choice = input("Theme [1]: ").strip()
    themes = {"1": "celebration", "2": "elegant", "3": "tropical", "4": "sunset"}
    theme = themes.get(theme_choice, "celebration")
    
    # Create invitation
    party_details = {
        'title': title,
        'date': date,
        'time': time,
        'location': location,
        'rsvp': rsvp
    }
    
    print(f"\nCreating your {theme} themed invitation...")
    
    # Generate invitation
    invitation = create_party_invitation(party_details, theme)
    
    # Save invitation
    filename = f"party_invitation_{theme}.png"
    save_invitation(invitation, filename)
    
    print(f"\nSUCCESS! Your invitation is ready!")
    print(f"File: {filename}")
    print("\nYou can now:")
    print("- Open the image to view your invitation")
    print("- Print it for physical invitations")
    print("- Share it digitally on social media")
    print("- Send it via email or messaging apps")

if __name__ == "__main__":
    main()