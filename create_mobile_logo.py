"""
Create a lightweight static logo for mobile devices
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_mobile_logo():
    # Create a 400x300 image with company colors
    width, height = 400, 300
    img = Image.new('RGB', (width, height), '#1e3a8a')  # Dark blue background
    draw = ImageDraw.Draw(img)
    
    # Add company name
    try:
        # Try to use a nice font, fallback to default
        font_large = ImageFont.truetype("arial.ttf", 36)
        font_medium = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 18)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw company name
    company_text = "SMITH & WILLIAMS"
    trucking_text = "TRUCKING LLC"
    
    # Get text dimensions
    company_bbox = draw.textbbox((0, 0), company_text, font=font_large)
    trucking_bbox = draw.textbbox((0, 0), trucking_text, font=font_medium)
    
    company_width = company_bbox[2] - company_bbox[0]
    trucking_width = trucking_bbox[2] - trucking_bbox[0]
    
    # Center the text
    company_x = (width - company_width) // 2
    trucking_x = (width - trucking_width) // 2
    
    # Draw text with white color
    draw.text((company_x, 80), company_text, fill='white', font=font_large)
    draw.text((trucking_x, 130), trucking_text, fill='white', font=font_medium)
    
    # Add truck emoji or simple truck graphic
    draw.text((width//2 - 20, 180), "🚚", fill='white', font=font_large)
    
    # Add TMS text
    tms_text = "Transportation Management System"
    tms_bbox = draw.textbbox((0, 0), tms_text, font=font_small)
    tms_width = tms_bbox[2] - tms_bbox[0]
    tms_x = (width - tms_width) // 2
    draw.text((tms_x, 220), tms_text, fill='#94a3b8', font=font_small)
    
    # Save the image
    os.makedirs('assets/images', exist_ok=True)
    img.save('assets/images/mobile_logo.png', 'PNG', optimize=True)
    print(f"Mobile logo created: {os.path.getsize('assets/images/mobile_logo.png')} bytes")
    
    return 'assets/images/mobile_logo.png'

if __name__ == "__main__":
    create_mobile_logo()