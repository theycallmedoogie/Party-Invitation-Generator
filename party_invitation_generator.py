#!/usr/bin/env python3
"""
Party Invitation Generator using Stable Diffusion
Creates photo-realistic party invitation images
"""
from DevInfrastructure import ErrorIntelligence
from DevInfrastructure.error_intelligence import log_error, safe_print

import torch
from diffusers import StableDiffusionPipeline
from PIL import Image, ImageDraw, ImageFont
import os
import sys

# Initialize error logging for this project
error_logger = ErrorIntelligence(project_name="Party_Invitation_Generator")

def check_gpu():
    """Check if CUDA is available"""
    try:
        if torch.cuda.is_available():
            safe_print(f"GPU available: {torch.cuda.get_device_name(0)}")
            safe_print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            return True
        else:
            safe_print("No GPU available, using CPU (will be slow)")
            return False
    except Exception as e:
        log_error("GPUCheckError", str(e), {"torch_version": torch.__version__, "cuda_available": torch.cuda.is_available()})
        safe_print("Error checking GPU availability, defaulting to CPU")
        return False

def setup_stable_diffusion():
    """Initialize Stable Diffusion pipeline"""
    pipe = None
    device = None
    model_id = "runwayml/stable-diffusion-v1-5"
    
    try:
        safe_print("Loading Stable Diffusion model...")
        
        # Check if GPU is available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load pipeline
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            safety_checker=None,
            requires_safety_checker=False
        )
        
        pipe = pipe.to(device)
        
        # Enable memory efficient attention if available
        if hasattr(pipe, "enable_attention_slicing"):
            pipe.enable_attention_slicing()
        
        safe_print(f"Model loaded on {device}")
        return pipe
        
    except Exception as e:
        log_error("StableDiffusionSetupError", str(e), {
            "model_id": model_id,
            "device": device,
            "torch_version": torch.__version__,
            "cuda_available": torch.cuda.is_available()
        })
        safe_print("Failed to load Stable Diffusion model")
        return None

def generate_party_image(pipe, prompt, output_path="party_invitation.png"):
    """Generate party invitation image"""
    print(f"Generating image with prompt: {prompt}")
    
    # Generate image
    with torch.autocast("cuda" if torch.cuda.is_available() else "cpu"):
        image = pipe(
            prompt,
            num_inference_steps=20,  # Faster generation
            guidance_scale=7.5,
            width=512,
            height=512
        ).images[0]
    
    # Save the image
    image.save(output_path)
    print(f"Image saved to: {output_path}")
    return image

def add_party_text(image, party_details, output_path="final_invitation.png"):
    """Add text overlay to the generated image"""
    # Create a copy to work with
    img = image.copy()
    draw = ImageDraw.Draw(img)
    
    # Try to load a nice font, fallback to default
    try:
        title_font = ImageFont.truetype("arial.ttf", 40)
        detail_font = ImageFont.truetype("arial.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        detail_font = ImageFont.load_default()
    
    # Add semi-transparent overlay for text
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # Add background rectangle for text
    overlay_draw.rectangle([(50, 50), (img.width-50, 200)], fill=(255, 255, 255, 200))
    
    # Composite overlay onto image
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)
    
    # Add text
    title = party_details.get('title', 'PARTY INVITATION')
    date = party_details.get('date', 'Date: TBD')
    time = party_details.get('time', 'Time: TBD')
    location = party_details.get('location', 'Location: TBD')
    
    # Draw text
    draw.text((60, 60), title, fill=(0, 0, 0), font=title_font)
    draw.text((60, 110), date, fill=(0, 0, 0), font=detail_font)
    draw.text((60, 140), time, fill=(0, 0, 0), font=detail_font)
    draw.text((60, 170), location, fill=(0, 0, 0), font=detail_font)
    
    # Save final invitation
    img.save(output_path)
    print(f"Final invitation saved to: {output_path}")
    return img

def main():
    """Main function to generate party invitation"""
    print("=== Party Invitation Generator ===")
    
    # Check GPU
    check_gpu()
    
    # Setup Stable Diffusion
    pipe = setup_stable_diffusion()
    
    # Example party prompt - you can customize this
    party_prompt = """
    beautiful festive party scene, colorful balloons, confetti, 
    celebration background, warm lighting, joyful atmosphere, 
    photorealistic, high quality, detailed
    """
    
    # Generate background image
    bg_image = generate_party_image(pipe, party_prompt)
    
    # Party details - customize these
    party_info = {
        'title': 'YOU\'RE INVITED!',
        'date': 'Saturday, March 15th',
        'time': '7:00 PM - Late',
        'location': '123 Party Street'
    }
    
    # Add text to create final invitation
    final_invitation = add_party_text(bg_image, party_info)
    
    print("Party invitation generated successfully!")
    print("Files created:")
    print("- party_invitation.png (background)")
    print("- final_invitation.png (with text)")

if __name__ == "__main__":
    main()