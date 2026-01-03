#!/usr/bin/env python3
"""
Generate placeholder icons for the Synology package.
Requires Pillow: pip install Pillow

Run this script to generate PACKAGE_ICON.PNG and PACKAGE_ICON_256.PNG
Or replace these files with your own custom icons.
"""

import sys

def generate_icons():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow not installed. Install with: pip install Pillow")
        print("Or manually create PACKAGE_ICON.PNG (72x72) and PACKAGE_ICON_256.PNG (256x256)")
        return False

    def create_icon(size, filename):
        # Create a simple gradient icon with "SH" text
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Draw rounded rectangle background (Streamlit red/pink gradient)
        padding = size // 10
        draw.rounded_rectangle(
            [padding, padding, size - padding, size - padding],
            radius=size // 6,
            fill=(255, 75, 75)  # Streamlit red
        )

        # Draw inner accent
        inner_padding = size // 5
        draw.rounded_rectangle(
            [inner_padding, inner_padding, size - inner_padding, size - inner_padding],
            radius=size // 8,
            fill=(255, 100, 100)
        )

        # Add "SH" text (Streamlit Hub)
        try:
            font_size = size // 3
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()

        text = "SH"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) // 2
        y = (size - text_height) // 2 - size // 10

        draw.text((x, y), text, fill=(255, 255, 255), font=font)

        img.save(filename, 'PNG')
        print(f"Created {filename}")

    create_icon(72, 'PACKAGE_ICON.PNG')
    create_icon(256, 'PACKAGE_ICON_256.PNG')
    return True

if __name__ == '__main__':
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    generate_icons()
