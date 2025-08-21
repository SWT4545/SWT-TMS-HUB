"""
Simple video compression using available tools
"""
import os
import shutil
from pathlib import Path

def compress_video():
    original_path = Path("assets/videos/company_logo_animation.mp4.MOV")
    compressed_path = Path("assets/videos/company_logo_animation_mobile.mp4")
    
    if not original_path.exists():
        print("Original video not found!")
        return None
    
    # Try to use Windows Media Format SDK if available, or create a smaller copy
    try:
        # For now, let's copy the original and rename it - we'll need external tools for real compression
        shutil.copy2(original_path, compressed_path)
        print(f"Created mobile version at: {compressed_path}")
        print(f"Size: {compressed_path.stat().st_size / 1024 / 1024:.2f} MB")
        
        # Suggest using online compression
        print("\nTo actually compress the video:")
        print("1. Upload to https://www.freeconvert.com/video-compressor")
        print("2. Set quality to 480p, reduce bitrate to 500kbps")
        print("3. Download and replace company_logo_animation_mobile.mp4")
        
        return str(compressed_path)
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    compress_video()