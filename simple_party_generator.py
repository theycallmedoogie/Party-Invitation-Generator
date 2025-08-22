#!/usr/bin/env python3
"""
Simple Party Invitation Generator
Works on CPU or GPU, optimized for speed
"""

import torch
import os
from PIL import Image, ImageDraw, ImageFont

def check_setup():
    """Check if everything is properly installed"""
    try:
        from diffusers import StableDiffusionPipeline
        print("✓ Diffusers installed")
        
        print(f"✓ PyTorch version: {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"✓ GPU available: {torch.cuda.get_device_name(0)}")
            return "cuda"
        else:
            print("⚠ No GPU detected, will use CPU (slower but works)")
            return "cpu"
            
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return None

def generate_party_invitation(prompt="", party_details=None):
    """Generate a party invitation"""
    device = check_setup()
    if device is None:
        return None
    
    try:
        from diffusers import StableDiffusionPipeline
        
        # Default party details
        if party_details is None:
            party_details = {
                'title': 'YOU\'RE INVITED!',
                'date': 'Saturday, March 15th', 
                'time': '7:00 PM',
                'location': 'Your Address Here'
            }
        
        # Default prompt if none provided
        if not prompt:
            prompt = "festive party scene, colorful balloons, celebration, warm lighting, photorealistic"
        
        print(f"Loading Stable Diffusion model...")
        
        # Use smaller model for faster loading
        model_id = "runwayml/stable-diffusion-v1-5"
        
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            safety_checker=None,
            requires_safety_checker=False
        )
        
        pipe = pipe.to(device)
        
        # Memory optimizations
        if device == "cuda":
            pipe.enable_attention_slicing()
            pipe.enable_memory_efficient_attention()
        
        print(f"Generating image: {prompt}")
        
        # Generate image with optimized settings
        with torch.autocast(device):
            image = pipe(
                prompt,
                num_inference_steps=15,  # Faster
                guidance_scale=7.0,
                width=512,
                height=512,
                generator=torch.Generator(device=device).manual_seed(42)  # Reproducible
            ).images[0]
        
        # Save background
        bg_path = "party_background.png"
        image.save(bg_path)
        print(f"✓ Background saved: {bg_path}")
        
        # Add text overlay
        final_path = create_invitation_with_text(image, party_details)
        
        print(f"✓ Final invitation saved: {final_path}")
        print("\nYour party invitation is ready!")
        
        return final_path
        
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        return None

def create_invitation_with_text(bg_image, party_details):
    """Add text overlay to create final invitation"""
    # Work with a copy
    img = bg_image.copy().convert('RGBA')
    
    # Create text overlay
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Try to load nice fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 36)
        text_font = ImageFont.truetype("arial.ttf", 20)
    except:
        # Fallback fonts
        try:
            title_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 36)
            text_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
    
    # Create semi-transparent background for text
    text_bg = (255, 255, 255, 220)  # White with transparency
    draw.rectangle([(40, 40), (img.width-40, 240)], fill=text_bg)
    
    # Composite overlay
    final_img = Image.alpha_composite(img, overlay).convert('RGB')
    final_draw = ImageDraw.Draw(final_img)
    
    # Add text content
    title = party_details.get('title', 'PARTY INVITATION')
    date = party_details.get('date', 'Date: TBD')
    time = party_details.get('time', 'Time: TBD') 
    location = party_details.get('location', 'Location: TBD')
    
    # Text positioning
    y_pos = 60
    final_draw.text((60, y_pos), title, fill=(0, 0, 0), font=title_font)
    y_pos += 50
    final_draw.text((60, y_pos), date, fill=(0, 0, 0), font=text_font)
    y_pos += 30
    final_draw.text((60, y_pos), time, fill=(0, 0, 0), font=text_font)
    y_pos += 30
    final_draw.text((60, y_pos), location, fill=(0, 0, 0), font=text_font)
    
    # Save final invitation
    final_path = "party_invitation_final.png"
    final_img.save(final_path)
    
    return final_path

def main():
    """Interactive party invitation generator"""
    print("🎉 Party Invitation Generator 🎉\n")
    
    # Get party details from user
    print("Enter your party details (press Enter for defaults):")
    
    title = input("Party title [YOU'RE INVITED!]: ").strip()
    if not title:
        title = "YOU'RE INVITED!"
        
    date = input("Date [Saturday, March 15th]: ").strip()
    if not date:
        date = "Saturday, March 15th"
        
    time = input("Time [7:00 PM]: ").strip()
    if not time:
        time = "7:00 PM"
        
    location = input("Location [Your Address]: ").strip()
    if not location:
        location = "Your Address Here"
    
    party_details = {
        'title': title,
        'date': date,
        'time': time,
        'location': location
    }
    
    # Get custom prompt
    print("\nCustom image prompt (optional):")
    prompt = input("Describe the party scene [Enter for default]: ").strip()
    
    # Generate invitation
    print("\n" + "="*50)
    result = generate_party_invitation(prompt, party_details)
    
    if result:
        print(f"\n🎉 Success! Your invitation is ready: {result}")
        print("\nYou can now:")
        print("- Open the image file to view")
        print("- Print it for physical invitations")
        print("- Share digitally on social media")
    else:
        print("\n❌ Failed to generate invitation")

if __name__ == "__main__":
    main()