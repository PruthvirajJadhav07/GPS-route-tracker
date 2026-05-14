import os
from PIL import Image
import shutil

# The path to the uploaded Routehawk logo
SOURCE_IMAGE = r"C:\Users\pruth\.gemini\antigravity\brain\810d910d-d728-48db-8f91-299b63c025cc\media__1778584988022.png"

# The path to the Android resources directory
RES_DIR = r"d:\live_route_tracker\android\app\src\main\res"

# Standard Android icon sizes (in pixels)
ICON_SIZES = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

def create_icons():
    if not os.path.exists(SOURCE_IMAGE):
        print(f"Error: Source image not found at {SOURCE_IMAGE}")
        return

    try:
        with Image.open(SOURCE_IMAGE) as img:
            # Ensure it's in RGBA mode for transparency/colors
            img = img.convert("RGBA")
            
            for folder, size in ICON_SIZES.items():
                folder_path = os.path.join(RES_DIR, folder)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    
                # Resize image using high-quality Lanczos resampling
                resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
                
                # Save as standard launcher icon
                icon_path = os.path.join(folder_path, "ic_launcher.png")
                resized_img.save(icon_path, "PNG")
                
                # Save as round launcher icon (using the same image for now)
                icon_round_path = os.path.join(folder_path, "ic_launcher_round.png")
                resized_img.save(icon_round_path, "PNG")
                
                print(f"✅ Generated {size}x{size} icon in {folder}")
                
        print("\n🎉 Success! The Routehawk icon has been installed in your Android app.")
        print("Please rebuild your APK to see the changes.")
        
    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == "__main__":
    create_icons()
